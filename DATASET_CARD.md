# Dataset Card

## Dataset Summary

Infrared Elements Dataset provides cropped infrared target elements and paired visible/RGB reference images. It is intended to support infrared simulation, target insertion experiments, data inspection, and model development tasks where reusable target primitives are useful.

## Intended Uses

- infrared simulation and target composition research
- non-commercial computer vision experiments
- teaching and demonstration
- dataset browsing, quality analysis, and benchmarking support

## Out-of-Scope Uses

- commercial redistribution without permission
- surveillance deployment or identification of real people
- use as a substitute for safety-critical validation data
- claims that the data represents all infrared imaging conditions

## Data Format

- image format: PNG
- annotation files: not included
- metadata: per-file manifest, per-image checksums, release-archive checksums, and aggregate statistics
- distribution: GitHub Release archive

## Dataset Structure

The complete archive contains 10 top-level subsets. Some subsets contain `infrared` and `visual` directories; others contain object categories such as `person` and `vehicle`, each with `ir` and `rgb` directories.

See [docs/structure.md](docs/structure.md) for the complete structure summary.

## Data Generation Notice

The data generation program and its implementation details are not published in this repository. Only dataset files, metadata, documentation, previews, and utility scripts are provided.

## Limitations

- The dataset is a curated element dataset and may not represent complete scene distributions.
- No semantic annotation files are included.
- Users should inspect samples and metadata before using the data for training or evaluation.

## Maintenance

Versioned releases are recorded in [CHANGELOG.md](CHANGELOG.md). Checksums are provided for reproducibility.
