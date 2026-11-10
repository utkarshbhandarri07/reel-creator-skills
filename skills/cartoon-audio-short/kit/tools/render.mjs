// node render.mjs <output-dir> <0-59 or 0,30,59>; RESUME=1 skips existing frames.
import { chromium } from 'playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { once } from 'node:events';

const [outdir, spec] = process.argv.slice(2);
if (!outdir || !spec) throw new Error('Usage: node render.mjs <output-dir> <frame-list>');
const frames=[];
for (const part of spec.split(',')) {
  if (!/^\d+(?:-\d+)?$/.test(part)) throw new Error(`Invalid frame range: ${part}`);
  const [a,b=a]=part.split('-').map(Number);
  if (b<a || b-a>100000 || !Number.isSafeInteger(b)) throw new Error('Invalid or excessive frame range');
  for(let f=a; f<=b; f++) frames.push(f);
}
const root=fs.realpathSync(path.resolve(process.env.WEB || 'web'));
// captions.py produces this file by default. CAPTIONS=none explicitly disables it.
const captionPath=process.env.CAPTIONS==='none'?null:(process.env.CAPTIONS || path.join(root,'captions.json'));
let captions=[];
if(captionPath && fs.existsSync(captionPath)) {
  const data=JSON.parse(fs.readFileSync(captionPath,'utf8'));
  captions=data.cues;
  let previous=0;
  if(!Array.isArray(captions)) throw new Error('Caption cues must be an array');
  for(const c of captions) {
    if(!Number.isFinite(c.s)||!Number.isFinite(c.e)||c.s<previous||c.e<=c.s||
       typeof c.text!=='string'||!c.text.trim()) throw new Error('Invalid caption cue');
    previous=c.e;
  }
} else if(process.env.CAPTIONS && captionPath) throw new Error('Requested caption file is missing');
fs.mkdirSync(outdir,{recursive:true});
const server=http.createServer((req,res)=>{
  if(req.url==='/favicon.ico') {res.writeHead(204);res.end();return;}
  try {
    const candidate=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
    const p=fs.realpathSync(candidate);
    const relative=path.relative(root,p);
    if(relative.startsWith('..') || path.isAbsolute(relative) || !fs.statSync(p).isFile()) {res.writeHead(403);res.end();return;}
    const mime=p.endsWith('.js')?'text/javascript':p.endsWith('.html')?'text/html':'application/octet-stream';
    res.writeHead(200,{'Content-Type':mime});fs.createReadStream(p).pipe(res);
  } catch {res.writeHead(404);res.end();}
});
let browser;
try {
  server.listen(0,'127.0.0.1'); await once(server,'listening');
  browser=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const page=await browser.newPage({viewport:{width:1080,height:1920}});
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error') errors.push(m.text());});
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'load'});
  await page.waitForFunction(()=>window.ready || window.err,null,{timeout:120000});
  const problem=await page.evaluate(()=>window.err);
  if(problem || errors.length) throw new Error(problem || errors.join('\n'));
  const total=await page.evaluate(()=>window.TOTAL);
  if(captions.some(c=>c.e>total/30+.02)) throw new Error('Caption outside video duration');
  if(frames.some(f=>f>=total)) throw new Error(`Frame outside story duration (${total} frames)`);
  const started=Date.now();
  for(const [i,f] of frames.entries()) {
    const dest=path.join(outdir,`f${String(f).padStart(4,'0')}.jpg`);
    if(process.env.RESUME==='1' && fs.existsSync(dest)) continue;
    const data=await page.evaluate(({f,captions})=>{
      window.renderFrame(f);
      const original=document.getElementById('c');
      if(!captions.length) return original.toDataURL('image/jpeg',0.96);
      const output=window.__captionCanvas || (window.__captionCanvas=document.createElement('canvas'));
      output.width=1080;output.height=1920;
      const g=output.getContext('2d');g.drawImage(original,0,0);
      const cue=captions.find(c=>f/30>=c.s&&f/30<c.e);
      if(cue) {
        let lines=[],size=42;
        for(;size>=16;size--) {
          g.font=`700 ${size}px Arial`;lines=[];let row='';
          for(const word of cue.text.split(/\s+/)) {
            const next=row?row+' '+word:word;
            if(row&&g.measureText(next).width>760){lines.push(row);row=word;}else row=next;
          }
          if(row) lines.push(row);
          if(lines.length<=2&&lines.every(l=>g.measureText(l).width<=760)) break;
        }
        if(lines.length>2||lines.some(l=>g.measureText(l).width>760)) throw new Error('Caption too long; split its cue');
        g.fillStyle='#30263e';g.beginPath();g.roundRect(95,1470,820,158,24);g.fill();
        g.fillStyle='#fff8eb';g.textAlign='center';g.textBaseline='middle';
        lines.forEach((line,i)=>g.fillText(line,505,1549+(i-(lines.length-1)/2)*(size+10)));
      }
      return output.toDataURL('image/jpeg',0.96);
    },{f,captions});
    if(errors.length) throw new Error(errors.join('\n'));
    const temporary=dest+'.tmp';
    fs.writeFileSync(temporary,Buffer.from(data.split(',')[1],'base64')); fs.renameSync(temporary,dest);
    console.log(`frame ${f}; ${i+1}/${frames.length}; elapsed ${((Date.now()-started)/1000).toFixed(1)}s`);
  }
} finally {
  if(browser) await browser.close();
  server.close();
}
