#!/usr/bin/env python3
# Hero banner for the Medium article. Dark, dramatic, glowing Φ₁ spectrum.
import pathlib
OUT=pathlib.Path("/home/dima/do-we-need-quantum-computing/assets")

GREEN="#19C39A"; AMBER="#FFB020"; RED="#FF5A4D"
INKBG0="#0B1020"; INKBG1="#131B30"
W,Hc=1400,740

HTML=f"""<!doctype html><html><head><meta charset='utf-8'><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{font-family:'Lato',sans-serif;-webkit-font-smoothing:antialiased;
 text-rendering:geometricPrecision;height:100%;background:{INKBG0};}}
.stage{{position:relative;width:{W}px;height:100%;overflow:hidden;
 background:
   radial-gradient(1100px 600px at 12% 8%, rgba(25,195,154,.20), transparent 55%),
   radial-gradient(1100px 600px at 92% 96%, rgba(255,90,77,.22), transparent 55%),
   linear-gradient(140deg, {INKBG0} 0%, {INKBG1} 100%);}}
/* faint dotted texture */
.dots{{position:absolute;inset:0;opacity:.06;
 background-image:radial-gradient(rgba(255,255,255,.9) 1.1px, transparent 1.1px);
 background-size:26px 26px;}}
.wrap{{position:absolute;inset:0;padding:74px 80px;}}
.kicker{{font-size:15px;font-weight:700;letter-spacing:.34em;text-transform:uppercase;
 color:rgba(255,255,255,.42);}}
.h1{{margin-top:30px;font-size:66px;font-weight:900;line-height:1.04;letter-spacing:-.02em;
 color:#fff;}}
.grad{{background:linear-gradient(95deg,{GREEN} 0%,{AMBER} 52%,{RED} 100%);
 -webkit-background-clip:text;background-clip:text;color:transparent;}}
.sub{{margin-top:24px;font-size:23px;line-height:1.5;font-weight:400;
 color:rgba(255,255,255,.66);max-width:880px;}}
.sub b{{color:#fff;font-weight:700;}}
/* spectrum */
.spec-wrap{{position:absolute;left:80px;right:80px;bottom:132px;}}
.zoneL,.zoneR{{position:absolute;top:-46px;font-size:15px;font-weight:900;
 letter-spacing:.1em;}}
.zoneL{{left:2px;color:{GREEN};}} .zoneR{{right:2px;color:{RED};text-align:right;}}
.zsub{{display:block;font-size:12.5px;font-weight:600;letter-spacing:.02em;
 color:rgba(255,255,255,.45);margin-top:5px;text-transform:none;}}
.bar{{position:relative;height:30px;border-radius:15px;
 background:linear-gradient(90deg,{GREEN} 0%,{AMBER} 50%,{RED} 100%);
 box-shadow:0 0 0 1px rgba(255,255,255,.06),
   0 14px 50px -8px rgba(25,195,154,.5),
   0 14px 50px -8px rgba(255,90,77,.5);}}
.glow{{position:absolute;bottom:108px;height:90px;width:420px;border-radius:50%;
 filter:blur(70px);z-index:0;}}
.glowL{{left:60px;background:rgba(25,195,154,.55);}}
.glowR{{right:60px;background:rgba(255,90,77,.55);}}
.divider{{position:absolute;left:50%;top:-30px;height:74px;border-left:2px dashed
 rgba(255,255,255,.32);}}
.node{{position:absolute;top:9px;width:12px;height:12px;border-radius:50%;
 background:#fff;box-shadow:0 0 0 4px rgba(11,16,32,.55);transform:translateX(-50%);}}
.tag{{position:absolute;bottom:-30px;font-size:13px;font-weight:700;
 transform:translateX(-50%);white-space:nowrap;}}
.ends{{position:absolute;left:0;right:0;bottom:-30px;}}
.lowphi{{position:absolute;left:0;font-size:14px;font-weight:800;color:{GREEN};}}
.highphi{{position:absolute;right:0;font-size:14px;font-weight:800;color:{RED};}}
.mark{{position:absolute;right:80px;bottom:44px;font-size:15px;
 color:rgba(255,255,255,.5);}}
.mark b{{color:rgba(255,255,255,.82);font-weight:800;}}
.phichip{{position:absolute;left:80px;bottom:44px;font-size:14px;font-weight:700;
 color:rgba(255,255,255,.5);font-variant-numeric:tabular-nums;}}
.phichip i{{color:rgba(255,255,255,.8);font-style:normal;}}
</style></head>
<body><div class='stage'>
 <div class='dots'></div>
 <div class='glow glowL'></div><div class='glow glowR'></div>
 <div class='wrap'>
   <div class='kicker'>Spectra&nbsp;Without&nbsp;Matrices</div>
   <div class='h1'>Do we really need<br><span class='grad'>quantum computing?</span></div>
   <div class='sub'>One matrix-free dial &mdash; the effective rank
     <b>&Phi;<sub>1</sub></b> &mdash; tells you which quantum speedups survive a
     classical attack, and which were <b>never quantum at all</b>.</div>
   <div class='phichip'>&Phi;<sub>1</sub> = <i>(Tr A)&sup2; / Tr A&sup2;</i></div>
   <div class='mark'><b>resona</b> &nbsp;&middot;&nbsp; matrix-free spectra</div>
 </div>
 <div class='spec-wrap'>
   <div class='zoneL'>DEQUANTIZABLE<span class='zsub'>structure a classical machine harvests</span></div>
   <div class='zoneR'>GENUINE FRONTIER<span class='zsub'>no handle &mdash; the quantum computer earns its price</span></div>
   <div class='bar'>
     <div class='divider'></div>
     <div class='node' style='left:14%'></div>
     <div class='node' style='left:30%'></div>
     <div class='node' style='left:44%'></div>
     <div class='node' style='left:66%'></div>
     <div class='node' style='left:84%'></div>
     <div class='tag' style='left:14%;color:{GREEN}'>Low-rank ML</div>
     <div class='tag' style='left:44%;color:{GREEN}'>free fermions</div>
     <div class='tag' style='left:66%;color:{RED}'>Shor</div>
     <div class='tag' style='left:84%;color:{RED}'>random circuits</div>
   </div>
   <div class='ends'>
     <span class='lowphi'>low &Phi;<sub>1</sub></span>
     <span class='highphi'>high &Phi;<sub>1</sub></span>
   </div>
 </div>
</div></body></html>"""

OUT.mkdir(parents=True, exist_ok=True)
(OUT/"hero.html").write_text(HTML,encoding="utf-8")
print("wrote hero.html", W, Hc)
