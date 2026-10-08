"""Thirty new scores. Absolute pitches, locally authored rhythms and individual forms.
No MUSIC.01 catalogue, motifs or arrangement code is imported.
Bars are zero-based; omitted beats are rests, never automatic filler.
"""
from score import Piece

def one():
    s=Piece(1,'The First Open Window','Hope','E major',78,'4/4',28,'Morning arrives before the plans do. A small room starts to feel like a beginning.','Felt-piano miniature; three-note questions, long silences, a rising middle register.')
    p=s.part('Window melody','felt',.88,.48,.2);l=s.part('Left hand','felt',.63,.4,.18);g=s.part('Sun on the sill','sine',.28,.65,.35)
    s.mark(0,'A question');s.mark(8,'The room brightens');s.mark(18,'An open door')
    s.line(p,0,'R:1 B3:1 E4:1 F#4:1 | G#4:2 R:2 | R:2 F#4:1 E4:1 | B3:3 | R:1 C#4:1 E4:1 G#4:1 | F#4:2 E4:1 | D#4:1 F#4:1 B4:1 | G#4:3',66,.94)
    s.line(l,0,'E2:3 | B2+E3:3 | C#3:3 | G#2+B2:3 | A2:3 | E3+A3:3 | B2+F#3:3 | E3+B3:3',50,.98)
    s.line(p,8,'B4:1 G#4:1 F#4:2 | E4:2 B3:1 | A3:1 C#4:1 E4:1 G#4:1 | F#4:3 | G#4:1 B4:1 C#5:2 | B4:1 G#4:1 E4:2 | D#4:1 E4:1 F#4:1 A4:1 | G#4:2 F#4:1 D#4:1 | E4:3 | R:4',72,.92)
    s.blocks(l,8,'G#2 E3 B3 | E2 B2 E3 | A2 E3 | B2 D#3 A3 | C#3 E3 | A2 E3 | F#2 C#3 A3 | B2 D#3 | E2 B2 |',v=50)
    s.line(g,12,'E5:4 | R:4 | R:4 | F#5:3 | E5:4',42,1)
    s.line(p,18,'R:1 B3:1 E4:1 G#4:1 | F#4:2 E4:1 | R:1 A4:1 G#4:1 E4:1 | B3:3 | C#4:2 E4:1 F#4:1 | G#4:2 B4:1 | A4:1 G#4:1 F#4:1 D#4:1 | E4:3 | B3:1 E4:3 | R:4',60,.96)
    s.blocks(l,18,'E2 B2 | C#3 G#3 | A2 E3 | E3 G#3 | F#2 C#3 | C#3 E3 | B2 F#3 | E3 G#3 | E2 B2 E3 |',v=43)
    return s

def two():
    s=Piece(2,'Soup Cooling on the Table','Home','F major',66,'3/4',32,'Mom has left a bowl for you. Nothing needs to be won tonight.','An electric-piano waltz with a singing inner voice and no percussion.')
    p=s.part('Right hand','epiano',.8,.58,.12);l=s.part('Left hand','epiano',.62,.32,.1)
    s.mark(0,'The kitchen');s.mark(12,'A familiar voice');s.mark(24,'Stay a little')
    a='A4:1 G4:.5 F4:.5 C4:1 | D4:2 F4:1 | E4:1 G4:1 C5:1 | A4:2 | G4:1 Bb4:1 A4:1 | F4:1 D4:1 C4:1 | E4:2 G4:1 | F4:2'
    h='F2 C3 A3 | D3 A3 F4 | C3 G3 Bb3 | F2 C3 A3 | Bb2 F3 D4 | G2 D3 Bb3 | C3 G3 Bb3 | F2 C3 A3'
    s.line(p,0,a,67,.92);s.arp(l,0,h,[(0,0,.9),(1,1,.8),(2,2,.8)],49)
    s.line(p,8,'C4:1 F4:2 | G4:1 A4:2 | Bb4:1 G4:1 E4:1 | C4:2',59)
    s.line(l,8,'A2+C3:2 | D3+F3:2 | C3+Bb3:2 | C3+G3:2',44)
    s.line(p,12,'D5:1 C5:.5 Bb4:.5 A4:1 | G4:2 F4:1 | E4:1 G4:1 A4:1 | C5:2 | Bb4:1 D5:1 C5:1 | A4:1 F4:1 D4:1 | E4:1 G4:1 Bb4:1 | A4:2 | G4:1 F4:1 E4:1 | D4:2 F4:1 | G4:1 E4:1 C4:1 | F4:2',70,.93)
    s.arp(l,12,'Bb2 F3 A3 | G2 D3 Bb3 | C3 G3 Bb3 | A2 E3 G3 | Bb2 F3 D4 | D3 A3 C4 | C3 E3 Bb3 | F2 C3 A3 | A2 C3 F3 | G2 D3 Bb3 | C3 G3 Bb3 | F2 C3 A3',[(0,0,1.4),(1.5,1,.65),(2.25,2,.6)],48)
    s.line(p,24,a,57,.96);s.blocks(l,24,h,dur=2.5,v=40)
    return s

def three():
    s=Piece(3,'A Button with Feet','Cute','D major',116,'2/4',48,'A tiny critter steals a button and proudly carries it three steps.','Dry marimba hops; a low triangle answers in the gaps. Mostly two voices.')
    m=s.part('Tiny hops','marimba',.85,.55,.04);b=s.part('Padded footsteps','triangle',.53,.38,.02)
    s.mark(0,'Three little steps');s.mark(16,'The button rolls');s.mark(32,'A very small victory')
    a='F#5:.5 R:.5 A5:.5 F#5:.5 | E5:.5 D5:.5 R:1 | F#5:.5 A5:.25 B5:.25 A5:.5 | E5:1 R:1 | G5:.5 F#5:.5 E5:.5 R:.5 | D5:.5 F#5:.5 A5:.5 | G5:.5 E5:.5 C#5:.5 | D5:1'
    for bar in [0,8,32]:s.line(m,bar,a,68 if bar!=8 else 59,.65)
    for bar in [0,8,32]:s.line(b,bar,'D3:.5 R:1 A3:.5 | R:1 D4:.5 | B2:.5 R:1 F#3:.5 | A2:.5 R:.5 C#4:.5 | G3:.5 R:1 B3:.5 | F#3:.5 R:1 A3:.5 | A2:.5 R:.5 E3:.5 | D3:1',55,.6)
    s.line(m,16,'A5:.25 G5:.25 F#5:.25 E5:.25 D5:.5 | R:.5 F#5:.5 G5:.5 A5:.5 | B5:.5 G5:.5 E5:.5 | A5:1 | F#5:.25 E5:.25 D5:.5 R:1 | E5:.5 F#5:.5 A5:.5 | G5:.5 E5:.5 C#5:.5 | D5:1',63,.6)
    s.line(b,16,'D3:1 | F#3:1 | E3:1 | A3:1 | B3:.5 A3:.5 | G3:.5 F#3:.5 | E3:.5 A2:.5 | D3:1',51,.65)
    s.line(m,24,'R:2 | D5:.5 R:.5 F#5:.5 | R:2 | E5:.5 R:.5 A5:.5 | R:2 | G5:.5 F#5:.5 E5:.5 | R:1 C#5:.5 | D5:1',53)
    s.line(b,24,'D4:.5 F#4:.5 A4:.5 | D3:1 | E4:.5 G4:.5 B4:.5 | A2:1 | G4:.5 B4:.5 D5:.5 | G3:1 | A3:1 | D3:1',53)
    s.line(m,40,'F#5:.5 A5:.5 D6:.5 | B5:.5 A5:.5 F#5:.5 | G5:.5 E5:.5 | A5:1 | F#5:.5 E5:.5 D5:.5 | R:2 | D5:.5 F#5:.5 A5:.5 | D5:1',66,.7)
    s.line(b,40,'D3:1 | B2:1 | G3:1 | A2:1 | D3:1 | R:2 | A3:.5 F#3:.5 | D3:1',53)
    s.drums(16,4,[(1.5,75,-23)],50)
    return s

def four():
    s=Piece(4,'Kaid Takes the Other Handle','Friendship','Bb major',92,'4/4',24,'The box is too heavy alone. Kaid takes the other side without being asked.','A square-wave and reed duet: neither voice owns the whole tune.')
    a=s.part('You','square',.61,.32,.09);b=s.part('Kaid','reed',.65,.68,.09);l=s.part('Shared weight','upright',.66,.5,.03)
    s.mark(0,'One side');s.mark(8,'The other side');s.mark(16,'Together')
    s.line(a,0,'Bb4:1 D5:.5 C5:.5 F5:1 | R:4 | G5:1 F5:1 D5:1 | R:4 | Eb5:1 D5:.5 C5:.5 Bb4:1 | R:4 | A4:1 C5:1 F5:1 | R:4',67)
    s.line(b,0,'R:4 | D4:1 F4:.5 G4:.5 Bb4:1 | R:4 | A4:1 G4:1 F4:1 | R:4 | G4:1 Eb4:1 C4:1 | R:4 | D4:1 C4:1 Bb3:1',72)
    s.line(a,8,'R:4 | G5:1 F5:1 Eb5:1 | R:4 | D5:1 C5:1 A4:1 | R:4 | Bb4:1 D5:1 G5:1 | F5:1 Eb5:1 C5:1 | D5:2',64)
    s.line(b,8,'C5:1 Bb4:.5 A4:.5 G4:1 | R:4 | A4:1 C5:1 Eb5:1 | R:4 | G4:1 Bb4:.5 A4:.5 G4:1 | R:4 | A4:1 G4:1 F4:1 | Bb4:2',70)
    s.line(a,16,'Bb4:1 D5:.5 C5:.5 F5:1 | G5:1 F5:1 D5:1 | Eb5:1 G5:1 F5:1 | D5:2 C5:1 | Bb4:1 A4:.5 Bb4:.5 D5:1 | G5:1 F5:1 Eb5:1 | D5:1 C5:1 A4:1 | Bb4:3',71)
    s.line(b,16,'F4:2 D4:1 | Eb4:1 F4:1 G4:1 | G4:2 A4:1 | Bb4:1 A4:1 F4:1 | G4:1 F4:1 D4:1 | Eb4:2 G4:1 | F4:1 Eb4:1 C4:1 | D4:3',61)
    for start in [0,8,16]:s.line(l,start,'Bb2:2 F3:1 | G2:2 D3:1 | Eb3:2 Bb2:1 | F2:2 C3:1 | Eb3:2 G2:1 | C3:2 G2:1 | F2:2 A2:1 | Bb2:3',57)
    return s

