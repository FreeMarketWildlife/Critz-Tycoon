import test from 'node:test';import assert from 'node:assert/strict';import{readFile}from'node:fs/promises';import{createHash}from'node:crypto';
import{decodeMidi}from'../src/audio/midi.js';import{renderSequence,synthNote,PROGRAMS,SAMPLE_RATE}from'../src/audio/synth.js';import{chooseCue,SCENE_CUES,readAudioSettings,writeAudioSettings,AUDIO_SETTINGS_KEY}from'../src/audio/cues.js';
function file(track){const b=Buffer.from(track);return Buffer.concat([Buffer.from('4d546864000000060000000101e0','hex'),Buffer.from('MTrk'),Buffer.from([0,0,b.length>>8,b.length&255]),b]);}
test('MIDI running status, tempo changes and velocity-zero note-offs map to seconds',()=>{
 const t=[0,0xff,0x51,3,7,0xa1,0x20,0,0xc0,80,0,0x90,60,80,0x83,0x60,60,0,0,0xff,0x51,3,0x0f,0x42,0x40,0,0x90,62,70,0x83,0x60,0x80,62,0,0,0xff,0x2f,0];
 const s=decodeMidi(file(t));assert.equal(s.notes.length,2);assert.equal(s.notes[0].duration,.5);assert.equal(s.notes[1].at,.5);assert.equal(s.notes[1].duration,1);assert.equal(s.notes[0].program,80);assert.equal(s.duration,1.5);
});
test('Malformed, hanging, bent and out-of-bounds MIDI fail before audio allocation',()=>{
 for(const b of [new Uint8Array(0),file([0,60,80]),file([0,0x90,60,80,0,0xff,0x2f,0]),file([0,0xe0,1,64]),file([0,0xff,81,10,1]),file([255,255,255,255,255])])assert.throws(()=>decodeMidi(b));
 const b=file([0,0xff,0x2f,0]);b[12]=0xe7;assert.throws(()=>decodeMidi(b),/SMPTE/);
});
test('All thirty canonical MIDI hashes, note counts, patches and durations match the approved collection',async()=>{
 const m=JSON.parse(await readFile('assets/audio/soundtrack.json'));assert.equal(m.tracks.length,30);
 for(const t of m.tracks){const b=await readFile('assets/audio/'+t.file),s=decodeMidi(b);assert.equal(createHash('sha256').update(b).digest('hex'),t.sha256);assert.equal(s.notes.length,t.noteCount);assert.ok(Math.abs(s.duration+3-t.seconds)<.01);assert.ok(s.notes.every(n=>n.channel===9||PROGRAMS[n.program]));}
});
test('Every current scene has a cue; story, habitat and night override without mutating saves',()=>{
 const s={scene:'town',stage:'morning',time:12};const before=JSON.stringify(s);assert.equal(chooseCue(s),5);assert.equal(chooseCue(s,'pause'),5);assert.equal(chooseCue(s,'options','pause'),5);assert.equal(chooseCue(s,'options','title'),1);assert.equal(chooseCue(s,'tank'),20);assert.equal(chooseCue({...s,time:22}),28);assert.equal(chooseCue({...s,stage:'night',storyBeat:'broken'}),11);assert.equal(chooseCue({...s,stage:'night',storyBeat:'kaid'}),4);assert.equal(JSON.stringify(s),before);assert.equal(Object.keys(SCENE_CUES).length,14);for(const id of Object.values(SCENE_CUES))assert.ok(id>=1&&id<=30);
});
test('Audio preferences are bounded, failure-safe and separate from game saves',()=>{
 const map=new Map([['critz-tycoon.save.v1','untouched']]),storage={getItem:k=>map.get(k),setItem:(k,v)=>map.set(k,v)};
 assert.deepEqual(readAudioSettings(storage),{enabled:true,volume:.4});writeAudioSettings(storage,{enabled:false,volume:.7});assert.deepEqual(readAudioSettings(storage),{enabled:false,volume:.7});assert.equal(map.get('critz-tycoon.save.v1'),'untouched');map.set(AUDIO_SETTINGS_KEY,'{"volume":500,"enabled":"false"}');assert.deepEqual(readAudioSettings(storage),{enabled:true,volume:1});assert.equal(writeAudioSettings({setItem(){throw Error();}},{enabled:true,volume:.4}),false);
});
test('Sine, square, triangle and saw have distinct spectra with a stable A440 fundamental',()=>{
 const amplitudes=(p)=>{const w=synthNote(p,69,1.5);return [440,880,1320].map(f=>{let x=0,y=0;for(let i=4410;i<26460;i++){x+=w[i]*Math.cos(2*Math.PI*f*i/SAMPLE_RATE);y+=w[i]*Math.sin(2*Math.PI*f*i/SAMPLE_RATE);}return Math.hypot(x,y);});};
 const sine=amplitudes('sine'),square=amplitudes('square'),triangle=amplitudes('triangle'),saw=amplitudes('saw');assert.ok(sine[2]/sine[0]<.001);assert.ok(square[2]/square[0]>.25);assert.ok(triangle[2]/triangle[0]>.1&&triangle[2]/triangle[0]<.12);assert.ok(saw[1]/saw[0]>.4);
});
test('MIDI-to-PCM is finite, non-silent, stereo and peak-bounded with a silent loop boundary',async()=>{
 const m=JSON.parse(await readFile('assets/audio/soundtrack.json')),t=m.tracks[0],r=renderSequence(decodeMidi(await readFile('assets/audio/'+t.file)));assert.equal(r.noteCount,t.noteCount);assert.ok(r.peak>0&&r.peak<=.721);assert.ok(r.left.every(Number.isFinite)&&r.right.every(Number.isFinite));assert.equal(r.left.length,r.right.length);assert.equal(r.left[0],0);assert.equal(r.left.at(-1),0);assert.ok(r.left.some((x,i)=>Math.abs(x-r.right[i])>.001));
});
