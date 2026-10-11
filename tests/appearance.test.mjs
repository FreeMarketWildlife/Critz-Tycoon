import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { npcAppearance } from '../src/appearance.js';
import { scenes } from '../src/world.js';

const manifest = JSON.parse(readFileSync(new URL('../assets/playable/atlas.json', import.meta.url)));
const entries = new Map(manifest.assets.map(a => [a.id, a]));

test('every existing NPC resolves to a complete native character without modifying the world', () => {
  const before = JSON.stringify(scenes), identities = new Set();
  for (const scene of Object.values(scenes)) for (const e of scene.entities.filter(e => e.type === 'npc')) {
    for (const gender of ['boy', 'girl']) {
      const id = npcAppearance(e, gender); identities.add(id);
      for (const direction of ['down','up','left','right']) for (const mode of ['walk','run']) for (const pose of ['idle','strideA','strideB']) {
        const frame = entries.get(`char.${id}.${direction}.${mode}.${pose}`);
        assert.ok(frame, `${e.id}: missing ${id}/${direction}/${mode}/${pose}`);
        assert.deepEqual(frame.rect.slice(2), [24,32]);
        assert.deepEqual(frame.anchor, [12,32]);
      }
    }
  }
  assert.equal(identities.size, 12);
  assert.equal(JSON.stringify(scenes), before);
});

test('named shopkeepers keep distinct designs despite shared old roles', () => {
  assert.deepEqual(['shop-critz','shop-vet','shop-pharmacy','shop-bike','shop-glass'].map(id => npcAppearance({id,look:'doctor'})),
    ['juniper','dr-fern','mina','ollie','aunt-ember']);
  assert.equal(npcAppearance({id:'nugget',name:'A changed display name'}), 'professor');
});

test('player choice determines opposite-gender rival appearance without reading names', () => {
  assert.equal(npcAppearance({id:'rival'}, 'boy'), 'hero.girl');
  assert.equal(npcAppearance({id:'rival'}, 'girl'), 'hero.boy');
});
