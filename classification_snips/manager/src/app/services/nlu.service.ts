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

@jsonObject()
class Intents {
  @jsonArrayMember(Intent)
  intents: Intent[];
}

@Injectable({
  providedIn: 'root'
})
export class NluService {

  private readonly apiUrl = '/api/nlu/';

  public constructor(
    private httpClient: HttpClient,
    public intentService: IntentService,
                     public entityService: EntityService
  ) {}

  public trainNLU(){
    this.httpClient.get(this.apiUrl + 'train');
  }


  public roleBack(){
    this.httpClient.get(this.apiUrl + 'roleback');
  }

}