def five():
    s=Piece(5,'Rootport on a Tuesday','Belonging','G major',104,'4/4',32,'Shop doors open at different times. Everyone still finds the same unhurried rhythm.','A syncopated organ trio, walking bass, and quiet brushed time.')
    m=s.part('Corner-shop organ','organ',.61,.58,.06);b=s.part('Walking between shops','upright',.78,.47,.03);p=s.part('Porch plucks','pluck',.46,.25,.07)
    s.mark(0,'Opening the shutters');s.mark(8,'The little square');s.mark(20,'Afternoon regulars')
    a='R:.5 B4:.5 D5:1 E5:.5 D5:1 | B4:1 A4:.5 G4:1 R:1.5 | A4:.5 C5:1 E5:.5 D5:1 | B4:2 | R:.5 C5:.5 E5:1 G5:.5 E5:.5 D5:1 | B4:1 G4:1 E4:1 | A4:1 C5:.5 B4:.5 A4:1 | G4:2'
    s.line(m,0,a,69,.78);s.line(m,8,a,62,.83)
    s.line(m,16,'F#5:1 A5:.5 G5:.5 F#5:1 | E5:1 D5:1 B4:1 | C5:.5 E5:.5 G5:1 A5:1 | F#5:2 D5:1',71)
    s.line(m,20,'B4:.5 D5:.5 G5:1 E5:.5 D5:.5 B4:1 | A4:1 B4:.5 C5:.5 D5:1 | C5:1 A4:1 E4:1 | G4:2 | E5:.5 G5:.5 B5:1 A5:.5 G5:.5 E5:1 | D5:1 B4:1 G4:1 | A4:.5 B4:.5 C5:1 F#4:1 | G4:2 | R:4 | B4:1 A4:1 G4:1 | F#4:1 A4:1 D5:1 | G4:3',68)
    walk='G2:1 B2:1 D3:1 F#3:1 | E3:1 B2:1 G2:1 F#2:1 | A2:1 C3:1 E3:1 F#3:1 | G3:1 D3:1 B2:1 G2:1 | C3:1 E3:1 G3:1 F#3:1 | E3:1 D3:1 B2:1 G2:1 | D3:1 A2:1 C3:1 F#2:1 | G2:2 D3:1'
    for bar in [0,8,20]:s.line(b,bar,walk,57,.64)
    s.line(b,16,'D3:1 F#3:1 A3:1 C3:1 | E3:1 G3:1 B3:1 G3:1 | C3:1 E3:1 G3:1 A3:1 | D3:1 C3:1 A2:1 F#2:1',57,.66)
    s.line(b,28,'C3:2 | G2:2 | D3:2 | G2:3',50)
    for bar in [8,20]:s.arp(p,bar,'B3 D4 G4 | B3 E4 G4 | A3 C4 E4 | B3 D4 G4 | C4 E4 G4 | B3 E4 G4 | A3 C4 F#4 | B3 D4 G4',[(.75,0,.2),(1.5,1,.25),(2.75,2,.3)],47)
    s.drums(8,20,[(0,42,-25),(1,37,-16),(2,42,-25),(3,37,-20)],56)
    return s

def six():
    s=Piece(6,'Mossway beyond the Map','Adventure','A major',138,'6/8',48,'The road bends out of sight. You go far enough to find a view that belongs to you.','A compound-meter travelling tune with picked bass and an upward pulse arpeggio.')
    m=s.part('Trail song','triangle',.88,.53,.12);a=s.part('Quick sunlight','pulse',.37,.7,.1);b=s.part('Boots on the path','pluck',.7,.35,.04)
    s.mark(0,'Leaving the signpost');s.mark(16,'The hill opens');s.mark(32,'Keep going')
    A='E5:.5 A5:1 B5:.5 A5:.5 E5:.5 | F#5:1 E5:.5 C#5:1 | D5:.5 F#5:.5 A5:.5 B5:1 | G#5:1 E5:.5 B4:1 | C#5:.5 E5:.5 A5:.5 C#6:1 | B5:1 A5:.5 F#5:1 | G#5:.5 A5:.5 B5:.5 E5:1 | A5:2'
    for at in [0,8,32]:s.line(m,at,A,75 if at!=8 else 65,.82)
    B='C#6:1 B5:.5 A5:.5 G#5:.5 F#5:.5 | E5:1 C#5:.5 F#5:1 | D5:.5 E5:.5 F#5:.5 A5:.5 B5:.5 C#6:.5 | B5:2 | A5:.5 F#5:.5 D5:.5 E5:1 | C#5:1 E5:.5 A5:1 | G#5:.5 B5:.5 E6:.5 D6:.5 C#6:.5 B5:.5 | A5:2'
    s.line(m,16,B,74);s.line(m,24,'F#5:1 E5:.5 D5:1 | C#5:2 | D5:1 A4:.5 B4:1 | E5:2 | R:3 | E5:.5 G#5:.5 B5:.5 A5:1 | G#5:1 F#5:.5 E5:1 | B4:2',60)
    s.line(m,40,B,78)
    H='A2 E3 A3 | F#2 C#3 F#3 | D3 A3 D4 | E3 B3 E4 | A2 E3 C#4 | D3 A3 F#4 | E3 B3 G#4 | A2 E3 A3'
    for at in [0,8,16,32,40]:s.arp(b,at,H,[(0,0,.8),(1.5,1,.5),(2.5,2,.25)],65)
    for at in [8,16,40]:s.arp(a,at,'A4 C#5 E5 | A4 C#5 F#5 | A4 D5 F#5 | G#4 B4 E5 | A4 C#5 E5 | A4 D5 F#5 | G#4 B4 E5 | A4 C#5 E5',[(0,0,.2),(.5,1,.2),(1,2,.3),(1.5,1,.2),(2.5,2,.2)],44)
    s.line(b,24,'D3:2 | A2:2 | B2:2 | E3:2 | R:3 | E3:2 | B2:2 | E2:2',51)
    s.drums(32,16,[(0,36,0),(1,42,-22),(1.5,38,-13),(2.5,42,-25)],61)
    return s

def seven():
    s=Piece(7,'The Page with No Answer','Curiosity','B Lydian',88,'4/4',26,'A notebook question leads to another question, and that feels like progress.','Bright fourths and a raised fourth; bell phrases of three, five and six bars over held plucks.')
    m=s.part('Questions in the margin','bell',.66,.62,.22);p=s.part('Pencil marks','nylon',.7,.34,.08)
    s.mark(0,'A question mark');s.mark(6,'A second possibility');s.mark(16,'More to discover')
    s.line(m,0,'B4:1 E#5:1 F#5:1 | R:2 D#5:1 | C#5:2 | F#5:1 B5:1 A#5:1 | G#5:2 E#5:1 | D#5:2',59,.9)
    s.line(m,6,'C#5:.5 D#5:.5 F#5:1 A#5:1 | E#5:2 | R:1 G#5:1 F#5:1 | D#5:1 C#5:2 | B4:3',63)
    s.line(m,11,'R:2 F#5:1 | E#5:1 D#5:1 C#5:1 | G#5:2 | F#5:.5 E#5:.5 D#5:1 | C#5:2',53)
    s.line(m,16,'B4:1 E#5:1 F#5:1 | A#5:1 F#5:1 C#5:1 | D#5:2 G#5:1 | E#5:3 | C#6:1 B5:1 F#5:1 | E#5:2 D#5:1 | C#5:2 | R:2 F#5:1 | D#5:1 C#5:1 B4:1 | B4:3',62)
    s.blocks(p,0,'B2 F#3 C#4 | | B2 F#3 D#4 | | C#3 G#3 E#4 |',dur=7,v=50)
    s.blocks(p,6,'D#3 A#3 F#4 | | C#3 G#3 E#4 | | B2 F#3 D#4',dur=3,v=49)
    s.line(p,11,'B3:.5 C#4:.5 D#4:1 | C#4:1 E#4:1 G#4:1 | G#3:1 D#4:1 | F#3:1 C#4:1 | B2+F#3:3',54)
    s.blocks(p,16,'B2 F#3 C#4 | | G#2 D#3 B3 | | C#3 G#3 D#4 | | B2 F#3 D#4 | | B2 F#3 C#4 |',dur=7,v=45)
    return s

def eight():
    s=Piece(8,'Five Steps and a Somersault','Playfulness','C Mixolydian',128,'5/8',56,'A critter tries a new way of walking. The fifth step always becomes a tumble.','A lopsided 3+2 pulse dance with mallet answers and wooden clicks.')
    m=s.part('Crooked grin','pulse',.59,.57,.02);b=s.part('Round little replies','marimba',.75,.35,.04)
    s.mark(0,'Try counting this');s.mark(20,'Upside down');s.mark(40,'Land on your feet')
    a='G4:.5 C5:.5 E5:.5 D5:.5 C5:.5 | Bb4:.5 G4:.5 R:.5 C5:1 | A4:.5 C5:.5 D5:.5 E5:1 | G5:.5 E5:.5 D5:.5 C5:1'
    for bar in [0,4,12,16,40,44]:s.line(m,bar,a,66,.62)
    for bar in [0,4,8,12,16,40,44,48]:s.line(b,bar,'C3:.5 R:1 G3:.5 | Bb2:.5 R:1 F3:.5 | F3:.5 R:1 A3:.5 | C3:.5 G3:.5 C4:.5',60,.62)
    s.line(m,8,'R:2.5 | R:1 E5:.5 D5:.5 C5:.5 | R:2.5 | G5:.5 E5:.5 C5:.5',61)
    s.line(m,20,'E5:.25 F5:.25 G5:.5 Bb5:.5 A5:.5 G5:.5 | E5:1 D5:.5 C5:.5 Bb4:.5 | A4:.5 C5:1 G4:.5 A4:.5 | Bb4:1 G4:.5 C5:1 | R:2.5 | C5:.5 Bb4:.5 G4:.5 E4:1 | F4:.5 A4:.5 C5:.5 D5:1 | E5:1 C5:1',67,.64)
    s.line(b,20,'C3:.5 E3:.5 G3:.5 | Bb2:.5 D3:.5 F3:.5 | F3:.5 A3:.5 C4:.5 | C3:.5 G3:.5 Bb3:.5 | C4:.5 E4:.5 G4:.5 Bb4:1 | C3:1 | F3:1 | C3:1',60)
    s.line(b,28,'C4:.5 D4:.5 E4:.5 G4:1 | Bb4:.5 G4:.5 E4:.5 C4:1 | F4:.5 A4:.5 C5:.5 A4:1 | G4:.5 E4:.5 D4:.5 C4:1',65)
    s.line(m,32,'C4:.5 R:1 G4:1 | Bb3:.5 R:1 F4:1 | A3:.5 R:1 F4:1 | C4:.5 R:1 E4:1 | R:2.5 | G4:.5 C5:.5 E5:.5 | R:2.5 | D5:.5 E5:.5 G5:.5',56)
    s.line(m,48,'G5:.5 E5:.5 C5:.5 Bb4:1 | A4:.5 F4:.5 C5:.5 D5:1 | E5:.5 G5:.5 C6:.5 G5:1 | E5:1 C5:1 | R:2.5 | C5:.5 R:.5 G4:.5 | E4:.5 G4:.5 C5:.5 | C4:2',64)
    s.drums(12,8,[(0,75,-15),(1.5,37,-20)],55);s.drums(40,12,[(0,75,-18),(1.5,37,-22)],55)
    return s

