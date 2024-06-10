import torch
import sounddevice as sd
import time
import inflect

language = 'ua'
model_id = 'v3_ua'
sample_rate = 48000
speaker = 'mykyta'#baya
put_accent = True
put_yo = True
device = torch.device('cpu')

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)

p = inflect.engine()

# Default volume level
volume_level = 1.0

def va_speak(what: str):
    audio = model.apply_tts(text=textify_numbers(what),
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    audio = adjust_volume(audio, volume_level)

    sd.play(audio.squeeze().numpy(), sample_rate * 1.05)
    sd.wait()
    time.sleep((len(audio) / sample_rate) + 0.5)
    sd.stop()

def textify_numbers(text: str) -> str:
    words = text.split()
    for i, word in enumerate(words):
        if word.isdigit():
            words[i] = p.number_to_words(word)
    return ' '.join(words)

def set_volume(level: int):
    global volume_level
    volume_level = level / 50.0  # Convert to a scale of 0.0 to 1.0

def adjust_volume(audio, level):
    return audio * level