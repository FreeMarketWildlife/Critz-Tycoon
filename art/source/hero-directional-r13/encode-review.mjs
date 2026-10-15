import fs from 'node:fs';
import {validateProject,gifBytes} from '../../../sprite-editor/model.js';
// Walk actual GIF blocks, never byte-search through compressed image data.
function retime(bytes,ms){
 const b=Buffer.from(bytes);let p=13,count=0;
 if(b[10]&128)p+=3*(1<<((b[10]&7)+1));
 const subblocks=()=>{while(b[p]){p+=1+b[p];}p++;};
 while(p<b.length){
  const tag=b[p];if(tag===0x3b)break;
  if(tag===0x21){
   if(b[p+1]===0xf9){if(b[p+2]!==4)throw Error('GCE size');b.writeUInt16LE(ms/10,p+4);count++;}
   p+=2;subblocks();
  }else if(tag===0x2c){const packed=b[p+9];p+=10;if(packed&128)p+=3*(1<<((packed&7)+1));p++;subblocks();}
  else throw Error(`Unexpected GIF block ${tag} at ${p}`);
 }
 if(count!==8)throw Error(`Expected 8 GCEs, got ${count}`);
 return b;
}
const jobs=JSON.parse(fs.readFileSync(process.argv[2]));
const report={tool:'Actual Sprite Editor validateProject/gifBytes',previews:[],editable:[]};
for(const job of jobs){
 const native=validateProject(JSON.parse(fs.readFileSync(job.project)));let project=native;
 if(job.deriveNearestScale===4){
  project={...native,width:native.width*4,height:native.height*4,frames:native.frames.map(frame=>{
   const pixels=[];for(let y=0;y<native.height;y++){const row=[];for(let x=0;x<native.width;x++){const v=frame.pixels[y*native.width+x];row.push(v,v,v,v);}for(let n=0;n<4;n++)pixels.push(...row);}return {...frame,pixels};})};
  if(project.width!==896||project.height!==768)throw Error('Unexpected combined review expansion');
 }
 let bytes=gifBytes(project);if(job.delayMs===400)bytes=retime(bytes,400);fs.writeFileSync(job.output,bytes);
 report.previews.push({output:job.output,width:project.width,height:project.height,frames:project.frames.length,delayMs:job.delayMs??100,nativeProjectValidated:true,derivedNearestScale:job.deriveNearestScale??1,editorCanvasNote:job.deriveNearestScale?'Export-only expansion from validated224x192 native panel; not an oversized editable Sprite Editor project':null});
}
for(const kind of ['hero','dummy']){for(const view of ['idles','south-walk','north-walk','west-walk','east-walk']){const name=kind+'-'+view;const p=validateProject(JSON.parse(fs.readFileSync(new URL(name+'.sprite.json',import.meta.url))));report.editable.push({name,width:p.width,height:p.height,frames:p.frames.length,validated:true});}}
fs.writeFileSync(new URL('../../../docs/reviews/M1-HR13/editor-validation.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
console.log('Validated '+report.previews.length+' preview projects and '+report.editable.length+' editable projects.');