def nine():
    s=Piece(9,'Seven Screws for a Tiny Roof','Craft','Eb major',96,'7/8',36,'Measure, fit, listen, try again. Something handmade becomes a home.','A 2+2+3 mallet machine; the melody is built from the work rhythm, then the tools fall quiet.')
    m=s.part('Worktable vibraphone','vibes',.78,.57,.1);k=s.part('Measured chords','epiano',.51,.32,.06);b=s.part('Foundation','sub',.72,.5,.01)
    s.mark(0,'Measure twice');s.mark(12,'It fits');s.mark(28,'Set the tools down')
    a='G4:.5 Bb4:.5 R:.5 Eb5:.5 D5:.5 Bb4:1 | Ab4:.5 G4:.5 F4:1 G4:.5 Eb4:1 | F4:.5 Ab4:.5 C5:.5 Bb4:.5 Ab4:.5 G4:1 | F4:1 D4:.5 Eb4:2'
    for at in [0,4,20,24]:s.line(m,at,a,68,.7)
    s.line(m,8,'Bb4:1 Eb5:.5 F5:.5 G5:1 | F5:.5 D5:.5 Bb4:.5 Ab4:1 G4:1 | F4:.5 Ab4:.5 C5:.5 D5:.5 F5:1 | Eb5:2',72)
    s.line(m,12,'G5:1 F5:.5 Eb5:1 Bb4:1 | C5:.5 Eb5:.5 G5:.5 F5:.5 Eb5:1 | Ab5:1 G5:.5 F5:1 C5:1 | D5:.5 F5:.5 Ab5:.5 G5:.5 F5:1 | Eb5:.5 D5:.5 C5:.5 Bb4:.5 G4:1 | Ab4:.5 C5:.5 Eb5:.5 F5:.5 G5:1 | F5:1 D5:1 Bb4:.5 | Eb5:2',71)
    H='Eb3 G3 Bb3 | C3 Eb3 G3 | Ab2 C3 Eb3 | Bb2 D3 Ab3'
    for at in [0,4,8,12,16,20,24]:
        s.arp(k,at,H,[(0,0,.4),(1,1,.4),(2,2,1)],52)
        s.line(b,at,'Eb2:1 R:1 Bb2:1 | C2:1 R:1 G2:1 | Ab2:1 R:1 Eb3:1 | Bb1:1 R:1 F2:1',55,.75)
    s.line(m,28,'Bb4:1 G4:1 Eb4:1 | R:3.5 | Ab4:1 G4:.5 F4:1 | R:3.5 | G4:.5 Bb4:.5 Eb5:1 | D5:.5 Bb4:.5 F4:1 | Eb4:2 | R:3.5',56,.96)
    s.blocks(k,28,'Eb3 G3 | | Ab3 C4 | | G3 Bb3 | Bb2 Ab3 | Eb3 G3 Bb3 |',v=44)
    return s

def ten():
    s=Piece(10,'Try Again, with Both Hands','Determination','D minor',152,'4/4',40,'The first attempt failed. You count in again, a little steadier this time.','A dry saw riff that sheds notes as it finds confidence; square bass and low toms.')
    m=s.part('Steady nerve','saw',.66,.58,.07);b=s.part('Square foundation','square',.7,.45,.02);h=s.part('Short support','brass',.38,.3,.08)
    s.mark(0,'Count in');s.mark(8,'The second attempt');s.mark(24,'Find the rhythm');s.mark(36,'Hold steady')
    riff='D4:.5 D4:.25 F4:.25 A4:.5 G4:.5 F4:1 E4:.5 | D4:.5 R:.5 C4:.5 D4:.5 F4:1 A4:.5 | Bb4:.5 A4:.5 G4:.5 F4:.5 E4:1 G4:.5 | A4:2 R:.5 C#4:.5 D4:.5'
    for at in [0,4,8,12,24,28]:s.line(m,at,riff,76 if at<8 else 82,.65)
    s.line(m,16,'F5:1 E5:.5 D5:.5 C5:1 A4:1 | Bb4:1 D5:1 F5:1 E5:1 | G5:1 F5:.5 E5:.5 D5:1 Bb4:1 | A4:3 | F4:1 A4:1 D5:2 | E5:1 D5:1 Bb4:2 | A4:.5 C#5:.5 E5:1 G5:1 E5:1 | D5:3',80)
    bass='D2:.5 R:.5 D3:.5 A2:.5 D2:.5 R:.5 A2:.5 C3:.5 | C2:.5 R:.5 G2:.5 C3:.5 C2:.5 R:.5 E2:.5 G2:.5 | Bb1:.5 R:.5 F2:.5 Bb2:.5 Bb1:.5 R:.5 F2:.5 G2:.5 | A1:.5 R:.5 E2:.5 A2:.5 A1:.5 R:.5 C#2:.5 E2:.5'
    for at in range(0,32,4):s.line(b,at,bass,72,.62)
    s.blocks(h,16,'D3 F3 A3 | Bb2 D3 F3 | G3 Bb3 D4 | A3 C#4 E4 | D3 F3 A3 | G3 Bb3 D4 | A3 C#4 G4 | D3 F3 A3',dur=1.25,v=65)
    s.line(m,32,'D4:1 F4:1 A4:2 | C5:1 A4:1 G4:2 | Bb4:1 G4:1 E4:2 | C#5:2 A4:1 | D5:3 | A4:2 | F4:1 E4:1 D4:2 | D4:3',73)
    s.line(b,32,'D2:2 A2:1 | C2:2 G2:1 | Bb1:2 F2:1 | A1:2 E2:1 | D2:3 | D3:2 | A2:2 | D2:3',68)
    s.drums(8,24,[(0,36,0),(1.5,45,-10),(2,38,-13),(3.5,47,-18)],67)
    return s

def eleven():
    s=Piece(11,'Rain after the Conversation','Melancholy','B minor',58,'4/4',22,'You replay something you wish you had said differently. Rain gives the thought enough room.','A slow piano elegy; exposed sixths, delayed resolutions and two genuinely empty bars.')
    p=s.part('Unsent words','felt',.84,.56,.25);l=s.part('Low piano','felt',.57,.35,.2)
    s.mark(0,'Still thinking');s.mark(8,'What went unsaid');s.mark(16,'The rain eases')
    s.line(p,0,'F#4:2 D4:1 | B3:3 | R:1 C#4:1 E4:1 | D4:2 C#4:1 | F#4:1 A4:2 | G4:2 E4:1 | C#4:1 D4:1 A#3:1 | B3:3',60,.97)
    s.line(l,0,'B2+F#3:3 | G2+D3:3 | E2+B2:3 | F#2+C#3:3 | D3+A3:3 | E3+B3:3 | F#2+E3:3 | B2+F#3:3',44,.98)
    s.line(p,8,'D5:2 C#5:1 B4:1 | A4:1 F#4:2 | G4:2 B4:1 | A4:2 F#4:1 | E4:1 D4:1 C#4:1 | A#3:2 F#3:1 | R:4 | R:4',65,.97)
    s.line(l,8,'G2+D3:3 | D3+A3:3 | E3+B3:3 | F#3+C#4:3 | G2+B2:3 | F#2+C#3:3',46)
    s.line(p,16,'F#4:2 D4:1 | C#4:1 E4:1 D4:1 | B3:2 F#4:1 | E4:2 C#4:1 | D4:1 C#4:1 B3:2 | R:4',54,.98)
    s.line(l,16,'B2+F#3:3 | E3+G3:3 | G2+D3:3 | F#2+C#3:3 | B2+F#3:4',39,1)
    return s

def twelve():
    s=Piece(12,'All the Little Lights Are On','Relief','Ab major',72,'6/8',32,'You check every habitat. Every little life is safe, and your shoulders finally drop.','A floating sine melody resolves a suspended harmony; the bell enters only after the worry passes.')
    m=s.part('A long exhale','sine',.83,.5,.25);p=s.part('Held breath','air',.46,.4,.34);b=s.part('Safe at last','bell',.42,.72,.2)
    s.mark(0,'Checking each light');s.mark(12,'Every one is safe');s.mark(24,'Let go')
    s.line(m,0,'Bb4:2 Ab4:.5 | G4:2 | Eb4:1 Ab4:1 | Bb4:2 | C5:1 Bb4:.5 Ab4:1 | G4:1 F4:1 | Eb4:2 | R:3 | F4:1 Ab4:1 | C5:2 Bb4:.5 | G4:2 | Eb4:2',58,.96)
    s.blocks(p,0,'Ab2 Eb3 Bb3 | | G3 Bb3 Eb4 | | F3 C4 Ab4 | | Eb3 Ab3 Bb3 | | Db3 Ab3 F4 | | Eb3 Bb3 Db4 |',dur=5.8,v=48)
    s.line(m,12,'Ab4:1 C5:1 Eb5:1 | Db5:1 C5:.5 Bb4:1 | Ab4:1 G4:.5 F4:1 | Eb4:2 | F4:.5 Ab4:.5 C5:1 | Bb4:2 | G4:1 Bb4:1 Eb5:1 | C5:2 | Db5:1 C5:1 Bb4:.5 | Ab4:2 | G4:1 Bb4:1 | Ab4:2',64,.95)
    s.blocks(p,12,'Ab2 Eb3 C4 | | F3 C4 Ab4 | | Db3 Ab3 F4 | | Eb3 Bb3 Db4 | | Db3 Ab3 F4 | | Eb3 Bb3 G4 |',dur=5.8,v=49)
    s.line(b,16,'R:1.5 Eb5:.5 Ab5:.5 | R:3 | R:1.5 G5:.5 Bb5:.5 | R:3 | F5:1 | R:3 | G5:1 | C5:1',43)
    s.line(m,24,'C5:1 Bb4:.5 Ab4:1 | F4:2 | Db5:1 C5:.5 Bb4:1 | G4:2 | Ab4:2 | Eb4:2 | Ab4:2 | R:3',54,.98)
    s.blocks(p,24,'F3 C4 Ab4 | | Db3 Ab3 F4 | | Ab2 Eb3 C4 | | Ab2 Eb3 Bb3 |',dur=5.8,v=40)
    return s

