import numpy as np
from .postprocess import area_interseccion, area_caja, iou


def cajas_a_mascara(cajas, ancho, alto):
    mascara = np.zeros((alto, ancho), dtype=bool)

    for caja in cajas:
        x1, y1, x2, y2 = [int(round(v)) for v in caja]

        x1 = max(0, min(ancho, x1))
        x2 = max(0, min(ancho, x2))
        y1 = max(0, min(alto, y1))
        y2 = max(0, min(alto, y2))

        if x2 > x1 and y2 > y1:
            mascara[y1:y2, x1:x2] = True

    return mascara


def cobertura_de_caja_gt(cajas_predichas, caja_gt):
    area_gt = area_caja(caja_gt)

    if area_gt <= 0:
        return 0.0

    area_cubierta = 0.0

    for caja_predicha in cajas_predichas:
        area_cubierta += area_interseccion(caja_predicha, caja_gt)

    return min(1.0, area_cubierta / area_gt)


def metricas_redaccion(cajas_predichas, cajas_gt, ancho, alto):
    mascara_predicha = cajas_a_mascara(cajas_predichas, ancho, alto)
    mascara_gt = cajas_a_mascara(cajas_gt, ancho, alto)

    area_predicha = mascara_predicha.sum()
    area_gt = mascara_gt.sum()

    interseccion = np.logical_and(mascara_predicha, mascara_gt).sum()
    extra = np.logical_and(mascara_predicha, ~mascara_gt).sum()

    precision_redaccion = interseccion / area_predicha if area_predicha > 0 else 1.0
    fraccion_area_censurada = area_predicha / (ancho * alto)

    if area_gt > 0:
        carga_extra = (extra / (ancho * alto)) / (area_gt / (ancho * alto))
    else:
        carga_extra = 0.0

    cajas_externas = 0
    for caja_predicha in cajas_predichas:
        max_iou = max([iou(caja_predicha, caja_gt) for caja_gt in cajas_gt], default=0.0)
        if max_iou < 0.01:
            cajas_externas += 1

    return {
        "fraccion_area_censurada": float(fraccion_area_censurada),
        "precision_redaccion": float(precision_redaccion),
        "carga_extra_vs_gt": float(carga_extra),
        "cajas_externas": int(cajas_externas),
    }
