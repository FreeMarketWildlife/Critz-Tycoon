const $ = (s) => document.querySelector(s);
const audio = $('#audio');
let tracks = [], index = 0, category = 'All', generation = 0;
const groups = {
  'All': null,
  'Home & heart': ['Hope','Home','Friendship','Belonging','Relief','Forgiveness','Recovery','Gratitude'],
  'Small delights': ['Cute','Playfulness','Craft','Curiosity','Delight','Joy'],
  'Out into the world': ['Adventure','Determination','Battle','Resolve','Freedom'],
  'Strange & shadow': ['Scary','Danger','Mystery'],
  'Slow evenings': ['Melancholy','Wonder','Chill','Wistfulness','Tenderness','Contentment','Nostalgia','Peace'],
};
const time = (n) => `${Math.floor(n / 60)}:${String(Math.floor(n % 60)).padStart(2, '0')}`;
function element(tag, attrs = {}, content = '') {
  const e = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) e.setAttribute(key, value);
  e.textContent = content;
  return e;
}
function paint() {
  const query = $('#search').value.trim().toLowerCase();
  const visible = tracks.filter(t => (!groups[category] || groups[category].includes(t.mood)) && `${t.title} ${t.mood} ${t.story}`.toLowerCase().includes(query));
  $('#result-count').textContent = `${visible.length} of 30 stories`;
  $('#empty').hidden = visible.length > 0;
  $('#tracks').replaceChildren(...visible.map(t => {
    const i = tracks.indexOf(t);
    const row = element('article', {class: `track${i === index ? ' active' : ''}`, 'data-track': t.id});
    const main = element('div', {class: 'track-main'});
    const button = element('button', {class: 'track-play', 'aria-label': `Play ${t.title}`}, i === index && !audio.paused ? 'Ⅱ' : '▶');
    button.addEventListener('click', () => i === index ? toggle() : select(i, true));
    const body = element('div');
    const title = element('div', {class:'track-title'});
    title.append(element('span', {class:'track-number'}, String(t.id).padStart(2, '0')), document.createTextNode(t.title));
    body.append(title, element('p',{class:'track-story'},t.story));main.append(button,body);
    const links = element('div', {class:'track-links'});
    links.append(element('a',{href:t.midi,download:'','aria-label':`Download MIDI: ${t.title}`},'MIDI ↗'), element('a',{href:t.audio,download:'','aria-label':`Download audio: ${t.title}`},'Audio ↗'));
    row.append(main,element('span',{class:'mood'},t.mood),element('span',{class:'duration'},time(t.duration)),links);
    return row;
  }));
  $('#filters').replaceChildren(...Object.keys(groups).map(name => {
    const button = element('button', {'aria-pressed':String(category===name)},name);
    button.addEventListener('click',()=>{category=name;paint();});return button;
  }));
  $('#toggle').textContent = audio.paused ? '▶' : 'Ⅱ';
  $('#toggle').setAttribute('aria-label',audio.paused?'Play selected track':'Pause selected track');
}
async function start() {
  const request = generation;
  $('#player-error').hidden = true;
  try { await audio.play(); } catch (err) {
    if(request !== generation || err.name === 'AbortError') return;
    $('#player-error').textContent = 'Playback couldn’t start. Press play again, or use the Audio download.';
    $('#player-error').hidden = false;
  }
  paint();
}
function select(i, play = false) {
  generation++;
  audio.pause();index=(i+tracks.length)%tracks.length;
  const t=tracks[index];audio.src=t.audio;
  $('#now-number').textContent=`${String(t.id).padStart(2,'0')} / 30`;
  $('#now-title').textContent=t.title;$('#now-story').textContent=t.story;
  $('#chapters').replaceChildren(...t.sections.map(section => {
    const button=element('button',{'aria-label':`Seek to ${section.label}, ${time(section.seconds)}`},`${time(section.seconds)} ${section.label}`);
    button.addEventListener('click',async()=>{
      const request = generation;
      if(audio.readyState < 1) {
        audio.load();
        await new Promise(resolve => {
          audio.addEventListener('loadedmetadata',resolve,{once:true});
          audio.addEventListener('error',resolve,{once:true});
        });
      }
      if(request !== generation || audio.error) return;
      audio.currentTime=section.seconds;start();
    });return button;
  }));
  $('#player-error').hidden = true;paint();if(play)start();
}
function toggle(){if(audio.paused)start();else audio.pause();}
$('#toggle').addEventListener('click',toggle);
$('#play-all').addEventListener('click',()=>select(0,true));
$('#previous').addEventListener('click',()=>select(index-1,true));
$('#next').addEventListener('click',()=>select(index+1,true));
$('#search').addEventListener('input',paint);
$('#repeat').addEventListener('change',e=>audio.loop=e.target.checked);
audio.addEventListener('play',paint);audio.addEventListener('pause',paint);
audio.addEventListener('ended',()=>{if(index<tracks.length-1)select(index+1,true);else{audio.currentTime=0;paint();}});
audio.addEventListener('error',()=>{$('#player-error').textContent='This audio file couldn’t load. Try the Audio download or another track.';$('#player-error').hidden=false;});
try {
  const response=await fetch('album.json');if(!response.ok)throw new Error('Album unavailable');
  const album=await response.json();tracks=album.tracks;
  $('#album-length').textContent=`30 original tracks · ${Math.round(tracks.reduce((sum,t)=>sum+t.duration,0)/60)} minutes`;
  select(0);
} catch {
  $('#tracks').textContent='The collection couldn’t load. Refresh the page, or download the complete MIDI collection above.';
  for(const id of ['#play-all','#previous','#next','#toggle'])$(id).disabled=true;
}
