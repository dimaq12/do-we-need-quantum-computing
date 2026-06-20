# Do We Really Need Quantum Computing?

A self-contained essay + runnable demos. The claim — that a matrix-free *dial*
(the effective rank Φ₁) tells you which "quantum speedups" survive a classical
attack — is not asserted, it is **run**.

- **The article:** [`article.md`](article.md) (also [`article.tex`](article.tex)).
- **The demos** live in [`stands/`](stands/) and are reproducible in seconds.

## Run the demos

```bash
pip install -r requirements.txt
python stands/dequantize.py      # low-rank QML collapses to classical sampling — Φ₁ ≈ 3.3
python stands/shor_wall.py       # factoring is a genuine wall — Φ₁ grows, no shortcut
```

Both stands are built on [`resona`](https://pypi.org/project/resona/) (matrix-free
spectral computation) and print every number the article quotes, checked against
ground truth. Don't trust the essay — run the stands.

---
*Part of the "Spectra Without Matrices" series. Author: Dmitry Sierikov.*
