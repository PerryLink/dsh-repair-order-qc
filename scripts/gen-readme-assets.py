#!/usr/bin/env python3
"""README visuals for dsh-repair-order-qc, derived from the plugin's own code.

Assets written (idempotent, overwrite):

  dsh-repair-order-qc-hero-{zh,en}-{light,dark}.webp   1440x576 Pillow banner
  dsh-repair-order-qc-flow-v5-{light,dark}.svg          1100x660 hand-written SVG

Hero (Pillow)
    Left column: kicker / two-line wordmark / two value lines / subtitle /
    meta / footer. Right side: the settlement sheet from
    `samples/quickstart/input/RO-001-unsafe.json` -- four header totals
    (partsTotal 360, laborTotal 200, discount 0, total 560), one detail row
    (front brake pad, 2 x 180 = 360), and the two findings the tool actually
    emits for that sample: RO-001 (customerConcern and workDone both empty)
    and RO-003 (one row's amount sums to 360 against a declared total of 560,
    gap 200). The report readout is the tool's own: 2 issues, skipped 0,
    error 0 / warn 2 / info 0. Nothing is invented.

Flow (hand-written SVG)
    Grammar: a SETTLEMENT PROOF BENCH, not a row of boxes. Material and rule
    pack arrive as two intake bars; the material becomes one settlement proof
    (header equation over one detail row, with five rule probes mounted on the
    cells they read), while the rule pack sits in a validation rack that states
    the load-time excerpt check, the citation gate and the severity caps. The
    proof then splits into the two
    ledgers the engine really returns -- `issues[]` and `skipped[]` -- and both
    are projected by `buildView()` into markdown / reportJson. Every number and
    stamp comes from the quickstart sample or from
    `rules/repair-order-qc.yaml` (pack 2026.1, seven rules, all `warn`:
    four `direct`, three `derived-from-principle`).

No evidence chart: this repository ships no benchmark or measured dataset. The
terminal captures under docs/assets/ are real captures kept as-is.

Palette, radii, fonts: the PerryLink family system (accent #4B67B4 / #8496f5,
light #f9f6fd -> #e4eaf8, dark #131a2a -> #0c1016, radius 18-22, soft shadow).

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + msyh.ttc / msyhbd.ttc / consola.ttf / consolab.ttf.
"""
from __future__ import annotations

import os
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_FILES = {
    "cjk": r"C:\Windows\Fonts\msyh.ttc",
    "cjk_bold": r"C:\Windows\Fonts\msyhbd.ttc",
    "mono": r"C:\Windows\Fonts\consola.ttf",
    "mono_bold": r"C:\Windows\Fonts\consolab.ttf",
}
for _kind, _path in FONT_FILES.items():
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing ({_kind}): {_path}")

WEBP_QUALITY = 92

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", card2="#fbf9ff", edge="#e6e0f0",
        text="#141419", sub="#4d5261", faint="#8b8fa1",
        accent="#4B67B4", accent_soft="#ece9f7", accent_line="#c9c2e6",
        pill="#f2eefb", band="#f8f5fc", grid="#ebe6f3",
        warn="#b45309", warn_bg="#fdf0e2", warn_line="#e8c9a4",
        ok="#15803d", ok_bg="#eaf6ee",
        shadow=(38, 28, 72), glow="#7a68c9", shadow_opacity=0.13,
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", card2="#1f2636", edge="#2e374b",
        text="#f0f3f9", sub="#aab3c6", faint="#737b8d",
        accent="#8496f5", accent_soft="#232c42", accent_line="#3a4560",
        pill="#202839", band="#171e2b", grid="#273045",
        warn="#e0a84e", warn_bg="#33270f", warn_line="#5c4820",
        ok="#4ec27d", ok_bg="#1b3327",
        shadow=(0, 0, 0), glow="#8496f5", shadow_opacity=0.42,
    ),
}


def hx(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def font(size: int, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], size)


_SCRATCH = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: int, kind: str = "cjk") -> float:
    return _SCRATCH.textlength(text, font=font(size, kind))


def require_w(text: str, size: int, kind: str, max_w: float, what: str) -> None:
    width = measure(text, size, kind)
    if width > max_w + 0.5:
        raise SystemExit(f"FATAL: {what} overflows: {text!r} needs {width:.1f}px > {max_w}px")


