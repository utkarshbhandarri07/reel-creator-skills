"""Change existing background stem gains without changing narration gain or video."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from common import decode, fit, write_audio, run, save_json, SR

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--voice',required=True,type=Path)
    parser.add_argument('--music',type=Path,default=Path('music.wav'))
    parser.add_argument('--sfx',type=Path,default=Path('sfx.wav'))
    parser.add_argument('--mix-report',required=True,type=Path)
    parser.add_argument('--qa',type=Path,help='Previous finish/remix QA; defaults beside input video')
    parser.add_argument('--music-multiplier',type=float,default=.5)
    parser.add_argument('--sfx-multiplier',type=float,default=.5)
    args=parser.parse_args()
    if any(not math.isfinite(v) or v<0 for v in (args.music_multiplier,args.sfx_multiplier)):
        parser.error('Multipliers must be finite and nonnegative')
    mix_path=args.output.with_suffix('.mix.wav')
    report_path=args.output.with_suffix('.mix.json')
    qa_path=args.output.with_suffix('.qa.json')
    if any(p.exists() for p in (args.output,mix_path,report_path,qa_path)):
        parser.error('Output exists; choose a new version name')
    previous=json.loads(args.mix_report.read_text())
    qa=json.loads((args.qa or args.video.with_suffix('.qa.json')).read_text())
    voice=decode(args.voice)
    if abs(len(voice)/SR-previous['duration'])>1/SR: parser.error('Narration duration differs from previous mix')
    def stem(path,gain):
        return fit(decode(path),len(voice))*gain if gain else np.zeros_like(voice)
    mg=previous['music_gain']*args.music_multiplier
    sg=previous['sfx_gain']*args.sfx_multiplier
    mixed=voice+stem(args.music,mg)+stem(args.sfx,sg)
    gain=qa['common_gain_db']
    if not math.isfinite(gain): parser.error('Previous narration gain is invalid')
    # Refuse clipping rather than silently changing the retained narration gain.
    if np.max(np.abs(mixed))*10**(gain/20)>=.99: parser.error('Mix would clip; choose lower background gains')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    write_audio(mix_path,mixed)
    run(['ffmpeg','-v','error','-nostdin','-i',args.video,'-i',mix_path,
         '-map','0:v:0','-map','1:a:0','-c:v','copy','-af',f'volume={gain:.8f}dB',
         '-c:a','aac','-b:a','192k','-movflags','+faststart',args.output],capture_output=True)
    def video_hash(path):
        return run(['ffmpeg','-v','error','-i',path,'-map','0:v:0','-c','copy',
                    '-f','hash','-hash','sha256','-'],capture_output=True,text=True).stdout.strip()
    same=video_hash(args.video)==video_hash(args.output)
    probe=json.loads(run(['ffprobe','-v','error','-show_format','-of','json',args.output],capture_output=True,text=True).stdout)
    duration=float(probe['format']['duration'])
    run(['ffmpeg','-v','error','-i',args.output,'-f','null','-'],capture_output=True)
    valid=same and abs(duration-len(voice)/SR)<=1/30+.002
    save_json(report_path,{'duration':len(voice)/SR,'music_gain':mg,'sfx_gain':sg,
                          'source_mix_report':str(args.mix_report.resolve())})
    save_json(qa_path,{'technical_pass':valid,'common_gain_db':gain,
        'narration_gain_changed':False,'video_stream_identical':same,'format_duration':duration,
        'music_multiplier':args.music_multiplier,'sfx_multiplier':args.sfx_multiplier,
        'mix_report':str(report_path.resolve()),'full_playback_review':'not performed'})
    if not valid: raise SystemExit('Remix failed technical validation; inspect QA report')
    print(args.output.resolve())

if __name__=='__main__': main()
