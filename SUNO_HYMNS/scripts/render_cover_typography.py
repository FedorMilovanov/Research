#!/usr/bin/env python3
"""Набор типографики обложки PHOS-001 поверх утверждённой базы D.

База (фотография) не трогается: меняется только текст. Кириллицу генератор
изображений ломает, поэтому надписи набираются здесь.

Зависимости: pillow. Шрифты — не в репозитории (лицензия OFL, бинарники):
  PT Serif      : https://github.com/google/fonts  ofl/ptserif/PT_Serif-Web-Regular.ttf
  Cormorant     : https://github.com/google/fonts  ofl/cormorantgaramond/CormorantGaramond[wght].ttf
Путь к каталогу со шрифтами: --fonts (по умолчанию ~/.fonts_manual).

Использование:
  python3 render_cover_typography.py --base ..._cover_battle-D.png --out-dir <dir>
"""

import argparse
import pathlib

from PIL import Image, ImageDraw, ImageFont

TITLE = "СВЕТ ОТРАДНЫЙ"
TITLE_STACK = ["СВЕТ", "ОТРАДНЫЙ"]
SUBTITLE = "ДРЕВНИЙ ГИМН"
CREDIT = "Автор неизвестен: Василий Великий ок. 375 г. уже называет его древним"

COL_TITLE = (247, 238, 219)
COL_SUB = (186, 176, 157)
COL_CREDIT = (156, 148, 135)
COL_RULE = (150, 140, 124)

SS = 3  # supersampling текста

DEFAULT_FONTS = pathlib.Path.home() / ".fonts_manual"
COR_MORANT = "CormorantGaramond.ttf"
PT_SERIF = "PT_Serif-Web-Regular.ttf"


def load(path, size, weight=None):
    f = ImageFont.truetype(str(path), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def tracked(draw, text, font, tr):
    return draw.textlength(text, font=font) + tr * max(len(text) - 1, 0)


def fit(draw, text, font_path, target, tr_ratio, weight=None):
    """Подобрать кегль так, чтобы ширина строки с трекингом была ближе всего к target."""
    lo, hi, best = 4, 600, None
    while lo <= hi:
        mid = (lo + hi) // 2
        f = load(font_path, mid * SS, weight)
        w = tracked(draw, text, f, tr_ratio * mid * SS)
        if best is None or abs(w - target) < abs(best[1] - target):
            best = (mid, w, f)
        if w < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return best[2], best[0]


def draw_tracked(draw, x, y, text, font, tr, fill):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=font, fill=fill, anchor="ls")
        cx += draw.textlength(ch, font=font) + tr
    return cx - tr - x


def line_height(font):
    ascent, descent = font.getmetrics()
    return ascent + descent


def render(base_path, out_path, layout):
    base = Image.open(base_path).convert("RGB")
    w, h = base.size
    layer = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    axis = w * 0.075 * SS
    font_dir = layout["fonts"]

    title_font, title_size = fit(
        d, layout["fit_text"], font_dir / layout["title_font"],
        w * layout["title_frac"] * SS, layout["title_tr"], layout.get("title_weight"),
    )
    sub_font, sub_size = fit(
        d, SUBTITLE, font_dir / layout["sub_font"],
        w * layout["sub_frac"] * SS, layout["sub_tr"], layout.get("sub_weight"),
    )
    credit_font, credit_size = fit(
        d, CREDIT, font_dir / layout["credit_font"],
        w * layout["credit_frac"] * SS, layout["credit_tr"], layout.get("credit_weight"),
    )

    th = line_height(title_font)
    sh = line_height(sub_font)
    ch = line_height(credit_font)
    lead_t = title_size * SS * layout["lead_title"]
    lead_s = title_size * SS * layout["lead_sub"]

    title_lines = layout.get("title_lines") or [TITLE]
    head_h = th * len(title_lines) + lead_t + sh
    if layout["rule"]:
        head_h += lead_s + max(1, SS)

    if layout["credit_at_bottom"]:
        head_top = h * layout["center"] * SS - head_h / 2
        credit_top = h * SS - (h * 0.085 * SS) - ch
        block_h = head_h
    else:
        head_h += lead_s + ch
        head_top = h * layout["center"] * SS - head_h / 2
        credit_top = head_top + th * len(title_lines) + lead_t + sh + (
            (lead_s + max(1, SS)) if layout["rule"] else 0
        ) + lead_s
        block_h = head_h

    y = head_top
    for ln in title_lines:
        draw_tracked(d, axis, y, ln, title_font, layout["title_tr"] * title_size * SS,
                     COL_TITLE)
        y += th
    y += lead_t
    draw_tracked(d, axis, y, SUBTITLE, sub_font, layout["sub_tr"] * sub_size * SS, COL_SUB)
    y += sh

    if layout["rule"]:
        y += lead_s
        rule_w = w * layout["rule_frac"] * SS
        d.rectangle([axis, y, axis + rule_w, y + max(1, SS)], fill=COL_RULE + (190,))
        y += max(1, SS)

    if not layout["credit_at_bottom"]:
        y += lead_s
    else:
        y = credit_top
    draw_tracked(d, axis, y, CREDIT, credit_font, layout["credit_tr"] * credit_size * SS,
                 COL_CREDIT)

    layer = layer.resize((w, h), Image.LANCZOS)
    out = Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")
    out.save(out_path)
    print(f"{out_path.name}: base {w}x{h}, кегль заголовка {title_size}px, "
          f"блок {block_h / SS:.0f}px")


LAYOUTS = {
    "V": dict(
        note="Cormorant Garamond Light, заголовок одной строкой, строка-отбивка",
        title_font=COR_MORANT, sub_font=COR_MORANT, credit_font=COR_MORANT,
        fit_text=TITLE, title_lines=[TITLE],
        title_frac=0.36, title_tr=0.06,
        sub_frac=0.105, sub_tr=0.20,
        credit_frac=0.335, credit_tr=0.005,
        lead_title=0.30, lead_sub=0.42, rule=True, rule_frac=0.185,
        center=0.445, credit_at_bottom=False,
    ),
    "W": dict(
        note="Cormorant Garamond Light, заголовок в две строки лесенкой",
        title_font=COR_MORANT, sub_font=COR_MORANT, credit_font=COR_MORANT,
        fit_text="ОТРАДНЫЙ", title_lines=TITLE_STACK,
        title_frac=0.285, title_tr=0.06,
        sub_frac=0.105, sub_tr=0.20,
        credit_frac=0.335, credit_tr=0.005,
        lead_title=0.26, lead_sub=0.60, rule=False,
        center=0.435, credit_at_bottom=False,
    ),
    "X": dict(
        note="PT Serif, заголовок одной строкой, выходные данные внизу",
        title_font=PT_SERIF, sub_font=PT_SERIF, credit_font=PT_SERIF,
        fit_text=TITLE, title_lines=[TITLE],
        title_frac=0.355, title_tr=0.05,
        sub_frac=0.115, sub_tr=0.18,
        credit_frac=0.345, credit_tr=0.004,
        lead_title=0.28, lead_sub=0.40, rule=True, rule_frac=0.20,
        center=0.40, credit_at_bottom=True,
    ),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--fonts", default=str(DEFAULT_FONTS))
    ap.add_argument("--only", default="")
    args = ap.parse_args()

    font_dir = pathlib.Path(args.fonts)
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for key, layout in LAYOUTS.items():
        if args.only and key not in args.only.split(","):
            continue
        layout = dict(layout)
        layout["fonts"] = font_dir
        render(args.base, out_dir / f"PHOS-001_cover_type-{key}.png", layout)


if __name__ == "__main__":
    main()
