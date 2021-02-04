from flask import Blueprint

from spleeterweb.spleeter import split

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/split/<file>/<sample_rate>/<model>", methods=["POST"])
def spleet_file(file, sample_rate, model):
    prediction = split(file, sample_rate, model)
