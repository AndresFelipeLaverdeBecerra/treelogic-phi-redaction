from pathlib import Path
import subprocess
import sys


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Ejecuta anonimizacion PHI sobre una carpeta de imagenes."
    )

    parser.add_argument("--config", default="config/final_pipeline.yaml")
    parser.add_argument("--pesos", "--weights", dest="pesos", default=None)
    parser.add_argument("--carpeta_entrada", "--input_dir", dest="carpeta_entrada", required=True)
    parser.add_argument("--carpeta_salida", "--out_dir", dest="carpeta_salida", required=True)

    args = parser.parse_args()

    extensiones = {".png", ".jpg", ".jpeg", ".bmp"}
    carpeta_entrada = Path(args.carpeta_entrada)

    imagenes = sorted([
        p for p in carpeta_entrada.iterdir()
        if p.suffix.lower() in extensiones
    ])

    if not imagenes:
        raise FileNotFoundError(f"No se encontraron imagenes en {carpeta_entrada}")

    for imagen in imagenes:
        comando = [
            sys.executable,
            "scripts/run_demo.py",
            "--config",
            args.config,
            "--imagen",
            str(imagen),
            "--salida",
            args.carpeta_salida,
        ]

        if args.pesos:
            comando += ["--pesos", args.pesos]

        print("Ejecutando:", " ".join(comando))
        subprocess.check_call(comando)


if __name__ == "__main__":
    main()
