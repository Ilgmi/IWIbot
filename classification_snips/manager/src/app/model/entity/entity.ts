import {Deserializable} from '../../interfaces/deserializable';
import {EntityData} from './entity-data';
import {DeserializerHelper} from '../../helper/deserializer-helper';

export class Entity implements Deserializable<Entity> {
  public automatically_extensible = false;
  public matching_strictness = 1.0;
  public use_synonyms = false;

  public data: EntityData[] = [];


  public constructor(){
  }

  deserialize(input: any): Entity {
    DeserializerHelper.checkObject(input, this);
    Object.assign(this, input);

    this.data = [];

    if(input.data !== undefined && input.data !== null){
      input.data.forEach( item => {
        this.data.push(new EntityData().deserialize(item));
      });
    }

    return this;
  }




}
