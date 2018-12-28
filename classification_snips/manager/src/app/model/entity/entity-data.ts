import {Deserializable} from '../../interfaces/deserializable';

export class EntityData implements Deserializable<EntityData> {
  public value = '';
  public synonyms: string[] = [];


  constructor() {
  }

  deserialize(input: any): EntityData {
    Object.assign(this, input);
    return this;
  }


}
