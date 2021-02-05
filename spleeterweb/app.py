import os
import tempfile
from scipy.io import wavfile
from flask import Flask, send_from_directory, request, render_template
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

    @app.route("/", methods=["GET", "POST"])
    def application_root():
        if request.method == "POST":
            model = request.form["model"]
            sample_rate = int(request.form["sample_rate"])
            output_paths = {"vocals": 10, "piano": 12}
            if "input_file" in request.files:
                buffer = request.files["input_file"]
                with tempfile.NamedTemporaryFile(dir=app.config["INPUT_DIR"]) as f:
                    buffer.save(f)
                    prediction = spleeter.split(f, sample_rate, model)
                output_paths = {}
                for stem in prediction:
                    with tempfile.NamedTemporaryFile(
                        dir=app.config["OUTPUT_DIR"], delete=False
                    ) as f:
                        wavfile.write(f.name, sample_rate, prediction[stem])
                        output_paths[stem] = os.path.basename(f.name)
            else:
                print("no `input_file` id found")
            return render_template("index.html", output=output_paths)
        else:
            return render_template("index.html")

    @app.route("/output/<stemfile>", methods=["GET", "POST"])
    def output(stemfile):
        return send_from_directory(
            app.config["OUTPUT_DIR"], stemfile, as_attachment=False,
            mimetype="audio/wav"
        )

    return app
