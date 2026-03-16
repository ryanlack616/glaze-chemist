# Glaze Chemist

A free, browsable reference directory for glaze chemistry — the people, books, and ideas that shaped the field. Part of [Stull Atlas](https://stullatlas.app).

**Live at:** `stullatlas.app/glaze-chemist`

## What's in it

| Category | Count | Description |
|----------|-------|-------------|
| People | 35 | Chemists, potters, educators, authors who shaped glaze science |
| Books | 30 | Essential texts on glazes, formulation, and ceramic chemistry |
| Concepts | 3 | Foundational ideas (UMF, Currie Grids, Limit Formulas) |

## Build

```
python build.py
```

Reads `data/glaze_references.json` and generates a static site into `dist/`.

## Structure

```
glaze-chemist/
  build.py              # Static site generator
  data/
    glaze_references.json  # Source data
  dist/                 # Built site (deploy this)
    index.html
    people/
    books/
    concepts/
```

## Deploy

Upload the contents of `dist/` to `stullatlas.app/glaze-chemist`.

## Adding data

Edit `data/glaze_references.json` and re-run `python build.py`. The JSON schema supports people, books, institutions, and concepts with cross-referencing via IDs.
