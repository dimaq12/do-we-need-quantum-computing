#!/usr/bin/env python3
# Two more concept illustrations: the reframing, and the quantum-costume test.
import math, pathlib
OUT=pathlib.Path("/home/dima/do-we-need-quantum-computing/assets")

INK="#1A2233"; MUTED="#6B7689"; FAINT="#9AA3B2"; HAIR="#EAECEF"
GREEN="#0CA678"; GREEN_BG="#E6FCF5"; RED="#E8453C"; RED_BG="#FFF1F0"
BLUE="#4C6EF5"; BLUE_BG="#EDF0FF"; AMBER="#F59F00"; TRACK="#EEF0F3"
PURPLE="#7048E8"; PURPLE_BG="#F3EFFF"

CSS=f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{font-family:'Lato',sans-serif;background:#fff;color:{INK};
 -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;}}
.card{{position:relative;width:1200px;padding:48px 60px 40px;}}
.title{{font-size:40px;font-weight:900;letter-spacing:-.01em;}}

/* reframing */
.qcard{{border-radius:20px;padding:32px 38px;position:relative;}}
.wrongcard{{background:{TRACK};}}
.rightcard{{background:{BLUE_BG};border:2.5px solid {BLUE};}}
.qlabel{{font-size:18px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;}}
.ql-wrong{{color:{FAINT};}} .ql-right{{color:{BLUE};}}
.qtext{{font-size:38px;font-weight:900;letter-spacing:-.01em;margin-top:10px;}}
.qt-wrong{{color:{FAINT};text-decoration:line-through;text-decoration-thickness:4px;
 text-decoration-color:{RED};padding-right:90px;}}
.qt-right{{color:{INK};}}
.xbadge{{position:absolute;right:32px;top:50%;transform:translateY(-50%);
 width:58px;height:58px;border-radius:50%;background:{RED};color:#fff;font-size:34px;
 font-weight:900;display:flex;align-items:center;justify-content:center;}}
.chip{{display:inline-block;margin-top:18px;
 background:#fff;border:2px solid {BLUE};color:{BLUE};font-weight:800;font-size:22px;
 padding:12px 22px;border-radius:999px;}}
.swap{{text-align:center;font-size:34px;color:{FAINT};margin:16px 0;font-weight:700;}}

/* costume cards */
.claimlab{{text-align:center;font-size:18px;font-weight:800;letter-spacing:.12em;
 text-transform:uppercase;color:{FAINT};margin-top:26px;}}
.bigclaim{{text-align:center;margin-top:12px;}}
.bigclaim span{{display:inline-block;background:{PURPLE_BG};color:{PURPLE};
 font-size:26px;font-weight:900;padding:14px 30px;border-radius:999px;}}
