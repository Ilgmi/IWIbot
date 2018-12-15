import {jsonMapMember, jsonObject} from 'typedjson';
import {Intent} from './intent/intent';
import {Deserializable} from '../interfaces/deserializable';
import {DataContainer} from "./data-container";

export class TrainingsData implements Deserializable<TrainingsData> {

  public intents: DataContainer<Intent>;


  constructor() {
  }



  deserialize(input: any): TrainingsData {
    Object.assign(this, input);
    this.intents = new DataContainer();
    const keys = Object.keys(input);
    keys.forEach( key => {
      this.intents.setValue(key, new Intent().deserialize(input[key]));
    });
    return this;
  }
}
