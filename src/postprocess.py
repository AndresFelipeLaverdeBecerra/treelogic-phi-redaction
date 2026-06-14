import math


def recortar_caja(caja, ancho, alto):
    x1, y1, x2, y2 = caja

    x1 = max(0.0, min(float(ancho), float(x1)))
    y1 = max(0.0, min(float(alto), float(y1)))
    x2 = max(0.0, min(float(ancho), float(x2)))
    y2 = max(0.0, min(float(alto), float(y2)))

    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1

    return [x1, y1, x2, y2]


def area_caja(caja):
    x1, y1, x2, y2 = caja
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def area_interseccion(caja_a, caja_b):
    ax1, ay1, ax2, ay2 = caja_a
    bx1, by1, bx2, by2 = caja_b

    x1 = max(ax1, bx1)
    y1 = max(ay1, by1)
    x2 = min(ax2, bx2)
    y2 = min(ay2, by2)

    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def iou(caja_a, caja_b):
    inter = area_interseccion(caja_a, caja_b)
    union = area_caja(caja_a) + area_caja(caja_b) - inter
    return inter / union if union > 0 else 0.0


def centro_caja(caja):
    x1, y1, x2, y2 = caja
    return [(x1 + x2) / 2.0, (y1 + y2) / 2.0]


def distancia_centros_normalizada(caja_a, caja_b, ancho, alto):
    ax, ay = centro_caja(caja_a)
    bx, by = centro_caja(caja_b)

    dx = (ax - bx) / max(1.0, float(ancho))
    dy = (ay - by) / max(1.0, float(alto))

    return math.sqrt(dx * dx + dy * dy)


def seleccionar_detecciones_por_umbral(detecciones, config, ancho, alto):
    """
    Filtra detecciones YOLO usando umbrales por clase.

    Esta etapa implementa la recalibracion final de class-specific confidence thresholds1.5:
    name=0.075, id=0.030, age=0.075, date=0.045, time=0.015.
    """
    umbrales = config["umbrales_por_clase"]
    seleccionadas = []

    if detecciones is None or len(detecciones) == 0:
        return seleccionadas

    for _, fila in detecciones.iterrows():
        clase = fila["clase"]
        score = float(fila["score"])

        if clase not in umbrales:
            continue

        if score < float(umbrales[clase]):
            continue

        caja_original = recortar_caja(
            [fila["x1"], fila["y1"], fila["x2"], fila["y2"]],
            ancho,
            alto,
        )

        seleccionadas.append({
            "id_clase": int(fila["id_clase"]),
            "clase": clase,
            "score": score,
            "caja_original": caja_original,
            "caja_final": caja_original,
            "traza": "deteccion_yolo",
        })

    return seleccionadas


def aplicar_padding_seguridad(detecciones, config, ancho, alto):
    """
    Agrega un margen pequeno alrededor de cada deteccion para evitar dejar
    caracteres parcialmente visibles.
    """
    cfg = config["postproceso"]["padding_seguridad"]

    if not cfg.get("activo", True):
        return detecciones

    margen_x = float(cfg.get("fraccion_x", 0.004)) * ancho
    margen_y = float(cfg.get("fraccion_y", 0.002)) * alto

    salida = []

    for det in detecciones:
        x1, y1, x2, y2 = det["caja_final"]
        caja = recortar_caja(
            [x1 - margen_x, y1 - margen_y, x2 + margen_x, y2 + margen_y],
            ancho,
            alto,
        )

        nueva = det.copy()
        nueva["caja_final"] = caja
        nueva["traza"] = nueva.get("traza", "") + "|padding_seguridad"
        salida.append(nueva)

    return salida


def ajustar_altura_segun_caja_original(detecciones, config, ancho, alto):
    """
    Evita que el padding vertical haga que la caja sea excesivamente alta.

    La caja final conserva el ancho con padding, pero su altura se limita usando
    como referencia la altura original predicha por YOLO.
    """
    cfg = config["postproceso"]["ajuste_vertical_por_caja_original"]

    if not cfg.get("activo", True):
        return detecciones

    factor_altura = float(cfg.get("factor_altura", 1.45))
    margen_pixeles = float(cfg.get("margen_pixeles", 4.0))

    salida = []

    for det in detecciones:
        x1, y1, x2, y2 = det["caja_final"]
        ox1, oy1, ox2, oy2 = det["caja_original"]

        altura_original = max(1.0, oy2 - oy1)
        altura_actual = max(1.0, y2 - y1)

        altura_maxima = max(altura_original * factor_altura, altura_original + margen_pixeles)

        if altura_actual > altura_maxima:
            centro_y = (oy1 + oy2) / 2.0
            y1 = centro_y - altura_maxima / 2.0
            y2 = centro_y + altura_maxima / 2.0

        nueva = det.copy()
        nueva["caja_final"] = recortar_caja([x1, y1, x2, y2], ancho, alto)
        nueva["traza"] = nueva.get("traza", "") + "|ajuste_altura_original"
        salida.append(nueva)

    return salida


