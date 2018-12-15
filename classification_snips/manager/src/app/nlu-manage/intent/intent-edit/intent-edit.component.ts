import {Component, Input, OnInit} from '@angular/core';
import {Intent} from "../../../model/intent/intent";

@Component({
  selector: 'app-intent-edit',
  templateUrl: './intent-edit.component.html',
  styleUrls: ['./intent-edit.component.css']
})
export class IntentEditComponent implements OnInit {

  @Input() key: string;
  myKey = '';
  @Input() intent: Intent;

  constructor() { }

  ngOnInit() {
  }

  myLog(){
    console.log(this.key);
  }

}
