#!/usr/bin/env python3
# Concept illustrations (idea-level) for the Medium article. HTML/SVG -> Chrome PNG.
import math, pathlib

OUT = pathlib.Path("/home/dima/do-we-need-quantum-computing/assets")
OUT.mkdir(parents=True, exist_ok=True)

INK="#1A2233"; MUTED="#6B7689"; FAINT="#9AA3B2"; HAIR="#EAECEF"
GREEN="#0CA678"; GREEN_BG="#E6FCF5"; RED="#E8453C"; RED_BG="#FFF1F0"
BLUE="#4C6EF5"; BLUE_BG="#EDF0FF"; AMBER="#F59F00"; TRACK="#F1F3F5"
INDIGO="#3B4CCA"

CSS=f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{font-family:'Lato',sans-serif;background:#fff;color:{INK};
 -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;}}
.card{{position:relative;width:1200px;padding:48px 60px 40px;}}
.title{{font-size:40px;font-weight:900;letter-spacing:-.01em;}}
"""
def frame(inner,h):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body><div class='card' style='height:{h}px'>{inner}</div></body></html>")

def pill(cx, y, text, fg, bg, anchor_dot_y, above):
    """Rounded label box centred at cx, with a connector down/up to (cx,anchor_dot_y)."""
    shown = text.replace("&middot;", "·").replace("&mdash;", "—")
    w = len(shown)*10.7 + 44
    h = 46
    x = cx - w/2
    py = y
    conn_y1 = py + (h if above else 0)
    line=(f"<line x1='{cx:.1f}' y1='{conn_y1:.1f}' x2='{cx:.1f}' y2='{anchor_dot_y:.1f}' "
          f"stroke='{fg}' stroke-width='1.5' opacity='.5'/>")
    box=(f"<rect x='{x:.1f}' y='{py:.1f}' width='{w:.1f}' height='{h}' rx='23' "
         f"fill='{bg}'/>"
         f"<text x='{cx:.1f}' y='{py+h/2+7:.1f}' text-anchor='middle' font-size='21' "
         f"font-weight='700' fill='{fg}'>{text}</text>")
    dot=(f"<circle cx='{cx:.1f}' cy='{anchor_dot_y:.1f}' r='8' fill='#fff' stroke='{fg}' "
         f"stroke-width='3.5'/>")
    return line+box+dot

# ==============================================================================
# CONCEPT 1 — the dial: one axis, dequantizable -> genuine frontier
# ==============================================================================
def concept_dial():
    W,H=1080,430
    bx0,bx1=70,1010; by=250; bh=28
    grad=(f"<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='0'>"
          f"<stop offset='0' stop-color='{GREEN}'/>"
          f"<stop offset='.5' stop-color='{AMBER}'/>"
          f"<stop offset='1' stop-color='{RED}'/></linearGradient></defs>")
    bar=(f"<rect x='{bx0}' y='{by}' width='{bx1-bx0}' height='{bh}' rx='{bh/2}' fill='url(#g)'/>")
    mid=(bx0+bx1)/2
    divider=(f"<line x1='{mid}' y1='130' x2='{mid}' y2='320' stroke='{FAINT}' "
             f"stroke-width='1.5' stroke-dasharray='5 5'/>")
    zoneL=(f"<text x='{(bx0+mid)/2:.0f}' y='104' text-anchor='middle' font-size='22' "
           f"font-weight='900' letter-spacing='.08em' fill='{GREEN}'>DEQUANTIZABLE</text>"
           f"<text x='{(bx0+mid)/2:.0f}' y='134' text-anchor='middle' font-size='19' "
           f"fill='{MUTED}'>classical sampling harvests it</text>")
    zoneR=(f"<text x='{(mid+bx1)/2:.0f}' y='104' text-anchor='middle' font-size='22' "
           f"font-weight='900' letter-spacing='.08em' fill='{RED}'>GENUINE FRONTIER</text>"
           f"<text x='{(mid+bx1)/2:.0f}' y='134' text-anchor='middle' font-size='19' "
           f"fill='{MUTED}'>no handle &mdash; the quantum computer earns its price</text>")
    ends=(f"<text x='{bx0}' y='{by+bh+36}' font-size='21' font-weight='700' fill='{GREEN}'>"
          f"low &Phi;<tspan baseline-shift='sub' font-size='15'>1</tspan></text>"
          f"<text x='{bx1}' y='{by+bh+36}' text-anchor='end' font-size='21' font-weight='700' "
          f"fill='{RED}'>high &Phi;<tspan baseline-shift='sub' font-size='15'>1</tspan></text>")
    # examples: (label, x-on-bar, above?)
    L=[("Low-rank ML &middot; Tang",168,True),
       ("Clifford circuits",282,False),
       ("Free fermions",405,True),
       ("Low-entanglement",518,False)]
    R=[("Shor &middot; discrete log",645,True),
       ("Volume-law growth",800,False),
       ("Random circuits",935,True)]
    pills=""
    for txt,x,ab in L:
        py = 158 if ab else 320
        pills+=pill(x,py,txt,GREEN,GREEN_BG,by+(0 if ab else bh),ab)
    for txt,x,ab in R:
        py = 158 if ab else 320
        pills+=pill(x,py,txt,RED,RED_BG,by+(0 if ab else bh),ab)
    svg=(f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{grad}{divider}"
         f"{zoneL}{zoneR}{bar}{ends}{pills}</svg>")
    inner=(f"<div class='title'>Not &ldquo;quantum or classical&rdquo; &mdash; "
           f"how much structure?</div>"
           f"<div style='margin-top:26px'>{svg}</div>")
    return frame(inner, 620)

# ==============================================================================
# CONCEPT 2 — dequantization: a giant operator that lives in r directions
# ==============================================================================
def concept_dequant():
    W,H=1080,400
    # big tall matrix
    mx,my,mw,mh=70,70,210,280
    cell_rows=14
    rowh=mh/cell_rows
    grid=(f"<rect x='{mx}' y='{my}' width='{mw}' height='{mh}' rx='6' fill='{BLUE_BG}' "
          f"stroke='{HAIR}'/>")
    for i in range(1,cell_rows):
        grid+=(f"<line x1='{mx}' y1='{my+i*rowh:.1f}' x2='{mx+mw}' y2='{my+i*rowh:.1f}' "
               f"stroke='#fff' stroke-width='1.5'/>")
    sampled=[2,5,9,12]
    for r in sampled:
        grid+=(f"<rect x='{mx}' y='{my+r*rowh:.1f}' width='{mw}' height='{rowh:.1f}' "
               f"fill='{BLUE}' opacity='.85'/>")
    mlabel=(f"<text x='{mx+mw/2}' y='{my-42}' text-anchor='middle' font-size='22' "
            f"font-weight='700' fill='{INK}'>A &mdash; implicit, never formed</text>"
            f"<text x='{mx+mw/2}' y='{my-14}' text-anchor='middle' font-size='19' "
            f"fill='{FAINT}'>N = 1,000,000 rows</text>")
    nbrace=""
    # sample bracket on left
    sbx=mx
    sbrace=(f"<text x='{sbx}' y='{my+mh+38}' font-size='21' font-weight='700' fill='{BLUE}'>"
            f"sample 60 rows &prop; &#8214;row&#8214;&sup2;</text>")
    # arrow
    ax=316
    arrow=(f"<line x1='{ax}' y1='{my+mh/2}' x2='{ax+86}' y2='{my+mh/2}' stroke='{INK}' "
           f"stroke-width='3'/><path d='M {ax+86} {my+mh/2} l -15 -9 v 18 z' fill='{INK}'/>"
           f"<text x='{ax+43}' y='{my+mh/2-16:.0f}' text-anchor='middle' font-size='19' "
           f"font-weight='700' fill='{MUTED}'>recover</text>")
    # subspace: r=5 colored vertical bars in a card
    sx,sy,sw,sh=440,120,240,180
    scard=(f"<rect x='{sx}' y='{sy}' width='{sw}' height='{sh}' rx='12' fill='#fff' "
           f"stroke='{HAIR}' stroke-width='1.5'/>")
    cols=[GREEN,BLUE,AMBER,RED,INDIGO]
    bw=26; gap=18; total=5*bw+4*gap; startx=sx+(sw-total)/2
    bars=""
    heights=[140,116,150,104,128]
    for k in range(5):
        bxx=startx+k*(bw+gap)
        bhh=heights[k]; byy=sy+sh-26-bhh
        bars+=(f"<rect x='{bxx:.0f}' y='{byy:.0f}' width='{bw}' height='{bhh}' rx='5' "
               f"fill='{cols[k]}'/>")
    slabel=(f"<text x='{sx+sw/2:.0f}' y='{sy-20}' text-anchor='middle' font-size='22' "
            f"font-weight='700' fill='{INK}'>the subspace it lives in</text>"
            f"<text x='{sx+sw/2:.0f}' y='{sy+sh+34}' text-anchor='middle' font-size='21' "
            f"font-weight='700' fill='{GREEN}'>rank r = 5 &nbsp;&#8810;&nbsp; N</text>")
    # big takeaway to the right
    tx=730
    take=(f"<text x='{tx}' y='142' font-size='30' font-weight='900' fill='{INK}'>"
          f"Cost tracks the</text>"
          f"<text x='{tx}' y='184' font-size='30' font-weight='900' fill='{GREEN}'>"
          f"rank, not the</text>"
          f"<text x='{tx}' y='226' font-size='30' font-weight='900' fill='{INK}'>"
          f"dimension.</text>"
          f"<text x='{tx}' y='274' font-size='21' fill='{MUTED}'>The million rows never</text>"
          f"<text x='{tx}' y='304' font-size='21' fill='{MUTED}'>get touched &mdash; only 60,</text>"
          f"<text x='{tx}' y='334' font-size='21' fill='{MUTED}'>chosen by their weight.</text>")
    svg=(f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{grid}{mlabel}{nbrace}"
         f"{sbrace}{arrow}{scard}{bars}{slabel}{take}</svg>")
    inner=(f"<div class='title'>A million-row operator that lives in five directions</div>"
           f"<div style='margin-top:30px'>{svg}</div>")
    return frame(inner, 640)

# ==============================================================================
# CONCEPT 3 — the wall: singular-value spectra (few modes vs many) = effective rank
# ==============================================================================
def _scree(x0, vals, effk, accent, accent_bg, title, phi, modes_note):
    pw, ph = 430, 280
    by = 110                       # top of plot
    base = by + ph
    n = len(vals); gap = 4
    bw = (pw - (n+1)*gap) / n
    # effective-rank shading band over first effk bars
    shade_w = effk*bw + (effk+1)*gap
    out = (f"<rect x='{x0}' y='{by}' width='{shade_w:.1f}' height='{ph}' rx='6' "
           f"fill='{accent_bg}'/>")
    # baseline
    out += (f"<line x1='{x0}' y1='{base}' x2='{x0+pw}' y2='{base}' stroke='{HAIR}' "
            f"stroke-width='1.5'/>")
    for k,v in enumerate(vals):
        bx = x0 + gap + k*(bw+gap)
        bh = max(2.0, v*ph)
        col = accent if k < effk else "#C7CCD6"
        out += (f"<rect x='{bx:.1f}' y='{base-bh:.1f}' width='{bw:.1f}' height='{bh:.1f}' "
                f"rx='2' fill='{col}'/>")
    # title, sigma axis label, modes brace
    out += (f"<text x='{x0+pw/2:.0f}' y='{by-56}' text-anchor='middle' font-size='25' "
            f"font-weight='900' fill='{accent}'>{title}</text>"
            f"<text x='{x0+pw/2:.0f}' y='{by-24}' text-anchor='middle' font-size='21' "
            f"font-weight='700' fill='{MUTED}'>&Phi;<tspan baseline-shift='sub' "
            f"font-size='15'>1</tspan> = {phi}</text>")
    # bracket under the shaded band marking the effective-rank modes
    bxl, bxr, byk = x0+gap, x0+shade_w, base+16
    out += (f"<path d='M {bxl:.1f} {byk} v 8 H {bxr:.1f} v -8' fill='none' "
            f"stroke='{accent}' stroke-width='2.5'/>"
            f"<text x='{(bxl+bxr)/2:.1f}' y='{byk+40:.0f}' text-anchor='middle' "
            f"font-size='22' font-weight='900' fill='{accent}'>{modes_note}</text>")
    return out

def concept_wall():
    W,H = 1080, 470
    # schematic normalized singular spectra, matching the stand's Phi_1 (2.0 vs 19.4)
    per  = [1.0, 0.97] + [0.05*0.62**k for k in range(22)]
    shor = [1.0 - 0.012*k for k in range(19)] + [0.10,0.07,0.045,0.03,0.02]
    left  = _scree(70,  per,  2,  GREEN, GREEN_BG,
                   "periodic signal", "2.0", "2 modes")
    right = _scree(W-70-430, shor, 19, RED, RED_BG,
                   "a&#739; mod N (Shor)", "19.4", "~19 modes")
    svg = f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{left}{right}</svg>"
    inner=(f"<div class='title'>A few modes to grab &mdash; or weight spread "
           f"across them all</div>"
           f"<div style='margin-top:22px'>{svg}</div>")
    return frame(inner, 700)

for name,fn in [("concept-dial",concept_dial),
                ("concept-dequantize",concept_dequant),
                ("concept-wall",concept_wall)]:
    (OUT/f"{name}.html").write_text(fn(),encoding="utf-8")
    print("wrote",name)
