from pathlib import Path
import sys
import cv2
import pandas as pd
from tqdm import tqdm

RAIZ = Path(__file__).resolve().parents[1]
sys.path.append(str(RAIZ))

from src.utils import cargar_yaml, mapas_de_clases
from src.predict import inferir_imagen
from src.postprocess import ejecutar_postproceso
from src.metrics import metricas_redaccion, cobertura_de_caja_gt


def leer_labels_yolo(ruta_label, ancho, alto, id_a_clase):
    """
    Lee labels YOLO en formato:
    class_id x_center y_center width height.

    Las clases se conservan con las etiquetas originales del dataset:
    name, id, age, date, time.
    """
    filas = []
    ruta_label = Path(ruta_label)

    if not ruta_label.exists():
        return filas

    texto = ruta_label.read_text().strip()
    if not texto:
        return filas

    for idx, linea in enumerate(texto.splitlines()):
        partes = linea.split()

        if len(partes) < 5:
            continue

        id_clase = int(float(partes[0]))
        xc, yc, w, h = [float(x) for x in partes[1:5]]

        x1 = (xc - w / 2) * ancho
        y1 = (yc - h / 2) * alto
        x2 = (xc + w / 2) * ancho
        y2 = (yc + h / 2) * alto

        filas.append({
            "gt_idx": idx,
            "id_clase": id_clase,
            "clase": id_a_clase.get(id_clase, str(id_clase)),
            "caja": [x1, y1, x2, y2],
        })

    return filas


def buscar_imagenes(carpeta_imagenes):
    rutas = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.bmp"]:
        rutas.extend(Path(carpeta_imagenes).glob(ext))
    return sorted(rutas)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Valida el pipeline final usando labels en formato YOLO."
    )

    parser.add_argument("--config", default="config/final_pipeline.yaml")
    parser.add_argument("--pesos", "--weights", dest="pesos", default=None)
    parser.add_argument("--carpeta_imagenes", "--image_dir", dest="carpeta_imagenes", required=True)
    parser.add_argument("--carpeta_labels", "--label_dir", dest="carpeta_labels", required=True)
    parser.add_argument("--csv_salida", "--out_csv", dest="csv_salida", default="results/validation_summary.csv")
    parser.add_argument("--umbral_cobertura", "--coverage_thr", dest="umbral_cobertura", type=float, default=0.98)

    args = parser.parse_args()

    config = cargar_yaml(args.config)
    id_a_clase, _ = mapas_de_clases(config)

    ruta_pesos = Path(args.pesos) if args.pesos else Path(config["modelo"]["pesos"])
    carpeta_imagenes = Path(args.carpeta_imagenes)
    carpeta_labels = Path(args.carpeta_labels)

    filas_imagen = []
    filas_gt = []

    rutas_imagenes = buscar_imagenes(carpeta_imagenes)

    for ruta_imagen in tqdm(rutas_imagenes, desc="Validando"):
        imagen = cv2.imread(str(ruta_imagen))

        if imagen is None:
            continue

        alto, ancho = imagen.shape[:2]

        ruta_label = carpeta_labels / f"{ruta_imagen.stem}.txt"
        gt = leer_labels_yolo(ruta_label, ancho, alto, id_a_clase)
        cajas_gt = [g["caja"] for g in gt]

        detecciones_yolo = inferir_imagen(
            ruta_pesos=ruta_pesos,
            ruta_imagen=ruta_imagen,
            tamano_entrada=int(config["modelo"]["tamano_entrada"]),
            confianza_minima_yolo=float(config["modelo"]["confianza_minima_yolo"]),
            iou_nms_yolo=float(config["modelo"]["iou_nms_yolo"]),
            id_a_clase=id_a_clase,
        )

        detecciones_finales = ejecutar_postproceso(
            detecciones_yolo,
            config,
            ancho,
            alto,
        )

        cajas_predichas = [d["caja_final"] for d in detecciones_finales]
        metricas = metricas_redaccion(cajas_predichas, cajas_gt, ancho, alto)

        coberturas = []

        for g in gt:
            cobertura = cobertura_de_caja_gt(cajas_predichas, g["caja"])
            coberturas.append(cobertura)

            filas_gt.append({
                "imagen": ruta_imagen.name,
                "gt_idx": g["gt_idx"],
                "clase": g["clase"],
                "cobertura": cobertura,
                "protegido": cobertura >= args.umbral_cobertura,
            })

        falsos_negativos = sum(c < args.umbral_cobertura for c in coberturas)

        filas_imagen.append({
            "imagen": ruta_imagen.name,
            "n_gt": len(cajas_gt),
            "n_cajas_predichas": len(cajas_predichas),
            "falsos_negativos": falsos_negativos,
            "cobertura_minima": min(coberturas) if coberturas else None,
            "cobertura_media": sum(coberturas) / len(coberturas) if coberturas else None,
            **metricas,
        })

    csv_salida = Path(args.csv_salida)
    csv_salida.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(filas_imagen).to_csv(csv_salida, index=False)
    pd.DataFrame(filas_gt).to_csv(
        csv_salida.with_name(csv_salida.stem + "_por_gt.csv"),
        index=False,
    )

    print("Guardado:", csv_salida)
    print("Guardado:", csv_salida.with_name(csv_salida.stem + "_por_gt.csv"))


if __name__ == "__main__":
    main()
