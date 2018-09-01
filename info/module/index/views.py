from info.module.index import index_bp
from flask import render_template


@index_bp.route("/")
def index():

    return render_template("index.html")
