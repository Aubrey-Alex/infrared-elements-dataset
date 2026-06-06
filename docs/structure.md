# Dataset Structure

The complete archive uses the following high-level layout:

```text
infrared-elements/
  202304131130_test01_filtered/
    infrared/
    visual/
  202304131130_test02_filtered/
    infrared/
    visual/
  202304131130_test03_filtered/
    infrared/
    visual/
  202304131130_test04_filtered/
    infrared/
    visual/
  202304131130_test05_filtered/
    infrared/
    visual/
  filtered_dataset_20210418_test01/
    person/
      ir/
      rgb/
    vehicle/
      ir/
      rgb/
  filtered_dataset_20210418_test02/
    person/
      ir/
      rgb/
    vehicle/
      ir/
      rgb/
  filtered_dataset_202304131400/
    person/
      ir/
      rgb/
    vehicle/
      ir/
      rgb/
  filtered_dataset_202304141211_test01/
    person/
      ir/
      rgb/
    vehicle/
      ir/
      rgb/
  filtered_dataset_202304141211_test02/
    person/
      ir/
      rgb/
    vehicle/
      ir/
      rgb/
```

Per-file details are available in [../metadata/manifest.csv](../metadata/manifest.csv). Per-image SHA256 checksums are available in [../metadata/file_checksums.sha256](../metadata/file_checksums.sha256). Aggregate counts are available in [../metadata/statistics.json](../metadata/statistics.json).
