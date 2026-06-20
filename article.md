# Do we really need quantum computing?

*A student dequantized a famous quantum algorithm. A single matrix-free dial tells you which speedups survive — and which were never quantum at all.*

## The hook

In 2018 a then-undergraduate, Ewin Tang, did something that was supposed to be impossible. There was a celebrated quantum algorithm for recommendation systems — the kind that suggests your next film — and it ran exponentially faster than any known classical method. It was a poster child for "quantum advantage in machine learning."

Tang dequantized it. She wrote a *classical* algorithm that matched the quantum one's speed. The exponential gap vanished. And it turned out not to be a one-off: a whole family of "quantum machine learning" speedups quietly collapsed the same way.

So the uncomfortable question is real. When someone shows you a quantum speedup, how do you know it is genuine — that no clever student will dequantize it next year — versus a speedup that was *redundant all along*, classical advantage wearing a quantum costume? It turns out there is a single number you can measure, matrix-free, that tells you which side of the line you are on.

## The idea

The number is **effective rank** — in resona, `Φ₁`. The shorthand: *quantum advantage needs structure a classical machine cannot cheaply simulate.* And the most common "structure" in quantum ML — low rank — is exactly the structure classical sampling harvests for free.

Here is the intuition. If a giant operator secretly lives in a low-dimensional subspace — its action is captured by a handful of directions — then you do not need to touch the whole thing. You can *sample* a few rows or columns and reconstruct that subspace. Cost scales with the rank, not the dimension. That is precisely what Tang's algorithm does, and it is why the quantum speedup evaporated: the quantum computer was paying (in entanglement, in qubits) for structure that classical sampling gets at a discount.

`Φ₁` measures that structure as a single scalar — the effective number of directions the operator really uses. **Low `Φ₁` ⇒ dequantizable.** **High `Φ₁` ⇒ genuine frontier**, no sampling handle, no shortcut. One dial, computed from matrix–vector products, no matrix formed.

The reframing this buys you is worth pausing on. The usual question — "is this algorithm quantum or classical?" — turns out to be the wrong one. The right question is "how much *structure* does the problem have?", and structure is measurable. A quantum computer is, in this view, a machine that pays a fixed price (qubits, coherence, error correction) to handle high-structure problems. If the structure is low, you overpaid: a classical sampler does the same job for free. The dial does not argue philosophy; it measures the resource and reads off which regime you are standing in.

## The demo: the dequantizable side

The stand is `stands/dequantize.py`. It builds an implicit low-rank operator (true rank `r = 5`, embedded in up to a million rows) and recovers its top singular subspace by sampling a fixed `s = 60` rows:

```
   n (rows)  rows sampled   data touched   subspace overlap
 ──────────────────────────────────────────────────────────
      2,000            60        3.0000%             1.0000
     20,000            60        0.3000%             1.0000
    200,000            60        0.0300%             1.0000
  1,000,000            60        0.0060%             1.0000
```

The same 60 samples work as `n` grows 500×. At a million rows we touch **0.006% of the data** and still recover the subspace with overlap **1.0000**. And the dial reads the situation correctly:

```
Φ₁ = resona.effective_rank(AᵀA) = 3.28   (true rank r=5) — LOW ⇒ dequantizable
```

Low `Φ₁`. The "exponential quantum advantage" here was redundant — it was paying for low-rank structure that classical sampling extracts for free.

[FIGURE: subspace overlap ≈ 1 holding flat as n grows from 2k to 1M, fraction of data touched plunging to 0.006%]

## The demo: the genuine wall

Now point the *same dial* at Shor's algorithm — factoring, the speedup that actually threatens RSA. The stand is `stands/shor_wall.py`. When the order `r` is small, even classical period-finding factors `N` cheaply (`N=15` via order 4, `N=323` via order 72). The trouble is that for RSA-sized `N`, the order is itself exponentially large. So look at what `Φ₁` reads on the sequence `a^x mod N` — the thing Shor's quantum period-finding chews on:

```
                    sequence   Φ₁ (eff. rank, max=60)
     a^x mod N (Shor target)                 19.4   ← ~10× higher: no handle
         periodic (period 7)                  2.0   ← low: we harvest it
```

The Shor sequence reads **`Φ₁ = 19.4`** — about **10× higher** than a simple periodic signal. No low-rank handle. And the dial's extractability test — does the structure *saturate* as you widen the window (removable) or keep *growing* (a genuine wall)? — is decisive:

```
                    window →    20     40     80    120   extractable?
     a^x mod N (Shor target)   1.5    6.1   24.7   40.3   False  ← GROWS: chart never closes
         periodic (period 7)   2.0    2.0    2.0    2.0   True   ← SATURATES: finite lift
```

The periodic signal saturates at 2.0 — a finite chart closes, you harvest it classically. The Shor target keeps growing (1.5 → 40.3) and never closes: `extractable? False`. The same dial that dequantized the low-rank problem here points firmly the other way.

One sentence on what this means: the dial said "redundant, sample it" for the low-rank case and "genuine quantum frontier, no shortcut" for Shor — and it said both *from the same matrix-free measurement*, the effective rank you already have.

## The honest limit

`Φ₁` does not beat *all* quantum computing — and the stand says so plainly. It beats exactly the **low-rank / structured class**: low-rank linear algebra (Tang), Clifford circuits, free fermions, low-entanglement dynamics. Speedups there are at most polynomial. It does **not** touch the genuine frontier: Shor factoring and discrete log, real-time volume-law entanglement growth, generic random-circuit sampling. Reading the dial as high does not give you a classical algorithm for Shor — beating Shor classically would mean factoring in polynomial time and breaking RSA, and there is no known path. The framework honestly points *away* from that. The dial tells you which fight you are in; it does not win the unwinnable one.

## Run it yourself

```
pip install -r requirements.txt
python stands/dequantize.py
python stands/shor_wall.py
```

Every number above is reproducible: subspace overlap 1.0000 at a million rows touching 0.006% of the data, `Φ₁ = 3.28` on the low-rank side, `Φ₁ = 19.4` and `extractable? False` on the Shor side. Don't trust me — run it.
