import { Injectable } from '@angular/core';
import {Intent} from "../model/intent/intent";
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {map} from "rxjs/operators";
import {jsonArrayMember, jsonObject, TypedJSON} from "typedjson";
import {IntentSentence} from "../model/intent/intent-sentence";
import {TrainingsData} from "../model/trainings-data";

@jsonObject()
class Intents{
  @jsonArrayMember(Intent)
  intents: Intent[];
}

@Injectable({
  providedIn: 'root'
})
export class NluService {

  constructor(private httpClient: HttpClient) { }




  public getIntents(): Observable<Intent[]> {
    return this.httpClient.get<Intent[]>('/assets/mock-data/intents.json')
      .pipe(
        map( value => {
          const result = new Array<Intent>();
          const keys = Object.keys(value);
          console.log(keys);
          keys.forEach( key => {
            result.push(new Intent().deserialize(value[key]));
          });
          return result;
        })
      );
  }

}
