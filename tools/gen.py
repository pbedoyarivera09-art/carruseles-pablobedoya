"""Genera las 9 láminas HTML del carrusel de Founder GPS (marca pablobedoya.ScaleUp).

Uso: python tools/gen.py ig   -> html/ig-01.html ... ig-09.html (1080 x 1350)
Descarga las fuentes Playfair Display y DM Sans de Google Fonts a fuentes/ si no están.
"""
import math, os, re, sys, urllib.request

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = "@pablobedoya.scaleup"
N = 9
INK, INK2, CREAM, CREAM2, LIME, MUTED = "#1C1A17", "#3A3730", "#F4F0E8", "#EDE8DE", "#E6E93F", "#9A9590"


def ensure_fonts():
    d = os.path.join(OUT, "fuentes")
    css_path = os.path.join(d, "fuentes.css")
    if os.path.exists(css_path):
        return
    os.makedirs(d, exist_ok=True)
    ua = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}
    url = "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=DM+Sans:wght@300;400;700;800&display=swap"
    css = urllib.request.urlopen(urllib.request.Request(url, headers=ua), timeout=30).read().decode("utf-8")
    out = []
    for sub, b in re.findall(r"/\* (\S+) \*/\s*(@font-face \{.*?\})", css, re.S):
        if sub != "latin":
            continue
        fam = re.search(r"font-family: '([^']+)'", b).group(1)
        w = re.search(r"font-weight: (\d+)", b).group(1)
        src = re.search(r"url\((\S+?)\)", b).group(1)
        fn = f"{fam.replace(' ', '')}-{w}.woff2"
        open(os.path.join(d, fn), "wb").write(urllib.request.urlopen(urllib.request.Request(src, headers=ua), timeout=30).read())
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('../fuentes/{fn}') format('woff2');}}")
    open(css_path, "w").write("\n".join(out))


def dot_scatter(W, H):
    c = []
    for x in range(40, W, 48):
        for y in range(40, H, 48):
            c.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{INK2}"/>')
    pts = [(136, 232), (904, 328), (952, 760), (88, 1000), (520, 1130)] if H > 1200 else [(136, 232), (904, 328), (952, 700), (88, 860), (520, 980)]
    for x, y in pts:
        c.append(f'<circle cx="{x-8}" cy="{y-8}" r="5" fill="{LIME}"/>')
    return f'<svg class="bg" viewBox="0 0 {W} {H}">{"".join(c)}</svg>'


def concentric(W, H):
    cx, cy = 800, H - 330
    c = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK2}" stroke-width="1.5"/>' for r in range(110, 1100, 110)]
    c.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="{LIME}"/>')
    return f'<svg class="bg" viewBox="0 0 {W} {H}">{"".join(c)}</svg>'


def halftone(W, H):
    c = []
    step = 36
    for x in range(0, W + step, step):
        for y in range(0, H + step, step):
            d1 = math.hypot((x - W) / W, (y - H) / H)
            t = max(0, 1 - d1 / 0.42)
            r = t * 21
            if r > 1.0:
                c.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{INK}"/>')
    return f'<svg class="bg" viewBox="0 0 {W} {H}">{"".join(c)}</svg>'


ICON = {
    "compass": f'<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" stroke="{LIME}"/>',
    "target": f'<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2" stroke="{LIME}" fill="{LIME}"/>',
    "mega": f'<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6" stroke="{LIME}"/>',
}


def icon(name, size=112):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{CREAM}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>'


def months(active, W):
    seg = []
    for i in range(3):
        col = LIME if i == active else INK2
        seg.append(f'<div class="seg"><b style="background:{col}"></b><span style="color:{CREAM2 if i == active else MUTED}">Mes {i+1}</span></div>')
    return f'<div class="months">{"".join(seg)}</div>'