def thirteen():
    s=Piece(13,'Something Heard You Listening','Scary','E Phrygian',54,'5/4',18,'A sound stops when you stop. You wait long enough to hear that it is small, too.','Low organ pedals and widely spaced glass notes; fear comes from silence and a semitone, never detuning.')
    g=s.part('Behind the wall','glass',.57,.67,.42);b=s.part('Floor vibration','organ',.4,.35,.2);p=s.part('A distant answer','sine',.6,.4,.36)
    s.mark(0,'Wait');s.mark(6,'It answered');s.mark(12,'Small footsteps')
    s.line(g,0,'R:2 E5:1 | R:4 F5:.5 | R:5 | B4:1 R:2 F5:1 | E5:2 | R:5',49,.9)
    s.line(b,0,'E2+B2:5 | R:5 | E2:4 | R:5 | F2+C3:4 | R:5',41,1)
    s.line(g,6,'R:1 F5:.5 E5:1 R:1 B4:.5 | C5:1 R:2 G4:1 | R:5 | E5:1 F5:1 B4:1 | R:3 C5:1 | B4:2',56)
    s.line(p,6,'E3:4 | F3:4 | E3:4 | G3:4 | F3:4 | E3:4',47,.95)
    s.line(b,8,'E2:4 | B2:4 | C3:4 | B2:4',39)
    s.line(g,12,'E5:.5 G5:.5 E5:1 R:2 F5:.5 | E5:2 | R:5 | B4:1 G4:1 | E4:2 | R:5',43,.85)
    s.line(p,12,'E3:4 | C3:4 | B2:4 | E3:4 | E3:4',43,.9)
    return s

def fourteen():
    s=Piece(14,'Water at the Door','Danger','F# minor',164,'7/8',48,'The water is rising. There is still time to move every tank if you keep thinking.','A 3+2+2 pulse alarm; changing accents, clipped bass and a deliberately interrupted motor.')
    m=s.part('Warning light','pulse',.62,.6,.04);b=s.part('Urgent steps','sub',.8,.45,.01);t=s.part('Alarm response','square',.36,.3,.03)
    s.mark(0,'Notice the water');s.mark(16,'Choose a route');s.mark(32,'Carry them higher')
    a='F#4:.5 C#5:.5 F#5:.5 E5:.5 C#5:.5 A4:.5 G#4:.5 | F#4:1 R:.5 A4:.5 B4:.5 C#5:1 | D5:.5 C#5:.5 B4:.5 A4:.5 G#4:.5 E#4:.5 G#4:.5 | C#5:1 E#5:.5 C#5:1 R:1'
    for at in [0,4,8,12,32,36]:s.line(m,at,a,78,.62)
    for at in [0,4,8,12,16,20,32,36,40,44]:s.line(b,at,'F#2:.5 R:.5 C#3:.5 F#2:.5 R:.5 C#3:.5 F#2:.5 | A2:.5 R:.5 E3:.5 A2:.5 R:.5 E3:.5 A2:.5 | D2:.5 R:.5 A2:.5 D2:.5 R:.5 A2:.5 D2:.5 | C#2:.5 R:.5 G#2:.5 C#2:.5 R:.5 G#2:.5 C#2:.5',73,.7)
    s.line(m,16,'A5:1 G#5:.5 F#5:1 E5:1 | C#5:.5 E5:.5 F#5:.5 A5:1 G#5:1 | B5:1 A5:.5 G#5:1 F#5:1 | E#5:.5 G#5:.5 C#6:.5 B5:1 G#5:1 | F#5:1 E5:.5 C#5:1 A4:1 | B4:.5 C#5:.5 D5:.5 F#5:1 A5:1 | G#5:1 E#5:.5 C#5:1 B4:1 | F#5:2',79,.8)
    s.line(t,8,'C#4:1 R:.5 C#4:1 | E4:1 R:.5 E4:1 | F#4:1 R:.5 F#4:1 | E#4:1 R:.5 G#4:1',52,.55)
    s.line(m,24,'F#4:.5 R:3 | R:3.5 | C#5:.5 R:3 | R:3.5 | D5:1 | C#5:1 | B4:.5 A4:.5 G#4:.5 | E#4:1',60)
    s.line(b,24,'F#2:2 | R:3.5 | C#2:2 | R:3.5 | D2:2 | C#2:2 | B1:2 | C#2:2',55)
    s.line(m,40,'A4:.5 C#5:.5 F#5:.5 A5:1 G#5:1 | F#5:1 E5:.5 C#5:1 A4:1 | D5:.5 F#5:.5 A5:.5 B5:1 A5:1 | G#5:1 E#5:.5 C#5:1 | F#5:2 | E5:.5 C#5:.5 A4:.5 | G#4:.5 E#4:.5 C#4:.5 | F#4:2',79)
    for at,count in [(4,20),(32,12)]:s.drums(at,count,[(0,36,3),(.5,42,-25),(1.5,38,-5),(2,42,-22),(2.5,36,-7),(3,42,-22)],72)
    return s

def fifteen():
    s=Piece(15,'Courage Is a Small Thing','Battle','C minor',176,'4/4',56,'Your hands shake, but you take your turn. Courage is choosing to protect what is small.','A saw-and-square battle rondo: a fast hook, a half-time challenge, then a new final answer.')
    m=s.part('Small brave voice','saw',.68,.56,.05);b=s.part('Square engine','square',.71,.43,.01);c=s.part('Team chords','brass',.48,.3,.08)
    s.mark(0,'Stand up');s.mark(16,'Hold your ground');s.mark(28,'The answer');s.mark(40,'One last push');s.mark(52,'Breathe')
    A='G4:.5 C5:.5 Eb5:.25 D5:.25 C5:.5 G5:1 F5:.5 Eb5:.5 | D5:.5 Eb5:.5 F5:1 G5:.5 F5:.5 D5:1 | Eb5:.5 C5:.5 G4:.5 Bb4:.5 C5:1 D5:.5 Eb5:.5 | D5:1 B4:.5 G4:.5 C5:1 R:1'
    for at in [0,4,8,12,28,32]:s.line(m,at,A,80 if at<8 else 84,.73)
    motor='C2:.5 C3:.5 G2:.5 C3:.5 C2:.5 G2:.5 Bb2:.5 G2:.5 | Ab1:.5 Ab2:.5 Eb2:.5 Ab2:.5 Ab1:.5 Eb2:.5 G2:.5 Eb2:.5 | F2:.5 F3:.5 C3:.5 F3:.5 F2:.5 C3:.5 Eb3:.5 C3:.5 | G1:.5 G2:.5 D2:.5 G2:.5 G1:.5 D2:.5 B2:.5 D2:.5'
    for at in [0,4,8,12,28,32,36,40,44,48]:s.line(b,at,motor,69,.6)
    s.line(m,16,'Ab5:2 G5:1 Eb5:1 | F5:2 Eb5:1 C5:1 | D5:1 F5:1 Ab5:1 G5:1 | B5:2 G5:1 | C6:1 Bb5:.5 Ab5:.5 G5:2 | F5:1 Eb5:1 D5:2 | Eb5:1 G5:1 F5:1 D5:1 | C5:3',80,.9)
    s.line(b,16,'Ab2:2 Eb3:1 | F2:2 C3:1 | Bb2:2 F3:1 | G2:2 D3:1 | Ab2:2 Eb3:1 | F2:2 C3:1 | G2:2 B2:1 | C2:3',72)
    s.blocks(c,16,'Ab3 C4 Eb4 | F3 Ab3 C4 | Bb3 D4 F4 | G3 B3 D4 | Ab3 C4 Eb4 | F3 Ab3 C4 | G3 B3 F4 | C3 Eb3 G3',dur=1.5,v=71)
    s.line(m,24,'G4:1 C5:1 | R:4 | Eb5:.5 D5:.5 C5:.5 Bb4:.5 Ab4:1 G4:1 | F4:.5 G4:.5 B4:.5 D5:.5 G5:1',65)
    s.line(b,24,'C2:2 | R:4 | Ab1:2 | G1:2',60)
    s.line(m,36,'Eb5:1 G5:1 C6:2 | Bb5:1 Ab5:1 G5:2 | F5:.5 Ab5:.5 C6:1 Bb5:1 Ab5:1 | G5:1 F5:1 D5:1 B4:1',84)
    s.line(m,40,'C5:.5 Eb5:.5 G5:.5 C6:.5 Bb5:1 G5:1 | Ab5:1 F5:.5 Eb5:.5 C5:1 Ab4:1 | F5:.5 G5:.5 Ab5:.5 C6:.5 Bb5:1 Ab5:1 | G5:.5 B5:.5 D6:1 B5:1 G5:1 | C6:1 G5:1 Eb5:1 C5:1 | Ab5:1 Eb5:1 C5:1 Ab4:1 | F5:1 Ab5:1 G5:.5 F5:.5 D5:1 | C5:3',87)
    s.line(m,48,'Eb5:.5 G5:.5 C6:1 Bb5:.5 Ab5:.5 G5:1 | F5:.5 Eb5:.5 D5:1 C5:.5 Bb4:.5 Ab4:1 | G4:.5 B4:.5 D5:.5 F5:.5 G5:1 B5:1 | C6:3 | G5:2 Eb5:1 | C5:3 | G4:1 Eb4:1 C4:2 | R:4',76)
    s.line(b,52,'C2:3 | Ab2:3 | C2:4',65)
    for at,count in [(0,16),(28,24)]:s.drums(at,count,[(0,36,4),(.5,42,-24),(1,38,0),(1.5,42,-23),(2,36,0),(2.5,36,-14),(3,38,2),(3.5,42,-21)],73)
    s.drums(16,8,[(0,36,0),(1.5,42,-26),(2,38,-5),(3.5,42,-25)],69)
    return s

