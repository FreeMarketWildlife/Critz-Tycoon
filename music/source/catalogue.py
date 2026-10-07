"""Original authored themes. Scale degrees are relative to the stated mode.
q=quarter, e=eighth, h=half, d=dotted quarter, w=whole, s=sixteenth.
Each A/B string has four explicitly composed measures; development lives in compose.py.
"""
TRACKS=[]
def T(title,mood,story,bpm,key,mode,meter,groove,lead,reply,keys,chords,bridge,A,B,form='journey'):
    TRACKS.append(dict(id=len(TRACKS)+1,title=title,mood=mood,story=story,bpm=bpm,key=key,mode=mode,meter=meter,groove=groove,lead=lead,reply=reply,keys=keys,chords=chords.split(),bridge=bridge.split(),A=A.split('|'),B=B.split('|'),form=form))

T('A Tiny World, A New Beginning','Hope','The title theme: one small act of care opens into a whole world.',112,'D','major','4/4','adventure','reed','glass','pad',
'Dmaj9 Bm7 Gmaj9 A7','Em9 Gmaj7 Bm7 A7',
'1q 3e 5e 6q 5q|3d 2e 1h|4q 6q 8e 7e 6q|5d 3e 2q Rq',
'3e 4e 6q 5q 3q|4d 3e 2q 1q|6e 7e 8q 10q 9q|8h 7q 5q')
T('Kitchen Light, Still On','Home','A familiar light under the door; tenderness and room to begin again.',78,'F','major','4/4','lofi','velvet','flute','epiano',
'Fmaj9 Dm9 Bbmaj7 C9','Gm9 C9 Am7 Dm9',
'3d 2e 1q Rq|5q 6e 5e 3h|4q 3q 2e 1e 2q|3h 2q Rq',
'6q 8q 7e 6e 5q|4d 5e 3h|2q 3e 4e 5q 3q|2h 1h','intimate')
T('Pebble in a Pocket','Cute','A gecko peeks out, freezes, then decides your sleeve is home.',126,'C','major','4/4','bounce','bubble','marimba','pluck',
'C6 Am7 Fmaj7 G7','Dm7 G7 Em7 A7',
'5e Re 3e 5e 6q 3q|2e 3e 1q Rq 5q|6e 5e 4e Re 3q 1q|2q 5e 4e 3q Rq',
'4e 6e 8q 7e Re 6q|5e 4e 2q Rq 5q|3e 2e 3e 5e 6q 8q|7e 6e 5q 2q 1q')
T('Kaid Brought Tomorrow','Friendship','A 25-gallon gift arrives; the tune starts alone and gains an answering friend.',104,'G','major','4/4','shuffle','glass','reed','epiano',
'Gmaj9 Em7 Cmaj9 D9','Am7 D9 Bm7 Em7',
'1d 2e 5q 3q|6q 5e 3e 2q Rq|4d 6e 5q 3q|2q 1e 2e 3h',
'6e 5e 6q 8q 7q|5d 4e 3h|2e 3e 4q 6q 5q|3q 2q 1h')
T('Rootport Wakes Up','Belonging','Shutters open, neighbors wave, and the town finds its walking rhythm.',116,'Bb','major','4/4','town','reed','brass','pluck',
'Bb6 Gm7 Ebmaj7 F9','Cm7 F9 Dm7 Gm7',
'3q 5e 6e 5q 2q|3e 2e 1q Rq 3q|4q 6q 5e 4e 3q|2d 3e 5h',
'8q 7e 6e 5q 6q|4d 3e 2h|6q 5q 3e 4e 5q|2q 3q 1h')
T('Past the Last Mailbox','Adventure','The first forest path feels enormous; a skipping tune grows into a confident stride.',138,'A','mixolydian','4/4','adventure','brass','flute','pluck',
'A G D A','Bm7 D G E7',
'1e 2e 3q 5d 6e|7q 5q 3e 2e 1q|4q 6e 5e 4q 2q|3e 5e 8q 7q 5q',
'2q 4e 6e 5q 4q|6d 5e 3q 2q|7e 6e 5q 3q 4q|5h 2q 3q')
T('Notebook Full of Wings','Curiosity','Professor Nugget helps turn a puzzling movement into a first field-note sketch.',98,'C','lydian','5/4','curious','marimba','bubble','epiano',
'Cmaj9 D Em7 Cmaj9','Am7 D Gmaj7 Cmaj9',
'1q 3e 5e 4q 2q Rq|3q 5q 7d 6e 5q|6e 7e 8q 5q 3q 2q|4h 3q 2q 1q',
'6q 8e 9e 10q 9q 7q|6h 4q 5q Rq|5e 7e 9q 8q 6q 4q|3h 2q 4q 5q')
T('Button Takes the Scenic Route','Playfulness','A snail makes a mighty expedition across one leaf.',108,'Eb','major','3/4','waltz','musicbox','bubble','pluck',
'Eb6 Cm7 Abmaj7 Bb7','Fm7 Bb7 Gm7 Cm7',
'5e 3e 1q 3q|6d 5e 3q|4e Re 6q 5q|2q 3q Rq',
'4e 5e 6q 8q|7q 5d 3e|6q 4e 3e 2q|5q 2q 1q')
T('Glow n’ Blow','Craft','Glass catches amber light; playful bubbles trade places with a warm workshop groove.',120,'D','mixolydian','4/4','funk','bubble','glass','organ',
'D9 Cmaj7 G6 D9','Em7 A9 Cmaj7 D9',
'Re 1e 3e 5e Rq 6e 5e|3q Re 2e 1q 7e 5e|4e Re 6q 5e 4e 3q|2e 3e 5q Rq 1q',
'6e 5e 6e 8e 7q Rq|5q 3e 2e 4q 6q|7e Re 5e 3e 2q 1q|3q 4q 5h')
T('A Rival, Not an Enemy','Determination','A friendly competitor strides ahead, then leaves space for you to catch up.',132,'E','dorian','4/4','funk','square','reed','epiano',
'Em9 A9 Cmaj7 B7','Gmaj7 D A9 B7',
'1e 1e 3q 4e 5e 6q|5d 3e 2q 1q|3e 5e 7q 6q 5q|4e 3e 2q 7q Rq',
'3q 5q 8e 7e 6q|5q 2e 3e 4h|6e 5e 4q 3q 2q|7d 2e 1h')
T('Rain Between the Houses','Melancholy','Rain blurs the streetlights; a small falling phrase slowly learns to rise.',76,'A','minor','4/4','lofi','epiano','velvet','pad',
'Am9 Fmaj9 Cmaj7 G6','Dm9 G9 Cmaj9 E7',
'5h 3q 2q|1d 2e 3q Rq|5q 4e 3e 2h|7q 5q Rq 2q',
'4q 6q 8d 7e|5h 4q 2q|3d 5e 6q 5q|2q 7q 1h','intimate')
T('Every Little Life Is Still Here','Relief','The hidden animals are safe. Sparse worry gives way to a gentle, breathing refrain.',84,'Ab','major','6/8','lullaby','flute','glass','epiano',
'Abmaj9 Fm7 Dbmaj7 Eb7','Bbm7 Eb7 Cm7 Fm7',
'3d 2e 1q|5q 6e 5e 3q|4d 3e 2q|3h Rq',
'6q 8e 7e 6q|5d 4e 3q|2e 3e 4q 5q|2q 1h','intimate')
T('Under the Floorboards','Scary','A harmless shadow seems enormous in the dark; listening replaces panic.',88,'D','phrygian','4/4','stealth','ghost','glass','pad',
'Dm Ebmaj7 Dm Bbmaj7','Gm Ebmaj7 Bb7 A7',
'1h Re 2e Rq|3q 2q Rq 1q|5d 4e 2q Rq|6h 5q Rq',
'4q Re 5e 6h|2d 3e 2q 1q|6e 5e 4q Rq 2q|7q 2q 1h','suspense')
T('The Water Is Rising','Danger','Quick decisions protect the habitat; an uneven pulse steadies as help arrives.',154,'F#','minor','7/8','urgent','saw','brass','pluck',
'F#m D E C#7','Bm D E C#7',
'1e 1e 5e 4e 3e 2e 1e|6q 5e 3q 2e 1e|7e 7e 5e 4e 2q Re|3e 2e 1e 7e 5d',
'4e 5e 6q 8e 7e 6e|6q 5e 3q 2q|7e 8e 9e 7e 5e 4e 2e|5q 7e 2q 1q','action')
T('Small Paws, Big Courage','Battle','An imagined friendly challenge: springy bass, quick feints, and a bright heroic answer.',164,'G','minor','4/4','battle','square','brass','organ',
'Gm Eb F D7','Cm Eb Bb D7',
'1e 5e 1e 3e 4q 5q|6e 5e 3e 2e 1q 3q|7e 2e 4q 5e 4e 2q|7d 5e 2q Rq',
'4q 6e 8e 7q 6q|5e 3e 6q 8q 7q|3e 5e 8q 9e 8e 7q|5e 4e 2q 7q 1q','action')
T('No One Gets Left Behind','Resolve','The rescue reaches its hardest moment; a nervous ostinato becomes collective courage.',146,'C','minor','4/4','battle','brass','saw','pad',
'Cm Ab Bb G7','Fm Ab Eb G7',
'1d 5e 4e 3e 2q|6q 5e 6e 8q 7q|7d 5e 4q 2q|3e 2e 7q 5h',
'4e 6e 8q 7e 6e 5q|6d 8e 10q 9q|8q 5q 3e 4e 5q|7q 2q 1h','action')
T('We Did It, Together','Joy','The work is done, the animals are safe, and every answering voice gets a moment.',136,'F','major','4/4','celebrate','brass','bubble','pluck',
'F6 Bb6 C7 F6','Dm7 Gm7 Bbmaj7 C9',
'1q 3e 5e 8q 6q|4e 6e 8q 9q 8q|7e 5e 2q 3q 2q|1h 5q Rq',
'6q 8q 10e 9e 8q|4d 6e 5q 3q|6e 5e 4q 3q 2q|5q 7q 8h','celebration')
T('Sorry Is a Beginning','Forgiveness','Mom and Hero share a quiet moment of care; an unresolved line finds a gentle answer.',70,'Db','major','3/4','lullaby','velvet','flute','epiano',
'Dbmaj9 Bbm7 Gbmaj7 Ab7','Ebm7 Ab7 Fm7 Bbm7',
'3h 2q|1d 3e 5q|4h 3q|2q Rq 5q',
'6q 5e 4e 3q|2d 3e 4q|5q 6q 5q|2q 1h','intimate')
T('New Leaves After Rain','Recovery','Care becomes routine again; the same few hopeful notes return with stronger roots.',96,'B','major','6/8','lullaby','reed','marimba','epiano',
'Bmaj9 G#m7 Emaj7 F#7','C#m7 F#7 D#m7 G#m7',
'1q 2e 3e 5q|6d 5e 3q|4q 6e 5e 3q|2q 3h',
'6e 7e 8q 9q|7q 5e 4e 3q|6d 5e 4q|2q 1h')
T('Little Root, Living Universe','Wonder','Inside the terrarium, tiny independent patterns turn into one balanced ecosystem.',90,'F','lydian','4/4','ambient','glass','bubble','pad',
'Fmaj9 G Em7 Am7','Dm9 G Cmaj9 Fmaj9',
'1q 5q 4h|2d 3e 5q 7q|7h 6q 5q|3q 2e 1e 6h',
'6q 8e 9e 10h|9d 7e 5q 4q|3e 5e 7q 8q 9q|8h 5h','dream')
T('Midnight Tank Watch','Chill','The room is asleep; the tank light turns small movements into constellations.',72,'D','dorian','4/4','lofi','velvet','glass','epiano',
'Dm9 G13 Cmaj9 Am9','Em7 A7 Dm9 G13',
'3d 5e 6q Rq|5q 4e 3e 2h|7d 6e 5q 3q|2q 1h Rq',
'2e 3e 5q 7q 6q|5h 3q 2q|1d 4e 6q 5q|3q 2q 1h','dream')
T('Critter, One Little Heart','Delight','The first kind response to a tank photo becomes a tiny dance around the room.',118,'E','major','4/4','funk','bubble','square','epiano',
'Emaj9 C#m7 Amaj7 B9','F#m7 B9 G#m7 C#m7',
'Re 3e 5q 6e 5e 3q|2e Re 1q 3q 5q|6q 8e 7e 6q 4q|5d 3e 2q Rq',
'4e 5e 6q 8q 6q|7e 6e 5e Re 3h|3q 2e 3e 5q 6q|5q 2q 1h')
T('Paper Boats to Liarsville','Wistfulness','A daydream of the neighboring town, carried by water and an unhurried melody.',100,'A','major','6/8','lullaby','flute','reed','pluck',
'Amaj9 F#m7 Dmaj7 E7','Bm7 Dmaj7 C#m7 E7',
'5q 3e 2e 1q|6q 5d 3e|4q 3e 2e 4q|5h 2q',
'2e 4e 6q 8q|6d 5e 4q|3q 5e 7e 6q|5q 2q 1q')
T('Bicycle Basket Sky','Freedom','A future ride imagined with wind in your sleeves and nowhere urgent to be.',142,'D','major','4/4','drive','saw','flute','pluck',
'D6 A Bm7 Gmaj7','Em7 G D A7',
'5e 6e 8q 7q 5q|3e 2e 5q 4q 2q|6e 5e 3q 2e 3e 5q|4h 3q 2q',
'2q 4e 5e 6q 8q|6q 5q 3e 4e 6q|5d 3e 2q 1q|2e 3e 5q 7h')
T('Footprints Where Nobody Went','Mystery','An imagined cave trail: an odd meter asks a question that never quite repeats.',94,'B','dorian','5/4','curious','ghost','marimba','pad',
'Bm9 E9 Dmaj7 Amaj7','Gmaj7 Em9 F#m7 F#7',
'1q Rq 3e 4e 6q 5q|2h 4q 3q Rq|3q 5e 7e 6h 5q|7q 6q 5q 2h',
'6q 8q 7e 6e 5q 4q|4d 3e 2q 1h|5q Rq 7e 6e 5q 3q|2h 7q 1h','suspense')
T('Snow Globe Promise','Tenderness','A winter daydream: bright specks of snow, warm hands, and a promise to return.',82,'Gb','major','3/4','waltz','musicbox','glass','pad',
'Gbmaj9 Ebm7 Bmaj7 Db7','Abm7 Db7 Bbm7 Ebm7',
'8q 7e 6e 5q|6h 3q|4q 6e 5e 3q|2h Rq',
'6q 8q 9q|7d 5e 4q|3q 5e 6e 8q|2q 1h','dream')
T('Salt Air, No Hurry','Contentment','A beach daydream with soft syncopation; the tide leaves enough space to breathe.',92,'C','mixolydian','4/4','bossa','marimba','flute','epiano',
'C9 Fmaj9 Bbmaj7 C9','Dm9 G9 Fmaj7 C6',
'3d 5e Rq 6q|4q 3e 2e 1h|7d 6e 5q 4q|3q 2q 1q Rq',
'2e 4e 6q 5d 4e|5q 3q 2e 1e 2q|6q 5e 4e 3q 2q|1h 3q 5q','dream')
T('Porch Radio, Summer 2004','Nostalgia','An imagined old radio plays while afternoon shadows lengthen across the porch.',74,'Eb','major','4/4','lofi','reed','velvet','epiano',
'Ebmaj9 Cm9 Abmaj9 Bb9','Fm9 Bb9 Gm7 Cm9',
'5d 3e 2q 1q|6h 5q Rq|4e 3e 2q 3d 5e|2h 5q Rq',
'6q 8q 7e 6e 5q|4d 3e 2h|3q 5e 6e 8q 7q|6q 5q 3h','intimate')
T('Fireflies Above the Filter','Peace','Little lights answer each other; the day ends without needing one more achievement.',66,'G','lydian','4/4','ambient','glass','musicbox','pad',
'Gmaj9 A6 Bm7 Gmaj9','Em9 A9 Dmaj9 Gmaj9',
'5h 4q Rq|3q 2q 5h|7d 6e 5q 3q|1h Rh',
'6h 8q 9q|7q 5q 4h|3d 5e 6q 5q|4q 2q 1h','dream')
T('Tomorrow Has Your Name','Gratitude','The album closes on a new melody that welcomes the title motif home, with friends answering.',102,'D','major','4/4','lofi','flute','reed','epiano',
'Dmaj9 Bm9 Gmaj9 A9','Em9 A9 F#m7 Bm7',
'5q 3e 2e 1d 2e|3h 6q 5q|4d 6e 5q 3q|2q Rq 3q 5q',
'6q 8e 9e 10q 9q|7d 6e 5q 4q|3e 4e 6q 5q 3q|2q 3q 1h','finale')

