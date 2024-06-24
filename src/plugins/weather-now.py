from PIL import Image, ImageDraw, ImageFont
import requests
from pprint import pprint
import io


def main(img, option):
    draw = ImageDraw.Draw(img)

    data = requests.get(
        "http://api.weatherapi.com/v1/forecast.json?key=6722e90d6a6c4cb2af9161908231212&q=Niigata-Shi&days=3&aqi=no&alerts=no"
    ).json()

    print()
    print("%s の天気を取得しました。" % (data["location"]["name"]))
    print()

    # 現在
    # http://api.weatherapi.com/v1/current.json?key=6722e90d6a6c4cb2af9161908231212&q=Niigata-Shi&aqi=no
    current = data["current"]
    pprint(current)
    print("現在の天気(%s)" % (current["last_updated"]))
    print("　天気： %s" % (current["condition"]["text"]))
    print("　気温： %4.1f 'C" % (current["temp_c"]))
    print("　湿度： %2d %%" % (current["humidity"]))
    print("　雲量： %2d %%" % (current["cloud"]))
    print()

    draw.text(
        (0, 0),
        "%sの現在\n天気：%s\n気温：%4.1f'C\n湿度：%d%%"
        % (
            data["location"]["name"],
            current["condition"]["text"],
            current["temp_c"],
            current["humidity"],
        ),
        "black",
        font=ImageFont.truetype("msgothic.ttc", 24),
    )

    # img.paste(weather_img, (0, 0))

    return img
