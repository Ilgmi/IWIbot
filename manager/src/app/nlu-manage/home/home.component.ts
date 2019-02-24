import { Component, OnInit } from '@angular/core';
import {NluService} from '../../services/nlu.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  sentence: string;
  entity;
  intent;

  intentSpinner = false;
  entitySpinner = false;

  constructor(private nluService: NluService) { }

  ngOnInit() {
  }

  testNlu() {
    this.intentSpinner = true;
    this.entitySpinner = true;

    this.nluService.getIntent({sentence: this.sentence}).subscribe( value => {
      this.intent = value.classifications.intent;
      this.intentSpinner = false;
    });
    this.nluService.getEntity({sentence: this.sentence}).subscribe( value => {
      this.entity = value.classifications.entity;
      this.entitySpinner = false;
    });

  }
}
