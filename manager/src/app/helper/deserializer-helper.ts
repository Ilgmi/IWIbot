export class DeserializerHelper {


  public static hasKey(value: any, key): boolean {
    return value.hasOwnProperty(key);
  }

  public static hasKeys(value: any, keys: string[]): boolean {

    for (let i = 0; i < keys.length; i++) {
      if (!this.hasKey(value, keys[i])) {
        return false;
      }
    }

    return true;
  }

  public static checkObject(input, value): boolean {
    const keys = Object.keys(value);

    if (!this.hasKeys(value, keys)) {
      throw new Error('Deserialize Error');
    }

    return true;
  }

}
