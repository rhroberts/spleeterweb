import tempfile

from scipy.io import wavfile

from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter

def split(input_file, sample_rate=44100, model="2stems"):
    if model.lower() not in ["2stems", "4stems", "5stems"]:
        print(f"Invalid model: {model}. Using 2stem model instead.")
        model = "2stems"
    separator = Separator(f"spleeter:{model}")
    audio_loader = AudioAdapter.default()
    with tempfile.NamedTemporaryFile() as f:
        input_file.save(f)
        # load requires a path-like obj, not buffer..
        waveform, _ = audio_loader.load(f.name, sample_rate=sample_rate)
    # prediction output is a dictionary whose keys contain instrument/stem names
    # and values the associated waveforms
    prediction = separator.separate(waveform, "dummy_descriptor")
    return(prediction)
