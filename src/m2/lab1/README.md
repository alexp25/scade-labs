# Module 2 · Lab 1 — Configuration Management (maintainer files)

Published lab: `docs/m2/lab1/` (`lab.md`, `index.html`, `cmp-submit.js`,
`CMP_template_CruiseControl.docx`). The GitHub part and its checker are a
separate lab, `docs/m2/lab2/` (no `src/` files).

| Path | What it is | Published? |
|---|---|---|
| `tools/build_cmp_docs.py` | Generates both CMP Word documents from one content definition | No |
| `solution/CMP_CruiseControl_reference.docx` | Instructor reference: the CMP template fully completed | **No — never copy into `docs/`** |
| `../../../docs/m2/lab1/CMP_template_CruiseControl.docx` | Student template (partially filled, red TODOs) | Yes |

## Regenerating the Word documents

Both `.docx` files are generated — edit `tools/build_cmp_docs.py`, not the
`.docx` files, then run from the repository root:

```
python src/m2/lab1/tools/build_cmp_docs.py
```

Requires `python-docx` (verified with 1.1.0).
