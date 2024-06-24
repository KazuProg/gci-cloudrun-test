# -*- coding: utf-8 -*-

import glob
import importlib
import io
import json
import os
import requests
import sys
import threading
import time
import wsgiref.simple_server

from datetime import datetime, timedelta

from PIL import Image

plugin_path = "plugins"
config_path = "config.json"

plugin = {}
config = None

LISTEN_PORT = os.getenv("PORT", 80)


def application(environ, start_response):
    if environ["PATH_INFO"] == "/":
        if environ["REQUEST_METHOD"] != "GET":
            start_response("405 Method Not Allowed", [])
            return create_body("Method Not Allowed")

        with open("./index.html", "r") as f:
            response = f.read()
            start_response("200 OK", [("Content-type", "text/html")])
            return create_body(response)

    if environ["PATH_INFO"] == "/e-paper.bmp":
        if environ["REQUEST_METHOD"] != "GET":
            start_response("405 Method Not Allowed", [])
            return create_body("Method Not Allowed")

        bmp = generate_image()
        start_response(
            "200 OK", [("Content-type", "image/bmp"), ("Cache-Control", "no-cache")]
        )
        return bmp

    if environ["PATH_INFO"] == "/load_config":
        if environ["REQUEST_METHOD"] != "GET":
            start_response("405 Method Not Allowed", [])
            return create_body("Method Not Allowed")

        load_config()
        start_response("200 OK", [])
        return create_body("Reload Configuration!")

    if environ["PATH_INFO"] == "/load_plugin":
        if environ["REQUEST_METHOD"] != "GET":
            start_response("405 Method Not Allowed", [])
            return create_body("Method Not Allowed")

        load_plugin()
        start_response("200 OK", [])
        return create_body("Reload Plugins!")

    start_response("404 Not Found", [])
    return create_body("Not Found")


def generate_image():
    image = Image.new("1", config["display"]["size"], 1)

    for part in config["parts"]:
        if part["type"] not in plugin:
            log("Not Found Plugin: %s" % (part["type"],))
            continue
        img = plugin[part["type"]].main(
            Image.new("1", (part["w"], part["h"]), 1), part["option"]
        )
        image.paste(img, (part["x"], part["y"]))

    output = io.BytesIO()
    image.save(output, format="BMP")
    return [output.getvalue()]


def load_plugin():
    global plugin
    plugin_files = glob.glob(plugin_path + "/*.py")
    plugin_names = list(
        map(lambda p: os.path.splitext(os.path.basename(p))[0], plugin_files)
    )

    # 消えたプラグインを削除(Err)
    for pname in list(plugin.keys()):
        if pname not in plugin_names:
            log(f"Plugin Del: {pname}")
            del plugin[pname]

    # プラグインの生成or再読み込み
    for pname in plugin_names:
        if pname in plugin:
            log(f"Plugin Rel: {pname}")
            importlib.reload(plugin[pname])
        else:
            log(f"Plugin Add: {pname}")
            plugin[pname] = importlib.import_module(plugin_path + "." + pname)


def load_config():
    global config
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        return False


def create_body(text):
    return [bytes(text, "utf-8")]


def dispatch_trigger():
    log("Dispatch Trigger")
    display_ip = config["display"]["ip"]

    if datetime.now().minute == 0:
        try:
            requests.get(f"http://{display_ip}/refresh", timeout=1)
            log("Sent Refresh Trigger")
        except requests.exceptions.RequestException as e:
            log(f"An error occurred: {e}")

    try:
        requests.get(f"http://{display_ip}/update", timeout=1)
        log("Sent Rewrite Trigger")
    except requests.exceptions.RequestException as e:
        log(f"An error occurred: {e}")


def sleep_until_next_minute():
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    time_difference = next_minute - now
    seconds_to_sleep = time_difference.total_seconds()
    time.sleep(seconds_to_sleep)


def log(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{current_time}: {message}")


def run_server():
    httpd = wsgiref.simple_server.make_server("", LISTEN_PORT, application)
    httpd.serve_forever()


if __name__ == "__main__":
    load_plugin()
    load_config()

    if config == False:
        print("Not found config file.")
        sys.exit(1)

    httpd_thread = threading.Thread(target=run_server)
    httpd_thread.start()

    while True:
        sleep_until_next_minute()
        dispatch_trigger()
