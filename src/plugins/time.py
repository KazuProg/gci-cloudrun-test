import datetime
from PIL import ImageDraw, ImageFont


def main(img, option):
    w, h = img.size

    dt_now = datetime.datetime.now()
    dt_str = dt_now.strftime(option["format"])

    draw = ImageDraw.Draw(img)
    draw.text(
        (w / 2, h / 2),
        dt_str,
        "black",
        anchor="mm",
        font=ImageFont.truetype("msgothic.ttc", option["fontsize"]),
    )

    return img
