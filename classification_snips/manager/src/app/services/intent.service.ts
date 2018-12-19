import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Intent} from '../model/intent/intent';
import {Observable} from 'rxjs';
import {DataContainer} from '../model/data-container';
import {map} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class IntentService {

  private readonly apiUrl = '/api/intent';

  constructor(private httpClient: HttpClient) { }

  public createIntent(key: string, intent: Intent) {
    console.log(key, intent);
    return this.httpClient.post(this.apiUrl + '/' + key, intent);
  }

  public updateIntent(key: string, intent: Intent) {
    console.log(key, intent);
    return this.httpClient.put(this.apiUrl + '/' + key, intent);
  }

  public getIntent(key: string): Observable<Intent> {
    return this.httpClient.get<Intent>(this.apiUrl + '/' + key)
      .pipe(
        map( value => {
          return new Intent().deserialize(value);
        })
      );
  }

  public deleteIntent(key: string){
    return this.httpClient.delete(this.apiUrl + '/' + key);
  }

  public getIntents(): Observable<DataContainer<Intent>> {
    return this.httpClient.get(this.apiUrl)
      .pipe(
        map( value => {
          const result = new DataContainer<Intent>();
          const keys = Object.keys(value);
          keys.forEach( key => {
            result.setValue(key, new Intent().deserialize(value[key]));
          });
          return result;
        })
      );
  }
}
