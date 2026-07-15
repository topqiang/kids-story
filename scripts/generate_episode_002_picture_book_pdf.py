#!/usr/bin/env python3
"""生成《独立自主吃饭》有字绘本 PDF。"""

from pathlib import Path

from PIL import Image
from reportlab.pdfgen import canvas


ROOT_DIR = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT_DIR / "picture_books" / "episode_002_du_li_zi_zhu_chi_fan" / "images"
OUTPUT_PATH = ROOT_DIR / "output" / "pdf" / "du_li_zi_zhu_chi_fan_picture_book.pdf"
PAGE_WIDTH = 1080
PAGE_HEIGHT = 1920


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


def main() -> None:
    """生成 10 页正文 PDF。"""
    pages = [IMAGE_DIR / f"page_{number:02d}_text_v5.png" for number in range(1, 11)]
    missing = [str(path) for path in pages if not path.exists()]
    if missing:
        raise FileNotFoundError(f"缺少绘本页面：{missing}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT_PATH), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle("独立自主吃饭")
    pdf.setAuthor("kids-story")
    for page in pages:
        draw_full_page(pdf, page)
        pdf.showPage()
    pdf.save()
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
