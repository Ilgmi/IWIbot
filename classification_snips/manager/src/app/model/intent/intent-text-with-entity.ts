import {IntentText} from './intent-text';

export class IntentTextWithEntity extends IntentText{
  public entity = '';
  public slot_name = '';


  constructor() {
    super();
  }

  deserialize(input: any): IntentTextWithEntity {
    super.deserialize(input);
    Object.assign(this, input);
    return this;
  }
}
