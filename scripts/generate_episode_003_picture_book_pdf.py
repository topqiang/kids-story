#!/usr/bin/env python3
"""生成《幼儿园里朋友有好多》绘本 PDF。"""

from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT_DIR = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT_DIR / "picture_books" / "episode_003_you_er_yuan_li_peng_you_you_hao_duo"
IMAGE_DIR = BOOK_DIR / "images"
OUTPUT_PATH = ROOT_DIR / "output" / "pdf" / "you_er_yuan_li_peng_you_you_hao_duo_picture_book.pdf"

PAGE_WIDTH = 1080
PAGE_HEIGHT = 1920
FONT_NAME = "ArialUnicode"
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")


def register_font() -> None:
    """注册支持中文的系统字体。"""
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"缺少中文字体：{FONT_PATH}")
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))


def draw_full_page(pdf: canvas.Canvas, image_path: Path) -> None:
    """按原比例满页绘制单张有字绘本页。"""
    with Image.open(image_path) as image:
        width, height = image.size
    scale = max(PAGE_WIDTH / width, PAGE_HEIGHT / height)
    draw_width = width * scale
    draw_height = height * scale
    pdf.drawImage(
        str(image_path),
        (PAGE_WIDTH - draw_width) / 2,
        (PAGE_HEIGHT - draw_height) / 2,
        draw_width,
        draw_height,
    )


def draw_cover(pdf: canvas.Canvas) -> None:
    """绘制独立封面，避免重复遮盖正文页面文字。"""
    pdf.setFillColor(colors.HexColor("#FFF4D8"))
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor("#BFE3F2"))
    pdf.roundRect(70, 1160, PAGE_WIDTH - 140, 520, 54, fill=1, stroke=0)

    rainbow_colors = ["#EF7B67", "#F3B65B", "#F4D96B", "#78C49A", "#72AADB"]
    for index, color in enumerate(rainbow_colors):
        pdf.setStrokeColor(colors.HexColor(color))
        pdf.setLineWidth(24)
        inset = index * 30
        pdf.arc(185 + inset, 660 + inset, 895 - inset, 1370 - inset, 0, 180)

    pdf.setFillColor(colors.HexColor("#F6C84F"))
    for x, y in [(150, 1720), (915, 1690), (145, 360), (920, 410)]:
        pdf.circle(x, y, 28, fill=1, stroke=0)

    pdf.setFillColor(colors.HexColor("#2D2520"))
    pdf.setFont(FONT_NAME, 72)
    pdf.drawCentredString(PAGE_WIDTH / 2, 1500, "幼儿园里朋友有好多")

    pdf.setFont(FONT_NAME, 34)
    pdf.drawCentredString(PAGE_WIDTH / 2, 1410, "朋友不是数量，是一个个记得住的名字")

    pdf.setFillColor(colors.HexColor("#6E563D"))
    pdf.setFont(FONT_NAME, 28)
    pdf.drawCentredString(PAGE_WIDTH / 2, 250, "小北斗 · 婷婷妈妈 · 林老师 · 乐乐 · 米粒 · 果果")
    pdf.showPage()


def main() -> None:
    """生成 1 页封面和 10 页正文。"""
    pages = [IMAGE_DIR / f"page_{number:02d}.png" for number in range(1, 11)]
    missing = [str(path) for path in pages if not path.exists()]
    if missing:
        raise FileNotFoundError(f"缺少绘本页面：{missing}")

    register_font()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT_PATH), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle("幼儿园里朋友有好多")
    pdf.setAuthor("kids-story")
    pdf.setSubject("3-6 岁儿童亲子绘本")

    draw_cover(pdf)
    for page in pages:
        draw_full_page(pdf, page)
        pdf.showPage()
    pdf.save()
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
