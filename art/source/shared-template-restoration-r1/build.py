"""SB1 exact selected-Hero body restoration using existing BS2 appearance separation."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-SB1';meta=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text());bmeta=json.loads((root/'art/source/hero-bald-shading-r2/changes.json').read_text());checks=[];records={};frames={};inputs={};selectedRevision='8726c9af6b8304148d2ff1e84b149bcfdc2785a6'
def ck(name,truth):assert truth,name;checks.append(name)
def load(path):
 p=root/path;inputs[path]=hashlib.sha256(p.read_bytes()).hexdigest();return Image.open(p).convert('RGBA')
def points(im):return {(i%32,i//32) for i,p in enumerate(im.get_flattened_data()) if p[3]}
def mask(pts):
 q=Image.new('RGBA',(32,64))
 for p in pts:q.putpixel(p,(255,255,255,255))
 return q
def extract(q,pts):
 im=Image.new('RGBA',(32,64))
 for p in pts:im.putpixel(p,q.getpixel(p))
 return im
def record_image(path,q):q.save(path);return {'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rgbaSHA256':hashlib.sha256(q.tobytes()).hexdigest(),'size':q.size,'paintedBounds':q.getbbox()}
for dr in ['south','north','west','east']:
 frames[dr]={};records[dr]={}
 for po in ['idle','A','P','C']:
  tag=dr+'-'+po;folder=out/tag;folder.mkdir(exist_ok=True);bp='docs/reviews/M1-BS2/'+tag+'/';selected_path=f'docs/reviews/M1-PS1/hero-{tag}.png';selected=load(selected_path);ck(tag+' selected source bytes match pinned PS1 revision',subprocess.check_output(['git','show',selectedRevision+':'+selected_path])==(root/selected_path).read_bytes());oldDressed=load(bp+'dressed-exact.png');base=load(bp+'bald-template.png');hair=load(bp+'hair-art.png');shade=load(bp+'hair-dependent-shading.png');attachment=load(bp+'optional-hair-attachment.png');hairpts=points(hair);shadepts=points(shade);hidden={tuple(p) for p in bmeta['poses'][dr][po]['selectedHairHiddenScalpCells']};e=meta['directions'][dr][po]
  # No drawing: restore actual selected material deltas, currently FM2foot colors.
  delta={(x,y) for y in range(64) for x in range(32) if selected.getpixel((x,y))!=oldDressed.getpixel((x,y))}
  ck(tag+' source alpha unchanged by historical footwear material pass',selected.getchannel('A').tobytes()==oldDressed.getchannel('A').tobytes())
  ck(tag+' all material restoration is lower costume, not head/body redesign',all(y>=54 and (x,y) not in hairpts|shadepts|hidden for x,y in delta))
  for p in delta:base.putpixel(p,selected.getpixel(p))
  recomposed=base.copy()
  for p in hidden:recomposed.putpixel(p,(0,0,0,0))
  recomposed.alpha_composite(shade);recomposed.alpha_composite(hair)
  recomposedDiff={(x,y) for y in range(64) for x in range(32) if recomposed.getpixel((x,y))!=selected.getpixel((x,y))}
  ck(tag+' exact complete selected Hero RGBA recomposition',not recomposedDiff)
  ck(tag+' original hair plus skin shadow exact attachment',Image.alpha_composite(shade,hair).tobytes()==attachment.tobytes())
  protected={tuple(p) for key in ['eyes','ears','hands'] for p in e['commonFeatureRegistration'][key]['cells']}
  visibleProtected=protected-hairpts-shadepts-hidden
  ck(tag+' actually visible registered eyes ears hands source RGBA exact',all(base.getpixel(p)==selected.getpixel(p) for p in visibleProtected))
  ck(tag+' all registered feature sites exact after original hair attachment',all(recomposed.getpixel(p)==selected.getpixel(p) for p in protected))
  ck(tag+' waist legs full shoe pixels exact below54',base.crop((0,54,32,64)).tobytes()==selected.crop((0,54,32,64)).tobytes())
  appearance=hairpts|shadepts|hidden
  bodypts={(x,y) for y in range(64) for x in range(32) if (x,y) not in appearance}
  diff={p for p in bodypts if base.getpixel(p)!=selected.getpixel(p)}
  ck(tag+' outside documented hair skinshadow scalp occlusion all source pixels exact',not diff)
  # Source-registered visible pack, explicitly excluded from observed-body proof.
  packflags=e['visiblePackMask'];packcandidate={(i%32,i//32) for i,on in enumerate(packflags) if on};packlayer=load(f'docs/reviews/M1-HR14/pack-layer-{tag}.png');pack={p for p in packcandidate if selected.getpixel(p)[3] and packlayer.getpixel(p)==selected.getpixel(p)}
  ck(tag+' source visible pack mask matches every actual selected pack pixel',pack==packcandidate)
  observed={p for p in bodypts if selected.getpixel(p)[3] and p not in pack}
  srcbody=extract(selected,observed);newbody=extract(base,observed);ck(tag+' observed body excludes pack and reuses exact visible source',srcbody.tobytes()==newbody.tobytes())
  alphaDiff={p for p in {(x,y) for y in range(64) for x in range(32)} if bool(base.getpixel(p)[3])!=bool(selected.getpixel(p)[3])}
  ck(tag+' every bald alpha difference explained by hair/scalp mask',alphaDiff<=hairpts|hidden)
  files={}
  layers={'restored-bald.png':base,'original-hair.png':hair,'hair-dependent-shading.png':shade,'hair-scalp-cutout-mask.png':mask(hidden),'source-hair-mask.png':mask(hairpts),'source-visible-pack-mask.png':mask(pack),'source-observed-body.png':srcbody,'restored-observed-body.png':newbody,'recomposed-hero.png':recomposed,'source-vs-bald-alpha-diff.png':mask(alphaDiff),'source-vs-recomposed-diff.png':mask(recomposedDiff),'outside-appearance-diff.png':mask(diff)}
  for name,q in layers.items():files[name]=record_image(folder/name,q)
  records[dr][po]={'selectedHero':selected_path,'selectedSourceSHA256':hashlib.sha256((root/selected_path).read_bytes()).hexdigest(),'frame':[32,64],'anchor':[16,64],'sourceTorsoAnchor':e['torsoAnchor'],'sourceCanonicalPackAnchor':e['canonicalPackAnchor'],'anchorStatus':'existing image/source registration, not observed hidden joints','materialRestoreCells':[list(p) for p in sorted(delta)],'hairCells':len(hairpts),'hairDependentShadeCells':len(shadepts),'hairHiddenScalpCutoutCells':[list(p) for p in sorted(hidden)],'visiblePackCandidateCells':len(packcandidate),'actualMatchingVisiblePackCells':len(pack),'observedBodyComparedCells':len(observed),'observedBodyRGBADifferenceCells':sum(base.getpixel(p)!=selected.getpixel(p) for p in observed),'outsideAppearanceRGBADifferenceCells':len(diff),'baldAlphaDifferenceCells':len(alphaDiff),'recompositionRGBADifferenceCells':len(recomposedDiff),'hairOccludedRegisteredFeatureCells':[list(p) for p in sorted(protected & hairpts)],'visibleRegisteredFeatureCells':[list(p) for p in sorted(visibleProtected)],'registeredFeatureSites':{k:e['commonFeatureRegistration'][k]['cells'] for k in ['eyes','ears','hands']},'files':files}
  frames[dr][po]={'source':selected,'bald':base,'recomposed':recomposed,'observed':newbody}
 # Matched current DS is only a comparison, never restoration source.
fnt=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
def compare(name,allposes=False,directions=None):
 rows=[(d,p) for d in (directions or frames) for p in (['idle','A','P','C'] if allposes else ['idle'])];plate=Image.new('RGB',(1020,230*len(rows)),'#eee8d1');d=ImageDraw.Draw(plate)
 for row,(dr,po) in enumerate(rows):
  current=Image.open(root/f'docs/reviews/{"M1-DS4" if dr in ["south","north"] else "M1-DS5"}/dummy-2x-{dr}-{po}.png').convert('RGBA')
  for col,(label,q) in enumerate([('SELECTED PS1 HERO',frames[dr][po]['source']),('CURRENT DS REDESIGN',current),('RESTORED SHARED BALD',frames[dr][po]['bald']),('RECOMPOSED EXACT HERO',frames[dr][po]['recomposed'])]):
   x=col*255;y=row*230;d.text((x+5,y+5),f'{dr}/{po} {label}',font=fnt,fill='#292634');big=q.resize((64,128),Image.Resampling.NEAREST);plate.paste(big,(x+25,y+35),big);plate.paste(q,(x+140,y+65),q);d.line((x+15,y+163,x+105,y+163),fill='#80503d')
  d.text((8,row*230+185),'INTERNAL / fixed32x64, anchor16,64 / native + integer2x / preservation-selected, not praise-selected',font=fnt,fill='#485b78')
 plate.save(out/name)
compare('source-current-restored-idles.png');compare('source-current-restored-all16.png',True)
for dr in frames:compare(dr+'-source-current-restored-static.png',True,[dr])
# Appearance exclusions and source-registered visible anchors, no bone inference.
plate=Image.new('RGB',(1020,920),'#eee8d1');d=ImageDraw.Draw(plate)
for row,dr in enumerate(frames):
 po='idle';folder=out/(dr+'-'+po)
 for col,(label,path) in enumerate([('SOURCE HAIR MASK','source-hair-mask.png'),('VISIBLE PACK MASK','source-visible-pack-mask.png'),('SOURCE OBSERVED BODY','source-observed-body.png'),('RESTORED OBSERVED BODY','restored-observed-body.png')]):
  q=Image.open(folder/path).convert('RGBA');x=col*255;y=row*230;d.text((x+5,y+5),dr+' '+label,font=fnt,fill='#292634');big=q.resize((64,128),Image.Resampling.NEAREST);plate.paste(big,(x+25,y+35),big);plate.paste(q,(x+140,y+65),q)
 d.text((10,row*230+185),'Excluded hair/shadow/pack pixels expose only observed source body; occluded body is NOT reconstructed.',font=fnt,fill='#485b78')
plate.save(out/'actual-appearance-exclusions-visible-body.png')
# The current gate is all16STATIC source/template poses. Animation work is deferred.
(src/'restoration.json').write_text(json.dumps({'task':'M1.SB1','baselineStatus':'preservation-selected from direct human instruction; earlier praise-selection unresolved; NWE approval unverified','selectedFamily':'PS1 native32x64','selectedRevision':selectedRevision,'poses':records,'inputs':inputs,'animationWork':'not part of current static shared-body checkpoint'},indent=2)+'\n')
(src/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'appearanceApproval':False,'native16x32Counterpart':'deferred; no selected-source downsampling'},indent=2)+'\n')
print('PASS',len(checks),'all16STATIC source RGBA restoration/mask/feature/attachment checks')
