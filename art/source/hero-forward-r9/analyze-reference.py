"""Read Phil's confirmed GIF; write numeric observations in repo, pixels only external."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR9';ext=Path(sys.argv[1]).resolve();assert ext!=root and root not in ext.parents
path=ext/'01agijgmbz561.gif';sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e'
im=Image.open(path);assert im.format=='GIF' and im.n_frames==8 and im.size==(256,192)
frames=[];report={'sourceURL':'https://i.redd.it/01agijgmbz561.gif','sha256':sha,'bytes':path.stat().st_size,'format':'GIF87a','displayCanvas':[256,192],'frameCount':8,'loop':im.info.get('loop'),'registration':{'leftCropDisplay':[0,0,128,192],'uniformDisplayBlocks':[4,4],'logicalCrop':[32,48],'targetFrame':[32,64],'fixedTopPadding':14,'fixedBottomPadding':2,'mapping':'target x=display x/4; target y=display y/4+14, identical every frame','groundAnchorConvention':[16,64],'limitations':'Bottom edge is visible occupied in stride frames. Unknown uncropped extent/padding; 14top+2bottom is a fixed registration proposal; chosen target anchor is comparison convention, not measured artist anchor. No per-frame fits.'},'frames':[],'observationType':'Actual decoded source GIF; not artist-workflow or hidden-bone inference'}
def bbox(points):return [min(x for x,y in points),min(y for x,y in points),max(x for x,y in points)+1,max(y for x,y in points)+1] if points else None
for i in range(8):
 im.seek(i);rgba=im.convert('RGBA');left=rgba.crop((0,0,128,192))
 assert im.info['duration']==100
 assert all(len({left.getpixel((xx,yy)) for yy in range(y,y+4) for xx in range(x,x+4)})==1 for y in range(0,192,4) for x in range(0,128,4))
 logical=left.resize((32,48),Image.Resampling.NEAREST);frame=Image.new('RGBA',(32,64));frame.paste(logical,(0,14));frames.append(frame);frame.save(ext/f'registered-left-{i:02}.png')
 pts=[(x,y) for y in range(64) for x in range(32) if frame.getpixel((x,y))[3]]
 eyes=[(x,y) for y in range(34,44) for x in range(10,22) if frame.getpixel((x,y))==(16,33,58,255)]
 bands={}
 for name,(l,t,r,b) in {'leftArmCostume':(3,43,11,54),'rightArmCostume':(21,43,29,54),'lowerCostumeFoot':(6,53,26,62)}.items():bands[name]=bbox([(x,y) for y in range(t,b) for x in range(l,r) if frame.getpixel((x,y))[3]])
 report['frames'].append({'index':i,'durationMs':im.info['duration'],'disposal':im.disposal_method,'pose':['A','A','P','P','C','C','P','P'][i],'rawDisplayBounds':list(left.getchannel('A').getbbox()),'rawLogicalBounds':list(logical.getchannel('A').getbbox()),'occupiedBounds':bbox(pts),'eyeBounds':bbox(eyes),'eyeCells':len(eyes),'eyeCoordinates':eyes,'displayGrid4x4MismatchCells':0,'observedBands':bands,'sourceCropBottomOccupied':any(logical.getpixel((x,47))[3] for x in range(32)),'decodedLeftSha256':hashlib.sha256(frame.tobytes()).hexdigest()})
assert frames[0].tobytes()==frames[1].tobytes() and frames[2].tobytes()==frames[3].tobytes()==frames[6].tobytes()==frames[7].tobytes() and frames[4].tobytes()==frames[5].tobytes()
report['uniqueLeftPoses']=3;report['timelineMs']=[100]*8;report['cycleDurationMs']=800;report['mainHeadEyeBouncePixels']=2;report['crownTopChangePixels']=4;report['crownTopIsNotRigidHeadMotion']=True
report['visibleGrammar']=['Head main face moves down2 in A/C; cap peak additionally changes contour.','A/C have opposite asymmetric arm/costume clusters; P is bilaterally balanced.','With fixed14px padding, passing lower-body/foot clusters occupy54–59; stride lower clusters extend to61.','Only one lower/forward foot has full bright sole cluster in A/C; other foot overlaps dark lower costume higher up.','Weight/contact/lift are interpretations: no floor/shadow and bottom clipping prevents complete anatomical inference.','High arm/costume clusters must not be interpreted as measured hand/elbow bones or reproduced as longer bare limbs.']
(out/'reference-observations.json').write_text(json.dumps(report,indent=2)+'\n')
p=Image.new('RGB',(1024,310),'#eee6d0');d=ImageDraw.Draw(p)
for i,f in enumerate(frames):
 x=i*128;d.text((x+6,8),str(i)+' '+report['frames'][i]['pose']+' 100ms',fill='#242330');b=f.resize((128,256),Image.Resampling.NEAREST);p.paste(b,(x,28),b)
p.save(ext/'registered-all-eight-contact.png');print(json.dumps({'frames':report['frames'],'cycleMs':800,'uniquePoses':3},indent=2))