def fit(text: str, kind: str, max_w: float, start: int, minimum: int) -> int:
    size = start
    while size >= minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 1
    raise SystemExit(f"FATAL: text does not fit {max_w}px at >= {minimum}px: {text!r}")


def fit_lines(lines: list[str], kind: str, max_w: float, start: int,
              minimum: int) -> int:
    return min(fit(line, kind, max_w, start, minimum) for line in lines)


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(c1), hx(c2)
    for y in range(h):
        t = 0.16 * (y / h) + 0.84 * (y / h) ** 1.5
        draw.line([(0, y), (w, y)],
                  fill=tuple(round(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, radius: int, color: tuple,
         alpha: int = 32) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for i in range(12, 0, -1):
        rr = radius * i / 12
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                     fill=color + (int(alpha * (1 - i / 13) ** 1.6),))
    layer = layer.filter(ImageFilter.GaussianBlur(28))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def card(img: Image.Image, box: tuple[int, int, int, int], s: dict,
         radius: int = 20, blur: int = 16, dy: int = 9,
         fill: str | None = None, edge: str | None = None) -> Image.Image:
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    alpha = int(46 * s["shadow_opacity"] * 2.4)
    for i in range(6, 0, -2):
        draw.rounded_rectangle(
            [x0 - 3, y0 + dy + i * 2, x1 + 3, y1 + dy + i * 3],
            radius=radius + i,
            fill=s["shadow"] + (max(4, int(alpha / (i + 1))),))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                           outline=hx(edge or s["edge"]), width=2)
    return base


