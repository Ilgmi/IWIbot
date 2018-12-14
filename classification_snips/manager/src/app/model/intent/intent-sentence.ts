import {IntentText} from './intent-text';
import {Deserializable} from '../../interfaces/deserializable';
import {IntentTextWithEntity} from './intent-text-with-entity';

export class IntentSentence implements Deserializable<IntentSentence> {
  public data: IntentText[] = [];

  deserialize(input: any): IntentSentence {
    Object.assign(this, input);
    this.data = [];
    input.data.forEach( item => {
      if (item.entity !== undefined && item.slot_name !== undefined ) {
        this.data.push(new IntentTextWithEntity().deserialize(item));
      } else {
        this.data.push(new IntentText().deserialize(item));
      }
    });
    return this;
  }


}
