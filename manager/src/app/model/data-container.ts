import {Intent} from './intent/intent';

export class DataContainer<T> {

  public constructor() {
    this.data = {};
  }

  private data: {[key: string]: T};

  public getKeys(): string[] {
    return Object.keys(this.data);
  }

  public setValue(key: string, value: T) {
    this.data[key] = value;
  }

  public getValue(key: string): T {
    if (this.keyExists(key)) {
      return this.data[key];
    } else {
      return null;
    }
  }

  public keyExists(key: string): boolean {
    const keys = this.getKeys();
    return keys.indexOf(key) >= 0;
  }



  public getValues(): T[] {
    const d: T[] = [];
    const keys = this.getKeys();
    keys.forEach( key => d.push(this.data[key]));
    return d;
  }

}
