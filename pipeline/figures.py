"""投影片用的 SVG 圖（全部在建置時產生，成品不依賴外部檔案）。"""
import math

import numpy as np

INK, MUTED, ACC, ACC2, SOFT = "#1d2a3a", "#6b7787", "#0f7c80", "#d9731a", "#e7eef0"
PALETTE = ["#0f7c80", "#d9731a", "#5b6fd6", "#c2417a", "#5a8f29"]


def _svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="inherit" role="img">{body}</svg>')


def multipath():
    b = []
    # 發射塔、接收端、建築物
    b.append(f'<g stroke="{INK}" stroke-width="3" fill="none"><path d="M60 230 L80 120 L100 230 M68 185 L92 185 M72 160 L88 160"/></g>')
    b.append(f'<circle cx="80" cy="112" r="6" fill="{ACC}"/>')
    b.append(f'<rect x="440" y="200" width="36" height="40" rx="6" fill="{INK}"/><rect x="447" y="207" width="22" height="18" rx="2" fill="#9fd3d5"/>')
    b.append(f'<rect x="230" y="20" width="90" height="70" fill="{SOFT}" stroke="{MUTED}"/>')
    b.append(f'<text x="275" y="60" text-anchor="middle" font-size="16" fill="{MUTED}">建築物</text>')
    b.append(f'<line x1="86" y1="118" x2="440" y2="215" stroke="{ACC}" stroke-width="3.5"/>')
    b.append(f'<path d="M86 116 L275 90 L442 205" fill="none" stroke="{ACC2}" stroke-width="3.5" stroke-dasharray="9 6"/>')
    b.append(f'<text x="170" y="200" font-size="18" fill="{ACC}" font-weight="700">直射（先到）</text>')
    b.append(f'<text x="345" y="125" font-size="18" fill="{ACC2}" font-weight="700">反射（晚到）</text>')
    # 時間軸：符號與回音
    y = 300
    b.append(f'<text x="20" y="{y-12}" font-size="16" fill="{MUTED}">接收端看到的訊號</text>')
    for i in range(4):
        x = 30 + i * 115
        b.append(f'<rect x="{x}" y="{y}" width="105" height="34" rx="4" fill="{ACC}" opacity=".9"/>')
        b.append(f'<text x="{x+52}" y="{y+23}" text-anchor="middle" font-size="16" fill="#fff">符號 {i+1}</text>')
        b.append(f'<rect x="{x+40}" y="{y+40}" width="105" height="26" rx="4" fill="{ACC2}" opacity=".55"/>')
    b.append(f'<text x="30" y="{y+92}" font-size="16" fill="{ACC2}" font-weight="700">回音疊到下一個符號上 → ISI</text>')
    return _svg(500, 400, "".join(b))


def lanes():
    b = [f'<text x="10" y="24" font-size="17" fill="{INK}" font-weight="700">單載波：一條快車道</text>']
    for i in range(12):
        b.append(f'<rect x="{10+i*40}" y="36" width="36" height="34" rx="3" fill="{MUTED}" opacity=".75"/>')
    b.append(f'<text x="10" y="118" font-size="17" fill="{INK}" font-weight="700">OFDM：很多條慢車道（子載波）</text>')
    for r in range(6):
        y = 130 + r * 40
        for i in range(2):
            b.append(f'<rect x="{10+i*240}" y="{y}" width="232" height="32" rx="4" fill="{PALETTE[r % 5]}" opacity=".85"/>')
        b.append(f'<text x="490" y="{y+22}" font-size="14" fill="{MUTED}" text-anchor="end">f{r+1}</text>')
    b.append(f'<text x="10" y="385" font-size="15" fill="{MUTED}">同一段時間、同樣的資料量；但每個符號長了 6 倍</text>')
    return _svg(500, 400, "".join(b))


def spectrum(interactive=False, fid="spec"):
    """5 個子載波的 sinc 頻譜。interactive=True 時加上 CFO 滑桿（JS 重畫）。"""
    W, H = 520, 330 if not interactive else 300
    svg = (f'<svg id="{fid}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" data-eps="0" '
           f'class="spectrum" data-w="{W}" data-h="{H}"></svg>')
    ctrl = ""
    if interactive:
        ctrl = (f'<div class="slider"><label>正規化頻率偏移 ε = <b id="{fid}-v">0.00</b></label>'
                f'<input type="range" min="0" max="0.5" step="0.01" value="0" '
                f'oninput="drawSpectrum(\'{fid}\', +this.value)">'
                f'<div class="ici">在子載波 3 的取樣點上，來自其他子載波的干擾（ICI）：<b id="{fid}-ici">0.000</b></div></div>')
    return f'<div class="spectrum-wrap">{svg}{ctrl}</div>'


