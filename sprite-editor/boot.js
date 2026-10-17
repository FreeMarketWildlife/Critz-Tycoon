// Keep mode state, handlers and autosaves isolated while sharing the existing editor shell.
const bodyRegions = new URLSearchParams(location.search).get('mode') === 'body-regions' || new URLSearchParams(location.search).get('mode') === 'dummy-creator';
const link = document.createElement('a');
link.className = 'editor-mode-link';
link.href = bodyRegions ? './' : '?mode=dummy-creator&labels=phil-walk-draft-20261017';
link.textContent = bodyRegions ? 'Drawing mode' : 'Dummy Creator';
document.querySelector('.app-header').append(link);
await import(bodyRegions ? './body-regions.js' : './editor.js');
