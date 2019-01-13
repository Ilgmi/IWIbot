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

  constructor(private nluService: NluService) { }

  ngOnInit() {
  }

  testNlu() {
    this.nluService.getIntent({sentence: this.sentence}).subscribe( value => this.intent = value);
    this.nluService.getEntity({sentence: this.sentence}).subscribe( value => this.entity = value);

  }
}