def blocks():
    tx = ["位元", "QAM", "IFFT", "加 CP"]
    rx = ["去 CP", "FFT", "÷ Hₖ", "位元"]
    b = []

    def row(items, y, color, label):
        out = [f'<text x="10" y="{y-14}" font-size="16" fill="{MUTED}">{label}</text>']
        for i, t in enumerate(items):
            x = 10 + i * 122
            out.append(f'<rect x="{x}" y="{y}" width="100" height="50" rx="8" fill="{color}"/>')
            out.append(f'<text x="{x+50}" y="{y+32}" text-anchor="middle" font-size="19" fill="#fff" font-weight="700">{t}</text>')
            if i < len(items) - 1:
                out.append(f'<path d="M{x+102} {y+25} L{x+120} {y+25}" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>')
        return "".join(out)

    b.append(f'<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8z" fill="{INK}"/></marker></defs>')
    b.append(row(tx, 40, ACC, "發射端"))
    b.append(f'<rect x="150" y="128" width="200" height="44" rx="22" fill="{SOFT}" stroke="{MUTED}"/>')
    b.append(f'<text x="250" y="156" text-anchor="middle" font-size="17" fill="{INK}">無線通道（多路徑）</text>')
    b.append(f'<path d="M424 92 L424 150 L354 150" fill="none" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>')
    b.append(f'<path d="M148 150 L60 150 L60 212" fill="none" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>')
    b.append(row(rx, 216, ACC2, "接收端"))
    return _svg(500, 290, "".join(b))


def cp():
    b = [f'<defs><marker id="ar2" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8z" fill="{ACC2}"/></marker></defs>']
    y = 120
    b.append(f'<rect x="20" y="{y}" width="90" height="70" fill="{ACC2}" opacity=".85"/>')
    b.append(f'<rect x="110" y="{y}" width="360" height="70" fill="{ACC}" opacity=".85"/>')
    b.append(f'<rect x="380" y="{y}" width="90" height="70" fill="{ACC2}" opacity=".85"/>')
    b.append(f'<text x="65" y="{y+43}" text-anchor="middle" font-size="20" fill="#fff" font-weight="700">CP</text>')
    b.append(f'<text x="245" y="{y+43}" text-anchor="middle" font-size="19" fill="#fff">IFFT 輸出（有效符號）</text>')
    b.append(f'<text x="425" y="{y+43}" text-anchor="middle" font-size="17" fill="#fff">尾端</text>')
    b.append(f'<path d="M425 {y-6} C425 40, 65 40, 65 {y-8}" fill="none" stroke="{ACC2}" stroke-width="3" marker-end="url(#ar2)"/>')
    b.append(f'<text x="245" y="52" text-anchor="middle" font-size="18" fill="{ACC2}" font-weight="700">複製尾端，貼到開頭</text>')
    # 回音
    b.append(f'<line x1="110" y1="{y-10}" x2="110" y2="{y+86}" stroke="{INK}" stroke-dasharray="5 5"/>')
    b.append(f'<text x="116" y="{y+92}" font-size="15" fill="{INK}">↑ FFT 視窗從這裡開始</text>')
    b.append(f'<rect x="20" y="{y+116}" width="60" height="26" fill="{MUTED}" opacity=".45"/>')
    b.append(f'<text x="90" y="{y+135}" font-size="16" fill="{MUTED}">上一個符號的回音只落在 CP 內 → 丟掉即可</text>')
    return _svg(500, 300, "".join(b))


