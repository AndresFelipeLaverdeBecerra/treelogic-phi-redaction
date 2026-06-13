# Treelogic PHI Redaction

Repositorio del pipeline final para detectar y anonimizar informacion sensible en radiografias de torax.

El objetivo es localizar regiones con informacion protegida del paciente y cubrirlas automaticamente para generar una imagen anonimizada.

## Pipeline final

La solucion final utiliza:

- Detector YOLO entrenado para informacion sensible en radiografias.
- Umbrales conservadores por clase.
- Padding de seguridad.
- Ajuste vertical basado en la caja original del detector.
- Ajuste vertical basado en alturas vecinas.
- Supresion conservadora de duplicados cercanos.
- Generacion de imagen anonimizada por redaccion de regiones detectadas.

## Clases detectadas

Se conservan los nombres originales del dataset:

| ID | Clase |
|---:|------|
| 0 | name |
| 1 | id |
| 2 | age |
| 3 | date |
| 4 | time |

## Instalacion

Con entorno virtual:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Con Conda:

    conda env create -f environment.yml
    conda activate treelogic_phi_redaction

## Pesos del modelo

Coloque el archivo del modelo entrenado en:

    models/best.pt

## Ejecutar demo en una imagen

    python scripts/run_demo.py \
      --pesos models/best.pt \
      --imagen examples/input/sample_xray.png \
      --salida examples/output

La demo genera:

    examples/output/sample_xray_anonimizada.png
    examples/output/sample_xray_cajas.png
    examples/output/sample_xray_cajas.csv

## Ejecutar sobre una carpeta

    python scripts/run_batch_redaction.py \
      --pesos models/best.pt \
      --carpeta_entrada examples/input \
      --carpeta_salida examples/output

## Validacion opcional

Si se tienen labels en formato YOLO:

    python scripts/validate_final_pipeline.py \
      --pesos models/best.pt \
      --carpeta_imagenes <ruta_imagenes> \
      --carpeta_labels <ruta_labels> \
      --csv_salida results/validation_summary.csv

## Resumen de validacion interna

El pipeline final obtuvo en validacion interna:

- 15 semillas de entrenamiento.
- 80 imagenes de validacion.
- 5160 instancias acumuladas de informacion sensible.
- 0 falsos negativos.
- 15/15 semillas con 0 falsos negativos.
- Fraccion media de area censurada: 0.01213.
- Precision media de redaccion: 0.79048.
- Cajas externas promedio: 0.0.
- Latencia p95 end-to-end: aproximadamente 25 ms.

## Limitaciones

Los resultados corresponden a validacion interna. Antes de un uso clinico o productivo se requiere validacion externa, revision regulatoria y evaluacion sobre datos independientes.
