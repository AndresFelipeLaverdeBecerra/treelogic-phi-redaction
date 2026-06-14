import cv2


def dibujar_cajas(imagen, detecciones):
    """
    Dibuja las cajas finales sobre la imagen original.
    """
    salida = imagen.copy()

    for det in detecciones:
        x1, y1, x2, y2 = [int(round(v)) for v in det["caja_final"]]
        etiqueta = f"{det['clase']} {det['score']:.2f}"

        cv2.rectangle(salida, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(
            salida,
            etiqueta,
            (x1, max(0, y1 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 0, 255),
            1,
            cv2.LINE_AA,
        )

    return salida
