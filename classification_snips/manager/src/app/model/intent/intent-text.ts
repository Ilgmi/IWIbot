import {Deserializable} from "../../interfaces/deserializable";
import {IntentTextInterface} from "./intent-text-interface";

export class IntentText implements IntentTextInterface, Deserializable<IntentText>{
  public text = '';


  constructor() {
  }

  deserialize(input: any): IntentText {
    Object.assign(this, input);
    return this;
  }
}
