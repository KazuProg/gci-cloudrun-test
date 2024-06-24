from PIL import ImageDraw, ImageFont
from datetime import date, datetime

font0 = ImageFont.truetype("msgothic.ttc", 64)


def main(img, option):
    draw = ImageDraw.Draw(img)
    dt_now = datetime.now()
    today = dt_now.date()
    days = (today - date(year=2000, month=1, day=1)).days
    draw_str3 = "幸希のパジャマ洗濯日" if (days % 2 == 0) else "一希のパジャマ洗濯日"
    draw_str4 = "風呂：おそうじ" if (days % 2 == 0) else "風呂：おいだき"

    draw.text((400, 60), draw_str3, "black", anchor="mb", font=font0)
    draw.text((400, 120), draw_str4, "black", anchor="mb", font=font0)

    return img