.row2{{display:flex;gap:40px;}}
.ccard{{flex:1;border-radius:20px;padding:28px 32px 32px;border:2.5px solid;}}
.cc-green{{background:{GREEN_BG};border-color:{GREEN};}}
.cc-red{{background:{RED_BG};border-color:{RED};}}
.cname{{font-size:29px;font-weight:900;letter-spacing:-.01em;}}
.year{{font-size:20px;font-weight:700;color:{FAINT};margin-left:8px;}}
.verdict{{font-size:27px;font-weight:900;margin-top:6px;}}
.vsub{{font-size:20px;font-weight:400;color:{MUTED};margin-top:8px;line-height:1.45;}}
.vsub b{{font-weight:800;}}
"""
def frame(inner,h):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body><div class='card' style='height:{h}px'>{inner}</div></body></html>")

# ------------------------------------------------------------------ reframing
def concept_reframing():
    inner=(f"<div class='title'>Stop asking the wrong question</div>"
           f"<div style='margin-top:28px'>"
           f"<div class='qcard wrongcard'>"
           f"<div class='qlabel ql-wrong'>The wrong question</div>"
           f"<div class='qtext qt-wrong'>&ldquo;Is this algorithm quantum or classical?&rdquo;</div>"
           f"<div class='xbadge'>&times;</div></div>"
           f"<div class='swap'>&darr;&nbsp; ask instead &nbsp;&darr;</div>"
           f"<div class='qcard rightcard'>"
           f"<div class='qlabel ql-right'>The right question</div>"
           f"<div class='qtext qt-right'>&ldquo;How much structure does the problem have?&rdquo;</div>"
           f"<div class='chip'>measurable &rarr; &Phi;<sub>1</sub></div></div>"
           f"</div>")
    return frame(inner, 660)

# ------------------------------------------------------------------ costume / gauge
def _gauge(val, accent, reading=""):
    """Half-circle gauge, val in [0,1] (0=left/low, 1=right/high)."""
    W,H=380,224; cx,cy=W/2,188; R=148; sw=26
    def pt(ang,r):
        return (cx+r*math.cos(math.radians(ang)), cy-r*math.sin(math.radians(ang)))
    # track gradient arc green->amber->red (left=180 .. right=0)
    gid=f"gg{int(val*100)}"
    grad=(f"<defs><linearGradient id='{gid}' x1='0' y1='0' x2='1' y2='0'>"
          f"<stop offset='0' stop-color='{GREEN}'/><stop offset='.5' stop-color='{AMBER}'/>"
          f"<stop offset='1' stop-color='{RED}'/></linearGradient></defs>")
    x0,y0=pt(180,R); x1,y1=pt(0,R)
    arc=(f"<path d='M {x0:.1f} {y0:.1f} A {R} {R} 0 0 1 {x1:.1f} {y1:.1f}' fill='none' "
         f"stroke='url(#{gid})' stroke-width='{sw}' stroke-linecap='round'/>")
    # needle: tapered wedge with a clear gap to the scale + marker dot on the arc
    ang=180-val*180
    a=math.radians(ang)
    tipx,tipy=pt(ang,R-44)
    perp=(math.sin(a), math.cos(a))          # unit vector perpendicular to needle
    bw2=7                                     # half-width at the hub
    b1=(cx+perp[0]*bw2, cy-perp[1]*bw2)
    b2=(cx-perp[0]*bw2, cy+perp[1]*bw2)
    mx,my=pt(ang,R)
    needle=(f"<polygon points='{tipx:.1f},{tipy:.1f} {b1[0]:.1f},{b1[1]:.1f} "
            f"{b2[0]:.1f},{b2[1]:.1f}' fill='{INK}'/>"
            f"<circle cx='{cx}' cy='{cy}' r='14' fill='{INK}'/>"
            f"<circle cx='{cx}' cy='{cy}' r='5.5' fill='#fff'/>"
            f"<circle cx='{mx:.1f}' cy='{my:.1f}' r='10' fill='#fff' "
            f"stroke='{accent}' stroke-width='5'/>")
    ends=(f"<text x='{x0:.0f}' y='{y0+30:.0f}' text-anchor='middle' font-size='18' "
          f"font-weight='700' fill='{GREEN}'>low</text>"
          f"<text x='{x1:.0f}' y='{y1+30:.0f}' text-anchor='middle' font-size='18' "
          f"font-weight='700' fill='{RED}'>high</text>"
          f"<text x='{cx}' y='{cy-44}' text-anchor='middle' font-size='27' "
          f"font-weight='900' fill='{accent}'>{reading}</text>")
    return f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{grad}{arc}{ends}{needle}</svg>"

def concept_costume():
    phi_l = "&Phi;<tspan baseline-shift='sub' font-size='19'>1</tspan> = 3.3"
    phi_r = "&Phi;<tspan baseline-shift='sub' font-size='19'>1</tspan> = 19.4"
    left=(f"<div class='ccard cc-green'>"
          f"<div class='cname'>Quantum recommendations<span class='year'>2016</span></div>"
          f"<div style='text-align:center;margin:16px 0 4px'>{_gauge(0.13,GREEN,phi_l)}</div>"
          f"<div class='verdict' style='color:{GREEN}'>Classical all along</div>"
          f"<div class='vsub'><b>The claim collapsed</b> &mdash; in 2018 Ewin Tang "
          f"matched it with a classical algorithm. Low &Phi;<sub>1</sub>: sampling "
          f"harvests the structure.</div></div>")
    right=(f"<div class='ccard cc-red'>"
           f"<div class='cname'>Shor&rsquo;s factoring<span class='year'>1994</span></div>"
           f"<div style='text-align:center;margin:16px 0 4px'>{_gauge(0.9,RED,phi_r)}</div>"
           f"<div class='verdict' style='color:{RED}'>Genuinely quantum</div>"
           f"<div class='vsub'><b>The claim stands</b> &mdash; thirty years, no classical "
           f"match. High &Phi;<sub>1</sub>: no handle to grab, the wall RSA rests "
           f"on.</div></div>")
    # connector: one shared claim splits into the two cards
    cxL, cxR = 270, 810   # card centres in the 1080px content row
    conn=(f"<svg width='1080' height='56' viewBox='0 0 1080 56' "
          f"style='display:block;margin:0 auto'>"
          f"<path d='M 540 2 V 22 M {cxL} 22 H {cxR} M {cxL} 22 V 54 M {cxR} 22 V 54' "
          f"stroke='#C3C9D4' stroke-width='2.5' fill='none'/>"
          f"<path d='M {cxL} 54 l -7 -11 h 14 z' fill='#C3C9D4'/>"
          f"<path d='M {cxR} 54 l -7 -11 h 14 z' fill='#C3C9D4'/></svg>")
    inner=(f"<div class='title'>Two &ldquo;exponential speedups&rdquo; &mdash; "
           f"only one is real</div>"
           f"<div class='claimlab'>Both wore the same badge</div>"
           f"<div class='bigclaim'><span>&ldquo;exponential quantum speedup&rdquo;</span></div>"
           f"{conn}"
           f"<div class='row2'>{left}{right}</div>")
    return frame(inner, 860)

OUT.mkdir(parents=True,exist_ok=True)
for name,fn in [("concept-reframing",concept_reframing),("concept-costume",concept_costume)]:
    (OUT/f"{name}.html").write_text(fn(),encoding="utf-8")
    print("wrote",name)
