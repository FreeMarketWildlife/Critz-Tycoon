"""Bounded rows48..53 upper-costume envelope from observed source geometry.
Original Critz material adaptation: r/c/C coral/cream, v shadow, n dark plane,
s/d/S record observed peach positions; build reclassifies those as costume and retains ONLY existing original hand sites.
This is visible costume construction, not inferred hidden anatomy.
No reference raster or palette is imported by the authoring build.
"""
UPPER={
'south':{
'A':[
'.....rsddprrrccccccrrrrpprpp....',
'.....rsppprrrrccccrrrrrpp.......',
'.....rprcpprrrrrccrrrcpp........',
'.....prcrrpcrrrrrrcccvpp........',
'.....pcCccpvcrrrrrcvCCpp........',
'.....ppccpppvcrrrcvvpppp........'],
'P':[
'...pvrrcrvcrrrrccrrrrcvrcrrvp...',
'...pccCcrvccrrrrCccrccvrcCccp...',
'...prccsppvccvrrrrCccvppsccrp...',
'....pcspppvvvcrrrrcvvCCCpscp....',
'.....pppvppvvcvvvvcvvppvppp.....',
'.......pbppppbbbbbbppppbp.......'],
'C':[
'....pprpprrrrccccccrrrpddsr.....',
'.......pprrrrrccccrrrrpppsr.....',
'........ppcrrrrrccrrrppcrpr.....',
'........ppvcrrrrrrccvprrcrp.....',
'........pppvccrrrrrcCpccCcp.....',
'........ppppvvcrrrcvpppccpp.....']},
'north':{
'A':[
'......pppprrpppppppprrddpp......',
'......pppprrpppppppprrddpp......',
'......ppppppCCccccCCppvvpp......',
'......ppppppCCccccCCppvvpp......',
'......ppppvvccccccccvvpprrvv....',
'......ppppvvccccccccvvpprrvv....'],
'P':[
'..vvrrvvppppCCccccCCppppvvrrvv..',
'..vvrrvvppppCCccccCCppppvvrrvv..',
'..vvccccppvvccccccccvvppccccrr..',
'..vvccccppvvccccccccvvppccccrr..',
'....ppppppvvvvvvvvvvvvpppprr....',
'....ppppppvvvvvvvvvvvvpppprr....'],
'C':[
'......ppddrrpppppppprrpppp......',
'......ppddrrpppppppprrpppp......',
'......ppvvppCCccccCCpppppp......',
'......ppvvppCCccccCCpppppp......',
'....vvrrppvvccccccccvvpppp......',
'....vvrrppvvccccccccvvpppp......']},
'west':{
'A':[
'..........vvrrvvrrrrnnnnpp......',
'..........vvrrvvrrrrnnnnpp......',
'........vvrrpppprrrrnnvvbbpp....',
'........vvrrpppprrrrnnvvbbpp....',
'......ppvvpprrrrpprrrrnnnnpp....',
'......ppvvpprrrrpprrrrnnnnpp....'],
'P':[
'........vvccrrpppprrnnvvbbpp....',
'........vvccrrpppprrnnvvbbpp....',
'........vvrrpprrrrpprrnnnnpp....',
'........vvrrpprrrrpprrnnnnpp....',
'........pprrppccccppppnnpp......',
'........pprrppccccppppnnpp......'],
'C':[
'..........vvvvccrrvvnnnnpp......',
'..........vvvvccrrvvnnnnpp......',
'........vvvvccrrppppnnvvbbpp....',
'........vvvvccrrppppnnvvbbpp....',
'........vvccrrpprrrrppnnnnpp....',
'........vvccrrpprrrrppnnnnpp....']}}
UPPER['east']={p:[r[::-1] for r in rows] for p,rows in UPPER['west'].items()}
assert all(len(rows)==6 and all(len(row)==32 for row in rows) for poses in UPPER.values() for rows in poses.values())
