#! /usr/bin/env python3
# _*_ coding: utf-8 _*_

from config import configs
from flask import Flask
from api import api, img_api


app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(img_api)
app.run(host=configs.server.host, port=configs.server.port)
