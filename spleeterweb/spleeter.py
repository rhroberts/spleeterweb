from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter

def split(input_file, model, sample_rate=44100):
    if model.lower() not in ["2stems", "4stems", "5stems"]:
        print(f"Invalid model: {model}. Using 2stem model instead.")
        model = "2stems"
    separator = Separator(f"spleeter:{model}")
    audio_loader = AudioAdapter.default()
    # load takes a filepath i think.. not buffer..
    waveform, _ = audio_loader.load(input_file, sample_rate=sample_rate)
    # from spleeter api docs:
    #   prediction output is a dictionary whose keys contain the name of the
    #   instruments, and values the associated instrument separated waveforms. For
    #   instance, using 2stems model, the returned dictionary would have two keys
    #   vocals and accompaniment with corresponding numpy arrays waveforms as value.
    prediction = separator.separate(waveform)
    return(prediction.keys())
