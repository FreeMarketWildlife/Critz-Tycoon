import {gifBytes} from '../sprite-editor/model.js';
// Retain the editor's exact palette/LZW encoding, then apply the explicitly
// recorded centisecond holds to real GIF control blocks (never byte-search LZW).
export function encodeGif(project,durationsMs){
 if(durationsMs.length!==project.frames.length||durationsMs.some(n=>!Number.isInteger(n)||n<20||n%10))throw Error('GIF needs one whole-centisecond hold per frame.');
 const b=gifBytes(project);let pos=13+((b[10]&128)?3*(1<<((b[10]&7)+1)):0),frame=0;
 function subblocks(){while(pos<b.length){const n=b[pos++];if(!n)return;pos+=n;}throw Error('Incomplete GIF data.');}
 while(pos<b.length){const kind=b[pos];if(kind===0x3b)break;
  if(kind===0x21){if(b[pos+1]===0xf9){if(b[pos+2]!==4||frame>=durationsMs.length)throw Error('Invalid GIF control block.');const hold=durationsMs[frame++]/10;b[pos+4]=hold&255;b[pos+5]=hold>>8;pos+=8;}else{pos+=2;subblocks();}}
  else if(kind===0x2c){const flags=b[pos+9];pos+=10;if(flags&128)pos+=3*(1<<((flags&7)+1));pos++;subblocks();}
  else throw Error('Unexpected GIF block.');
 }
 if(frame!==durationsMs.length)throw Error('GIF frame count differs from its timing metadata.');return b;
}
