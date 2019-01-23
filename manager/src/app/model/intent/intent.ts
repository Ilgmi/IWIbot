import {IntentSentence} from './intent-sentence';
import {Deserializable} from '../../interfaces/deserializable';
import {DeserializerHelper} from '../../helper/deserializer-helper';

export class Intent implements Deserializable<Intent> {

  public utterances: IntentSentence[] = [];


  constructor() {
  }

  deserialize(input: any): Intent {
    DeserializerHelper.checkObject(input, this);
    console.log(input);

    Object.assign(this, input);
    this.utterances = [];
    input.utterances.forEach( item => this.utterances.push(new IntentSentence().deserialize(item)));
    return this;
  }



}
