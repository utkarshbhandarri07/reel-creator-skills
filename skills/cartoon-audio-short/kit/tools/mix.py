"""Mix narration with constant music/SFX gains; no ducking or compression."""
import argparse
import math
import numpy as np
from common import decode, fit, gated_rms, write_audio, save_json, SR

def build_mix(voice, music, sfx, music_level=0.25, sfx_level=0.25, sfx_peak_ratio=0.35):
    if any(not math.isfinite(v) or v < 0 for v in (music_level,sfx_level,sfx_peak_ratio)):
        raise ValueError('Stem levels and peak ratio must be finite and nonnegative')
    vr = gated_rms(voice)
    if vr == 0: raise ValueError('Narration has no measurable non-silent signal')
    music, sfx = fit(music, len(voice)), fit(sfx, len(voice))
    mr, sr = gated_rms(music), gated_rms(sfx)
    mg = music_level * vr / mr if mr else 0.0
    sg = sfx_level * vr / sr if sr else 0.0
    vp, sp = float(np.max(np.abs(voice))), float(np.max(np.abs(sfx)))
    if sp: sg = min(sg, sfx_peak_ratio * vp / sp)
    mixed = voice + music * mg + sfx * sg
    ratio = lambda value: 20 * math.log10(value / vr) if value else None
    return mixed, {
        'sample_rate': SR, 'samples': len(voice), 'duration': len(voice)/SR,
        'voice_gated_rms': vr, 'music_gain': mg, 'sfx_gain': sg,
        'music_db_vs_voice': ratio(gated_rms(music * mg)),
        'sfx_db_vs_voice': ratio(gated_rms(sfx * sg)),
        'sfx_peak_vs_voice_peak': float(np.max(np.abs(sfx * sg))) / vp,
        'raw_peak': float(np.max(np.abs(mixed))),
        'voice_retimed': False, 'ducking': False, 'compression': False,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('voice'); parser.add_argument('music'); parser.add_argument('sfx')
    parser.add_argument('--out', default='mix_raw.wav')
    parser.add_argument('--music-level', type=float, default=0.25, help='Gated RMS relative to narration')
    parser.add_argument('--sfx-level', type=float, default=0.25)
    parser.add_argument('--sfx-peak-ratio', type=float, default=0.35)
    parser.add_argument('--no-music', action='store_true')
    parser.add_argument('--no-sfx', action='store_true')
    args = parser.parse_args()
    voice=decode(args.voice)
    mixed, report = build_mix(voice,
        np.zeros(1) if args.no_music else decode(args.music),
        np.zeros(1) if args.no_sfx else decode(args.sfx),
        0 if args.no_music else args.music_level,
        0 if args.no_sfx else args.sfx_level, args.sfx_peak_ratio)
    write_audio(args.out, mixed)
    save_json(str(args.out)+'.json', report)
    print(report)

if __name__ == '__main__': main()
