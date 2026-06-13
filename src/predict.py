from pathlib import Path
import pandas as pd
from ultralytics import YOLO


def inferir_imagen(ruta_pesos, ruta_imagen, tamano_entrada=960, confianza_minima_yolo=0.001, iou_nms_yolo=0.70, id_a_clase=None):
    """
    Ejecuta inferencia YOLO sobre una imagen y devuelve las detecciones crudas
    en un DataFrame.

    Las coordenadas se devuelven en formato x1, y1, x2, y2.
    """
    modelo = YOLO(str(ruta_pesos))

    resultado = modelo.predict(
        source=str(ruta_imagen),
        imgsz=int(tamano_entrada),
        conf=float(confianza_minima_yolo),
        iou=float(iou_nms_yolo),
        save=False,
        verbose=False,
        stream=False,
    )[0]

    filas = []

    if resultado.boxes is None or len(resultado.boxes) == 0:
        return pd.DataFrame(filas)

    coordenadas = resultado.boxes.xyxy.cpu().numpy()
    scores = resultado.boxes.conf.cpu().numpy()
    clases = resultado.boxes.cls.cpu().numpy().astype(int)

    for caja, score, id_clase in zip(coordenadas, scores, clases):
        if id_a_clase is not None and int(id_clase) not in id_a_clase:
            continue

        filas.append({
            "imagen": Path(ruta_imagen).name,
            "id_clase": int(id_clase),
            "clase": id_a_clase.get(int(id_clase), str(id_clase)) if id_a_clase else str(id_clase),
            "score": float(score),
            "x1": float(caja[0]),
            "y1": float(caja[1]),
            "x2": float(caja[2]),
            "y2": float(caja[3]),
        })

    return pd.DataFrame(filas)