def chip(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fg: str,
         bg: str, size: int = 11, padx: int = 8, height: int = 20,
         kind: str = "mono_bold") -> int:
    f = font(size, kind)
    w = draw.textlength(text, font=f)
    x, y = xy
    draw.rounded_rectangle([x, y, x + w + padx * 2, y + height],
                           radius=height // 2, fill=hx(bg))
    draw.text((x + padx, y + height / 2), text, font=f, fill=hx(fg), anchor="lm")
    return int(w + padx * 2)


# --------------------------------------------------------------------------- hero
# Everything on the right is read from the quickstart sample and the tool's
# output for that sample. The two findings are the tool's own sentences.
HERO = {
    "zh": dict(
        kicker="DEEPSEEK HARNESS · 维修工单检查器",
        value1="7 条规则，核对一张维修工单的算术",
        value2="每条差异写明哪一行、哪一栏、依据哪条",
        sub="规则库是数据：只列差异，不下结论，不联网、不写盘",
        meta="repair_order_qc · file | material → report · 7 rules",
        footer="只读 · 纯本地 · Apache-2.0 · PerryLink DSH 插件家族",
        sheet_title="维修结算单",
        sheet_sub="表头 + rows[1] · 1 个项目行",
        detail_tag="quickstart · 自带样例",
        check_formula="√ RO-004 · 360 + 200 − 0 = 560",
        check_product="2 × 180 = 360 √ RO-002",
        check_presence="都为空 × RO-001",
        empty_cell="空  /  空",
        mismatch_label="Σ amount 对 total",
        mismatch_sub="1 个项目行 · 容差 0.01 · RO-003",
        find1="第 1 行 · 客户反映、施工内容都为空",
        find2="字段 amount · 合计 360，总额 560（差 200）",
        report_issues="2 issues",
        report_skipped="skipped 0",
        report_summary="error 0 · warn 2 · info 0",
        report_pack="pack 2026.1 · 7 rules",
    ),
    "en": dict(
        kicker="DEEPSEEK HARNESS · REPAIR-ORDER CHECKER",
        value1="Seven rules, one repair order's arithmetic",
        value2="Each finding names row, column, clause",
        sub="Rule pack is data; differences only, no verdicts",
        meta="repair_order_qc · file | material → report · 7 rules",
        footer="read-only · local only · Apache-2.0 · PerryLink DSH family",
        sheet_title="维修结算单",
        sheet_sub="header + rows[1] · 1 detail row",
        detail_tag="quickstart · sample",
        check_formula="√ RO-004 · 360 + 200 − 0 = 560",
        check_product="2 × 180 = 360 √ RO-002",
        check_presence="both empty × RO-001",
        empty_cell="—  /  —",
        mismatch_label="Σ amount vs total",
        mismatch_sub="1 detail row · tolerance 0.01 · RO-003",
        find1="row 1 · customer report and work done are empty",
        find2="amount sums to 360, settlement is 560 (gap 200)",
        report_issues="2 issues",
        report_skipped="skipped 0",
        report_summary="error 0 · warn 2 · info 0",
        report_pack="pack 2026.1 · 7 rules",
    ),
}

HERO_TITLE_1 = "dsh-repair-"
HERO_TITLE_2 = "order-qc"


def draw_hero(lang: str, skin: str) -> Image.Image:
    h = HERO[lang]
    s = SKIN[skin]
    w, ht = 1440, 576
    img = gradient(w, ht, s["bg_from"], s["bg_to"])
    img = glow(img, 1210, 60, 330, hx(s["glow"]), 36 if skin == "light" else 26)
    img = glow(img, 930, 520, 280, hx(s["glow"]), 15 if skin == "light" else 11)
    draw = ImageDraw.Draw(img)

    # ---- left column ------------------------------------------------------
    draw.rounded_rectangle([76, 76, 80, 98], radius=2, fill=hx(s["accent"]))
    draw.text((94, 94), h["kicker"], font=font(18, "cjk_bold"),
              fill=hx(s["accent"]), anchor="ls")

    title_size = 92
    draw.text((74, 198), HERO_TITLE_1, font=font(title_size, "mono_bold"),
              fill=hx(s["text"]), anchor="ls")
    draw.text((74, 300), HERO_TITLE_2, font=font(title_size, "mono_bold"),
              fill=hx(s["text"]), anchor="ls")
    draw.rounded_rectangle([76, 332, 216, 338], radius=3, fill=hx(s["accent"]))
    require_w(HERO_TITLE_1, title_size, "mono_bold", 660, "hero title line 1")
    require_w(HERO_TITLE_2, title_size, "mono_bold", 660, "hero title line 2")

    value_size = fit_lines([h["value1"], h["value2"]], "cjk_bold", 660, 30, 26)
    draw.text((76, 372), h["value1"], font=font(value_size, "cjk_bold"),
              fill=hx(s["text"]), anchor="ls")
    draw.text((76, 410), h["value2"], font=font(value_size, "cjk_bold"),
              fill=hx(s["text"]), anchor="ls")
    require_w(h["value1"], value_size, "cjk_bold", 660, "hero value 1")
    require_w(h["value2"], value_size, "cjk_bold", 660, "hero value 2")

    sub_size = fit(h["sub"], "cjk", 660, 26, 22)
    draw.text((76, 452), h["sub"], font=font(sub_size, "cjk"),
              fill=hx(s["sub"]), anchor="ls")
    require_w(h["sub"], sub_size, "cjk", 660, "hero subtitle")

    meta_size = 20
    draw.text((76, 490), h["meta"], font=font(meta_size, "mono"),
              fill=hx(s["faint"]), anchor="ls")
    require_w(h["meta"], meta_size, "mono", 660, "hero meta")

    draw.line([76, 510, 736, 510], fill=hx(s["grid"]), width=1)
    foot_size = fit(h["footer"], "cjk", 660, 15, 12)
    draw.text((76, 546), h["footer"], font=font(foot_size, "cjk"),
              fill=hx(s["faint"]), anchor="ls")

    # ---- right side: the settlement sheet ---------------------------------
    # Two pages peeking out behind the sheet, then the sheet itself.
    draw.rounded_rectangle([812, 58, 1364, 492], radius=22, fill=hx(s["pill"]))
    draw.rounded_rectangle([804, 51, 1356, 485], radius=22, fill=hx(s["band"]))
    img = card(img, (788, 44, 1368, 492), s, radius=20, blur=17, dy=10)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([788, 44, 794, 492], radius=6, fill=hx(s["accent"]))

    draw.text((816, 84), h["sheet_title"], font=font(19, "cjk_bold"),
              fill=hx(s["text"]), anchor="ls")
    draw.text((1350, 84), "WX-2026-0018", font=font(11, "mono"),
              fill=hx(s["sub"]), anchor="rs")
    draw.text((816, 110), h["sheet_sub"], font=font(10, "cjk"),
              fill=hx(s["faint"]), anchor="ls")
    chip(draw, (1350 - int(measure(h["detail_tag"], 10, "cjk")) - 16, 96),
         h["detail_tag"], fg=s["accent"], bg=s["accent_soft"],
         size=10, kind="cjk", padx=8, height=19)
    draw.line([816, 124, 1350, 124], fill=hx(s["grid"]), width=1)

    # Header totals: partsTotal + laborTotal - discount = total
    cell_x = (816, 950, 1084, 1218)
    cell_w = 120
    for index, (label, value) in enumerate((
        ("partsTotal", "360"), ("laborTotal", "200"),
        ("discount", "0"), ("total", "560"),
    )):
        cx = cell_x[index]
        draw.rounded_rectangle([cx, 134, cx + cell_w, 194], radius=12,
                               fill=hx(s["band"]), outline=hx(s["grid"]))
        draw.text((cx + 12, 156), label, font=font(10, "mono"),
                  fill=hx(s["faint"]), anchor="ls")
        draw.text((cx + 12, 182), value,
                  font=font(20, "mono_bold"),
                  fill=hx(s["accent"] if index == 3 else s["text"]), anchor="ls")
    for opx, op in ((944, "+"), (1078, "−"), (1212, "=")):
        draw.text((opx, 178), op, font=font(15, "mono_bold"),
                  fill=hx(s["faint"]), anchor="ms")

    draw.text((1350, 218), h["check_formula"], font=font(10, "cjk"),
              fill=hx(s["ok"]), anchor="rs")
    draw.line([816, 230, 1350, 230], fill=hx(s["grid"]), width=1)

    # One detail row: front brake pad, 2 x 180 = 360, both narrative cells empty.
    draw.text((816, 252), "itemName", font=font(10, "mono"),
              fill=hx(s["faint"]), anchor="ls")
    draw.text((944, 252), "quantity", font=font(10, "mono"),
              fill=hx(s["faint"]), anchor="ls")
    draw.text((1016, 252), "unitPrice", font=font(10, "mono"),
              fill=hx(s["faint"]), anchor="ls")
    draw.text((1098, 252), "amount", font=font(10, "mono"),
              fill=hx(s["faint"]), anchor="ls")
    draw.text((1184, 252), "customerConcern · workDone", font=font(10, "mono"),
              fill=hx(s["faint"]), anchor="ls")

    draw.text((816, 280), "前制动片", font=font(15, "cjk_bold"),
              fill=hx(s["text"]), anchor="ls")
    for x, value in ((944, "2"), (1016, "180"), (1098, "360")):
        draw.text((x, 280), value, font=font(15, "mono_bold"),
                  fill=hx(s["text"]), anchor="ls")
    draw.text((1184, 280), h["empty_cell"], font=font(15, "cjk_bold"),
              fill=hx(s["warn"]), anchor="ls")

    draw.text((944, 302), h["check_product"], font=font(10, "cjk"),
              fill=hx(s["ok"]), anchor="ls")
    draw.text((1184, 302), h["check_presence"], font=font(10, "cjk"),
              fill=hx(s["warn"]), anchor="ls")
    draw.line([816, 316, 1350, 316], fill=hx(s["grid"]), width=1)

    # The mismatch that RO-003 reports: 360 against 560, gap 200.
    draw.text((816, 342), h["mismatch_label"], font=font(10, "mono"),
              fill=hx(s["faint"]), anchor="ls")
    draw.text((816, 386), "Σ 360", font=font(30, "mono_bold"),
              fill=hx(s["warn"]), anchor="ls")
    draw.text((932, 386), "≠", font=font(34, "mono_bold"),
              fill=hx(s["warn"]), anchor="ls")
    draw.text((984, 386), "560", font=font(30, "mono_bold"),
              fill=hx(s["text"]), anchor="ls")
    chip(draw, (1096, 358), "gap 200", fg=s["warn"], bg=s["warn_bg"],
         size=12, kind="mono_bold", padx=10, height=24)
    draw.text((1236, 384), "RO-003", font=font(12, "mono_bold"),
              fill=hx(s["warn"]), anchor="ls")
    draw.text((816, 410), h["mismatch_sub"], font=font(10, "cjk"),
              fill=hx(s["faint"]), anchor="ls")
    draw.line([816, 424, 1350, 424], fill=hx(s["grid"]), width=1)

    # The two findings, with the tool's locator and phrasing.
    chip(draw, (816, 438), "RO-001", fg=s["warn"], bg=s["warn_bg"],
         size=11, kind="mono_bold", padx=8, height=20)
    draw.text((886, 452), h["find1"], font=font(12, "cjk"),
              fill=hx(s["text"]), anchor="ls")
    chip(draw, (816, 466), "RO-003", fg=s["warn"], bg=s["warn_bg"],
         size=11, kind="mono_bold", padx=8, height=20)
    draw.text((886, 480), h["find2"], font=font(12, "cjk"),
              fill=hx(s["text"]), anchor="ls")

    require_w(h["find1"], 12, "cjk", 452, "hero finding 1")
    require_w(h["find2"], 12, "cjk", 452, "hero finding 2")

    # ---- report readout ---------------------------------------------------
    img = card(img, (788, 504, 1368, 554), s, radius=16, blur=12, dy=6)
    draw = ImageDraw.Draw(img)
    draw.text((816, 536), h["report_issues"], font=font(18, "mono_bold"),
              fill=hx(s["warn"]), anchor="ls")
    draw.text((942, 536), h["report_skipped"], font=font(18, "mono_bold"),
              fill=hx(s["sub"]), anchor="ls")
    draw.line([1068, 518, 1068, 542], fill=hx(s["grid"]), width=1)
    draw.text((1090, 534), h["report_summary"], font=font(11, "mono"),
              fill=hx(s["sub"]), anchor="ls")
    draw.text((1350, 534), h["report_pack"], font=font(10, "cjk"),
              fill=hx(s["faint"]), anchor="rs")
    require_w(h["report_summary"], 11, "mono", 250, "hero report summary")
    require_w(h["report_pack"], 10, "cjk", 250, "hero report pack")
    return img


def write_heroes() -> None:
    for lang in ("zh", "en"):
        for skin in ("light", "dark"):
            img = draw_hero(lang, skin)
            path = os.path.join(OUT, f"dsh-repair-order-qc-hero-{lang}-{skin}.webp")
            img.save(path, "WEBP", quality=WEBP_QUALITY, method=6)
            print(f"wrote {os.path.relpath(path, ROOT)}")


# --------------------------------------------------------------------------- SVG
SANS = "'Microsoft YaHei','Segoe UI','PingFang SC','Noto Sans CJK SC',sans-serif"
MONO = "Consolas,'Microsoft YaHei',ui-monospace,monospace"


def tw(text: str, size: int, kind: str = "mono") -> float:
    return measure(text, size, "mono" if kind == "mono" else "cjk")


def need(text: str, size: int, kind: str, max_w: float, what: str) -> None:
    require_w(text, size, "mono" if kind == "mono" else "cjk", max_w, what)


def num(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".")


def stext(x: float, y: float, text: str, size: int, fill: str,
          kind: str = "mono", bold: bool = False,
          anchor: str | None = None, opacity: float | None = None,
          spacing: str | None = None) -> str:
    family = MONO if kind == "mono" else SANS
    attrs = [f'x="{num(x)}"', f'y="{num(y)}"', f'fill="{fill}"',
             f'font-family="{family}"', f'font-size="{num(size)}"']
    if bold:
        attrs.append('font-weight="700"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        attrs.append(f'opacity="{num(opacity)}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    return f'<text {" ".join(attrs)}>{escape(text)}</text>'


def srect(x: float, y: float, w: float, h: float, radius: float, fill: str,
          stroke: str | None = None, sw: float = 1,
          shadow: bool = False) -> str:
    attrs = [f'x="{num(x)}"', f'y="{num(y)}"', f'width="{num(w)}"',
             f'height="{num(h)}"', f'rx="{num(radius)}"', f'fill="{fill}"']
    if stroke:
        attrs += [f'stroke="{stroke}"', f'stroke-width="{num(sw)}"']
    if shadow:
        attrs.append('filter="url(#soft)"')
    return f'<rect {" ".join(attrs)}/>'


def schip(x: float, y: float, text: str, size: int, fg: str, bg: str,
          kind: str = "mono", bold: bool = False, h: float = 20,
          padx: float = 8, stroke: str | None = None) -> tuple[str, float]:
    width = tw(text, size, kind) + padx * 2
    out = [srect(x, y, width, h, h / 2, bg, stroke=stroke, sw=1)]
    out.append(stext(x + padx, y + h / 2 + size * 0.36, text, size, fg,
                     kind=kind, bold=bold))
    return "".join(out), width


def arrow(x1: float, y1: float, x2: float, y2: float, color: str,
          width: float = 1.6, dash: str | None = None) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{num(x1)} {num(y1)}L{num(x2)} {num(y2)}" '
            f'fill="none" stroke="{color}" stroke-width="{num(width)}" '
            f'stroke-linecap="round"{dash_attr} marker-end="url(#head)"/>')


def flow_svg(skin: str) -> str:
    s = SKIN[skin]
    w, ht = 1100, 660
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{ht}" '
        f'viewBox="0 0 {w} {ht}" role="img" '
        f'aria-label="dsh-repair-order-qc structure">',
        '<title>dsh-repair-order-qc structure</title>',
        '<defs>',
        f'<linearGradient id="bg" x1="0" y1="0" x2="0.15" y2="1">'
        f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
        f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>',
        '<filter id="soft" x="-20%" y="-20%" width="140%" height="150%">'
        '<feDropShadow dx="0" dy="5" stdDeviation="7" '
        'flood-color="#221a42" flood-opacity="0.10"/></filter>',
        f'<marker id="head" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0 0L10 5L0 10z" fill="{s["accent"]}"/></marker>',
        '</defs>',
        f'<rect width="{w}" height="{ht}" rx="18" fill="url(#bg)"/>',
    ]

    # ---- masthead ---------------------------------------------------------
    title = "repair_order_qc · one repair order, seven checks"
    need(title, 21, "cjk", 760, "flow title")
    parts.append(stext(40, 44, title, 21, s["text"], kind="cjk", bold=True))
    sub = "material → canonical table → 7 checks → issues[] / skipped[] → buildView()"
    need(sub, 13, "mono", 760, "flow subtitle")
    parts.append(stext(40, 68, sub, 13, s["sub"], kind="mono"))
    chip1, w1 = schip(1060 - tw("pack 2026.1", 11) - 30, 30,
                      "pack 2026.1", 11, s["accent"], s["accent_soft"], h=22,
                      padx=10, stroke=s["accent_line"])
    parts.append(chip1)
    chip2, w2 = schip(1060 - tw("7 rules · all warn", 11) - 30, 56,
                      "7 rules · all warn", 11, s["warn"], s["warn_bg"], h=22,
                      padx=10, stroke=s["warn_line"])
    parts.append(chip2)
    _ = (w1, w2)

    # ---- intake bars ------------------------------------------------------
    parts.append(srect(40, 92, 660, 64, 16, s["card"], stroke=s["edge"],
                       shadow=True))
    parts.append(stext(60, 116, "file | material → parseMaterial()", 13,
                       s["text"], bold=True))
    sub_l = "JSON / YAML · column aliases → canonical fields · header + rows"
    need(sub_l, 11, "mono", 616, "intake left sub")
    parts.append(stext(60, 137, sub_l, 11, s["sub"]))

    parts.append(srect(724, 92, 336, 64, 16, s["card"], stroke=s["edge"],
                       shadow=True))
    parts.append(stext(744, 114, "rules/repair-order-qc.yaml", 13, s["text"],
                       bold=True))
    parts.append(stext(744, 133, "loadRuleset() · excerpt ≥ 8 chars", 11,
                       s["sub"]))
    parts.append(stext(744, 149, "kind → severity cap · validated on load", 11,
                       s["sub"]))
    need("kind → severity cap · validated on load", 11, "mono", 296,
         "intake right sub")
    parts.append(arrow(370, 156, 370, 174, s["accent"], 1.8))
    parts.append(arrow(892, 156, 892, 174, s["accent"], 1.8))

    # ---- settlement proof sheet ------------------------------------------
    parts.append(srect(40, 176, 660, 324, 18, s["card"], stroke=s["edge"],
                       shadow=True))
    parts.append(srect(40, 192, 5, 56, 2.5, s["accent"]))
    parts.append(stext(60, 200, "settlement proof · WX-2026-0018", 13,
                       s["text"], bold=True))
    parts.append(stext(680, 200, "runTableCheck()", 11, s["faint"],
                       anchor="end"))

    # Header equation: four real values from the quickstart sample.
    cells = (60, 214, 368, 522)
    for index, (label, value) in enumerate((
        ("partsTotal", "360"), ("laborTotal", "200"),
        ("discount", "0"), ("total", "560"),
    )):
        cx = cells[index]
        parts.append(srect(cx, 214, 144, 58, 11, s["band"],
                           stroke=s["grid"]))
        parts.append(stext(cx + 12, 235, label, 11, s["faint"]))
        parts.append(stext(cx + 12, 261, value, 20,
                           s["accent"] if index == 3 else s["text"],
                           bold=True))
    for opx, op in ((209, "+"), (363, "−"), (517, "=")):
        parts.append(stext(opx, 258, op, 16, s["faint"], bold=True,
                           anchor="middle"))
    chk = "√ RO-004 · 360 + 200 − 0 = 560"
    need(chk, 11, "mono", 300, "RO-004 line")
    parts.append(stext(680, 288, chk, 11, s["ok"], anchor="end"))

    # One detail row from that sample.
    parts.append(stext(60, 308, "itemName", 11, s["faint"]))
    parts.append(stext(300, 308, "quantity", 11, s["faint"]))
    parts.append(stext(372, 308, "unitPrice", 11, s["faint"]))
    parts.append(stext(454, 308, "amount", 11, s["faint"]))
    parts.append(stext(520, 308, "customerConcern · workDone", 11, s["faint"]))
    need("customerConcern · workDone", 11, "mono", 160, "table last header")
    parts.append(stext(60, 334, "前制动片", 14, s["text"], kind="cjk",
                       bold=True))
    for x, value in ((300, "2"), (372, "180"), (454, "360")):
        parts.append(stext(x, 334, value, 15, s["text"], bold=True))
    parts.append(stext(520, 334, "空  /  空", 15, s["warn"], kind="cjk", bold=True))

    product = "2 × 180 = 360 √ RO-002"
    need(product, 11, "mono", 230, "RO-002 line")
    parts.append(stext(300, 356, product, 11, s["ok"]))
    parts.append(stext(520, 356, "both empty × RO-001", 11, s["warn"]))
    parts.append(f'<line x1="60" y1="368" x2="680" y2="368" '
                 f'stroke="{s["grid"]}"/>')

    # RO-003: the sum of amount against the declared total.
    parts.append(stext(60, 392, "Σ amount 360", 15, s["warn"], bold=True))
    parts.append(stext(212, 396, "≠", 24, s["warn"], bold=True))
    parts.append(stext(252, 392, "total 560", 15, s["text"], bold=True))
    gap, gap_w = schip(378, 376, "gap 200", 11, s["warn"], s["warn_bg"],
                       bold=True, h=22, padx=9, stroke=s["warn_line"])
    parts.append(gap)
    parts.append(stext(378 + gap_w + 14, 392, "× RO-003", 13, s["warn"],
                       bold=True))
    parts.append(stext(60, 412, "1 detail row · tolerance 0.01", 11,
                       s["faint"]))

    # Three side checks, drawn as a small rule strip under the arithmetic.
    side = (
        ("RO-005", "receivedAt ≤ deliveredAt", "03-02 ≤ 03-04 √", s["ok"]),
        ("RO-006", "orderNo unique", "×1 √", s["ok"]),
        ("RO-007", "itemName placeholders", "none √", s["ok"]),
    )
    for index, (rid, label, result, color) in enumerate(side):
        sx = 60 + index * 210
        parts.append(srect(sx, 428, 190, 62, 10, s["band"],
                           stroke=s["grid"]))
        parts.append(stext(sx + 12, 446, rid, 13, s["text"], bold=True))
        parts.append(stext(sx + 12, 464, label, 11, s["sub"]))
        parts.append(stext(sx + 12, 481, result, 11, color))
        need(label, 11, "mono", 168, f"{rid} label")
        need(result, 11, "mono", 168, f"{rid} result")

    # ---- rule-pack validation rack ---------------------------------------
    parts.append(srect(724, 176, 336, 324, 18, s["card"], stroke=s["edge"],
                       shadow=True))
    parts.append(stext(744, 200, "rule pack gate", 13, s["text"], bold=True))
    parts.append(stext(744, 218, "rules/repair-order-qc.yaml · 2026.1", 11,
                       s["faint"]))

    caps = (
        ("direct", "error allowed", "4 rules", s["accent"]),
        ("derived-from-principle", "warn cap", "3 rules", s["warn"]),
        ("institutional-configuration", "info cap", "0 rules", s["faint"]),
    )
    for index, (kind, cap, count, color) in enumerate(caps):
        cy = 232 + index * 40
        parts.append(srect(744, cy, 296, 36, 8, s["band"],
                           stroke=s["grid"]))
        parts.append(srect(744, cy, 4, 36, 2, color))
        parts.append(stext(758, cy + 16, kind, 11, color, bold=True))
        parts.append(stext(758, cy + 31, f"→ {cap} · {count}", 11,
                           s["sub"]))
        need(kind, 11, "mono", 270, f"{kind} kind")
        need(f"→ {cap} · {count}", 11, "mono", 270, f"{kind} cap")

    checks = (
        "√ excerpt ≥ 8 chars · on load",
        "√ citation gate · verbatim trace",
        "√ all 7 rules ship as warn",
    )
    for index, text in enumerate(checks):
        parts.append(stext(744, 368 + index * 18, text, 11, s["sub"]))
        need(text, 11, "mono", 296, f"pack check {index}")
    parts.append(f'<line x1="744" y1="416" x2="1040" y2="416" '
                 f'stroke="{s["grid"]}"/>')
    parts.append(stext(744, 434, "config", 13, s["text"], bold=True))
    parts.append(stext(744, 452, "disabledRules / onlyRules", 11, s["sub"]))
    parts.append(stext(744, 470, "every skip carries a reason", 11, s["warn"]))
    parts.append(stext(744, 488, "swap the YAML → new rule set", 11,
                       s["faint"]))
    need("swap the YAML → new rule set", 11, "mono", 296, "pack swap note")

    # ---- report split: issues[] / skipped[] / summary --------------------
    bus_y = 510
    parts.append(f'<path d="M210 {bus_y}H892" fill="none" '
                 f'stroke="{s["accent"]}" stroke-width="1.6"/>')
    parts.append(f'<path d="M370 500V{bus_y}" fill="none" '
                 f'stroke="{s["accent"]}" stroke-width="1.6"/>')
    parts.append(f'<path d="M892 500V{bus_y}" fill="none" '
                 f'stroke="{s["accent"]}" stroke-width="1.6"/>')
    for drop in (210, 548, 892):
        parts.append(arrow(drop, bus_y, drop, 518, s["accent"], 1.6))

    trays = (
        (40, 340, "issues[] · 2", "RO-001 · RO-003 · both warn",
         "found · expected · fix", s["warn"]),
        (396, 304, "skipped[] · 0", "every declared check ran",
         "empty ≠ clean", s["sub"]),
        (724, 336, "summary", "error 0 · warn 2 · info 0",
         "ruleset 2026.1 · checkedAt", s["accent"]),
    )
    for x, twidth, head, line1, line2, color in trays:
        parts.append(srect(x, 520, twidth, 62, 12, s["card"],
                           stroke=s["edge"], shadow=True))
        is_summary = head == "summary"
        parts.append(stext(x + 16, 544, head, 13 if is_summary else 15,
                           s["text"], bold=True))
        parts.append(stext(x + 16, 562, line1, 13 if is_summary else 11,
                           color, bold=is_summary))
        parts.append(stext(x + 16, 578, line2, 11, s["faint"]))
        need(line1, 13 if is_summary else 11, "mono", twidth - 32,
             f"tray {head} line 1")
        need(line2, 11, "mono", twidth - 32, f"tray {head} line 2")

    # ---- buildView projection --------------------------------------------
    parts.append(arrow(210, 582, 210, 592, s["accent"], 1.6))
    parts.append(arrow(548, 582, 548, 592, s["accent"], 1.6))
    parts.append(srect(40, 594, 1020, 52, 14, s["card"], stroke=s["accent"],
                       sw=1.5, shadow=True))
    parts.append(stext(60, 618, "buildView(report) → markdown · reportJson",
                       14, s["text"], bold=True))
    need("buildView(report) → markdown · reportJson", 14, "mono", 520,
         "buildView line")
    parts.append(stext(1040, 618, "issueCount 2 · skippedCount 0", 11,
                       s["accent"], anchor="end", bold=True))
    parts.append(stext(1040, 636,
                       "summary · error 0 / warn 2 / info 0 · verdict stays with the reviewer",
                       11, s["faint"], anchor="end"))
    need("summary · error 0 / warn 2 / info 0 · verdict stays with the reviewer",
         11, "mono", 680, "buildView footnote")

    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def write_flows() -> None:
    for skin in ("light", "dark"):
        path = os.path.join(OUT, f"dsh-repair-order-qc-flow-v5-{skin}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin))
        print(f"wrote {os.path.relpath(path, ROOT)}")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    write_heroes()
    write_flows()


if __name__ == "__main__":
    main()
