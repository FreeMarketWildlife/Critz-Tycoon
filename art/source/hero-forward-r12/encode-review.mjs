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
for(const job of jobs){const project=validateProject(JSON.parse(fs.readFileSync(job.project)));let bytes=gifBytes(project);if(job.delayMs===400)bytes=retime(bytes,400);fs.writeFileSync(job.output,bytes);report.previews.push({output:job.output,width:project.width,height:project.height,frames:project.frames.length,delayMs:job.delayMs??100,validated:true});}
for(const name of ['idle','walk']){const project=validateProject(JSON.parse(fs.readFileSync(new URL(`hero-forward-${name}.sprite.json`,import.meta.url))));report.editable.push({name,width:project.width,height:project.height,frames:project.frames.length,validated:true});}
const mannequin=validateProject(JSON.parse(fs.readFileSync(new URL('mannequin.sprite.json',import.meta.url))));report.editable.push({name:'neutral-mannequin',width:mannequin.width,height:mannequin.height,frames:mannequin.frames.length,validated:true});
fs.writeFileSync(new URL('../../../docs/reviews/M1-HR12/editor-validation.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
console.log('Seven preview projects and three editable projects validate; slow review GIF delays set to exactly 400ms.');
