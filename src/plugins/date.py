import datetime
import locale
from PIL import ImageDraw, ImageFont

font0 = ImageFont.truetype("msgothic.ttc", 64)
font = ImageFont.truetype("msgothic.ttc", 256)

# https://log.mkuriki.com/raspberrypi_locale_japanese/
locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")


def main(img, option):
    jpw_list = ["月", "火", "水", "木", "金", "土", "日"]

    dt_now = datetime.datetime.now()

    # 日本語の曜日表示に対応させる
    date_str = option["format"].replace("%jpw", jpw_list[dt_now.weekday()])

    # Windows上のPythonのdatetime.strftimeで日本語を使うとエラーになる?
    # https://ja.stackoverflow.com/questions/44597/windows%E4%B8%8A%E3%81%AEpython%E3%81%AEdatetime-strftime%E3%81%A7%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%82%92%E4%BD%BF%E3%81%86%E3%81%A8%E3%82%A8%E3%83%A9%E3%83%BC%E3%81%AB%E3%81%AA%E3%82%8B
    date_str = (
        dt_now.strftime(date_str.encode("unicode-escape").decode())
        .encode()
        .decode("unicode-escape")
    )

    draw = ImageDraw.Draw(img)
    draw.text(
        (0, 0),
        date_str,
        "black",
        anchor="lt",
        font=ImageFont.truetype("msgothic.ttc", option["fontsize"]),
    )

    return img