def pilots():
    b = []
    rows, cols, cell = 8, 10, 34
    ox, oy = 50, 20
    for r in range(rows):
        for c in range(cols):
            pilot = (r % 4 == 1 and c % 3 == 0) or (r % 4 == 3 and c % 3 == 2)
            fill = ACC2 if pilot else SOFT
            b.append(f'<rect x="{ox+c*cell}" y="{oy+r*cell}" width="{cell-3}" height="{cell-3}" rx="3" fill="{fill}"/>')
    b.append(f'<text x="{ox+cols*cell/2}" y="{oy+rows*cell+26}" text-anchor="middle" font-size="16" fill="{MUTED}">時間（OFDM 符號）→</text>')
    b.append(f'<text x="22" y="{oy+rows*cell/2}" font-size="16" fill="{MUTED}" transform="rotate(-90 22 {oy+rows*cell/2})" text-anchor="middle">子載波 →</text>')
    b.append(f'<rect x="{ox}" y="{oy+rows*cell+44}" width="20" height="20" rx="3" fill="{ACC2}"/>')
    b.append(f'<text x="{ox+28}" y="{oy+rows*cell+60}" font-size="16" fill="{INK}">導頻（已知）</text>')
    b.append(f'<rect x="{ox+150}" y="{oy+rows*cell+44}" width="20" height="20" rx="3" fill="{SOFT}" stroke="{MUTED}"/>')
    b.append(f'<text x="{ox+178}" y="{oy+rows*cell+60}" font-size="16" fill="{INK}">資料（用內插的通道）</text>')
    return _svg(420, 360, "".join(b))


def papr():
    rng = np.random.default_rng(7)
    n, N = 600, 32
    t = np.linspace(0, 1, n)
    ph = rng.uniform(0, 2 * np.pi, N)
    x = sum(np.cos(2 * np.pi * (k + 1) * t + ph[k]) for k in range(N))
    p = x ** 2
    avg, pk = p.mean(), p.max()
    W, H, ox, oy, h = 500, 300, 20, 20, 220
    pts = " ".join(f"{ox + i * (W - 2*ox) / (n - 1):.1f},{oy + h - v / pk * h:.1f}" for i, v in enumerate(p))
    ya = oy + h - avg / pk * h
    i_pk = int(p.argmax())
    xp = ox + i_pk * (W - 2*ox) / (n - 1)
    b = [f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="1.6"/>',
         f'<line x1="{ox}" y1="{ya:.1f}" x2="{W-ox}" y2="{ya:.1f}" stroke="{INK}" stroke-dasharray="6 5" stroke-width="2"/>',
         f'<text x="{ox}" y="{oy+h+18}" font-size="15" fill="{INK}">- - - 平均功率</text>',
         f'<circle cx="{xp:.1f}" cy="{oy}" r="7" fill="none" stroke="{ACC2}" stroke-width="3"/>',
         f'<text x="{xp-14:.1f}" y="{oy+6}" text-anchor="end" font-size="16" fill="{ACC2}" font-weight="700">峰值 ≈ 平均的 {pk/avg:.0f} 倍</text>',
         f'<text x="{ox}" y="{oy+h+42}" font-size="15" fill="{MUTED}">示意：32 個隨機相位子載波相加後的瞬時功率</text>']
    return _svg(W, H, "".join(b))


def grid():
    b = []
    rows, cols, cell = 8, 12, 32
    ox, oy = 50, 20
    owner = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            owner[r][c] = (0 if r < 3 else 1 if r < 6 else 2) if c < 6 else (1 if r < 2 else 2 if r < 5 else 0)
    names = ["使用者 A", "使用者 B", "使用者 C"]
    for r in range(rows):
        for c in range(cols):
            b.append(f'<rect x="{ox+c*cell}" y="{oy+r*cell}" width="{cell-3}" height="{cell-3}" rx="3" fill="{PALETTE[owner[r][c]]}" opacity=".85"/>')
    b.append(f'<text x="{ox+cols*cell/2}" y="{oy+rows*cell+24}" text-anchor="middle" font-size="16" fill="{MUTED}">時間 →</text>')
    b.append(f'<text x="22" y="{oy+rows*cell/2}" font-size="16" fill="{MUTED}" transform="rotate(-90 22 {oy+rows*cell/2})" text-anchor="middle">子載波 →</text>')
    for i, nm in enumerate(names):
        b.append(f'<rect x="{ox+i*120}" y="{oy+rows*cell+40}" width="18" height="18" rx="3" fill="{PALETTE[i]}"/>')
        b.append(f'<text x="{ox+i*120+25}" y="{oy+rows*cell+55}" font-size="16" fill="{INK}">{nm}</text>')
    return _svg(450, 340, "".join(b))


FIGS = {"multipath": multipath, "lanes": lanes, "spectrum": lambda: spectrum(False, "spec0"),
        "spectrum-cfo": lambda: spectrum(True, "spec1"), "blocks": blocks, "cp": cp,
        "pilots": pilots, "papr": papr, "grid": grid}
