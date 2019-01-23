import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SentenceService {
  private readonly apiUrl = '/api/sentence/';
  constructor(private httpClient: HttpClient) { }


  public getSentences(): Observable<string[]> {
    return this.httpClient.get<string[]>(this.apiUrl);
  }

  public updateSentences(sentences: string[]){
    return this.httpClient.put<string[]>(this.apiUrl, sentences);
  }

}
