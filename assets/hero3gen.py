#!/usr/bin/env python3
# Three hero-banner candidates for the article. HTML -> headless Chrome PNG @2x.
#   v1  "spectra"  — editorial serif title over a ridgeline field (EB Garamond)
#   v2  "verdict"  — two singular-value spectra, one dial, two verdicts
#   v3  "gauge"    — the Φ₁ dial as a literal glowing gauge
import math, random, pathlib

OUT = pathlib.Path("/home/dima/do-we-need-quantum-computing/assets")
W, H = 1400, 740

GREEN = "#19C39A"; AMBER = "#FFB020"; RED = "#FF5A4D"
INK0 = "#0A0F1E"; INK1 = "#111A31"; MUT = "rgba(255,255,255,.62)"
FAINT = "rgba(255,255,255,.40)"

BASE_CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{INK0};
 font-family:'Lato',sans-serif;-webkit-font-smoothing:antialiased;
 text-rendering:geometricPrecision;}}
.stage{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
 background:linear-gradient(150deg,{INK0} 0%,{INK1} 100%);}}
.dots{{position:absolute;inset:0;opacity:.05;
 background-image:radial-gradient(rgba(255,255,255,.9) 1px, transparent 1px);
 background-size:28px 28px;}}
.mark{{position:absolute;right:64px;bottom:36px;font-size:14.5px;color:{FAINT};z-index:9;}}
.mark b{{color:rgba(255,255,255,.85);font-weight:800;}}
"""

def page(name, css, body):
    html = (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{BASE_CSS}{css}</style></head><body>"
            f"<div class='stage'>{body}</div></body></html>")
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")
    print("wrote", name)

# ══════════════════════════════════════════════════════════════════════════
# V1 — SPECTRA: serif editorial title over a ridgeline field.
#      Left massif small & sharp (low rank), right massif tall & broad (high).
# ══════════════════════════════════════════════════════════════════════════
def v1():
    rng = random.Random(11)
    rows, x0, x1, step = 22, -20, W + 20, 14
    y_top, spacing = 348, 15.5
    def envelope(x):
        g1 = 78 * math.exp(-((x - 385) / 105) ** 2)     # low-rank: narrow spike
        g2 = 168 * math.exp(-((x - 1010) / 205) ** 2)   # frontier: broad massif
        return g1 + g2
    paths = []
    for i in range(rows):
        depth = i / (rows - 1)                     # 0 = back row, 1 = front
        base = y_top + i * spacing
        # smooth per-row randomness: coarse uniform noise, moving-average x3
        n = (x1 - x0) // step + 2
        raw = [rng.random() for _ in range(n)]
        sm = [(raw[max(0, j-1)] + raw[j] + raw[min(n-1, j+1)]) / 3 for j in range(n)]
        pts = []
        for j in range(n):
            x = x0 + j * step
            amp = envelope(x) * (0.28 + 0.72 * sm[j]) * (0.45 + 0.55 * depth)
            pts.append((x, base - amp))
        d = f"M {pts[0][0]:.0f} {pts[0][1]:.1f} " + " ".join(
            f"L {x:.0f} {y:.1f}" for x, y in pts[1:])
        fill = d + f" L {x1} {H+20} L {x0} {H+20} Z"
        op = 0.28 + 0.62 * depth
        paths.append(f"<path d='{fill}' fill='{INK0}'/>"
                     f"<path d='{d}' fill='none' stroke='url(#sg)' "
                     f"stroke-width='{1.1 + 0.9*depth:.2f}' stroke-opacity='{op:.2f}' "
                     f"stroke-linejoin='round'/>")
    svg = (f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}' "
           f"style='position:absolute;inset:0'>"
           f"<defs><linearGradient id='sg' x1='0' y1='0' x2='1' y2='0'>"
           f"<stop offset='0' stop-color='{GREEN}'/>"
           f"<stop offset='.48' stop-color='{AMBER}'/>"
           f"<stop offset='1' stop-color='{RED}'/></linearGradient></defs>"
           + "".join(paths) + "</svg>")
    css = f"""
