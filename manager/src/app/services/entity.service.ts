import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Intent} from '../model/intent/intent';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {DataContainer} from '../model/data-container';
import {Entity} from '../model/entity/entity';

@Injectable({
  providedIn: 'root'
})
export class EntityService {
  private readonly apiUrl = '/api/entity';
  private readonly apiUrlSnips = this.apiUrl + '/snips';

  constructor(private httpClient: HttpClient) { }

  public createEntity(key: string, entity: Entity) {
    console.log(key, entity);
    key = key.replace('/', '%2F');
    console.log(key);
    return this.httpClient.post(this.apiUrl + '/' + key, entity);
  }

  public updateEntity(key: string, entity: Entity) {
    console.log(key, entity);
    return this.httpClient.put(this.apiUrl + '/' + key, entity);
  }

  public getEntity(key: string): Observable<Entity> {
    return this.httpClient.get<Entity>(this.apiUrl + '/' + key)
      .pipe(
        map( value => {
          return new Entity().deserialize(value);
        })
      );
  }

  public deleteEntity(key: string) {
    return this.httpClient.delete(this.apiUrl + '/' + key);
  }

  public getBuildInEntities(): Observable<string[]> {
    return this.httpClient.get<string[]>(this.apiUrlSnips);
  }

  public addBuildInEntity(name: string): Observable<any>{
    return this.httpClient.post<any>(this.apiUrlSnips + '/' + name, null);
  }

  public deleteBuildInEntity(name: string): Observable<any>{
    return this.httpClient.delete<any>(this.apiUrlSnips + '/' + name);
  }


  public getEntities(): Observable<DataContainer<Entity>> {
    return this.httpClient.get(this.apiUrl)
      .pipe(
        map( value => {
          const result = new DataContainer<Entity>();
          const keys = Object.keys(value);
          keys.forEach( key => {
            result.setValue(key, new Entity().deserialize(value[key]));
          });
          return result;
        })
      );
  }

}
