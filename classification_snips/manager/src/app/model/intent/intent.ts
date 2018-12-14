import {IntentSentence} from "./intent-sentence";
import {Deserializable} from "../../interfaces/deserializable";

export class Intent implements Deserializable<Intent>{
  public utterances: IntentSentence[] = [];


  constructor() {
  }

  deserialize(input: any): Intent {
    Object.assign(this, input);
    this.utterances = [];
    input.utterances.forEach( item => this.utterances.push(new IntentSentence().deserialize(item)));
    return this;
  }



}
