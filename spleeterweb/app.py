import os
import tempfile
from scipy.io import wavfile
from flask import Flask, send_from_directory, request, render_template
from werkzeug.utils import secure_filename

from spleeterweb import spleeter, utils

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
            # first, remove any old tmp directories
            # shouldn't be handled by the app in prod, but convenient for debugging
            # w/o accumulating several GBs of wav files
            if app.config["ENV"] == "development":
                utils.remove_temp_dirs(
                    app.config["OUTPUT_DIR"], app.config["REMOVE_DIR_AGE"]
                )
            model = request.form["model"]
            sample_rate = int(request.form["sample_rate"])
            if "input_file" in request.files:
                buffer = request.files["input_file"]
                with tempfile.NamedTemporaryFile(dir=app.config["INPUT_DIR"]) as f:
                    buffer.save(f)
                    prediction = spleeter.split(f, sample_rate, model)
                output_paths = {}
                output_subdir = tempfile.mkdtemp(dir=app.config["OUTPUT_DIR"])
                for stem in prediction:
                    stem_file = f"{stem}.wav"
                    stem_path = os.path.join(output_subdir, stem_file)
                    with open(stem_path, "w") as f:
                        wavfile.write(f.name, sample_rate, prediction[stem])
                        output_paths[stem_file] = (os.path.basename(output_subdir), stem_file)
            else:
                print("no `input_file` id found")
            return render_template("index.html", output=output_paths)
        else:
            return render_template("index.html")

    @app.route("/output/<temp_dir>/<stemfile>", methods=["GET", "POST"])
    def output(temp_dir, stemfile):
        return send_from_directory(
            os.path.join(app.config["OUTPUT_DIR"], temp_dir),
            stemfile, as_attachment=False, mimetype="audio/wav"
        )

    return app
