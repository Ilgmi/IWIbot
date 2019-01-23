import { Component } from '@angular/core';
import {NluService} from './services/nlu.service';
import {isInstanceOf} from 'typedjson/js/typedjson/helpers';
import {IntentTextWithEntity} from './model/intent/intent-text-with-entity';
import {IntentText} from "./model/intent/intent-text";
import {Intent} from "./model/intent/intent";
import {InformationMessageService} from './services/information-message.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'manager';

  error = '';
  information = '';

  constructor(private informationMessageService: InformationMessageService) {
    this.informationMessageService.errorMessage.subscribe( message => {
      this.error = message;
      console.log(this.error);
    });
    this.informationMessageService.informationMessage.subscribe( message => this.information = message);
  }
}
