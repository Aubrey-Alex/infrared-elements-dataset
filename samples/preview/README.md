# Preview Samples

`ir_cutout_grid.png` shows extracted infrared primitive examples generated with:

```bash
python scripts/preview_grid.py ../Primitive/filtered_dataset_20210418_test02 --ir-only --output samples/preview/ir_cutout_grid.png --count 30 --tile-size 128 --columns 10 --seed 3
```

`object_grid.png` shows a broader mixed object-only sample generated with:

```bash
python scripts/preview_grid.py ../Primitive --object-only --output samples/preview/object_grid.png --count 40 --tile-size 128 --columns 10 --seed 21
```

`paired_examples.png` shows paired infrared and visible/RGB examples generated with:

```bash
python scripts/preview_pairs.py ../Primitive --output samples/preview/paired_examples.png
```

`preview_grid.png` is a deterministic sample grid generated from the full dataset with:

```bash
python scripts/preview_grid.py ../Primitive --output samples/preview/preview_grid.png --count 36 --tile-size 128 --columns 6
```

The preview is included for quick visual inspection only. Use the release archive for the full dataset.
