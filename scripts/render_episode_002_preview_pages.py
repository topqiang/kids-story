#!/usr/bin/env python3
"""为《独立自主吃饭》前三页预览图叠加准确中文。"""

from __future__ import annotations

from pathlib import Path
from shutil import copy2
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT_DIR = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT_DIR / "picture_books" / "episode_002_du_li_zi_zhu_chi_fan"
IMAGE_DIR = BOOK_DIR / "images"

FONT_PATHS = [
    Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    Path("/System/Library/Fonts/Supplemental/Songti.ttc"),
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
]

SOURCE_IMAGES = {
    1: Path("/Users/qiang/.codex/generated_images/019f44b5-2981-74d1-8a27-3a7956c74f1d/ig_08156da479ae4fdd016a4f14aa388c819ba8f00b575964896a.png"),
    2: Path("/Users/qiang/.codex/generated_images/019f44b5-2981-74d1-8a27-3a7956c74f1d/ig_08156da479ae4fdd016a4f15549598819ba27a732b0b5e06db.png"),
    3: Path("/Users/qiang/.codex/generated_images/019f44b5-2981-74d1-8a27-3a7956c74f1d/ig_08156da479ae4fdd016a4f15dc2314819bba887458cfca3674.png"),
}

SOURCE_IMAGES_V2 = {
    1: Path("/Users/qiang/.codex/generated_images/019f44b5-2981-74d1-8a27-3a7956c74f1d/ig_082fdaf37984e31e016a4f2cf47d70819a82e31052274e8d0a.png"),
    2: Path("/Users/qiang/.codex/generated_images/019f44b5-2981-74d1-8a27-3a7956c74f1d/ig_06c565a872e2d2a4016a4f2beb2dfc819a8532b596b640d4da.png"),
    3: Path("/Users/qiang/.codex/generated_images/019f44b5-2981-74d1-8a27-3a7956c74f1d/ig_06c565a872e2d2a4016a4f2c4abebc819aaa513a0900ea8f35.png"),
}


def get_font(size: int) -> ImageFont.FreeTypeFont:
    """加载本机中文字体。"""
    for font_path in FONT_PATHS:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    raise FileNotFoundError("未找到可用中文字体")


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    """计算文字宽度。"""
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    """按中文字符宽度换行。"""
    lines: list[str] = []
    current = ""
    for char in text:
        if char == "\n":
            if current:
                lines.append(current)
            current = ""
            continue
        candidate = current + char
        if text_width(draw, candidate, font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    start_size: int,
    min_size: int = 20,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    """自动缩小字号，确保文字放进指定区域。"""
    x1, y1, x2, y2 = box
    max_width = x2 - x1
    max_height = y2 - y1
    for size in range(start_size, min_size - 1, -2):
        font = get_font(size)
        leading = int(size * 1.35)
        lines = wrap_text(draw, text, font, max_width)
        if len(lines) * leading <= max_height:
            return font, lines, leading
    font = get_font(min_size)
    return font, wrap_text(draw, text, font, max_width), int(min_size * 1.35)


def draw_text_box(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    font_size: int,
    align: str = "center",
) -> None:
    """在预留文字区绘制中文，保留原图气泡和便签底色。"""
    x1, y1, x2, y2 = box
    padding_x = 18
    padding_y = 14
    inner_box = (x1 + padding_x, y1 + padding_y, x2 - padding_x, y2 - padding_y)
    font, lines, leading = fit_font(draw, text, inner_box, font_size)

    total_height = len(lines) * leading
    y = inner_box[1] + max(0, (inner_box[3] - inner_box[1] - total_height) // 2)
    color = (58, 42, 30)
    stroke = (255, 250, 240)

    for line in lines:
        line_width = text_width(draw, line, font)
        if align == "left":
            x = inner_box[0]
        else:
            x = inner_box[0] + max(0, (inner_box[2] - inner_box[0] - line_width) // 2)
        draw.text((x, y), line, font=font, fill=color, stroke_width=2, stroke_fill=stroke)
        y += leading


PAGE_TEXTS = {
    1: [
        ((120, 90, 585, 320), "晚饭时间到了，\n小北斗忽然挺直小背。", 30, "center"),
        ((55, 455, 300, 585), "今天，我要\n独立自主吃饭！", 26, "center"),
        ((615, 820, 885, 965), "好呀，妈妈坐旁边看你。", 26, "center"),
    ],
    2: [
        ((160, 55, 785, 290), "小北斗把小勺子\n举得高高的。", 34, "center"),
        ((130, 360, 485, 515), "饭饭小铲车，\n准备出发！", 30, "center"),
        ((615, 705, 880, 915), "报告，餐桌站长\n已到位。", 28, "center"),
    ],
    3: [
        ((55, 55, 640, 245), "米饭站一队，青菜站一队，\n胡萝卜也站一队。", 30, "center"),
        ((35, 430, 265, 565), "不要挤，\n一个一个\n上车。", 22, "center"),
        ((700, 805, 895, 945), "原来吃饭\n还要排队呀。", 22, "center"),
    ],
}


def render_page(page: int, variant: str = "v1") -> Path:
    """渲染单页预览图。"""
    sources = SOURCE_IMAGES_V2 if variant == "v2" else SOURCE_IMAGES
    suffix = "_v2" if variant == "v2" else ""
    source = sources[page]
    if not source.exists():
        raise FileNotFoundError(f"缺少底图：{source}")

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    base_path = IMAGE_DIR / f"page_{page:02d}{suffix}_base.png"
    output_path = IMAGE_DIR / f"page_{page:02d}{suffix}.png"
    copy2(source, base_path)

    with Image.open(source).convert("RGB") as image:
        draw = ImageDraw.Draw(image)
        for box, text, font_size, align in PAGE_TEXTS[page]:
            draw_text_box(draw, text, box, font_size, align)
        image.save(output_path, quality=95)

    return output_path


def main() -> None:
    variant = sys.argv[1] if len(sys.argv) > 1 else "v1"
    if variant not in {"v1", "v2"}:
        raise ValueError("只支持 v1 或 v2")
    for page in (1, 2, 3):
        print(render_page(page, variant))


if __name__ == "__main__":
    main()
