from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)


@app.route("/api/data", methods=["GET"])
def get_data():
    # 模拟数据处理过程
    data = pd.DataFrame({"x": ["A", "B", "C", "D"], "y": [10, 20, 30, 40]})

    result = data.to_dict(orient="records")
    return jsonify(result)


# 设置图表文件夹路径
CHARTS_FOLDER = "templates/charts"


@app.route("/")
def index():
    # 获取所有HTML文件的路径
    chart_files = [f for f in os.listdir(CHARTS_FOLDER) if f.endswith(".html")]
    print(chart_files)
    return render_template("index.html", charts=chart_files)


@app.route("/charts/<filename>")
def get_chart(filename):
    return send_from_directory(CHARTS_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)
