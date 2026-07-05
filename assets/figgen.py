#!/usr/bin/env python3
# Generate beautiful editorial figures (HTML/SVG) for the Medium article.
import math, os, pathlib

OUT = pathlib.Path("/home/dima/do-we-need-quantum-computing/assets")
OUT.mkdir(parents=True, exist_ok=True)

# ---- design system -----------------------------------------------------------
INK      = "#1A2233"
MUTED    = "#6B7689"
FAINT    = "#9AA3B2"
HAIR     = "#EAECEF"
GREEN    = "#0CA678"   # harvestable / classical
GREEN_BG = "#E6FCF5"
RED      = "#E8453C"   # quantum frontier / the wall
RED_BG   = "#FFF1F0"
BLUE     = "#4C6EF5"   # neutral data
BLUE_BG  = "#EDF0FF"
TRACK    = "#F1F3F5"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{font-family:'Lato',sans-serif;background:#fff;color:{INK};
  -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;}}
.card{{position:relative;width:1200px;padding:48px 60px 40px;}}
.title{{font-size:40px;font-weight:900;letter-spacing:-.01em;}}
.row{{display:flex;gap:36px;margin-top:28px;align-items:flex-start;}}
table{{border-collapse:collapse;font-size:21px;}}
th{{font-size:16px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:{FAINT};text-align:right;padding:0 0 14px 22px;border-bottom:2px solid {HAIR};}}
th:first-child{{text-align:left;padding-left:0;}}
td{{padding:15px 0;text-align:right;font-weight:700;font-variant-numeric:tabular-nums;
  border-bottom:1px solid {HAIR};}}
td:first-child{{text-align:left;font-weight:400;color:{MUTED};
  font-variant-numeric:tabular-nums;}}
td.lead{{padding-left:22px;}}
tr:last-child td{{border-bottom:none;}}
.pill{{display:inline-block;padding:6px 15px;border-radius:999px;font-size:19px;
  font-weight:700;}}
