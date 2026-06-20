# I spent ~$1000 on AI tools to find out if we actually need quantum computers

*The honest companion to the [technical piece](article.md). Same question, different angle — less math, more confession.*

## The confession

Here is the unglamorous version of how this project started: I spent roughly a
thousand dollars on AI tools — subscriptions, credits, the usual stack — chasing a
question that had been nagging me for months. *Which quantum speedups are real, and
which ones are just classical algorithms wearing a costume?*

And here is the very 2025–2026 part of the story. You pour money into one tool, you
get used to its quirks, you build your workflow around it — and a couple of months
later something else shows up that does 80–90% of the same job for noticeably less.
You sit there thinking: *wait, could I have done this three times cheaper?* 😄

If you've shipped anything with AI in the last year, you know this feeling. The
ecosystem is moving fast enough that almost everyone goes through some version of
it. So let me not pretend I played it perfectly. I didn't. I overpaid, I switched
tools mid-stream, I burned credits on dead ends.

## But that's the wrong question

The thing is, "did you waste $1000 on Cursor?" is not actually the interesting
question. The interesting one is:

> **Would this thing exist without it?**

And if the honest answer is *"no,"* or *"it would have taken another six months,"*
then it stops looking like such a bad trade.

I've watched this happen to a lot of people — myself included. A project sits in a
folder of notes for months. *I'll get to it.* Then, with AI in the loop, a few
weeks later there's suddenly:

- a working library,
- a test suite,
- documentation,
- a gallery of examples,
- a stack of articles,

— a *finished thing* instead of a folder of good intentions. That transition, from
"interesting idea I keep meaning to build" to "package other people can install,"
is the part that used to quietly kill projects. The $1000 mostly bought a way
through that wall.

## What actually came out

So here's what the thousand dollars and — more honestly — a lot of stubbornness
turned into.

The original question was about **dequantization**: when a famous quantum machine
learning algorithm got matched by a classical one (a then-undergraduate did it in
2018, and a whole family of "quantum advantages" quietly collapsed afterward), I
wanted to know if there was a *measurable* way to tell the genuine speedups from
the costumes. It turns out there is — a single matrix-free number, the effective
rank, that reads *low → dequantizable* and *high → genuine frontier*. The
[technical article](article.md) walks through it with code, and the demos in
[`stands/`](stands/) print every number, checked against ground truth. You can run
them in about a minute.

But the diagnostic was one read of one object, and the object kept opening doors.
The dial that dequantizes low-rank machine learning is the same dial that says
*Shor's factoring is a real wall, no shortcut.* The same machinery reads the
spectrum of a million-node graph, the curvature of a neural network's loss
landscape, the eigenvalues of a non-symmetric operator scattered across the complex
plane, a Gaussian process likelihood on data too big to store. So the
"dequantization experiment" grew into a small matrix-free spectral library —
[`resona`](https://pypi.org/project/resona/), now on PyPI, with a test suite and a
couple dozen short articles, each built on a runnable demo.

I'm not going to oversell it. The mathematics it stands on is established — free
probability, stochastic trace estimation, pseudospectra, the Brown measure — all of
it has rightful owners, credited in the project. What's mine is the synthesis: one
interface, matrix-free, that makes a dozen disconnected fields answer to the same
handful of commands. That's a framing and an engineering job, not a new theorem,
and I try to say exactly that wherever I can. A tool that overclaims is a tool you
can't trust.

## The part the receipt doesn't show

If you total it up, the $1000 is the visible cost, and it's a real number. But it's
not the big one. The expensive part was the hours — turning a pile of conjectures
and half-finished scripts into something that runs, passes its own tests, and
explains itself to a stranger. That always costs far more than it looks like from
the outside. The AI tools compressed it; they didn't make it free.

So would I do it again? Knowing what I know now — different tools, fewer dead ends —
probably for less. But the trade itself, money-and-stubbornness for a finished
package instead of a folder of notes, I'd take again without much hesitation.

And honestly, it makes for a better opening line than most. *"I spent about a
thousand dollars on AI tools trying to figure out which quantum advantages are
real, and ended up with a whole package of experiments and a library"* is a more
interesting sentence than *"I built a library over a weekend."* 😄

---

**If you want the actual science** — the dial, the demos, the line between
dequantizable and genuine — it's all in the [companion article](article.md), with
code you can run:

```bash
pip install -r requirements.txt
python stands/dequantize.py    # the dequantizable side: Φ₁ ≈ 3.3
python stands/shor_wall.py     # the genuine wall: Φ₁ grows, no shortcut
```

*Part of the "Spectra Without Matrices" series. Author: Dmitry Sierikov.*
