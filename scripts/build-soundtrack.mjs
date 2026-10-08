import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const album=JSON.parse(await readFile('music/album.json','utf8'));
if(album.tracks.length!==30)throw Error('Expected the approved thirty-track collection');
const tracks=[];
for(const t of album.tracks){
 const file=t.midi.replace('../','');const bytes=await readFile(file);
 const hash=createHash('sha256').update(bytes).digest('hex');
 if(hash!==t.midiSha256||bytes.toString('ascii',0,4)!=='MThd')throw Error(`Invalid MIDI ${file}`);
 tracks.push({id:t.id,title:t.title,mood:t.mood,bpm:t.bpm,key:t.key,meter:t.meter,file:'midi/'+file.split('/').at(-1),sha256:hash,noteCount:t.noteCount,seconds:t.duration});
}
await mkdir('assets/audio',{recursive:true});
await writeFile('assets/audio/soundtrack.json',JSON.stringify({version:1,collection:'Thirty Different Days',accepted:'2026-10-08',tracks},null,2)+'\n');
console.log('Soundtrack manifest: 30 verified canonical MIDI assets');
