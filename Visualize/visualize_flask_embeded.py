from flask import Flask, jsonify, request, render_template, send_from_directory

from pyecharts.globals import CurrentConfig, NotebookType
from pyecharts.charts import *
from pyecharts import options as opts

from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB


def create_bar_chart():
    bar = (
        Bar()
        .add_xaxis(["A", "B", "C", "D"])
        .add_yaxis("Series 1", [10, 20, 30, 40])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar Chart"))
    )
    html_content = bar.render_embed()

    # 使用BeautifulSoup解析HTML并提取<div>内容
    soup = bs(html_content, "html.parser")
    body_soup = soup.find("body")
    div_content = body_soup.find("div")
    script_content = body_soup.find("script")
    return str(div_content), str(script_content)


create_bar_chart()


@app.route("/")
def index():
    # 获取所有HTML文件的路径
    return render_template("show_charts_embed.html", comps=create_bar_chart())


if __name__ == "__main__":
    app.run(debug=True)
