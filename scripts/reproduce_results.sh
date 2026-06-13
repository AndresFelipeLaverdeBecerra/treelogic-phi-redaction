#!/usr/bin/env bash
set -euo pipefail

echo "1. Instalar dependencias:"
echo "   pip install -r requirements.txt"
echo
echo "2. Colocar pesos del modelo en:"
echo "   models/best.pt"
echo
echo "3. Ejecutar demo en una imagen:"
echo "   python scripts/run_demo.py --pesos models/best.pt --imagen examples/input/sample_xray.png --salida examples/output"
echo
echo "4. Ejecutar anonimizacion en una carpeta:"
echo "   python scripts/run_batch_redaction.py --pesos models/best.pt --carpeta_entrada examples/input --carpeta_salida examples/output"
echo
echo "5. Validacion opcional si hay labels YOLO:"
echo "   python scripts/validate_final_pipeline.py --pesos models/best.pt --carpeta_imagenes <imagenes> --carpeta_labels <labels> --csv_salida results/validation_summary.csv"