def sixteen():
    s=Piece(16,'Make Room for Everyone','Resolve','G minor',112,'3/4',40,'One more habitat can fit if everyone carries a corner. No one gets left outside.','An organ passacaglia over a descending four-bar bass; a measured triple-time march.')
    o=s.part('Promises','organ',.7,.58,.18);b=s.part('Four firm steps','saw',.38,.35,.05)
    s.mark(0,'Make the promise');s.mark(12,'Shoulder to shoulder');s.mark(28,'Room for everyone')
    for bar in range(0,36,4):s.line(b,bar,'G2:2 D3:.5 | F2:2 C3:.5 | Eb2:2 Bb2:.5 | D2:2 A2:.5',62,.86)
    s.line(o,0,'G3+D4:2 | A3+C4:2 | G3+Bb3:2 | F#3+A3:2 | D4:1 G4:1 A4:1 | Bb4:2 A4:.5 | G4:1 Eb4:1 C4:1 | D4:2',62)
    s.line(o,8,'D4:1 G4:.5 A4:.5 Bb4:1 | C5:1 A4:1 F4:1 | G4:1 Bb4:1 Eb5:1 | D5:2',68)
    s.line(o,12,'Bb4:1 D5:1 G5:1 | F5:1 C5:1 A4:1 | Eb5:1 G5:1 Bb5:1 | A5:1 F#5:1 D5:1 | G5:1 D5:1 Bb4:1 | C5:1 F5:1 A5:1 | G5:1 Eb5:1 C5:1 | D5:2',76)
    s.line(o,20,'G4+Bb4:2 | F4+A4:2 | Eb4+G4:2 | D4+F#4:2 | G4:1 D4:1 Bb3:1 | F4:1 C4:1 A3:1 | Eb4:1 Bb3:1 G3:1 | D4:2',57,.96)
    s.line(o,28,'D4:1 G4:1 Bb4:1 | A4:1 C5:1 F5:1 | Eb5:1 G5:1 Bb5:1 | A5:1 F#5:1 D5:1 | G5:2 D5:.5 | C5:1 A4:1 F4:1 | Eb5:1 Bb4:1 G4:1 | F#4:2 D4:.5 | G4+Bb4:2 | A4+C5:2 | Bb4+D5:2 | G4+B4+D5:2',73)
    s.line(b,36,'Eb2:2 | F2:2 | D2:2 | G2:2',63)
    s.drums(12,8,[(0,36,-7),(2,38,-26)],64);s.drums(28,8,[(0,36,-7),(1.5,37,-20),(2.5,38,-26)],61)
    return s

def seventeen():
    s=Piece(17,'The Whole Street Cheered','Joy','F major',144,'2/4',56,'Good news travels from porch to porch until the whole street is celebrating.','A bright square-wave jig in short, breathy phrases; offbeat nylon chords and a small kit.')
    m=s.part('Shout of joy','square',.65,.58,.05);p=s.part('Clapping porches','nylon',.71,.3,.04);b=s.part('Dancing feet','upright',.73,.48,.02)
    s.mark(0,'One porch');s.mark(16,'The whole street');s.mark(32,'Catch your breath');s.mark(40,'Everybody again')
    a='C5:.5 F5:.5 A5:.5 C6:.5 | Bb5:.5 A5:.5 G5:.5 | A5:.5 F5:.5 C5:.5 | G5:1 | A5:.5 C6:.5 F6:.5 | E6:.5 C6:.5 Bb5:.5 | A5:.5 G5:.5 E5:.5 | F5:1'
    for at in [0,8,40]:s.line(m,at,a,72,.65)
    s.line(m,16,'D6:.5 C6:.5 Bb5:.5 A5:.5 | G5:1 Bb5:.5 | C6:.5 Bb5:.5 A5:.5 G5:.5 | F5:1 A5:.5 | Bb5:.5 D6:.5 C6:.5 Bb5:.5 | A5:1 F5:.5 | G5:.5 Bb5:.5 C6:.5 E6:.5 | F6:1',76)
    s.line(m,24,'C6:.5 A5:.5 F5:1 | R:2 | D6:.5 Bb5:.5 G5:1 | R:2 | E6:.5 C6:.5 G5:1 | Bb5:.5 A5:.5 G5:.5 | F5:.5 A5:.5 C6:.5 | F5:1',73)
    s.line(p,32,'F4:.5 A4:.5 C5:.5 | A4:1 | G4:.5 Bb4:.5 D5:.5 | Bb4:1 | A4:.5 C5:.5 F5:.5 | C5:1 | Bb4:.5 G4:.5 E4:.5 | F4:1',68)
    H='F3 A3 C4 | Bb3 D4 F4 | F3 A3 C4 | C3 E3 Bb3 | F3 A3 C4 | Bb3 D4 F4 | C3 E3 Bb3 | F3 A3 C4'
    for at in [0,8,16,24,40,48]:
        s.arp(p,at,H,[(.5,0,.25),(.5,1,.25),(.5,2,.25),(1.5,0,.25),(1.5,1,.25),(1.5,2,.25)],57)
        s.line(b,at,'F2:.5 C3:.5 | Bb2:.5 F3:.5 | A2:.5 C3:.5 | C3:.5 G2:.5 | F2:.5 A2:.5 | Bb2:.5 D3:.5 | C3:.5 G2:.5 | F2:1',62,.72)
    s.line(m,48,'A5:.5 C6:.5 F6:.5 E6:.5 | D6:.5 C6:.5 Bb5:.5 A5:.5 | G5:.5 A5:.5 Bb5:.5 G5:.5 | E5:1 C5:.5 | F5:.5 A5:.5 C6:.5 | Bb5:.5 G5:.5 E5:.5 | F5:1 | R:2',75)
    s.drums(16,16,[(0,36,-3),(.5,42,-24),(1,38,-15),(1.5,42,-24)],64);s.drums(40,12,[(0,36,-3),(1,38,-17)],62)
    return s

def eighteen():
    s=Piece(18,'Leave a Chair beside You','Forgiveness','Db major',62,'4/4',24,'An apology is awkward. Leaving space for someone can be the first gentle answer.','Two piano voices start apart, then share a cadence; a soft triangle arrives only near the end.')
    a=s.part('The apology','felt',.77,.32,.23);b=s.part('The answer','felt',.73,.65,.23);h=s.part('A place to sit','triangle',.34,.5,.22)
    s.mark(0,'Finding the words');s.mark(8,'Listening');s.mark(16,'Sitting together')
    s.line(a,0,'Db4:1 F4:1 Ab4:1 | Gb4:2 F4:1 | Eb4:2 | R:4 | Db4:1 Eb4:1 F4:1 | Bb4:2 Ab4:1 | Gb4:1 F4:1 Eb4:1 | R:4',57,.96)
    s.line(b,0,'Db3+Ab3:3 | Bb2+F3:3 | R:4 | Eb4:1 F4:1 Ab4:1 | Gb3+Db4:3 | Db3+Ab3:3 | R:4 | C4:1 Eb4:1 Gb4:1',48,.97)
    s.line(b,8,'Ab4:1 F4:1 Db4:1 | Eb4:2 Gb4:1 | F4:2 Ab4:1 | Bb4:2 | Ab4:1 Gb4:1 F4:1 | Eb4:2 C4:1 | Db4:3 | R:4',59,.96)
    s.line(a,8,'Db3+Ab3:3 | Eb3+Bb3:3 | F3+Ab3:3 | Gb3+Db4:3 | Bb2+F3:3 | Ab2+Eb3:3 | Db3+Ab3:3',46,.98)
    s.line(a,16,'Db4:1 F4:1 Ab4:1 | Bb4:2 Ab4:1 | Gb4:1 F4:1 Eb4:1 | F4:2 | Gb4:1 Bb4:1 Ab4:1 | Gb4:1 Eb4:1 C4:1 | Db4:3 | R:4',61,.97)
    s.line(b,16,'Ab3:2 F3:1 | Gb3:2 Db4:1 | Bb3:2 Gb3:1 | Ab3:2 Db4:1 | Bb3:2 Gb3:1 | Ab3:2 Eb3:1 | F3+Ab3:3',49,.97)
    s.line(h,16,'Db3:4 | Bb2:4 | Eb3:4 | Db3:4 | Gb3:4 | Ab2:4 | Db3:4',45,1)
    return s

def nineteen():
    s=Piece(19,'New Leaves, Uneven Edges','Recovery','D Dorian',82,'6/8',32,'New growth is crooked at first. You notice it anyway.','A breathy flute over open nylon strings; the Dorian sixth lifts the tune without forcing a happy ending.')
    f=s.part('New growth','flute',.77,.59,.16);g=s.part('Open strings','nylon',.8,.34,.1)
    s.mark(0,'A small green point');s.mark(10,'Turning toward light');s.mark(24,'Still growing')
    s.line(f,0,'D4:1 F4:.5 A4:1 | G4:1 E4:1 | F4:1 E4:.5 D4:1 | A3:2 | D4:.5 F4:.5 A4:.5 B4:1 | A4:1 G4:.5 E4:1 | F4:2 | D4:2 | R:3 | R:3',59,.92)
    s.arp(g,0,'D3 A3 D4 | C3 G3 E4 | D3 A3 F4 | A2 E3 A3 | G2 D3 B3 | C3 G3 E4 | F3 A3 D4 | D3 A3 D4 | D3 A3 E4 | D3 A3 F4',[(0,0,1),(1,1,.65),(2,2,.65)],54)
    s.line(f,10,'B4:1 A4:.5 G4:1 | E4:1 G4:.5 A4:1 | C5:1 B4:.5 A4:1 | F4:2 | G4:.5 A4:.5 B4:1 | D5:1 C5:.5 B4:1 | A4:2 | G4:1 E4:1 | F4:.5 G4:.5 A4:1 | D4:2',65)
    s.arp(g,10,'G3 B3 D4 | C3 G3 E4 | A2 E3 A3 | D3 A3 F4 | G3 B3 D4 | G3 B3 D4 | F3 A3 C4 | C3 G3 E4 | D3 A3 F4 | D3 A3 E4',[(0,0,.8),(1.5,1,.6),(2,2,.6)],53)
    s.line(g,20,'D4:.5 E4:.5 F4:1 | G4:1 B4:1 | A4:.5 G4:.5 E4:1 | D4:2',59)
    s.line(f,24,'D4:1 F4:.5 A4:1 | B4:1 A4:.5 G4:1 | F4:1 E4:1 | D4:2 | B4:1 A4:.5 F4:1 | G4:1 E4:1 | D4:2 | R:3',57,.96)
    s.blocks(g,24,'D3 A3 | G3 B3 | C3 G3 | D3 A3 | G3 B3 | C3 G3 | D3 A3 E4 |',dur=2.5,v=48)
    return s

