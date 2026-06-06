# Preview Samples

`paired_examples.png` shows paired infrared and visible/RGB examples generated with:

```bash
python scripts/preview_pairs.py ../Primitive --output samples/preview/paired_examples.png
```

`preview_grid.png` is a deterministic sample grid generated from the full dataset with:

```bash
python scripts/preview_grid.py ../Primitive --output samples/preview/preview_grid.png --count 36 --tile-size 128 --columns 6
```

The preview is included for quick visual inspection only. Use the release archive for the full dataset.
