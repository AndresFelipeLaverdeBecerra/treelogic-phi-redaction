import cv2


def anonimizar_imagen(imagen, detecciones, valor_relleno=0):
    """
    Cubre con negro las regiones detectadas como informacion sensible.
    """
    anonimizada = imagen.copy()

    for det in detecciones:
        x1, y1, x2, y2 = [int(round(v)) for v in det["caja_final"]]

        x1 = max(0, min(anonimizada.shape[1], x1))
        x2 = max(0, min(anonimizada.shape[1], x2))
        y1 = max(0, min(anonimizada.shape[0], y1))
        y2 = max(0, min(anonimizada.shape[0], y2))

        if x2 <= x1 or y2 <= y1:
            continue

        anonimizada[y1:y2, x1:x2] = valor_relleno

    return anonimizada


def guardar_imagen(ruta, imagen):
    cv2.imwrite(str(ruta), imagen)
