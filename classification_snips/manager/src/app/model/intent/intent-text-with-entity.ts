import {IntentText} from './intent-text';
import {IntentTextInterface} from "./intent-text-interface";
import {Deserializable} from "../../interfaces/deserializable";

export class IntentTextWithEntity implements IntentTextInterface, Deserializable<IntentTextWithEntity>{
  public text = '';
  public entity = '';
  public slot_name = '';


  constructor() {
  }

  deserialize(input: any): IntentTextWithEntity {
    Object.assign(this, input);
    return this;
  }
}
