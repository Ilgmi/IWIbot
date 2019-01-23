import {IntentText} from './intent-text';
import {IntentTextInterface} from "./intent-text-interface";
import {Deserializable} from "../../interfaces/deserializable";
import {DeserializerHelper} from '../../helper/deserializer-helper';

export class IntentTextWithEntity implements IntentTextInterface, Deserializable<IntentTextWithEntity>{
  public text = '';
  public entity = '';
  public slot_name = '';


  constructor() {
  }

  deserialize(input: any): IntentTextWithEntity {
    DeserializerHelper.checkObject(input, this);
    Object.assign(this, input);
    return this;
  }
}
