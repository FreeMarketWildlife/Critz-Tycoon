// Several keys/fingers can own the same direction. Releasing one source must
// never release another source; blur, menus and visibility clear every source.
export class HeldDirections extends Set {
  constructor(){super();this.sources=new Map();}
  press(source,direction){
    if(this.sources.get(source)===direction)return;
    this.sources.delete(source);this.sources.set(source,direction);this.sync();
  }
  release(source){if(this.sources.delete(source))this.sync();}
  sync(){super.clear();for(const direction of this.sources.values())super.add(direction);}
  clear(){this.sources.clear();super.clear();}
  latest(){return [...this.sources.values()].at(-1)||null;}
}
