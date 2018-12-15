import { Component } from '@angular/core';
import {NluService} from './services/nlu.service';
import {isInstanceOf} from 'typedjson/js/typedjson/helpers';
import {IntentTextWithEntity} from './model/intent/intent-text-with-entity';
import {IntentText} from "./model/intent/intent-text";
import {Intent} from "./model/intent/intent";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'manager';

  constructor(private nluService: NluService) {}

  t: Intent = null;


  testService() {
    this.nluService.intentService.getIntents().subscribe( value => {
      this.t = value.getValues()[0];
      const tmp = value.getValues()[0].utterances[0].data;
    });

  }
}
