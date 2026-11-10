"""Encode contiguous rendered frames and a narration-length mix, then report QA."""
import argparse
import json
import math
import re
from pathlib import Path
from common import decode, run, save_json, SR

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--frames', type=Path, default=Path('frames'))
    parser.add_argument('--mix', type=Path, default=Path('mix_raw.wav'))
    parser.add_argument('--voice', type=Path, required=True)
    args=parser.parse_args()
    if args.output.exists(): parser.error('Output exists; choose a new output name')
    voice=decode(args.voice); audio=decode(args.mix)
    if len(audio)!=len(voice): parser.error('Mix duration differs from narration; rerun mix.py')
    duration=len(voice)/SR; count=round(duration*30)
    if count<1: parser.error('Narration is shorter than one video frame')
    missing=[i for i in range(count) if not (args.frames/f'f{i:04d}.jpg').is_file()]
    if missing: parser.error(f'Missing frames (first ten): {missing[:10]}')
    measured=run(['ffmpeg','-hide_banner','-i',args.mix,'-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    blocks=re.findall(r'\{[^{}]*"input_i"[^{}]*\}',measured,re.S)
    if not blocks: raise ValueError('Unable to measure mix loudness')
    levels=json.loads(blocks[-1]); loudness=float(levels['input_i']); tp=float(levels['input_tp'])
    if not math.isfinite(loudness) or not math.isfinite(tp): raise ValueError('Mix loudness is not measurable')
    desired=-14-loudness
    # Keep headroom with one common linear gain rather than compressing narration.
    gain_db=min(desired,-1.5-tp)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-v','error','-nostdin','-framerate','30','-i',args.frames/'f%04d.jpg','-i',args.mix,
         '-map','0:v:0','-map','1:a:0','-frames:v',count,'-af',f'volume={gain_db:.8f}dB',
         '-vf','scale=in_range=pc:out_range=tv,format=yuv420p','-color_range','tv',
         '-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','192k','-movflags','+faststart',args.output],capture_output=True)
    probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',args.output],capture_output=True,text=True).stdout)
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    sound=next(s for s in probe['streams'] if s['codec_type']=='audio')
    valid=(video['width']==1080 and video['height']==1920 and video['r_frame_rate']=='30/1'
           and video['codec_name']=='h264' and video['pix_fmt']=='yuv420p'
           and video.get('color_range')=='tv' and sound['codec_name']=='aac'
           and abs(float(probe['format']['duration'])-duration)<=1/30+0.002)
    scan=run(['ffmpeg','-hide_banner','-i',args.output,'-vf','freezedetect=n=0.0005:d=0.4,blackdetect=d=0.05','-an','-f','null','-'],capture_output=True,text=True).stderr
    concerns=[line for line in scan.splitlines() if 'freeze_start' in line or 'black_start' in line]
    final_measure=run(['ffmpeg','-hide_banner','-i',args.output,'-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    final_levels=json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}',final_measure,re.S)[-1])
    qa_image=args.output.with_suffix('.qa.jpg')
    tiles=max(1,min(40,math.ceil(duration*2)))
    columns=min(10,tiles); rows=math.ceil(tiles/columns)
    # Select explicit evenly spaced frames, including the first and last.
    indices=sorted(set(round(i*(count-1)/max(1,tiles-1)) for i in range(tiles)))
    selection='+'.join(f'eq(n,{i})' for i in indices)
    run(['ffmpeg','-v','error','-y','-i',args.output,'-vf',
         f"select='{selection}',scale=180:-1,tile={columns}x{rows}",'-frames:v','1',qa_image],capture_output=True)
    report={'technical_pass':valid,'voice_duration':duration,'frames':count,'format_duration':float(probe['format']['duration']),
            'common_gain_db':gain_db,'peak_constrained':gain_db<desired,'limiting_applied':False,
            'review_frames':indices,'pixel_format':video['pix_fmt'],'color_range':video.get('color_range'),
            'loudness_before':levels,'loudness_after':final_levels,'qa_concerns':concerns,
            'full_playback_review':'not performed by this script','contact_sheet':str(qa_image.resolve())}
    save_json(args.output.with_suffix('.qa.json'),report)
    print(json.dumps(report,indent=2))
    if not valid: raise SystemExit('Encoded output failed technical validation')

if __name__=='__main__': main()