def timeline(W):
    w = W - 128
    x0, x1 = 14, w - 14
    y = 44
    parts = [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{INK2}" stroke-width="2"/>']
    for i in range(12):
        x = x0 + i * (x1 - x0) / 11
        parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="9" fill="{INK}" stroke="{CREAM2}" stroke-width="2"/>')
    for m in range(3):
        a = x0 + (m * 4) * (x1 - x0) / 11
        b = x0 + (m * 4 + 3) * (x1 - x0) / 11
        parts.append(f'<line x1="{a-9:.1f}" y1="92" x2="{b+9:.1f}" y2="92" stroke="{LIME if m == 0 else INK2}" stroke-width="3" opacity="1"/>')
        parts.append(f'<text x="{(a+b)/2:.1f}" y="132" text-anchor="middle" fill="{CREAM2}" font-family="DM Sans" font-weight="700" font-size="24" letter-spacing="3">MES {m+1}</text>')
    return f'<svg class="tl" width="{w}" height="150" viewBox="0 0 {w} 150">{"".join(parts)}</svg>'


def score_line(W):
    w = W - 128
    x0, x1 = 40, w - 40
    y = 70
    parts = [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{INK2}" stroke-width="2"/>']
    for s, lab, sub in [(1, "Sesión 1", "Al empezar"), (8, "Sesión 8", "A mitad"), (12, "Sesión 12", "Al terminar")]:
        x = x0 + (s - 1) * (x1 - x0) / 11
        anc = "start" if s == 1 else ("end" if s == 12 else "middle")
        tx = x - 28 if s == 1 else (x + 28 if s == 12 else x)
        parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="17" fill="{LIME}"/>')
        parts.append(f'<text x="{tx:.1f}" y="22" text-anchor="{anc}" fill="{CREAM}" font-family="DM Sans" font-weight="800" font-size="28">{lab}</text>')
        parts.append(f'<text x="{tx:.1f}" y="136" text-anchor="{anc}" fill="{MUTED}" font-family="DM Sans" font-weight="400" font-size="26">{sub}</text>')
    return f'<svg class="tl" width="{w}" height="150" viewBox="0 0 {w} 150">{"".join(parts)}</svg>'


def slide(n, H, sq):
    W = 1080
    s = 0.82 if sq else 1.0
    lime = (n == 9)
    bg = LIME if lime else INK
    fg = INK if lime else CREAM
    mut = INK2 if lime else MUTED
    pat = ""
    body = ""
    if n == 1:
        pat = dot_scatter(W, H)
        body = f'''<div class="rule"></div>
<p class="lead" style="font-size:{54*s}px">Si llevas años haciéndolo todo, con valor pero sin rumbo,</p>
<h1 class="play" style="font-size:{134*s}px">esto es lo que te <em>falta.</em></h1>'''
    elif n == 2:
        pat = concentric(W, H)
        body = f'''<div class="quote" style="font-size:{220*s}px">“</div>
<h2 class="play" style="font-size:{104*s}px;max-width:940px">Tu empresa no puede ser más clara</h2>
<h2 class="play" style="font-size:{104*s}px;color:{LIME}">que tú.</h2>'''
    elif n == 3:
        body = f'''<div class="rows" style="font-size:{41*s}px">
<p>Tu equipo te consulta lo mismo una y otra vez.</p>
<p>Trabajas 60 o 70 horas y el viernes no hiciste lo que importaba.</p>
<p>Nadie lo hace como tú, así que no sueltas nada.</p></div>
<div class="accent"><h2 class="play" style="font-size:{72*s}px">Casi nunca es falta de equipo. <em>Es que tu criterio vive en tu cabeza.</em></h2></div>'''
    elif n == 4:
        body = f'''<div class="kicker"><i></i>Founder GPS</div>
<div class="stats"><div><span class="big" style="font-size:{200*s}px">90</span><span class="u" style="font-size:{44*s}px">días</span></div>
<div><span class="big" style="font-size:{200*s}px">12</span><span class="u" style="font-size:{44*s}px">sesiones 1:1<br><small>de 90 minutos</small></span></div></div>
{timeline(W)}
<p class="body" style="font-size:{44*s}px;color:{CREAM2}">Para dueños que quieren que su empresa sepa quién son y hacia dónde van.</p>'''
    elif n in (5, 6, 7):
        k = n - 5
        t = [("Tu claridad", "compass", "Defines hacia dónde va tu empresa y lo dices en una frase, con número y fecha."),
             ("Tu posición", "target", "Dejas de contestar con tu cargo. Logras que te entiendan a la primera."),
             ("Tu mensaje", "mega", "Tu equipo y tu mercado repiten lo mismo que tú, y tu mensaje sale cada semana.")][k]
        body = f'''{months(k, W)}
<div class="ico">{icon(t[1], int(150*s))}</div>
<h2 class="play" style="font-size:{136*s}px">{t[0]}</h2>
<div class="rule" style="margin-top:34px"></div>
<p class="body" style="font-size:{54*s}px;min-height:{3*54*1.36*s}px">{t[2]}</p>'''
    elif n == 8:
        body = f'''<h2 class="play" style="font-size:{96*s}px">Y sabes cuánto avanzaste.</h2>
<div class="chips"><div><span class="play" style="font-size:{110*s}px">25</span><span>afirmaciones</span></div>
<div><span class="play" style="font-size:{110*s}px">0–100</span><span>tu nivel</span></div></div>
{score_line(W)}
<p class="body" style="font-size:{38*s}px;color:{CREAM2}">El Score de claridad lo mides al empezar, a mitad y al terminar.</p>
<p class="fine">Herramienta de orientación; no es un diagnóstico clínico ni una evaluación de tu equipo.</p>'''
    else:
        pat = halftone(W, H)
        body = f'''<p class="lead" style="font-size:{60*s}px;font-weight:800;color:{INK}">Comenta</p>
<h1 class="play" style="font-size:{196*s}px;color:{INK}">SCORE</h1>
<div class="rule" style="background:{INK}"></div>
<p class="body" style="font-size:{44*s}px;color:{INK};max-width:820px">y te envío el Score de claridad: 25 afirmaciones y tu nivel de 0 a 100.</p>'''
    dot = INK if lime else LIME
    swipe = "" if n == N else f'<div class="swipe">Desliza <svg width="44" height="14" viewBox="0 0 44 14" fill="none" stroke="{MUTED}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 7h38M34 2l6 5-6 5"/></svg></div>'
    return f'''<section class="slide{' sq' if sq else ''}" style="background:{bg};color:{fg};--mut:{mut};--H:{H}px">
{pat}
<div class="top"><div class="num"><span>{n:02d}</span><i style="background:{dot}"></i><small>/ {N:02d}</small></div><div class="label">Founder GPS</div></div>
<div class="main">{body}</div>
<div class="foot"><div class="tag">{TAG}</div>{swipe}</div>
</section>'''


CSS = f'''
@page{{margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#000}}
.slide{{position:relative;width:1080px;height:var(--H);overflow:hidden;font-family:'DM Sans',sans-serif;page-break-after:always;break-after:page}}
.bg{{position:absolute;left:0;top:0;width:1080px;height:var(--H)}}
.top{{position:absolute;left:64px;right:64px;top:64px;display:flex;justify-content:space-between;align-items:flex-start;z-index:2}}
.num{{position:relative;display:flex;align-items:baseline;padding-right:20px}}
.num span{{font-family:'Playfair Display',serif;font-weight:900;font-size:60px;line-height:1;font-feature-settings:'lnum'}}
.num i{{position:absolute;left:68px;top:4px;width:12px;height:12px;border-radius:50%}}
.num small{{font-weight:700;font-size:26px;color:var(--mut);margin-left:22px}}
.label{{font-weight:700;font-size:22px;letter-spacing:.2em;text-transform:uppercase;color:var(--mut);padding-top:14px}}
.main{{position:absolute;left:64px;right:64px;top:190px;bottom:150px;display:flex;flex-direction:column;justify-content:center;z-index:2}}
.sq .main{{top:150px;bottom:124px}}
.foot{{position:absolute;left:64px;right:64px;bottom:64px;display:flex;justify-content:space-between;align-items:center;z-index:2}}
.tag{{font-weight:700;font-size:30px;letter-spacing:-.01em;color:var(--mut)}}
.swipe{{font-weight:700;font-size:24px;color:{MUTED};display:flex;gap:14px;align-items:center}}
.play{{font-family:'Playfair Display',serif;font-weight:900;line-height:1.06;letter-spacing:-.01em;font-feature-settings:'lnum'}}
.play em{{font-style:normal;color:{LIME}}}
.lead{{font-weight:400;line-height:1.3;color:{CREAM2};margin-bottom:28px;max-width:900px}}
.body{{font-weight:400;line-height:1.36;max-width:900px;text-wrap:balance}}
.rows p,.lead,.play{{text-wrap:balance}}
.rule{{width:96px;height:3px;background:{LIME};margin:0 0 36px}}
.quote{{font-family:'Playfair Display',serif;font-weight:900;color:{LIME};line-height:.7;height:130px;margin-bottom:12px}}
.rows p{{padding:30px 0;border-top:1px solid {INK2};line-height:1.3;color:{CREAM2}}}
.rows p:last-child{{border-bottom:1px solid {INK2}}}
.accent{{border-left:3px solid {LIME};padding-left:32px;margin-top:56px}}
.kicker{{font-family:'Playfair Display',serif;font-weight:900;font-size:86px;display:flex;align-items:center;gap:26px;margin-bottom:40px}}
.kicker i{{width:32px;height:32px;border-radius:50%;background:{LIME};display:block}}
.stats{{display:flex;gap:56px;margin-bottom:36px}}
.stats>div{{display:flex;align-items:baseline;gap:18px}}
.big{{font-family:'Playfair Display',serif;font-weight:900;color:{LIME};line-height:1;font-feature-settings:'lnum'}}
.u{{font-weight:800;line-height:1.1;color:{CREAM}}}
.u small{{font-weight:400;font-size:.62em;color:{MUTED}}}
.tl{{display:block;margin:6px 0 30px}}
.months{{display:flex;gap:16px;margin-bottom:48px}}
.seg{{flex:1}}
.seg b{{display:block;height:6px;border-radius:3px;margin-bottom:12px}}
.seg span{{font-weight:700;font-size:22px;letter-spacing:.14em;text-transform:uppercase}}
.ico{{margin-bottom:28px}}
.chips{{display:flex;margin:48px 0 64px}}
.chips>div{{flex:1;display:flex;flex-direction:column;gap:2px}}
.chips>div+div{{border-left:1px solid {INK2};padding-left:44px}}
.chips .play{{color:{CREAM};line-height:1.05}}
.chips span:last-child{{font-weight:700;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:{MUTED}}}
.fine{{font-size:22px;color:{MUTED};margin-top:22px;line-height:1.4;max-width:900px}}
'''


def page(inner, H, title):
    fonts = open(os.path.join(OUT, "fuentes", "fuentes.css")).read()
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{title}</title>
<style>{fonts}{CSS}</style></head><body>{inner}</body></html>'''


if __name__ == "__main__":
    ensure_fonts()
    os.makedirs(os.path.join(OUT, "html"), exist_ok=True)
    for n in range(1, N + 1):
        open(os.path.join(OUT, "html", f"ig-{n:02d}.html"), "w", encoding="utf-8").write(page(slide(n, 1350, False), 1350, f"IG {n}"))
    print("ok", N)
