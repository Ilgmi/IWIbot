import { Component } from '@angular/core';
import {NluService} from "./services/nlu.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'manager';

  constructor(private nluService: NluService){}

  testService() {
    this.nluService.getIntents().subscribe( value => console.log(value));
  }
}
