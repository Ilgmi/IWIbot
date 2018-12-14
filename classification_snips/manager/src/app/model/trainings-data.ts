import {jsonMapMember, jsonObject} from 'typedjson';
import {Intent} from './intent/intent';
import {Deserializable} from '../interfaces/deserializable';

export class TrainingsData implements Deserializable<TrainingsData> {

  public intents: { [key: string]: Intent};


  constructor() {
  }

  public getKeys(): string[] {
    return Object.keys(this.intents);
  }

  public setIntent(key: string, intent: Intent) {
    this.intents[key] = intent;
  }

  public keyExists(key: string): boolean {
    const keys = this.getKeys();
    return keys.indexOf(key) >= 0;
  }

  public getIntent(key): Intent {
    if (this.keyExists(key)) {
      return this.intents[key];
    } else {
      return null;
    }
  }

  public getIntents(): Intent[] {
    const intents: Intent[] = [];
    const keys = this.getKeys();
    keys.forEach( key => intents.push(this.intents[key]));
    return intents;
  }

  deserialize(input: any): TrainingsData {
    Object.assign(this, input);
    this.intents = {};
    const keys = Object.keys(input);
    keys.forEach( key => {
      this.setIntent(key, new Intent().deserialize(input[key]));
    });
    return this;
  }
}