def ajustar_altura_segun_vecinos(detecciones, config, ancho, alto):
    """
    Segundo ajuste vertical conservador.

    Usa la distribucion de alturas de las detecciones cercanas en la misma imagen
    para evitar cajas verticalmente sobredimensionadas. Nunca reduce la caja por
    debajo de un margen seguro respecto a la caja original.
    """
    cfg = config["postproceso"]["ajuste_vertical_por_vecinos"]

    if not cfg.get("activo", True):
        return detecciones

    if len(detecciones) <= 1:
        return detecciones

    factor_altura_original = float(cfg.get("factor_altura_original", 1.35))
    factor_mediana_vecinos = float(cfg.get("factor_mediana_vecinos", 1.20))
    margen_pixeles = float(cfg.get("margen_pixeles", 3.0))

    alturas_originales = [
        max(1.0, det["caja_original"][3] - det["caja_original"][1])
        for det in detecciones
    ]

    alturas_ordenadas = sorted(alturas_originales)
    mediana_altura = alturas_ordenadas[len(alturas_ordenadas) // 2]

    salida = []

    for det in detecciones:
        x1, y1, x2, y2 = det["caja_final"]
        ox1, oy1, ox2, oy2 = det["caja_original"]

        altura_original = max(1.0, oy2 - oy1)
        altura_actual = max(1.0, y2 - y1)

        altura_maxima = max(
            altura_original * factor_altura_original,
            mediana_altura * factor_mediana_vecinos,
            altura_original + margen_pixeles,
        )

        if altura_actual > altura_maxima:
            centro_y = (oy1 + oy2) / 2.0
            y1 = centro_y - altura_maxima / 2.0
            y2 = centro_y + altura_maxima / 2.0

        nueva = det.copy()
        nueva["caja_final"] = recortar_caja([x1, y1, x2, y2], ancho, alto)
        nueva["traza"] = nueva.get("traza", "") + "|ajuste_altura_vecinos"
        salida.append(nueva)

    return salida


def suprimir_duplicados_cercanos(detecciones, config, ancho, alto):
    """
    Elimina duplicados locales de la misma clase.

    Esta etapa conserva la deteccion de mayor score y elimina una deteccion de la
    misma clase solo si:
    1. esta muy cerca en coordenadas normalizadas, y
    2. su score es suficientemente menor que el score de la deteccion retenida.

    Es una version conservadora de NMS centrado en distancia de centros.
    """
    cfg = config["postproceso"]["supresion_duplicados_cercanos"]

    if not cfg.get("activo", True):
        return detecciones

    if len(detecciones) <= 1:
        return detecciones

    distancia_maxima = float(cfg.get("distancia_centros_normalizada", 0.020))
    razon_score = float(cfg.get("razon_score", 0.35))

    orden = sorted(
        range(len(detecciones)),
        key=lambda i: float(detecciones[i]["score"]),
        reverse=True,
    )

    retenidas = []
    eliminadas = set()

    for i in orden:
        if i in eliminadas:
            continue

        actual = detecciones[i]
        es_duplicado = False

        for j in retenidas:
            referencia = detecciones[j]

            if actual["id_clase"] != referencia["id_clase"]:
                continue

            if actual["score"] > razon_score * referencia["score"]:
                continue

            distancia = distancia_centros_normalizada(
                actual["caja_final"],
                referencia["caja_final"],
                ancho,
                alto,
            )

            if distancia <= distancia_maxima:
                es_duplicado = True
                break

        if es_duplicado:
            eliminadas.add(i)
        else:
            retenidas.append(i)

    return [detecciones[i] for i in retenidas]


def ejecutar_postproceso(detecciones_yolo, config, ancho, alto):
    """
    Ejecuta el pipeline final completo:

    1. Seleccion por umbrales de clase.
    2. Padding de seguridad.
    3. Ajuste vertical por caja original.
    4. Ajuste vertical por vecinos.
    5. Supresion conservadora de duplicados cercanos.
    """
    detecciones = seleccionar_detecciones_por_umbral(detecciones_yolo, config, ancho, alto)
    detecciones = aplicar_padding_seguridad(detecciones, config, ancho, alto)
    detecciones = ajustar_altura_segun_caja_original(detecciones, config, ancho, alto)
    detecciones = ajustar_altura_segun_vecinos(detecciones, config, ancho, alto)
    detecciones = suprimir_duplicados_cercanos(detecciones, config, ancho, alto)
    return detecciones
