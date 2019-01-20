import {Deserializable} from "../../interfaces/deserializable";
import {IntentTextInterface} from "./intent-text-interface";
import {DeserializerHelper} from '../../helper/deserializer-helper';

export class IntentText implements IntentTextInterface, Deserializable<IntentText>{
  public text = '';


  constructor(text = '') {
    this.text = text;
  }

  deserialize(input: any): IntentText {
    DeserializerHelper.checkObject(input, this)
    Object.assign(this, input);
    return this;
  }
}
