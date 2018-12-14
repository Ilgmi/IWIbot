import {Deserializable} from "../../interfaces/deserializable";

export class IntentText implements Deserializable<IntentText>{
  public text = '';


  constructor() {
  }

  deserialize(input: any): IntentText {
    Object.assign(this, input);
    return this;
  }
}
