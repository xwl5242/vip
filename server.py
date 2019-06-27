# -*- coding:utf-8 -*-
from flask import Flask, render_template, jsonify
from dao import DB
# name, static resource path, templates resource path
app = Flask("yo_vip_tv", static_folder="static", template_folder="templates")


@app.route('/')
def index():
    return render_template('index.html', news=DB.query_news())


@app.route('/tv')
def tv():
    return render_template('tv/tv.html')


@app.route('/news')
def news():
    return jsonify(DB.query_news())


if __name__ == '__main__':
    # DEBUG RUN
    app.run(port=80, debug=True)