.glowL{{position:absolute;left:120px;top:430px;width:360px;height:150px;border-radius:50%;
 background:rgba(25,195,154,.30);filter:blur(90px);}}
.glowR{{position:absolute;right:120px;top:330px;width:480px;height:220px;border-radius:50%;
 background:rgba(255,90,77,.26);filter:blur(100px);}}
.wrap{{position:absolute;left:80px;top:64px;right:80px;z-index:5;}}
.kicker{{font-size:14.5px;font-weight:700;letter-spacing:.36em;text-transform:uppercase;
 color:{FAINT};}}
.h1{{margin-top:26px;font-family:'EB Garamond',serif;font-size:88px;line-height:1.02;
 color:#F4F6FB;letter-spacing:-.005em;}}
.h1 em{{font-style:italic;background:linear-gradient(95deg,{GREEN},{AMBER} 55%,{RED});
 -webkit-background-clip:text;background-clip:text;color:transparent;}}
.sub{{margin-top:22px;font-size:21px;font-weight:300;line-height:1.55;color:{MUT};
 max-width:760px;}}
.sub b{{color:#fff;font-weight:700;}}
.zone{{position:absolute;bottom:34px;font-size:13px;font-weight:800;
 letter-spacing:.14em;text-transform:uppercase;z-index:6;}}
.zone i{{font-style:normal;font-weight:600;color:{FAINT};letter-spacing:.02em;
 text-transform:none;}}
"""
    body = f"""
<div class='glowL'></div><div class='glowR'></div>
{svg}
<div class='wrap'>
  <div class='kicker'>Spectra&nbsp;Without&nbsp;Matrices</div>
  <div class='h1'>Do we really need<br><em>quantum computing?</em></div>
  <div class='sub'>One matrix-free number &mdash; the effective rank
    <b>&Phi;<sub>1</sub></b> &mdash; separates the speedups that survive a classical
    attack from the ones that were <b>never quantum at all</b>.</div>
</div>
<div class='zone' style='left:80px;color:{GREEN}'>low &Phi;<sub>1</sub> &nbsp;<i>&middot;&nbsp; dequantizable</i></div>
<div class='zone' style='right:64px;color:{RED};text-align:right'>high &Phi;<sub>1</sub> &nbsp;<i>&middot;&nbsp; genuine frontier</i></div>
"""
    # v1 keeps its corner zones; move resona mark up out of the ridges
    body += f"<div class='mark' style='bottom:auto;top:70px'><b>resona</b> &nbsp;&middot;&nbsp; matrix-free spectra</div>"
    page("hero-v1", css, body)

# ══════════════════════════════════════════════════════════════════════════
# V2 — VERDICT: two singular-value spectra side by side. Same dial, two reads.
# ══════════════════════════════════════════════════════════════════════════
def lerp_hex(c1, c2, t):
    a = [int(c1[i:i+2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i+2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(a[k]+(b[k]-a[k])*t):02X}" for k in range(3))

def v2():
    n, bw = 30, 9
    maxh = 210
    left_v = [1.0, .87, .70, .16, .10] + [max(.028, .07 * math.exp(-k/3)) for k in range(n-5)]
    right_v = [math.exp(-k / 16) for k in range(n)]
    def bars(vals, colors, glow):
        out = []
        for k, v in enumerate(vals):
            h = max(5, v * maxh)
            sh = f"box-shadow:0 0 22px {colors[k]}99;" if (glow and v > .3) else ""
            out.append(f"<div class='bar' style='height:{h:.0f}px;"
                       f"background:{colors[k]};{sh}'></div>")
        return "".join(out)
    lcol = [GREEN if v > .3 else "#33415C" for v in left_v]
    rcol = [lerp_hex(AMBER, RED, k / (n - 1)) for k in range(n)]
    css = f"""
.head{{position:absolute;top:58px;left:0;right:0;text-align:center;z-index:5;}}
.kicker{{font-size:14px;font-weight:700;letter-spacing:.36em;text-transform:uppercase;
 color:{FAINT};}}
.h1{{margin-top:18px;font-size:58px;font-weight:900;letter-spacing:-.02em;color:#fff;}}
.h1 span{{background:linear-gradient(95deg,{GREEN},{AMBER} 55%,{RED});
 -webkit-background-clip:text;background-clip:text;color:transparent;}}
.sub{{margin-top:14px;font-size:19px;font-weight:300;color:{MUT};}}
.sub b{{color:#fff;font-weight:700;}}
.panel{{position:absolute;bottom:96px;width:560px;z-index:5;}}
.pL{{left:88px;}} .pR{{right:88px;}}
.ptop{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:16px;}}
.pname{{font-size:14px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;}}
.pphi{{font-size:26px;font-weight:900;font-variant-numeric:tabular-nums;}}
.pphi small{{font-size:15px;font-weight:700;color:{FAINT};}}
.bars{{position:relative;display:flex;align-items:flex-end;gap:6px;height:{maxh}px;
 border-bottom:1.5px solid rgba(255,255,255,.16);}}
.bar{{width:{bw}px;border-radius:4px 4px 0 0;}}
.pcap{{margin-top:14px;font-size:15.5px;color:{MUT};height:52px;line-height:1.45;}}
.pcap b{{font-weight:800;}}
.div{{position:absolute;left:50%;bottom:96px;height:290px;
 border-left:2px dashed rgba(255,255,255,.22);z-index:4;}}
.note{{position:absolute;bottom:10px;left:210px;font-size:14.5px;font-style:italic;
 color:{FAINT};}}
.formula{{position:absolute;left:88px;bottom:36px;font-size:14.5px;color:{FAINT};
 font-variant-numeric:tabular-nums;z-index:9;}}
.formula i{{color:rgba(255,255,255,.8);font-style:normal;}}
.glowL{{position:absolute;left:120px;bottom:80px;width:420px;height:180px;border-radius:50%;
 background:rgba(25,195,154,.20);filter:blur(90px);}}
.glowR{{position:absolute;right:120px;bottom:80px;width:420px;height:180px;border-radius:50%;
 background:rgba(255,90,77,.20);filter:blur(90px);}}
"""
    body = f"""
<div class='dots'></div>
<div class='glowL'></div><div class='glowR'></div>
<div class='head'>
  <div class='kicker'>Spectra&nbsp;Without&nbsp;Matrices</div>
  <div class='h1'>Do we really need <span>quantum computing?</span></div>
  <div class='sub'>The same matrix-free dial, pointed at two famous speedups &mdash;
    <b>two opposite verdicts</b>.</div>
</div>
<div class='panel pL'>
  <div class='ptop'><span class='pname' style='color:{GREEN}'>Quantum recommendations</span>
    <span class='pphi' style='color:{GREEN}'><small>&Phi;<sub>1</sub> =</small> 3.3</span></div>
  <div class='bars'>{bars(left_v, lcol, True)}
    <div class='note'>&hellip;the other 27 directions are noise</div></div>
  <div class='pcap'><b style='color:{GREEN}'>Dequantizable.</b> Three directions carry
    everything &mdash; classical sampling harvests it.</div>
</div>
<div class='div'></div>
<div class='panel pR'>
  <div class='ptop'><span class='pname' style='color:{RED}'>Shor's factoring target</span>
    <span class='pphi' style='color:{RED}'><small>&Phi;<sub>1</sub> =</small> 19.4</span></div>
  <div class='bars'>{bars(right_v, rcol, False)}</div>
  <div class='pcap'><b style='color:{RED}'>Genuine frontier.</b> The weight never
    concentrates &mdash; no handle for sampling to grab.</div>
</div>
<div class='formula'>&Phi;<sub>1</sub> = <i>(Tr A)&sup2; / Tr A&sup2;</i> &mdash; effective rank</div>
<div class='mark'><b>resona</b> &nbsp;&middot;&nbsp; matrix-free spectra</div>
"""
    page("hero-v2", css, body)

# ══════════════════════════════════════════════════════════════════════════
# V3 — GAUGE: the Φ₁ dial as a literal glowing半 gauge, needle on the wall.
# ══════════════════════════════════════════════════════════════════════════
def v3():
    cx, cy, R = 985, 560, 285
    def pol(ang_deg, r):
        a = math.radians(ang_deg)
        return cx + r * math.cos(a), cy - r * math.sin(a)
    # main arc
    ax0, ay0 = pol(180, R); ax1, ay1 = pol(0, R)
    arc = (f"<path d='M {ax0:.1f} {ay0:.1f} A {R} {R} 0 0 1 {ax1:.1f} {ay1:.1f}' "
           f"fill='none' stroke='url(#gg)' stroke-width='30' stroke-linecap='round'/>")
    # ticks
    ticks = []
    for k in range(1, 28):
        a = 180 - k * 180 / 28
        x1_, y1_ = pol(a, R - 34); x2_, y2_ = pol(a, R - (48 if k % 7 else 58))
        w = 2.4 if k % 7 == 0 else 1.3
        ticks.append(f"<line x1='{x1_:.1f}' y1='{y1_:.1f}' x2='{x2_:.1f}' y2='{y2_:.1f}' "
                     f"stroke='rgba(255,255,255,.30)' stroke-width='{w}'/>")
    # labeled nodes on the arc
    nodes = []
    for ang, txt, col in [(163, "low-rank ML", GREEN), (133, "Clifford", GREEN),
                          (103, "free fermions", GREEN), (53, "Shor", RED),
                          (27, "random circuits", RED)]:
        nx, ny = pol(ang, R)
        lx, ly = pol(ang, R + 44)
        anchor = "end" if ang > 97 else "start"
        if 80 < ang < 97: anchor = "middle"
        nodes.append(
            f"<circle cx='{nx:.1f}' cy='{ny:.1f}' r='7' fill='#fff' "
            f"stroke='{INK0}' stroke-width='4'/>"
            f"<text x='{lx:.1f}' y='{ly:.1f}' text-anchor='{anchor}' font-size='16' "
            f"font-weight='700' fill='{col}' font-family='Lato'>{txt}</text>")
    # midline divider
    dx0, dy0 = pol(90, R - 64); dx1, dy1 = pol(90, R + 30)
    divider = (f"<line x1='{dx0:.1f}' y1='{dy0:.1f}' x2='{dx1:.1f}' y2='{dy1:.1f}' "
               f"stroke='rgba(255,255,255,.30)' stroke-width='1.6' stroke-dasharray='5 6'/>")
    # needle at Shor-ish angle
    na = 53
    nx1, ny1 = pol(na, R - 52); nx0, ny0 = pol(na + 180, 34)
    needle = (f"<line x1='{nx0:.1f}' y1='{ny0:.1f}' x2='{nx1:.1f}' y2='{ny1:.1f}' "
              f"stroke='#fff' stroke-width='5' stroke-linecap='round' "
              f"filter='url(#nglow)'/>"
              f"<circle cx='{cx}' cy='{cy}' r='13' fill='#fff'/>"
              f"<circle cx='{cx}' cy='{cy}' r='5.5' fill='{INK0}'/>")
    zone_txt = (
        f"<text x='{pol(180, R+8)[0]:.0f}' y='{cy+42}' font-size='14.5' font-weight='800' "
        f"fill='{GREEN}' letter-spacing='.1em' font-family='Lato'>LOW &Phi;&#8321;</text>"
        f"<text x='{pol(0, R+8)[0]:.0f}' y='{cy+42}' text-anchor='end' font-size='14.5' "
        f"font-weight='800' fill='{RED}' letter-spacing='.1em' font-family='Lato'>HIGH &Phi;&#8321;</text>"
        f"<text x='{cx}' y='{cy+46}' text-anchor='middle' font-size='15.5' "
        f"fill='rgba(255,255,255,.55)' font-family='Lato'>&Phi;&#8321; &mdash; effective rank</text>")
    svg = (f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}' "
           f"style='position:absolute;inset:0;z-index:3'>"
           f"<defs>"
           f"<linearGradient id='gg' x1='0' y1='0' x2='1' y2='0'>"
           f"<stop offset='0' stop-color='{GREEN}'/><stop offset='.5' stop-color='{AMBER}'/>"
           f"<stop offset='1' stop-color='{RED}'/></linearGradient>"
           f"<filter id='nglow' x='-60%' y='-60%' width='220%' height='220%'>"
           f"<feDropShadow dx='0' dy='0' stdDeviation='4.5' flood-color='#fff' "
           f"flood-opacity='.45'/></filter>"
           f"</defs>{arc}{''.join(ticks)}{divider}{''.join(nodes)}{needle}{zone_txt}</svg>")
    css = f"""
.glow1{{position:absolute;left:660px;top:300px;width:340px;height:220px;border-radius:50%;
 background:rgba(25,195,154,.22);filter:blur(95px);}}
.glow2{{position:absolute;right:60px;top:280px;width:400px;height:260px;border-radius:50%;
 background:rgba(255,90,77,.26);filter:blur(95px);}}
.wrap{{position:absolute;left:80px;top:0;bottom:0;width:520px;z-index:5;
 display:flex;flex-direction:column;justify-content:center;}}
.kicker{{font-size:14px;font-weight:700;letter-spacing:.36em;text-transform:uppercase;
 color:{FAINT};}}
.h1{{margin-top:24px;font-size:64px;font-weight:900;line-height:1.05;
 letter-spacing:-.02em;color:#fff;}}
.h1 span{{background:linear-gradient(95deg,{GREEN},{AMBER} 55%,{RED});
 -webkit-background-clip:text;background-clip:text;color:transparent;}}
.sub{{margin-top:22px;font-size:20px;font-weight:300;line-height:1.55;color:{MUT};}}
.sub b{{color:#fff;font-weight:700;}}
.chips{{margin-top:30px;display:flex;flex-direction:column;gap:12px;}}
.chip{{display:flex;align-items:center;gap:12px;font-size:15.5px;color:{MUT};}}
.chip .sw{{width:12px;height:12px;border-radius:50%;flex:none;}}
.chip b{{color:#fff;font-weight:800;}}
.formula{{margin-top:30px;font-size:15px;color:{FAINT};font-variant-numeric:tabular-nums;}}
.formula i{{color:rgba(255,255,255,.8);font-style:normal;}}
"""
    body = f"""
<div class='dots'></div>
<div class='glow1'></div><div class='glow2'></div>
{svg}
<div class='wrap'>
  <div class='kicker'>Spectra&nbsp;Without&nbsp;Matrices</div>
  <div class='h1'>Do we really need <span>quantum computing?</span></div>
  <div class='sub'>One dial &mdash; the effective rank <b>&Phi;<sub>1</sub></b> &mdash;
    reads a problem's structure and says who wins: <b>classical sampling, or the
    quantum machine</b>.</div>
  <div class='chips'>
    <div class='chip'><span class='sw' style='background:{GREEN}'></span>
      <span><b>Low &Phi;<sub>1</sub></b> &mdash; dequantizable, sample it classically</span></div>
    <div class='chip'><span class='sw' style='background:{RED}'></span>
      <span><b>High &Phi;<sub>1</sub></b> &mdash; no handle, the quantum computer earns its price</span></div>
  </div>
  <div class='formula'>&Phi;<sub>1</sub> = <i>(Tr A)&sup2; / Tr A&sup2;</i></div>
</div>
<div class='mark'><b>resona</b> &nbsp;&middot;&nbsp; matrix-free spectra</div>
"""
    page("hero-v3", css, body)

v1(); v2(); v3()
