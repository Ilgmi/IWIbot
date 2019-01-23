import { Injectable } from '@angular/core';
import {Intent} from '../model/intent/intent';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {map} from 'rxjs/operators';
import {jsonArrayMember, jsonObject, TypedJSON} from 'typedjson';
import {IntentSentence} from '../model/intent/intent-sentence';
import {TrainingsData} from '../model/trainings-data';
import {DataContainer} from '../model/data-container';
import {IntentService} from './intent.service';
import {EntityService} from './entity.service';
import {SentenceService} from './sentence.service';

@jsonObject()
class Intents {
  @jsonArrayMember(Intent)
  intents: Intent[];
}

@Injectable({
  providedIn: 'root'
})
export class NluService {

  private readonly apiUrl = '/api/';

  public constructor(
    private httpClient: HttpClient,
    public intentService: IntentService,
                     public entityService: EntityService,
    public sentenceService: SentenceService
  ) {}

  public getIntent(s: {sentence: string}): Observable<{classifications: {intent: string}}> {
    return this.httpClient.post<{classifications: {intent: string}}>(this.apiUrl + 'getIntent', s);
  }

  public getEntity(s: {sentence: string}): Observable<{classifications: {entity: string}}> {
    return this.httpClient.post<{classifications: {entity: string}}>(this.apiUrl + 'getEntity', s);
  }

  public trainNLU(): Observable<string> {
    return this.httpClient.get(this.apiUrl + 'trainEngine').pipe(
      map( v => v.toString())
    );
  }


  public roleBack(): Observable<string> {
    return this.httpClient.get(this.apiUrl + 'rollbackEngine').pipe(
      map( v => v.toString())
    );
  }

}
