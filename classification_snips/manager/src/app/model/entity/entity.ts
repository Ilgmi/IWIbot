import {Deserializable} from '../../interfaces/deserializable';
import {EntityData} from './entity-data';

export class Entity implements Deserializable<Entity> {
  public automatically_extensible = false;
  public matching_strictness = 1.0;
  public use_synonyms = false;

  public data: EntityData[] = [];


  public constructor(){
  }

  deserialize(input: any): Entity {
    Object.assign(this, input);

    this.data = [];
    input.data.forEach( item => {
      this.data.push(new EntityData().deserialize(item));
    });

    return this;
  }




}