def twenty():
    s=Piece(20,'A Universe behind the Glass','Wonder','A Lydian',60,'4/4',24,'In the tank, a leaf turns slowly. For a moment it looks like a whole planet.','An ambient constellation: isolated glass tones orbit three slow, open harmonies. No beat grid is played aloud.')
    g=s.part('Points of light','glass',.64,.62,.42);p=s.part('Still water','air',.45,.4,.45);n=s.part('Near the surface','sine',.51,.55,.3)
    s.mark(0,'Look closer');s.mark(9,'A whole world');s.mark(18,'Keep watching')
    s.blocks(p,0,'A2 E3 B3 | | | | G#2 D#3 B3 | | | | F#2 C#3 G#3 | | | | A2 E3 B3 | | | | B2 F#3 C#4 | | | | A2 E3 B3',dur=15,v=48)
    s.line(g,0,'R:1.5 E5:1 | R:2.5 A5:1 | R:4 | D#5:2 | R:4 | B4:1 R:1 F#5:1 | R:4 | G#5:1 | R:4 | A5:1 E5:1 | R:3 C#6:.5 | B5:2 | R:4 | D#5:1 E5:2 | R:4 | A4:1 B4:1 | R:4 | F#5:2 | R:2 G#5:1 | E5:2 | R:4 | B4:1 A4:2 | R:4 | R:4',48,.98)
    s.line(n,9,'C#4:4 | E4:4 | F#4:4 | G#4:4 | A4:4 | E4:4 | D#4:4 | C#4:4 | B3:4',43,1)
    return s

def twentyone():
    s=Piece(21,'Filter Hum at 1 AM','Chill','E minor',70,'4/4',32,'The house is asleep. The tank filter keeps you company while the last thought drifts away.','A restrained half-time lo-fi beat, mellow electric-piano ninths, and an unhurried low melody.')
    m=s.part('Half-asleep thought','epiano',.82,.58,.16);h=s.part('Warm ninths','epiano',.47,.3,.14);b=s.part('Soft sub','sub',.78,.5,.01)
    s.mark(0,'One lamp left');s.mark(8,'The filter keeps time');s.mark(24,'Almost asleep')
    A='R:.65 B3:.35 D4:1 E4:.65 G4:.35 F#4:.65 | E4:2 D4:.65 B3:.35 | A3:.65 C4:.35 E4:1 G4:1 | F#4:2 D4:.65 B3:.35 | G3:.65 B3:.35 D4:1 F#4:1 | E4:2 B3:1 | C4:1 B3:.65 A3:.35 F#3:1 | B3:2'
    s.line(m,0,A,60,.92);s.line(m,16,A,55,.95)
    s.line(m,8,'B4:.65 G4:.35 F#4:1 E4:1 | D4:1 B3:1 G3:1 | A3:.65 C4:.35 E4:1 A4:1 | F#4:2 E4:.65 D4:.35 | B3:.65 D4:.35 G4:1 A4:1 | G4:1 E4:.65 D4:.35 B3:1 | A3:.65 C4:.35 E4:1 F#4:1 | D#4:2 B3:1',63,.91)
    s.line(m,24,'E4:2 B3:1 | G3:2 | A3:1 C4:1 E4:1 | D4:2 | B3:1 D4:1 F#4:1 | E4:2 | B3:1 D4:1 E4:2 | R:4',50,.98)
    H='G3 B3 D4 F#4 | G3 B3 D4 E4 | G3 C4 E4 B4 | A3 C4 D4 F#4 | F#3 B3 D4 A4 | G3 B3 D4 E4 | G3 C4 E4 A4 | A3 B3 D#4 F#4'
    for at in [0,8,16]:
        s.blocks(h,at,H,dur=2.3,offset=.1,v=45)
        s.line(b,at,'E2:1.5 R:1 B2:.5 | E2:2 | A2:1.5 R:1 E3:.5 | D2:2 | G2:1.5 R:1 D3:.5 | C2:2 | A1:1.5 R:1 E2:.5 | B1:2',56,.87)
    s.blocks(h,24,H,dur=3,v=37);s.line(b,24,'E2:3 | E2:3 | A2:3 | D2:3 | G2:3 | C2:3 | E2:3',44)
    s.drums(8,16,[(0,36,-3),(.65,42,-28),(1.65,42,-33),(2,37,-15),(2.65,42,-27),(3.5,36,-20),(3.65,42,-34)],60)
    return s

def twentytwo():
    s=Piece(22,'One Critter, One Very Big Day','Delight','G major',120,'3/8',64,'Critter discovers its reflection, a snack, and a hiding place. All three are astonishing.','Bubbly FM pips in tiny three-eighth-note cells, with a wooden bass and absolutely no pad.')
    m=s.part('Curious bubbles','bubble',.8,.61,.03);b=s.part('Little wooden feet','marimba',.68,.32,.02)
    s.mark(0,'A reflection');s.mark(24,'A snack');s.mark(48,'A hiding place')
    A='G4:.5 B4:.5 D5:.5 | E5:.5 D5:.5 | B4:.5 A4:.5 G4:.5 | D4:1 | C5:.5 E5:.5 G5:.5 | F#5:.5 E5:.5 | D5:.5 A4:.5 F#4:.5 | G4:1'
    for at in [0,8,16,48]:s.line(m,at,A,64,.58)
    for at in [0,8,16,24,32,48,56]:s.line(b,at,'G2:.5 | B2:.5 | E3:.5 | G2:.5 | C3:.5 | A2:.5 | D3:.5 | G2:.5',58,.6)
    s.line(m,24,'B5:.25 A5:.25 G5:.5 D5:.5 | E5:1 | G5:.25 F#5:.25 E5:.5 B4:.5 | D5:1 | C5:.25 D5:.25 E5:.5 G5:.5 | A5:1 | F#5:.25 E5:.25 D5:.5 C5:.5 | B4:1',65,.58)
    s.line(m,32,'G4:.5 R:1 | G5:.5 R:1 | A4:.5 R:1 | A5:.5 R:1 | B4:.5 D5:.5 G5:.5 | E5:1 | C5:.5 A4:.5 F#4:.5 | G4:1',61,.6)
    s.line(b,40,'G3:.5 A3:.5 B3:.5 | D4:1 | E4:.5 D4:.5 B3:.5 | G3:1 | C4:.5 E4:.5 G4:.5 | F#4:.5 D4:.5 | C4:.5 A3:.5 F#3:.5 | G3:1',62)
    s.line(m,56,'G5:.5 D5:.5 B4:.5 | G4:1 | C5:.5 G5:.5 E5:.5 | C5:1 | D5:.5 F#5:.5 A5:.5 | G5:.5 D5:.5 B4:.5 | G4:1 | R:1.5',64)
    return s

def twentythree():
    s=Piece(23,'Postcard from Liarsville','Wistfulness','C major / A minor',84,'3/4',36,'A postcard smells faintly of a place you miss. You are glad someone remembered to write.','A clarinet-like reed waltz that wanders into the relative minor; piano accompaniment follows a descending inner line.')
    m=s.part('Postcard voice','reed',.76,.62,.2);p=s.part('Paper and ink','felt',.66,.35,.15)
    s.mark(0,'Dear friend');s.mark(12,'A place you miss');s.mark(24,'Write soon')
    s.line(m,0,'E4:1 G4:1 C5:1 | B4:1 A4:1 G4:1 | F4:2 A4:1 | G4:2 | E4:.5 G4:.5 C5:1 D5:1 | E5:1 C5:1 A4:1 | G4:1 F4:1 D4:1 | E4:2 | F4:1 A4:1 C5:1 | B4:1 G4:1 D4:1 | E4:1 D4:1 C4:1 | R:3',62,.94)
    s.line(p,0,'C3:1 G3+E4:1 | B2:1 G3+D4:1 | A2:1 F3+C4:1 | G2:1 E3+C4:1 | C3:1 G3+E4:1 | A2:1 E3+C4:1 | G2:1 F3+B3:1 | C3:1 G3+C4:1 | F3:1 A3+C4:1 | G3:1 B3+D4:1 | C3:2',48)
    s.line(m,12,'E4:1 A4:1 C5:1 | B4:1 G#4:1 E4:1 | F4:1 A4:1 D5:1 | C5:2 B4:1 | A4:1 C5:1 E5:1 | F5:1 E5:1 D5:1 | C5:1 B4:1 G#4:1 | A4:2 | G4:1 E4:1 C4:1 | D4:1 F4:1 A4:1 | B4:1 A4:1 F4:1 | G4:2',68,.94)
    s.line(p,12,'A2:1 E3+C4:1 | G#2:1 E3+B3:1 | F2:1 A3+D4:1 | E2:1 G3+C4:1 | A2:1 E3+C4:1 | D3:1 A3+F4:1 | E3:1 B3+D4:1 | A2:1 E3+C4:1 | C3:1 G3+E4:1 | F3:1 A3+D4:1 | G3:1 B3+D4:1 | G2:2',51)
    s.line(m,24,'E4:1 G4:1 C5:1 | B4:1 A4:1 G4:1 | A4:1 F4:1 D4:1 | G4:2 | C5:1 B4:1 A4:1 | G4:1 E4:1 C4:1 | D4:1 F4:1 B4:1 | C5:2 | A4:1 G4:1 F4:1 | E4:2 D4:.5 | C4:2 | R:3',59,.97)
    s.blocks(p,24,'C3 E3 G3 | B2 D3 G3 | F3 A3 C4 | E3 G3 C4 | A2 E3 C4 | E3 G3 C4 | G2 F3 B3 | C3 G3 E4 | F3 A3 C4 | G3 B3 D4 | C3 E3 G3 |',dur=2.5,v=43)
    return s

