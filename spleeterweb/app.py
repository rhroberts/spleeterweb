import os

from flask import Flask, send_file, request, render_template
from werkzeug.utils import secure_filename

from spleeterweb import spleeter

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object("spleeterweb.config")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/", methods=["GET", "POST"])
    def application_root():
        result = None
        if request.method == "POST":
            print(request.form)
            if "input_file" in request.files:
                input_file = request.files["input_file"]
                result = spleeter.split(input_file, "2stem")
            else:
                print("no `input_file` id found")
        return render_template("index.html", output=result)

    return app
