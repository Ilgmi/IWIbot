import {jsonMapMember, jsonObject} from 'typedjson';
import {Intent} from './intent/intent';
import {Deserializable} from '../interfaces/deserializable';
import {DataContainer} from "./data-container";
import {Entity} from './entity/entity';
import {DeserializerHelper} from '../helper/deserializer-helper';

export class TrainingsData implements Deserializable<TrainingsData> {

  public intents: DataContainer<Intent>;
  public entities: DataContainer<Entity>;
  public language: string;


  constructor() {
    this.intents = new DataContainer();
    this.entities = new DataContainer();
    this.language = '';
  }



  deserialize(input: any): TrainingsData {
    DeserializerHelper.checkObject(input, this);
    Object.assign(this, input);
    this.intents = new DataContainer();
    let tmpData = input['intents'];
    let keys = Object.keys(tmpData);
    keys.forEach( intentKey => {
      this.intents.setValue(intentKey, new Intent().deserialize(tmpData[intentKey]));
    });

    this.entities = new DataContainer();
    tmpData = input['entities'];
    console.log(tmpData);
    keys = Object.keys(tmpData);
    keys.forEach( entityKeys => {
      console.log(entityKeys);
      this.entities.setValue(entityKeys, new Entity().deserialize(tmpData[entityKeys]));
    });

    return this;
  }
}
