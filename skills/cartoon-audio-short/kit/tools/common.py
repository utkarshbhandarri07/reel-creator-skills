"""Checked local media operations shared by the Reel tools."""
import json
import subprocess
from pathlib import Path
import numpy as np

SR = 48000

def run(args, **kwargs):
    return subprocess.run([str(a) for a in args], check=True, **kwargs)

def decode(path):
    raw = run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', SR,
               '-f', 'f32le', '-'], capture_output=True).stdout
    audio = np.frombuffer(raw, dtype='<f4').copy()
    if not len(audio) or not np.isfinite(audio).all():
        raise ValueError('Audio is empty or contains non-finite samples')
    return audio

def write_audio(path, audio):
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', SR, '-ac', '1',
         '-i', '-', '-c:a', 'pcm_f32le', path], input=np.asarray(audio, dtype='<f4').tobytes(), capture_output=True)

def gated_rms(audio):
    # Amplitude metric: 50 ms blocks, -80 dBFS absolute gate, then -40 dB relative gate.
    size = SR // 20
    powers = np.array([float(np.mean(np.square(audio[i:i+size].astype(np.float64))))
                       for i in range(0, len(audio), size)])
    active = powers[powers > max(1e-8, float(powers.max(initial=0)) * 1e-4)]
    return float(np.sqrt(active.mean())) if len(active) else 0.0

def fit(audio, count):
    result = np.zeros(count, dtype=np.float32)
    result[:min(count, len(audio))] = audio[:count]
    return result

def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False)+'\n', encoding='utf-8')
