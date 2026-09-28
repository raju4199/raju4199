"""Generate the animated SVGs used by the profile README.

Run from the repo root:  python scripts/gen_svgs.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

RED = "#ff1f3d"
DIM = "#8b949e"
WHITE = "#f0f6fc"
BG = "#07070a"
MONO = "Consolas,'JetBrains Mono','Courier New',monospace"
CHAR_W = 0.55  # approx advance width of a monospace glyph, in em


def banner():
    w, h = 1200, 380
    phrases = [
        "Offensive Security Researcher",
        "Red Teaming  ·  Web & API  ·  Android",
        "CEH v12  ·  Published Researcher",
        "Cyber Security Analyst @ QOS Technology",
    ]
    cycle, fs, y = 4.0 * len(phrases), 26, 262
    subs = []
    for i, p in enumerate(phrases):
        text = f"> {p}"
        tw = len(text) * fs * CHAR_W
        x0 = (w - tw) / 2
        a, b = i / len(phrases), (i + 1) / len(phrases)
        typed = a + 0.35 / len(phrases)
        kt = f"0;{a:.4f};{typed:.4f};{b - 0.01:.4f};{b:.4f};1"
        subs.append(f"""
  <clipPath id="c{i}"><rect x="{x0:.1f}" y="{y - 30}" height="42" width="0">
    <animate attributeName="width" dur="{cycle}s" repeatCount="indefinite"
      values="0;0;{tw:.1f};{tw:.1f};0;0" keyTimes="{kt}"/></rect></clipPath>
  <text x="{x0:.1f}" y="{y}" class="sub" clip-path="url(#c{i})">{escape(text)}</text>
  <rect y="{y - 22}" width="13" height="28" fill="{RED}" opacity="0">
    <animate attributeName="x" dur="{cycle}s" repeatCount="indefinite"
      values="{x0:.1f};{x0:.1f};{x0 + tw + 4:.1f};{x0 + tw + 4:.1f};{x0:.1f};{x0:.1f}" keyTimes="{kt}"/>
    <animate attributeName="opacity" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete"
      values="0;1;1;0;0" keyTimes="0;{a:.4f};{b - 0.01:.4f};{b:.4f};1"/></rect>""")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
  <radialGradient id="glow" cx="50%" cy="42%" r="65%">
    <stop offset="0" stop-color="#2a0309"/><stop offset="1" stop-color="{BG}"/></radialGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{RED}" stroke-opacity=".09"/></pattern>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity=".35"/></pattern>
  <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{RED}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{RED}" stop-opacity=".16"/>
    <stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
</defs>
<style>
  text {{ font-family:{MONO}; }}
  .name {{ font-size:96px; font-weight:700; letter-spacing:10px; text-anchor:middle; }}
  .sub {{ font-size:{fs}px; fill:{WHITE}; }}
  .hud {{ font-size:14px; fill:{DIM}; letter-spacing:2px; }}
  .g1 {{ animation:g1 3.2s infinite steps(1); }}
  .g2 {{ animation:g2 3.2s infinite steps(1); }}
  .blink {{ animation:blink 1.2s infinite; }}
  @keyframes g1 {{ 0%,84%,100% {{ transform:translate(0,0) }} 86% {{ transform:translate(-7px,2px) }}
    89% {{ transform:translate(5px,-3px) }} 92% {{ transform:translate(-3px,1px) }} }}
  @keyframes g2 {{ 0%,84%,100% {{ transform:translate(0,0) }} 86% {{ transform:translate(6px,-2px) }}
    89% {{ transform:translate(-5px,3px) }} 92% {{ transform:translate(3px,-1px) }} }}
  @keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:.15 }} }}
</style>
<rect width="{w}" height="{h}" fill="url(#glow)"/>
<rect x="-40" y="-40" width="{w + 80}" height="{h + 80}" fill="url(#grid)">
  <animateTransform attributeName="transform" type="translate" values="0 0;40 40" dur="6s" repeatCount="indefinite"/></rect>
<rect y="-140" width="{w}" height="140" fill="url(#beam)">
  <animate attributeName="y" values="-140;{h}" dur="5s" repeatCount="indefinite"/></rect>

<g fill="none" stroke="{RED}" stroke-width="3">
  <path d="M24 64V24H64"/><path d="M{w - 64} 24H{w - 24}V64"/>
  <path d="M24 {h - 64}V{h - 24}H64"/><path d="M{w - 64} {h - 24}H{w - 24}V{h - 64}"/></g>

<text x="80" y="52" class="hud"><tspan fill="{RED}" class="blink">●</tspan> ONLINE  //  raju4199</text>
<text x="{w - 80}" y="52" class="hud" text-anchor="end">DELHI, IN  //  SECURITY RESEARCH</text>

<text x="{w / 2}" y="190" class="name g1" fill="#00e5ff" opacity=".55">RAJU RANJAN</text>
<text x="{w / 2}" y="190" class="name g2" fill="{RED}" opacity=".75">RAJU RANJAN</text>
<text x="{w / 2}" y="190" class="name" fill="{WHITE}">RAJU RANJAN</text>
<rect x="{w / 2 - 140}" y="214" width="280" height="2" fill="{RED}"/>
{''.join(subs)}

<text x="{w / 2}" y="{h - 40}" class="hud" text-anchor="middle">think like an attacker  ·  build like a defender</text>
<rect width="{w}" height="{h}" fill="url(#lines)"/>
</svg>
"""
    (OUT / "banner.svg").write_text(svg, encoding="utf-8")


def terminal(name, title, rows, height):
    """rows: list of (kind, text) where kind is 'cmd', 'out', 'hl' or 'gap'."""
    w, lh, top = 1000, 26, 78
    cycle = 3.0 + 0.45 * len(rows) + 6
    body, t = [], 0.6
    for i, (kind, text) in enumerate(rows):
        y = top + i * lh
        if kind == "gap":
            continue
        a = t / cycle
        if kind == "cmd":
            prompt = "raju@research:~$ "
            tw