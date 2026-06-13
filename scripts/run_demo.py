from pathlib import Path
import sys
import cv2
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.append(str(RAIZ))

from src.utils import cargar_yaml, crear_carpeta, mapas_de_clases
from src.predict import inferir_imagen
from src.postprocess import ejecutar_postproceso
from src.redact import anonimizar_imagen, guardar_imagen
from src.visualize import dibujar_cajas


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Ejecuta la demo del pipeline final de anonimizacion PHI sobre una imagen."
    )

    parser.add_argument("--config", default="config/final_pipeline.yaml")
    parser.add_argument("--pesos", "--weights", dest="pesos", default=None)
    parser.add_argument("--imagen", "--image", dest="imagen", required=True)
    parser.add_argument("--salida", "--out", dest="salida", default="examples/output")

    args = parser.parse_args()

    config = cargar_yaml(args.config)
    id_a_clase, _ = mapas_de_clases(config)

    ruta_pesos = Path(args.pesos) if args.pesos else Path(config["modelo"]["pesos"])
    ruta_imagen = Path(args.imagen)
    carpeta_salida = crear_carpeta(args.salida)

    imagen = cv2.imread(str(ruta_imagen))
    if imagen is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta_imagen}")

    alto, ancho = imagen.shape[:2]

    detecciones_yolo = inferir_imagen(
        ruta_pesos=ruta_pesos,
        ruta_imagen=ruta_imagen,
        tamano_entrada=int(config["modelo"]["tamano_entrada"]),
        confianza_minima_yolo=float(config["modelo"]["confianza_minima_yolo"]),
        iou_nms_yolo=float(config["modelo"]["iou_nms_yolo"]),
        id_a_clase=id_a_clase,
    )

    detecciones_finales = ejecutar_postproceso(detecciones_yolo, config, ancho, alto)

    imagen_anonimizada = anonimizar_imagen(imagen, detecciones_finales)
    imagen_con_cajas = dibujar_cajas(imagen, detecciones_finales)

    stem_imagen = ruta_imagen.stem

    guardar_imagen(carpeta_salida / f"{stem_imagen}_anonimizada.png", imagen_anonimizada)
    guardar_imagen(carpeta_salida / f"{stem_imagen}_cajas.png", imagen_con_cajas)

    pd.DataFrame([
        {
            "id_clase": det["id_clase"],
            "clase": det["clase"],
            "score": det["score"],
            "x1": det["caja_final"][0],
            "y1": det["caja_final"][1],
            "x2": det["caja_final"][2],
            "y2": det["caja_final"][3],
            "traza": det.get("traza", ""),
        }
        for det in detecciones_finales
    ]).to_csv(carpeta_salida / f"{stem_imagen}_cajas.csv", index=False)

    print("Archivos guardados:")
    print(" -", carpeta_salida / f"{stem_imagen}_anonimizada.png")
    print(" -", carpeta_salida / f"{stem_imagen}_cajas.png")
    print(" -", carpeta_salida / f"{stem_imagen}_cajas.csv")


if __name__ == "__main__":
    main()
