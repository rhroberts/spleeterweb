import tempfile

from scipy.io import wavfile

from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter

def split(input_file, sample_rate=44100, model="2stems"):
    if model.lower() not in ["2stems", "4stems", "5stems"]:
        print(f"Invalid model: '{model}'. Using '2stems' model instead.")
        model = "2stems"
    separator = Separator(f"spleeter:{model}")
    audio_loader = AudioAdapter.default()
    waveform, _ = audio_loader.load(input_file.name, sample_rate=sample_rate)
    # prediction output is a dictionary whose keys contain instrument/stem names
    # and values the associated waveforms
    prediction = separator.separate(waveform, "_")
    return(prediction)