"""

def frame(inner, w, h):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style>"
            f"</head><body><div class='card' style='width:{w}px;height:{h}px'>"
            f"{inner}</div></body></html>")

# ==============================================================================
# FIGURE A — the dequantizable side: table + dual-line chart
# ==============================================================================
def fig_dequantize():
    rows = [("2,000","60","3.0000 %","1.0000"),
            ("20,000","60","0.3000 %","1.0000"),
            ("200,000","60","0.0300 %","1.0000"),
            ("1,000,000","60","0.0060 %","1.0000")]
    trh = "".join(
        f"<tr><td>{a}</td><td class='lead'>{b}</td>"
        f"<td class='lead' style='color:{BLUE}'>{c}</td>"
        f"<td class='lead' style='color:{GREEN}'>{d}</td></tr>" for a,b,c,d in rows)
    table = (f"<table><tr><th>rows&nbsp;n</th><th>sampled</th>"
             f"<th>data&nbsp;touched</th><th>overlap</th></tr>{trh}</table>"
             f"<div style='margin-top:24px;font-size:20px;color:{MUTED}'>"
             f"<span class='pill' style='background:{GREEN_BG};color:{GREEN}'>"
             f"&Phi;<sub>1</sub> = 3.28 &nbsp;·&nbsp; true rank 5</span>"
             f"&nbsp;&nbsp;LOW &rArr; dequantizable</div>")

    # chart geometry
    W,H = 560,400
    L,R,T,B = 80,24,52,92
    px = [L + (W-L-R)*i/3 for i in range(4)]
    xlab = ["2k","20k","200k","1M"]
    # left axis: log %, 10 -> 0.001
    def ylog(v):
        return T + ((1-math.log10(v))/4)*(H-T-B)
    dvals = [3.0,0.3,0.03,0.006]
    dpts = [(px[i], ylog(dvals[i])) for i in range(4)]
    yov  = T + 6  # overlap pinned line near top
    # gridlines for log ticks
    grid=""
    for tick in [10,1,0.1,0.01,0.001]:
        y=ylog(tick)
        lbl = (f"{tick:g}%" if tick>=1 else f"{tick:g}%").replace("0.001%","0.001%")
        grid+=(f"<line x1='{L}' y1='{y:.1f}' x2='{W-R}' y2='{y:.1f}' "
               f"stroke='{HAIR}' stroke-width='1'/>"
               f"<text x='{L-10}' y='{y+5:.1f}' text-anchor='end' "
               f"font-size='17' fill='{FAINT}'>{tick:g}%</text>")
    xticks="".join(f"<text x='{px[i]:.1f}' y='{H-B+30}' text-anchor='middle' "
                   f"font-size='19' fill='{MUTED}' font-weight='700'>{xlab[i]}</text>"
                   for i in range(4))
    # overlap flat line (green)
    ovline=(f"<line x1='{px[0]:.1f}' y1='{yov}' x2='{px[3]:.1f}' y2='{yov}' "
            f"stroke='{GREEN}' stroke-width='3.5'/>")
    ovdots="".join(f"<circle cx='{px[i]:.1f}' cy='{yov}' r='6' fill='#fff' "
                   f"stroke='{GREEN}' stroke-width='3.5'/>" for i in range(4))
    ovtag=(f"<text x='{px[0]:.1f}' y='{yov-16}' font-size='20' font-weight='700' "
           f"fill='{GREEN}'>subspace overlap = 1.0000</text>")
    # data-touched descending line (blue)
    poly=" ".join(f"{x:.1f},{y:.1f}" for x,y in dpts)
    dline=f"<polyline points='{poly}' fill='none' stroke='{BLUE}' stroke-width='3.5'/>"
    ddots="".join(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='6' fill='{BLUE}'/>"
                  for x,y in dpts)
    dlabs=""
    for i,(x,y) in enumerate(dpts):
        anchor = "start" if i==0 else ("end" if i==3 else "middle")
        dx = 11 if i==0 else (2 if i==3 else 0)
        dy = -15
        dlabs+=(f"<text x='{x+dx:.1f}' y='{y+dy:.1f}' text-anchor='{anchor}' "
                f"font-size='18' font-weight='700' fill='{BLUE}'>"
                f"{('%g'%dvals[i])}%</text>")
    dtag=(f"<text x='{px[3]:.1f}' y='{dpts[3][1]+30:.1f}' text-anchor='end' "
          f"font-size='20' font-weight='700' fill='{BLUE}'>% of data touched</text>")
    chart=(f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}'>"
           f"{grid}{xticks}{dline}{ddots}{ovline}{ovdots}{dtag}{dlabs}{ovtag}</svg>")

    inner=(f"<div class='title'>500&times; more data, the same 60 samples</div>"
           f"<div class='row'><div style='flex:0 0 480px'>{table}</div>"
           f"<div>{chart}</div></div>")
    return frame(inner, 1200, 580)

# ==============================================================================
# FIGURE B — Phi_1 bars: Shor vs periodic
# ==============================================================================
def fig_phi1():
    W,H = 1080,300
    L = 300                # label column
    maxv = 60
    barw = 620
    unit = barw/maxv
    y1,y2 = 72,192
    bh = 66
    def bar(y,label,val,col,colbg,note):
        track=(f"<rect x='{L}' y='{y}' width='{barw}' height='{bh}' rx='12' "
               f"fill='{TRACK}'/>")
        w=val*unit
        fill=(f"<rect x='{L}' y='{y}' width='{w:.1f}' height='{bh}' rx='12' "
              f"fill='{col}'/>")
        lab=(f"<text x='{L-26}' y='{y+bh/2-6:.0f}' text-anchor='end' font-size='24' "
             f"font-weight='700' fill='{INK}'>{label}</text>")
        sub=(f"<text x='{L-26}' y='{y+bh/2+24:.0f}' text-anchor='end' font-size='19' "
             f"fill='{MUTED}'>{note}</text>")
        val_t=(f"<text x='{L+w+18:.1f}' y='{y+bh/2+11:.0f}' font-size='30' "
               f"font-weight='900' fill='{col}'>{val:.1f}</text>")
        return track+fill+lab+sub+val_t
    # max marker
    grid=(f"<line x1='{L+barw}' y1='48' x2='{L+barw}' y2='{y2+bh+16}' "
          f"stroke='{HAIR}' stroke-width='1.5' stroke-dasharray='4 4'/>"
          f"<text x='{L+barw}' y='36' text-anchor='middle' font-size='17' "
          f"fill='{FAINT}' font-weight='700'>max = 60</text>")
    b1=bar(y1,"a&#739; mod N",19.4,RED,RED_BG,"Shor&rsquo;s target")
    b2=bar(y2,"period 7",2.0,GREEN,GREEN_BG,"a plain periodic signal")
    arrow=(f"<text x='{L+19.4*unit+110:.0f}' y='{y1+bh/2+8:.0f}' font-size='20' "
           f"font-weight='700' fill='{RED}'>~10&times; higher &mdash; no handle</text>"
           f"<text x='{L+2.0*unit+108:.0f}' y='{y2+bh/2+8:.0f}' font-size='20' "
           f"font-weight='700' fill='{GREEN}'>low &mdash; we harvest it</text>")
    chart=f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{grid}{b1}{b2}{arrow}</svg>"
    inner=(f"<div class='title'>Effective rank of the sequence Shor factors</div>"
           f"<div style='margin-top:22px'>{chart}</div>")
    return frame(inner, 1200, 480)

# ==============================================================================
# FIGURE C — extractability: window line chart + table
# ==============================================================================
def fig_extract():
    windows=[20,40,80,120]
    shor=[1.5,6.1,24.7,40.3]
    per =[2.0,2.0,2.0,2.0]
    W,H=560,400
    L,R,T,B=64,132,44,66
    px=[L+(W-L-R)*i/3 for i in range(4)]
    ymax=45
    def yv(v): return (H-B)-(v/ymax)*((H-B)-T)
    grid=""
    for tick in [0,15,30,45]:
        y=yv(tick)
        grid+=(f"<line x1='{L}' y1='{y:.1f}' x2='{W-R}' y2='{y:.1f}' stroke='{HAIR}' "
               f"stroke-width='1'/><text x='{L-12}' y='{y+5:.1f}' text-anchor='end' "
               f"font-size='17' fill='{FAINT}'>{tick}</text>")
    xticks="".join(f"<text x='{px[i]:.1f}' y='{H-B+30}' text-anchor='middle' "
                   f"font-size='19' font-weight='700' fill='{MUTED}'>{windows[i]}</text>"
                   for i in range(4))
    xtitle=(f"<text x='{(L+W-R)/2:.0f}' y='{H-10}' text-anchor='middle' font-size='17' "
            f"fill='{FAINT}'>window width</text>")
    def line(vals,col):
        poly=" ".join(f"{px[i]:.1f},{yv(vals[i]):.1f}" for i in range(4))
        dots="".join(f"<circle cx='{px[i]:.1f}' cy='{yv(vals[i]):.1f}' r='6' "
                     f"fill='{col}'/>" for i in range(4))
        return f"<polyline points='{poly}' fill='none' stroke='{col}' stroke-width='3.5'/>"+dots
    ls=line(shor,RED); lp=line(per,GREEN)
    tag_s=(f"<text x='{px[3]+14:.1f}' y='{yv(shor[3])+6:.1f}' font-size='20' "
           f"font-weight='900' fill='{RED}'>40.3</text>"
           f"<text x='{px[3]+14:.1f}' y='{yv(shor[3])+30:.1f}' font-size='17' "
           f"font-weight='700' fill='{RED}'>GROWS</text>")
    tag_p=(f"<text x='{px[3]+14:.1f}' y='{yv(per[3])+6:.1f}' font-size='20' "
           f"font-weight='900' fill='{GREEN}'>2.0</text>"
           f"<text x='{px[3]+14:.1f}' y='{yv(per[3])+30:.1f}' font-size='17' "
           f"font-weight='700' fill='{GREEN}'>SATURATES</text>")
    chart=(f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{grid}{xticks}{xtitle}"
           f"{lp}{ls}{tag_s}{tag_p}</svg>")
    # table
    def trow(name,vals,col,note):
        cells="".join(f"<td class='lead' style='color:{col}'>{v:g}</td>" for v in vals)
        return (f"<tr><td>{name}</td>{cells}"
                f"<td class='lead' style='color:{col}'>{note}</td></tr>")
    table=(f"<table><tr><th>window</th><th>20</th><th>40</th><th>80</th><th>120</th>"
           f"<th>closes?</th></tr>"
           f"{trow('a&#739; mod N', shor, RED, 'never')}"
           f"{trow('period 7', per, GREEN, 'at 2.0')}"
           f"</table>"
           f"<div style='margin-top:22px;font-size:20px;color:{MUTED};line-height:1.5'>"
           f"Widen the window: a removable structure <b style='color:{GREEN}'>saturates</b> "
           f"(a finite chart closes &mdash; harvest it). The Shor target "
           f"<b style='color:{RED}'>keeps growing</b> and never closes.</div>")
    inner=(f"<div class='title'>Removable structure saturates; a wall keeps growing</div>"
           f"<div class='row'><div>{chart}</div>"
           f"<div style='flex:0 0 470px'>{table}</div></div>")
    return frame(inner, 1200, 640)

figs = {
    "fig-dequantize": (fig_dequantize(), 1200, 580),
    "fig-phi1":       (fig_phi1(),       1200, 480),
    "fig-extractability": (fig_extract(), 1200, 640),
}
for name,(html,w,h) in figs.items():
    p = OUT / f"{name}.html"
    p.write_text(html, encoding="utf-8")
    print(f"{name} {w}x{h} -> {p}")
