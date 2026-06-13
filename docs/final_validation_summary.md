# Final B7 validation report

## Frozen pipeline

B7_R11R12_box10_dfl1p5_img960_mosaic02 + thresholds x1.5 + padding + BC + V1 + center_nms_medium + no P2.


## Single final model summary

```text
       model_id  n_rows  n_images  total_gt  total_fn  mean_fn  max_fn  mean_privacy_recall  min_privacy_recall  worst_min_coverage  mean_area  std_area  max_area  mean_precision  std_precision  mean_extra_burden  mean_n_redboxes  mean_external_boxes  fn_rate_per_gt
final_single_B7      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
```


## 15-seed summary

```text
model_id  n_rows  n_images  total_gt  total_fn  mean_fn  max_fn  mean_privacy_recall  min_privacy_recall  worst_min_coverage  mean_area  std_area  max_area  mean_precision  std_precision  mean_extra_burden  mean_n_redboxes  mean_external_boxes  fn_rate_per_gt
 seed101      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed11      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed13      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed19      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed23      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed29      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
   seed3      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed37      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed42      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed53      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed61      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
   seed7      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed73      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed89      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
  seed97      80        80       344         0      0.0       0                  1.0                 1.0            0.980583   0.012128  0.000673  0.014072        0.790481       0.032718           0.267183           4.3125                  0.0             0.0
```


## Stability summary

```json
{
  "n_images": 80,
  "mean_image_area_std_across_seeds": 0.0,
  "max_image_area_std_across_seeds": 0.0,
  "mean_image_box_std_across_seeds": 0.0,
  "mean_pairwise_mask_iou": 1.0,
  "min_pairwise_mask_iou": 1.0
}
```


## Calibration summary

```text
class_name  bin  bin_lo  bin_hi   n  mean_confidence  empirical_accuracy      ece
       ALL   -1     NaN     NaN 345         0.947750            0.994203 0.046453
       age   -1     NaN     NaN  80         0.956698            1.000000 0.043302
      date   -1     NaN     NaN  80         0.953106            1.000000 0.046894
        id   -1     NaN     NaN  80         0.961904            1.000000 0.038096
      name   -1     NaN     NaN  81         0.938447            0.975309 0.039813
      time   -1     NaN     NaN  24         0.884284            1.000000 0.115716
```


## Latency percentiles

```json
{
  "yolo_predict_ms": {
    "p95": 23.856336902827024,
    "p99": 24.457422979176037
  },
  "postprocess_ms": {
    "p95": 1.4068054035305977,
    "p99": 1.7294592037796974
  },
  "end_to_end_ms": {
    "p95": 25.138378888368607,
    "p99": 25.86800083518028
  }
}
```


## Figures folder

/hpcfs/home/ing_biomedica/a.laverdeb/treelogic/results_hypatia/final_b7_validation/plots_results
