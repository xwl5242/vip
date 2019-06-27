# -*- coding:utf-8 -*-
from flask import Flask, render_template, jsonify
from dao import DB, Config
# name, static resource path, templates resource path
app = Flask("yo_vip_tv", static_folder="static", template_folder="templates")


@app.route('/')
def index():
    return render_template('index.html', news=DB.query_index_news(), mvs=DB.query_index_mvs(Config.MV),
                           dsjs=DB.query_index_mvs(Config.DSJ), dms=DB.query_index_mvs(Config.DM),
                           zys=DB.query_index_mvs(Config.ZY))


@app.route('/tv')
def tv():
    return render_template('tv/tv.html')


@app.route('/news')
def news():
    return jsonify(DB.query_index_news())


if __name__ == '__main__':
    # DEBUG RUN
    app.run(port=80, debug=True)

