// Keep mode state, handlers and autosaves isolated while sharing the existing editor shell.
const bodyRegions = new URLSearchParams(location.search).get('mode') === 'body-regions';
const link = document.createElement('a');
link.className = 'editor-mode-link';
link.href = bodyRegions ? './' : '?mode=body-regions';
link.textContent = bodyRegions ? 'Drawing mode' : 'Body regions';
document.querySelector('.app-header').append(link);
await import(bodyRegions ? './body-regions.js' : './editor.js');