def twentyfour():
    s=Piece(24,'Downhill with Your Arms Out','Freedom','E major',148,'4/4',40,'The road tips downhill and the sky seems to get wider. You remember how light a day can feel.','A filtered saw lead over offbeat chords, a melodic sine bass, and a breezy straight beat.')
    m=s.part('Open sky','saw',.6,.59,.11);h=s.part('Passing fenceposts','pluck',.52,.29,.07);b=s.part('Wheels','sine',.81,.49,.02)
    s.mark(0,'The crest');s.mark(8,'Let the hill carry you');s.mark(24,'Wide sky');s.mark(36,'Coast home')
    a='B4:.5 E5:1 G#5:.5 B5:1 G#5:.5 F#5:.5 | E5:1 F#5:.5 G#5:.5 A5:1 G#5:.5 E5:.5 | F#5:1 A5:.5 C#6:.5 B5:1 A5:.5 F#5:.5 | G#5:2 E5:1'
    for at in [0,4,8,12,28,32]:s.line(m,at,a,74,.87)
    s.line(m,16,'C#6:2 B5:1 G#5:1 | A5:1 F#5:1 E5:2 | D#5:1 F#5:1 A5:1 B5:1 | G#5:3 | E5:1 C#5:1 B4:1 G#4:1 | A4:1 C#5:1 F#5:2 | D#5:1 F#5:1 B5:2 | E5:3',71)
    s.line(m,24,'R:4 | B4:1 E5:1 G#5:1 | R:4 | F#5:1 G#5:1 B5:1',58)
    H='E3 G#3 B3 | A3 C#4 E4 | F#3 A3 C#4 | B3 D#4 F#4'
    for at in [0,4,8,12,16,20,28,32]:
        s.arp(h,at,H,[(.5,0,.3),(.5,1,.3),(.5,2,.3),(2.5,0,.3),(2.5,1,.3),(2.5,2,.3)],54)
        s.line(b,at,'E2:1 R:.5 B2:.5 G#2:1 B2:.5 | A2:1 R:.5 E3:.5 C#3:1 E3:.5 | F#2:1 R:.5 C#3:.5 A2:1 C#3:.5 | B1:1 R:.5 F#2:.5 D#2:1 F#2:.5',63,.86)
    s.line(b,24,'E2:3 | A2:3 | F#2:3 | B1:3',51)
    s.line(m,36,'G#5:1 F#5:1 E5:2 | C#5:1 B4:1 G#4:2 | F#4:1 G#4:1 B4:1 | E4:3',62,.96)
    s.blocks(h,36,'E3 G#3 B3 | A3 C#4 E4 | B3 D#4 F#4 | E3 G#3 B3',v=47);s.line(b,36,'E2:3 | A2:3 | B1:3 | E2:3',53)
    s.drums(8,16,[(0,36,0),(.5,42,-27),(1,38,-12),(1.5,42,-30),(2,36,-8),(2.5,42,-26),(3,38,-13),(3.5,42,-30)],63);s.drums(28,8,[(0,36,0),(1,38,-12),(2.5,36,-8),(3,38,-12)],64)
    return s

def twentyfive():
    s=Piece(25,'The Footprint That Stops','Mystery','F minor',90,'5/4',24,'The footprints end beside an ordinary stone. You start looking at ordinary things differently.','A pizzicato puzzle in 3+2; low flute questions and one high bell that never quite answers.')
    p=s.part('Careful steps','pluck',.75,.32,.09);f=s.part('Unanswered question','flute',.73,.64,.19);g=s.part('A glint','glass',.39,.7,.3)
    s.mark(0,'Follow the marks');s.mark(8,'An ordinary stone');s.mark(18,'Look again')
    for at in [0,4,8,12]:s.line(p,at,'F3:.5 C4:.5 Ab3:1 R:1 G3:.5 C4:.5 Eb4:1 | Db3:.5 Ab3:.5 F4:1 R:1 Eb4:.5 C4:.5 Ab3:1 | Bb2:.5 F3:.5 C4:1 R:1 Db4:.5 C4:.5 Ab3:1 | C3:.5 G3:.5 Bb3:1 R:1 E4:.5 G4:.5 C4:1',56,.64)
    s.line(f,0,'R:3 C4:1 Eb4:1 | F4:2 Ab4:1 G4:1 | R:2 F4:1 Db4:1 | E4:2 C4:1 | R:5 | Ab4:1 F4:1 Db4:1 | Eb4:1 F4:1 G4:1 | E4:3',57,.94)
    s.line(f,8,'C5:1 Ab4:1 G4:1 F4:1 | Db4:2 F4:1 Ab4:1 | Bb4:1 Ab4:.5 G4:.5 F4:1 Db4:1 | E4:2 G4:1 C5:1 | Ab4:1 G4:1 F4:1 Eb4:1 | Db4:2 C4:1 Ab3:1 | Bb3:1 Db4:1 F4:1 G4:1 | E4:3',65)
    s.line(g,7,'R:4 C6:.5 | R:5 | R:5 | R:5 | R:4 Db6:.5',39)
    s.line(p,16,'F3:.5 C4:.5 Ab4:1 | R:5',48)
    s.line(f,18,'C4:1 Eb4:1 F4:2 | Ab4:1 G4:1 Db4:1 | F4:2 Eb4:1 | C4:2 E4:1 | F4:3 | R:5',53,.98)
    s.blocks(p,18,'F3 Ab3 C4 | Db3 Ab3 F4 | Bb2 F3 Db4 | C3 G3 Bb3 | F3 Ab3 C4 |',dur=3,v=43)
    s.line(g,23,'R:1 G5:1',34)
    return s

def twentysix():
    s=Piece(26,'A Pocket Full of Snow','Tenderness','Gb major',56,'3/4',28,'You bring a melting handful home to show someone. They listen as if it is treasure.','A music-box lullaby in a low, gentle register; widely spaced felt-piano fifths.')
    m=s.part('A tiny treasure','box',.69,.59,.21);p=s.part('Warm hands','felt',.64,.33,.18)
    s.mark(0,'Hold it carefully');s.mark(10,'It is already melting');s.mark(20,'Thank you for showing me')
    s.line(m,0,'Db5:1 Bb4:1 Gb4:1 | Ab4:2 Bb4:.5 | Db5:1 Eb5:1 Db5:1 | Bb4:2 | B4:1 Ab4:1 Gb4:1 | F4:2 Ab4:.5 | Bb4:1 Db5:1 Gb5:1 | F5:2 Eb5:.5 | Db5:1 Bb4:1 Ab4:1 | Gb4:2',54,.97)
    s.blocks(p,0,'Gb2 Db3 Bb3 | Eb3 Bb3 Gb4 | B2 Gb3 Db4 | Gb3 Bb3 Db4 | B2 Gb3 Eb4 | Db3 Ab3 B3 | Gb2 Db3 Bb3 | Db3 Ab3 B3 | Db3 Gb3 Bb3 | Gb2 Db3',dur=2.6,v=40)
    s.line(m,10,'Eb5:1 Gb5:1 Ab5:1 | Gb5:1 Eb5:1 Db5:1 | B4:2 Ab4:.5 | Bb4:2 | Db5:1 Eb5:1 F5:1 | Ab5:2 Gb5:.5 | F5:1 Eb5:1 Db5:1 | Bb4:2 | Ab4:1 B4:1 Db5:1 | F4:2',59,.96)
    s.blocks(p,10,'Eb3 Bb3 Gb4 | B2 Gb3 Eb4 | B2 Gb3 Db4 | Gb3 Bb3 Db4 | Ab2 Eb3 C4 | Db3 Ab3 B3 | Db3 Ab3 B3 | Gb3 Bb3 Db4 | Ab2 Eb3 C4 | Db3 Ab3 B3',dur=2.6,v=42)
    s.line(m,20,'Db5:1 Bb4:1 Gb4:1 | Ab4:2 | B4:1 Ab4:1 F4:1 | Gb4:2 | Bb4:1 Ab4:1 Gb4:1 | Db4:2 | Gb4:2 | R:3',48,.98)
    s.blocks(p,20,'Gb2 Db3 | Eb3 Bb3 | Db3 Ab3 | Gb2 Db3 | B2 Gb3 | Db3 Ab3 | Gb2 Db3 Bb3 |',dur=2.6,v=35)
    return s

def twentyseven():
    s=Piece(27,'Salt Air, Empty Calendar','Contentment','Bb major',76,'6/8',36,'There is nowhere you need to be. A slow walk is enough of a plan.','A nylon-string barcarolle with an organ appearing like distant boats; no bass track or drum kit.')
    g=s.part('Seaside guitar','nylon',.85,.56,.12);l=s.part('Thumb pattern','nylon',.7,.29,.1);o=s.part('Far-away boats','organ',.3,.71,.24)
    s.mark(0,'No hurry');s.mark(12,'Boats in the distance');s.mark(28,'Stay until sunset')
    a='F4:.5 Bb4:1 D5:.5 C5:1 | Bb4:1 G4:.5 F4:1 | Eb4:.5 G4:1 Bb4:.5 A4:1 | F4:2 | G4:.5 Bb4:1 D5:.5 Eb5:1 | D5:1 Bb4:.5 G4:1 | F4:.5 A4:1 C5:.5 Eb5:1 | D5:2'
    s.line(g,0,a,61,.94);s.line(g,20,a,58,.95)
    s.line(g,8,'C5:1 Bb4:.5 G4:1 | A4:1 C5:.5 F5:1 | Eb5:.5 C5:.5 A4:1 | Bb4:2',58)
    s.line(g,12,'G5:1 F5:.5 Eb5:1 | D5:1 Bb4:.5 F4:1 | G4:1 Bb4:.5 Eb5:1 | F5:2 | D5:.5 F5:.5 Bb5:1 | A5:1 G5:.5 F5:1 | Eb5:.5 D5:.5 C5:1 | Bb4:2',65)
    H='Bb2 F3 D4 | G2 D3 Bb3 | Eb3 Bb3 G4 | F3 C4 A4 | Eb3 Bb3 G4 | G2 D3 Bb3 | F3 C4 A4 | Bb2 F3 D4'
    for at in [0,12,20]:s.arp(l,at,H,[(0,0,.8),(1,1,.4),(1.5,2,.6),(2.5,1,.35)],52)
    s.arp(l,8,'C3 G3 Eb4 | F3 C4 A4 | F3 C4 Eb4 | Bb2 F3 D4',[(0,0,1),(1.5,1,.7),(2.5,2,.4)],51)
    s.blocks(o,12,'Eb3 G3 Bb3 | | Bb3 D4 F4 | | G3 Bb3 D4 | | F3 A3 Eb4 |',dur=5.8,v=43)
    s.line(g,28,'D5:1 C5:.5 Bb4:1 | G4:2 | Eb5:1 D5:.5 C5:1 | A4:2 | Bb4:1 F4:.5 D4:1 | C4:1 F4:1 | Bb3:2 | R:3',51,.98)
    s.blocks(l,28,'Bb2 F3 | G2 D3 | Eb3 Bb3 | F3 C4 | Bb2 F3 | F3 A3 | Bb2 F3 D4 |',dur=2.8,v=43)
    return s

