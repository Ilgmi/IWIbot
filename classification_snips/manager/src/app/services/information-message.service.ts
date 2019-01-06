import {EventEmitter, Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class InformationMessageService {

  public errorMessage = new EventEmitter<string>();
  public informationMessage = new EventEmitter<string>();

  constructor() { }
}
