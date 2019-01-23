import {Deserializable} from '../../interfaces/deserializable';
import {DeserializerHelper} from '../../helper/deserializer-helper';

export class EntityData implements Deserializable<EntityData> {
  public value = '';
  public synonyms: string[] = [];


  constructor() {
  }

  deserialize(input: any): EntityData {
    DeserializerHelper.checkObject(input, this);
    Object.assign(this, input);
    return this;
  }


}
