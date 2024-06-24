from PIL import ImageDraw, ImageFont


def main(img, option):
    draw = ImageDraw.Draw(img)
    draw.text(
        (0, 0),
        option["text"],
        "black",
        font=ImageFont.truetype("msgothic.ttc", option["fontsize"]),
    )

    return img
