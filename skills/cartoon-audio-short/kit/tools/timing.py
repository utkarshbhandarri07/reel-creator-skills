#!/usr/bin/env python3
"""Word timings for a voiceover -> words.json + phrases.json.

Usage:
  python timing.py voice.mp3 script.txt [--out work/]

1. Uses supplied script text and detects speech segments by silence (ffmpeg silencedetect),
   splits the script into phrases at punctuation, and aligns phrases to segments with a DP that
   matches phrase length (syllables) to segment duration. Words inside a phrase are spread by syllables.
2. Optional --asr-model uses an existing local faster-whisper model; no automatic model download.
Always check phrases.json against the audio; this is approximate alignment.
"""
import json, re, subprocess, sys, os

def syll(w):
    if w.isdigit(): return 2
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w: return 1
    v = re.findall(r"[aeiouy]+", w); n = len(v)
    if w.endswith("e") and n > 1 and not w.endswith("le"): n -= 1
    return max(1, n)

def num_words(text):  # "30" spoken as "thirty" -> 2 syllables handled by isdigit
    return text

def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True, check=True).stdout)

def speech_segments(path, db=-35, mind=0.12):
    err = subprocess.run(["ffmpeg", "-i", path, "-af", f"silencedetect=n={db}dB:d={mind}", "-f", "null", "-"], capture_output=True, text=True, check=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    D = duration(path); segs = []; cur = 0.0
    for s, e in zip(starts, ends + [D] * (len(starts) - len(ends))):
        if s - cur > 0.08: segs.append([cur, s])
        cur = e
    if D - cur > 0.08: segs.append([cur, D])
    # trim leading silence of first segment if file starts with silence
    return segs, D


def align(script, segs):
    # phrases: split after , . ; : ! ? and closing quotes
    raw = re.findall(r"[^,.;:!?]+[,.;:!?\"”']*", script.replace("\n", " "))
    phrases = [p.strip() for p in raw if p.strip()]
    P, S = len(phrases), len(segs)
    syl = [sum(syll(w) for w in p.split()) for p in phrases]
    tot_syl = sum(syl); tot_dur = sum(e - s for s, e in segs); rate = tot_syl / tot_dur
    import functools
    INF = 1e9
    # dp over (phrase i, segment j): segment j holds phrases [i..k); a phrase may also span several segments (merge)
    @functools.lru_cache(None)
    def best(i, j):
        if i == P and j == S: return (0.0, ())
        if i == P or j == S: return (INF, ())
        out = (INF, ())
        for k in range(i + 1, min(P, i + 4) + 1):          # 1-3 phrases into one segment
            for l in range(j + 1, min(S, j + 3) + 1):      # or one group across 1-2 segments
                if k - i > 1 and l - j > 1: continue
                d = segs[l - 1][1] - segs[j][0]; s_ = sum(syl[i:k]) / rate
                cost = (d - s_) ** 2 / max(d, 0.3)
                # a sentence end inside a segment is unlikely (speakers pause there); a long gap inside one phrase too
                cost += sum(0.35 for m in range(i, k - 1) if re.search(r"[.!?][\"”']?$", phrases[m]))
                cost += sum(1.5 * (segs[m + 1][0] - segs[m][1]) for m in range(j, l - 1))
                sub = best(k, l)
                if sub[0] + cost < out[0]: out = (sub[0] + cost, ((i, k, j, l),) + sub[1])
        return out
    cost, plan = best(0, 0)
    words, phr = [], []
    for i, k, j, l in plan:
        a, b = segs[j][0], segs[l - 1][1]
        text = " ".join(phrases[i:k]); ws = text.split(); sy = [syll(w) for w in ws]; T = sum(sy); t = a
        phr.append({"text": text, "s": round(a, 3), "e": round(b, 3)})
        for w, s_ in zip(ws, sy):
            d = (b - a) * s_ / T; words.append({"w": w, "s": round(t, 3), "e": round(t + d, 3)}); t += d
    return words, phr, cost

def main():
    import argparse
    from pathlib import Path
    from common import decode, gated_rms, SR, save_json
    parser = argparse.ArgumentParser(description='Approximate script timing without automatic ASR downloads')
    parser.add_argument('audio', type=Path)
    parser.add_argument('script', type=Path)
    parser.add_argument('--out', type=Path, default=Path('work'))
    parser.add_argument('--asr-model', type=Path, help='Optional existing local faster-whisper model folder')
    args = parser.parse_args()
    try:
        text = args.script.read_text(encoding='utf-8-sig').strip()
        if not text: raise ValueError('Script is empty; supply final narration text')
        audio = decode(args.audio)
        if gated_rms(audio)==0: raise ValueError('Audio contains no measurable speech signal')
        D=len(audio)/SR; words=None; cost=None
        if args.asr_model:
            if not args.asr_model.is_dir(): raise ValueError('ASR model must be an existing local folder')
            from faster_whisper import WhisperModel
            model=WhisperModel(str(args.asr_model),compute_type='int8',local_files_only=True)
            segments,_=model.transcribe(str(args.audio),word_timestamps=True)
            words=[{'w':w.word.strip(),'s':round(w.start,3),'e':round(w.end,3)} for segment in segments for w in segment.words]
            if not words: raise ValueError('ASR returned no words')
        segs,_=speech_segments(str(args.audio))
        if not segs: raise ValueError('No speech segments detected; inspect recording')
        if words:
            phrases=[]; current=[]
            for word in words:
                current.append(word)
                if re.search(r'[,.;:!?]$',word['w']):
                    phrases.append({'text':' '.join(w['w'] for w in current),'s':current[0]['s'],'e':current[-1]['e']}); current=[]
            if current: phrases.append({'text':' '.join(w['w'] for w in current),'s':current[0]['s'],'e':current[-1]['e']})
            source='local ASR; verify against supplied script'
        else:
            words,phrases,cost=align(text,segs)
            source='approximate silence/script alignment; not exact word timestamps'
            if not words or not phrases or cost>=1e9: raise ValueError('Alignment failed; inspect script and segments')
        if any(w['s']<0 or w['e']<=w['s'] or w['e']>D+0.02 for w in words): raise ValueError('Invalid word timing')
        args.out.mkdir(parents=True,exist_ok=True)
        save_json(args.out/'words.json',words)
        save_json(args.out/'phrases.json',{'duration':D,'frames30':round(D*30),'source':source,'alignment_cost':cost,'segments':segs,'phrases':phrases})
        print(f'{source}; duration={D:.3f}; frames={round(D*30)}')
    except (ValueError,OSError,subprocess.CalledProcessError) as exc:
        parser.exit(2,f'Timing failed: {exc}\n')

if __name__=='__main__': main()
