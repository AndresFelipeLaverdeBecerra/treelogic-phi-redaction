from pathlib import Path
import yaml


def cargar_yaml(ruta):
    ruta = Path(ruta)
    with open(ruta, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def crear_carpeta(ruta):
    ruta = Path(ruta)
    ruta.mkdir(parents=True, exist_ok=True)
    return ruta


def mapas_de_clases(config):
    id_a_clase = {int(k): v for k, v in config["clases"].items()}
    clase_a_id = {v: k for k, v in id_a_clase.items()}
    return id_a_clase, clase_a_id
