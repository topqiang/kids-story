#!/usr/bin/env python3
"""生成《宝宝初入幼儿园》绘本最终版 PDF。"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT_DIR = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT_DIR / "picture_books" / "episode_001_bao_bao_chu_ru_you_er_yuan"
OUTPUT_DIR = ROOT_DIR / "output" / "pdf"
OUTPUT_PDF = OUTPUT_DIR / "bao_bao_chu_ru_you_er_yuan_picture_book.pdf"

PAGE_W = 1080
PAGE_H = 1920
MARGIN = 72
TEXT_BOX_H = 420

FONT_NAME = "ArialUnicode"
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")


def register_fonts() -> None:
    """注册中文字体。"""
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"缺少中文字体：{FONT_PATH}")
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))


def draw_wrapped_text(
    pdf: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    max_width: float,
    font_size: int,
    leading: int,
    max_lines: int | None = None,
) -> float:
    """按中文字符宽度自动换行，返回最后一行的 y 坐标。"""
    lines: list[str] = []
    current = ""
    for char in text:
        if char == "\n":
            lines.append(current)
            current = ""
            continue
        candidate = current + char
        if pdf.stringWidth(candidate, FONT_NAME, font_size) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)

    if max_lines is not None:
        lines = lines[:max_lines]

    pdf.setFont(FONT_NAME, font_size)
    for line in lines:
        pdf.drawString(x, y, line)
        y -= leading
    return y


def draw_page_background(pdf: canvas.Canvas, image_path: Path) -> None:
    """绘制 9:16 全页图片。"""
    with Image.open(image_path) as img:
        img_w, img_h = img.size
    scale = max(PAGE_W / img_w, PAGE_H / img_h)
    draw_w = img_w * scale
    draw_h = img_h * scale
    x = (PAGE_W - draw_w) / 2
    y = (PAGE_H - draw_h) / 2
    pdf.drawImage(str(image_path), x, y, draw_w, draw_h)


def draw_text_box(pdf: canvas.Canvas, page_number: int, text: str) -> None:
    """绘制底部绘本文案区。"""
    box_y = 0
    pdf.setFillColor(colors.Color(1, 0.97, 0.9))
    pdf.rect(0, box_y, PAGE_W, TEXT_BOX_H, fill=1, stroke=0)

    pdf.setFillColor(colors.Color(0.95, 0.62, 0.24))
    pdf.rect(0, TEXT_BOX_H - 12, PAGE_W, 12, fill=1, stroke=0)

    pdf.setFillColor(colors.Color(0.25, 0.18, 0.12))
    pdf.setFont(FONT_NAME, 30)
    pdf.drawString(MARGIN, TEXT_BOX_H - 70, f"第 {page_number} 页")

    pdf.setFillColor(colors.Color(0.18, 0.14, 0.1))
    draw_wrapped_text(
        pdf,
        text,
        MARGIN,
        TEXT_BOX_H - 125,
        PAGE_W - MARGIN * 2,
        font_size=32,
        leading=46,
        max_lines=6,
    )


def draw_cover(pdf: canvas.Canvas, first_image: Path) -> None:
    """绘制封面。"""
    draw_page_background(pdf, first_image)
    pdf.setFillColor(colors.Color(1, 0.96, 0.86))
    pdf.roundRect(76, 1180, PAGE_W - 152, 460, 28, fill=1, stroke=0)

    pdf.setFillColor(colors.Color(0.24, 0.14, 0.08))
    pdf.setFont(FONT_NAME, 68)
    pdf.drawCentredString(PAGE_W / 2, 1490, "宝宝初入幼儿园")

    pdf.setFont(FONT_NAME, 34)
    pdf.drawCentredString(PAGE_W / 2, 1410, "第一天上幼儿园")
    pdf.drawCentredString(PAGE_W / 2, 1360, "最需要勇气的可能是爸爸妈妈")

    pdf.setFillColor(colors.Color(0.74, 0.34, 0.18))
    pdf.setFont(FONT_NAME, 28)
    pdf.drawCentredString(PAGE_W / 2, 1260, "小北斗 · 婷婷妈妈 · 北斗爸爸")
    pdf.showPage()


def draw_story_pages(pdf: canvas.Canvas, pages: list[dict]) -> None:
    """绘制 10 页绘本正文。"""
    for item in pages:
        image_path = BOOK_DIR / item["image"]
        draw_page_background(pdf, image_path)
        draw_text_box(pdf, item["page"], item["text"])
        pdf.showPage()


def draw_dialogue_appendix(pdf: canvas.Canvas) -> None:
    """绘制完整对白台词附录。"""
    dialogues = [
        ("小北斗", "小书包背好啦，幼儿园我来啦，见到老师笑一笑，早上好！"),
        ("婷婷妈妈", "小北斗，要不妈妈再陪你五分钟？"),
        ("小北斗", "妈妈，你也要上幼儿园吗？"),
        ("北斗爸爸", "爸爸觉得，可以先开个家庭会议。"),
        ("小北斗", "不用开会，我已经是大班预备队了。"),
        ("婷婷妈妈", "你要是想妈妈，就跟老师说。"),
        ("小北斗", "那妈妈想我，也要跟爸爸说。"),
        ("小北斗", "来，一人一个勇气贴纸。"),
        ("北斗爸爸", "爸爸也需要吗？"),
        ("小北斗", "你刚刚已经看了门口三次。"),
        ("林老师", "小北斗，早上好，我们一起去看小汽车积木吧。"),
        ("小北斗", "好！妈妈爸爸，挥手三下，不能多。"),
        ("北斗爸爸", "那爸爸偷偷再看一眼。"),
        ("小北斗", "爸爸，不能趴门缝，会吓到积木。"),
        ("婷婷妈妈", "他跑回来了，是不是舍不得？"),
        ("小北斗", "不是，妈妈，你的勇气贴纸掉了。"),
        ("小北斗", "你们乖乖上班，下午我来接你们。"),
    ]

    pdf.setFillColor(colors.Color(1, 0.98, 0.93))
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    pdf.setFillColor(colors.Color(0.24, 0.14, 0.08))
    pdf.setFont(FONT_NAME, 54)
    pdf.drawString(MARGIN, PAGE_H - 120, "完整对白台词")

    y = PAGE_H - 210
    for speaker, line in dialogues:
        if y < 150:
            pdf.showPage()
            pdf.setFillColor(colors.Color(1, 0.98, 0.93))
            pdf.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
            y = PAGE_H - 120

        pdf.setFillColor(colors.Color(0.72, 0.32, 0.16))
        pdf.setFont(FONT_NAME, 28)
        pdf.drawString(MARGIN, y, f"{speaker}：")

        pdf.setFillColor(colors.Color(0.18, 0.14, 0.1))
        y = draw_wrapped_text(
            pdf,
            line,
            MARGIN + 150,
            y,
            PAGE_W - MARGIN * 2 - 150,
            font_size=28,
            leading=40,
        )
        y -= 22

    pdf.showPage()


def main() -> None:
    register_fonts()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = json.loads((BOOK_DIR / "pages.json").read_text(encoding="utf-8"))
    pages = data["pages"]

    pdf = canvas.Canvas(str(OUTPUT_PDF), pagesize=(PAGE_W, PAGE_H))
    pdf.setTitle("宝宝初入幼儿园")
    pdf.setAuthor("kids-story")

    draw_cover(pdf, BOOK_DIR / pages[0]["image"])
    draw_story_pages(pdf, pages)
    draw_dialogue_appendix(pdf)
    pdf.save()

    print(OUTPUT_PDF)


if __name__ == "__main__":
    main()