# Individually written answers turn the four-bar questions into eight-bar periods.
# These replace bars seven/eight in A and B, rather than simply looping the hook.
ANSWERS=[
('6q 5e 4e 3q 2q|5q 7q 2h','8q 6q 5e 4e 3q|2q 7q 1h'),
('6d 5e 4q 3q|2q 5q 1h','4q 3q 2e 3e 5q|3h 1h'),
('6e Re 5e 4e 3q 2q|5e 3e 2q 1q Rq','8e 6e 5q 4e 3e 2q|5e Re 2e 3e 1h'),
('4q 5e 6e 8q 6q|5d 2e 1h','8q 6e 5e 4q 3q|2e 3e 5q 1h'),
('6q 8e 7e 6q 5q|4e 3e 2q 1h','5q 6q 8e 6e 5q|4q 2q 1h'),
('6e 7e 8q 9q 7q|5d 3e 1h','8q 7e 6e 5q 3q|4e 3e 2q 1h'),
('6q 5e 4e 3q 2q 1q|2q 4q 5q 3h','9q 8q 6e 5e 4q 3q|2h 4q 3q 1q'),
('6e 5e 4q 3q|2e 3e 1h','8q 6e 5e 4q|3q 2q 1q'),
('6e Re 8e 6e 5q 4q|3e 2e 1q Rq 5q','8e 7e 6e 5e 3q 4q|2q 3q 1h'),
('6q 8e 7e 5q 4q|3e 2e 7q 1h','8q 6q 5e 4e 3q|2e 3e 2q 1h'),
('6h 5q 3q|2d 7e 1h','5q 3q 2e 3e 4q|2h 1h'),
('6d 5e 3q|2q 1h','5q 4e 3e 2q|3q 1h'),
('2q Rq 3e 2e 1q|6q 5q Rh','6h 5e 4e 2q|2q 1h Rq'),
('7e 8e 7e 5e 4e 2e 1e|3q 2e 7e 1d','8e 7e 6e 5e 4e 3e 2e|7q 2e 1h'),
('8e 7e 5q 6e 5e 3q|4e 3e 2q 1h','8q 9e 8e 7q 5q|4e 3e 2q 1h'),
('8q 7e 6e 5q 4q|3e 2e 7q 1h','10q 8q 7e 6e 5q|4q 2q 1h'),
('6e 5e 4q 3q 2q|1q 3e 5e 8h','8q 6e 5e 4q 3q|2q 5q 8h'),
('4q 5q 3q|2q 1h','6d 5e 3q|2q 1h'),
('6q 8e 6e 5q|2q 1h','8q 6e 5e 4q|3q 1h'),
('6h 4q 3q|2q 5q 1h','8q 6q 4e 3e 2q|4h 1h'),
('7q 6e 5e 3q 2q|4q 3q 1h','5d 4e 3q 2q|1h Rh'),
('8e 7e 6q 5e Re 3q|4q 2q 1h','8q 6e 5e 4q 3q|2e 3e 5q 1h'),
('6q 5e 4e 3q|2q 1h','6q 4e 3e 2q|3q 1h'),
('8q 6e 5e 3q 4q|5e 3e 2q 1h','8q 7q 6e 5e 4q|3q 2q 1h'),
('6h 5q 3e 2e 1q|2q 4q 6q 5h','8q 7e 6e 5q 3q 2q|4h 2q 1h'),
('6q 5q 3q|2q 1h','8q 6e 5e 4q|3q 1h'),
('6d 5e 4q 3q|2q 3q 1h','5q 4e 3e 2q 1q|3h 1h'),
('6q 5e 4e 3q 2q|5q 3q 1h','8h 6q 5q|4q 2q 1h'),
('6h 5q 3q|4q 2q 1h','8h 6q 5q|4q 3q 1h'),
('6q 8e 6e 5q 3q|2d 3e 1h','8q 6q 5e 4e 3q|2q 5q 1h')]
assert len(ANSWERS)==len(TRACKS)==30
for track,(a,b) in zip(TRACKS,ANSWERS):
    track['answerA']=a.split('|');track['answerB']=b.split('|')
