# Resumen de validación interna

Este documento resume la validación interna del pipeline de anonimización de información sensible en radiografías de tórax.

## Objetivo

Evaluar si el pipeline detecta y cubre regiones con información sensible del paciente, manteniendo una censura limitada al área necesaria de la imagen.

## Pipeline evaluado

El sistema final combina:

- Detector YOLO entrenado para localizar regiones sensibles.
- Umbrales conservadores por clase.
- Padding de seguridad alrededor de cada detección.
- Ajuste vertical de las cajas detectadas.
- Supresión conservadora de duplicados cercanos.
- Redacción visual de las regiones detectadas.

Las clases del modelo se mantienen con las etiquetas originales del dataset:

| ID | Clase |
|---:|------|
| 0 | name |
| 1 | id |
| 2 | age |
| 3 | date |
| 4 | time |

## Resultados principales

| Métrica | Resultado |
|---|---:|
| Imágenes evaluadas | 80 |
| Semillas de entrenamiento evaluadas | 15 |
| Instancias sensibles acumuladas | 5160 |
| Falsos negativos acumulados | 0 |
| Semillas con 0 falsos negativos | 15/15 |
| Cobertura mínima observada | 0.9806 |
| Área media censurada | 0.01213 |
| Precisión media de redacción | 0.79048 |
| Cajas externas promedio | 0.0 |
| Latencia p95 end-to-end | ~25 ms |

## Interpretación

La validación interna muestra que el pipeline logró cubrir todas las regiones sensibles anotadas en el conjunto evaluado, con un área censurada promedio cercana al 1.2% de la imagen.

El objetivo principal fue priorizar privacidad, por lo que el diseño favorece una cobertura conservadora de las regiones sensibles antes que una censura mínima absoluta.

## Figuras incluidas

La carpeta `docs/figures/` contiene gráficas de apoyo sobre:

- Falsos negativos por semilla.
- Área censurada promedio.
- Precisión media de redacción.
- Estabilidad entre semillas.
- Sensibilidad del postprocesamiento.
- Calibración.
- Latencia.

## Limitaciones

Estos resultados corresponden a validación interna. Antes de usar el sistema en un entorno clínico, productivo o externo, se requiere validación adicional con datos independientes y revisión de los requisitos regulatorios aplicables.