def twentyeight():
    s=Piece(28,'Porch Radio, Last Summer','Nostalgia','A major',80,'4/4',32,'The song on the porch radio is new, but the afternoon feels remembered.','A warm electric-piano pocket with straight sixteenths, a triangle countermelody, and dry rim clicks. No artificial tape wobble.')
    k=s.part('Porch keys','epiano',.78,.57,.1);m=s.part('A half-remembered tune','triangle',.62,.3,.15);b=s.part('Slow bass guitar','upright',.76,.49,.04)
    s.mark(0,'The radio comes on');s.mark(8,'Summer in the yard');s.mark(24,'The long way home')
    # Here the keyboard comp is the foreground; the tune waits eight bars.
    H='A3 C#4 E4 G#4 | G#3 B3 C#4 E4 | F#3 A3 C#4 E4 | E3 G#3 B3 D4'
    for at in [0,4,8,12,24,28]:s.arp(k,at,H,[(0,0,.4),(0,1,.4),(0,2,.4),(.75,3,.4),(1.75,1,.45),(2.5,0,.6),(2.5,2,.6),(3.5,3,.35)],61)
    s.line(m,8,'R:1 E4:.75 C#4:.25 B3:1 A3:.75 | C#4:1 E4:.5 G#4:.5 B4:1 | A4:1 F#4:.5 E4:.5 C#4:1 | B3:2 G#3:.5 B3:.5 | C#4:1 E4:.75 F#4:.25 G#4:1 | E4:1 C#4:.5 B3:.5 G#3:1 | A3:.75 C#4:.25 E4:1 F#4:1 | D4:1 B3:1 G#3:1',64,.91)
    s.line(k,16,'C#5:1 B4:.5 A4:.5 F#4:1 | E4:.75 G#4:.25 B4:1 D5:1 | C#5:1 A4:1 F#4:.75 E4:.25 | D4:1 F#4:.5 A4:.5 C#5:1 | B4:.75 D5:.25 E5:1 F#5:1 | E5:1 C#5:.5 B4:.5 A4:1 | G#4:.5 F#4:.5 E4:1 D4:1 | C#4:2',68)
    s.blocks(m,16,'F#3 A3 | E3 G#3 | D3 A3 | D3 F#3 | B3 D4 | A3 C#4 | E3 G#3 | A3 C#4',dur=2.8,v=44)
    s.line(m,24,'E4:2 C#4:1 | B3:2 G#3:1 | A3:1 C#4:1 F#4:1 | E4:2 | C#4:1 E4:1 A4:1 | G#4:1 E4:1 C#4:1 | B3:1 G#3:1 E3:1 | A3:3',55,.97)
    for at in [0,4,8,12,24,28]:s.line(b,at,'A2:1.5 R:1 E3:.5 G#2:.5 | C#3:2 G#2:1 | F#2:1.5 R:1 C#3:.5 E3:.5 | E2:2 B2:1',58,.8)
    s.line(b,16,'F#2:2 C#3:1 | E2:2 B2:1 | D2:2 A2:1 | D2:2 F#2:1 | B2:2 F#3:1 | A2:2 E3:1 | E2:2 B2:1 | A2:3',58)
    s.drums(4,24,[(0,36,-8),(.75,42,-34),(1,37,-19),(2.5,36,-16),(2.75,42,-35),(3,37,-22)],60)
    return s

def twentynine():
    s=Piece(29,'Fireflies Need No Audience','Peace','D major pentatonic',52,'4/4',20,'The fireflies keep making their little lights whether anyone is watching or not.','Only sine and felt piano; a five-note palette, irregular entries, long rests and no harmonic urgency.')
    m=s.part('Fireflies','sine',.68,.64,.34);p=s.part('Garden after dark','felt',.71,.35,.3)
    s.mark(0,'The first light');s.mark(7,'More lights');s.mark(14,'Simply being here')
    s.line(m,0,'R:2 A4:1 | R:4 | F#4:1 E4:1 | D4:3 | R:4 | B4:1 A4:2 | R:4 | F#5:1 E5:2 | R:3 D5:.5 | A4:3 | R:4 | E5:1 F#5:1 | B4:2 A4:1 | R:4 | F#4:2 E4:1 | D4:3 | R:4 | A4:1 F#4:1 | D4:3 | R:4',49,.99)
    s.line(p,0,'D2+A2:4 | R:4 | B2+F#3:4 | R:4 | G2+D3:4 | R:4 | A2+E3:4 | R:4 | B2+F#3:4 | R:4 | G2+D3:4 | R:4 | A2+E3:4 | R:4 | D3+A3:4 | R:4 | G2+D3:4 | A2+E3:4 | D2+A2+E3:4',41,1)
    return s

def thirty():
    s=Piece(30,'Thank You for This Ordinary Day','Gratitude','Eb major',98,'4/4',36,'Nothing spectacular happened. You cared for small lives, came home, and will get another day.','A through-composed piano-and-flute epilogue; each phrase moves forward and the final harmony stays open.')
    p=s.part('Today','felt',.85,.56,.19);f=s.part('Tomorrow','flute',.65,.7,.2);l=s.part('Steady hands','felt',.63,.3,.16);h=s.part('Last light','strings',.3,.4,.28)
    s.mark(0,'A morning remembered');s.mark(10,'The people you met');s.mark(22,'What you will keep');s.mark(32,'Tomorrow')
    s.line(p,0,'Eb4:1 G4:.5 Bb4:.5 C5:1 Bb4:1 | Ab4:2 G4:1 | F4:1 Ab4:.5 C5:.5 D5:1 C5:1 | Bb4:2 G4:1 | Eb5:1 D5:.5 C5:.5 Bb4:1 G4:1 | Ab4:1 C5:1 F5:2 | Eb5:1 C5:1 Ab4:1 | G4:1 Bb4:1 D5:1 | Eb5:3 | R:4',66,.95)
    s.blocks(l,0,'Eb3 Bb3 | C3 G3 | F3 C4 | G3 Bb3 | Eb3 Bb3 | F3 Ab3 | Ab3 C4 | Bb2 F3 | Eb3 G3 Bb3 |',v=48)
    s.line(f,10,'Bb4:1 C5:1 Eb5:1 G5:1 | F5:2 D5:1 | Eb5:1 C5:1 Ab4:1 | G4:2 Bb4:1 | C5:.5 D5:.5 Eb5:1 Ab5:2 | G5:1 F5:1 Eb5:1 | D5:2 Bb4:1 | C5:1 Ab4:1 F4:1 | G4:1 Bb4:1 Eb5:1 | F5:1 D5:1 Bb4:1 | Eb5:3 | R:4',64,.94)
    s.line(p,10,'Eb4:2 G4:1 | D4:2 F4:1 | Eb4:2 C4:1 | Bb3:2 Eb4:1 | Ab3:2 C4:1 | Bb3:2 Eb4:1 | F4:2 D4:1 | Eb4:2 C4:1 | Eb4:2 G4:1 | D4:2 F4:1 | G4:3',52,.96)
    s.blocks(l,10,'Eb3 Bb3 | Bb2 F3 | Ab2 Eb3 | G2 D3 | F3 C4 | Eb3 Bb3 | Bb2 F3 | Ab2 Eb3 | C3 G3 | Bb2 F3 | Eb3 Bb3 |',v=45)
    s.line(p,22,'G4:.5 Bb4:.5 Eb5:1 F5:1 G5:1 | Ab5:1 G5:.5 F5:.5 Eb5:1 C5:1 | Bb4:1 C5:1 Eb5:1 G5:1 | F5:2 D5:1 | Eb5:1 Bb4:1 G4:1 | Ab4:1 C5:1 F5:1 | Eb5:1 D5:1 C5:1 | Bb4:1 Ab4:1 F4:1 | G4:1 Bb4:1 Eb5:1 | D5:1 Bb4:1 F4:1',70,.95)
    s.line(f,22,'Eb4:3 | C4:3 | G4:2 Eb4:1 | F4:3 | G4:2 Eb4:1 | Ab4:2 C5:1 | Bb4:2 G4:1 | D5:2 Bb4:1 | Eb5:3 | F5:2 D5:1',55,.97)
    s.blocks(l,22,'Eb3 Bb3 | F3 C4 | G3 Bb3 | Bb2 F3 | C3 G3 | Ab2 Eb3 | G2 D3 | Bb2 F3 | Eb3 Bb3 | Bb2 F3',v=49)
    s.blocks(h,22,'Eb3 G3 Bb3 | | Ab3 C4 Eb4 | | G3 Bb3 Eb4 | | Ab3 C4 Eb4 | | Bb3 D4 F4 |',dur=7.8,v=40)
    s.line(p,32,'Eb4:1 G4:1 Bb4:2 | Ab4:1 G4:1 F4:1 | Eb4+G4:3 | R:4',54,.99)
    s.line(f,32,'G5:2 F5:1 | Eb5:2 Bb4:1 | Eb5:3',48,.98)
    s.blocks(l,32,'Ab2 Eb3 | Bb2 F3 | Eb3 Bb3 F4 |',dur=3.7,v=40)
    return s

PIECES=[one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,twentythree,twentyfour,twentyfive,twentysix,twentyseven,twentyeight,twentynine,thirty]
