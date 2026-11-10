"""Build approximate caption cues and SRT from timing.py words.json."""
import argparse
import json
import math
from pathlib import Path

def cues_from_words(words, duration):
    if not words or not math.isfinite(duration) or duration<=0:
        raise ValueError('Supply nonempty words and a positive audio duration')
    cues=[]; chunk=[]; previous=0
    def flush():
        if chunk:
            cues.append({'s':chunk[0]['s'],'e':chunk[-1]['e'],
                         'text':' '.join(w['w'] for w in chunk)})
            chunk.clear()
    for word in words:
        s,e=word['s'],word['e']; text=word['w'].strip()
        if not text or not all(math.isfinite(v) for v in (s,e)) or not (previous<=s<e<=duration):
            raise ValueError('Invalid, overlapping or out-of-duration word timestamps')
        if chunk and (len(chunk)>=5 or len(' '.join(w['w'] for w in chunk))+len(text)>44
                      or s-chunk[-1]['e']>.35): flush()
        chunk.append({'w':text,'s':s,'e':e});previous=e
        if text.endswith(('.', '?', '!', ';')): flush()
    flush()
    return cues

def timestamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('words',type=Path)
    parser.add_argument('--duration',required=True,type=float)
    parser.add_argument('--json',type=Path,default=Path('web/captions.json'))
    parser.add_argument('--srt',type=Path,default=Path('out/captions.srt'))
    args=parser.parse_args()
    if args.json.exists() or args.srt.exists(): parser.error('Caption output exists; choose new paths')
    cues=cues_from_words(json.loads(args.words.read_text(encoding='utf-8-sig')),args.duration)
    for path in (args.json,args.srt): path.parent.mkdir(parents=True,exist_ok=True)
    args.json.write_text(json.dumps({'source':'approximate script alignment; verify against audio',
                                    'duration':args.duration,'cues':cues},indent=2),encoding='utf-8')
    args.srt.write_text('\n\n'.join(f"{i+1}\n{timestamp(c['s'])} --> {timestamp(c['e'])}\n{c['text']}"
                                  for i,c in enumerate(cues))+'\n',encoding='utf-8')
    print(f'{len(cues)} approximate cues; {args.json}; {args.srt}')

if __name__=='__main__': main()
