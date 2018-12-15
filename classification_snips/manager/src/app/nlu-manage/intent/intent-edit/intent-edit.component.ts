import {Component, Input, OnInit} from '@angular/core';
import {Intent} from "../../../model/intent/intent";
import {NluService} from "../../../services/nlu.service";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-intent-edit',
  templateUrl: './intent-edit.component.html',
  styleUrls: ['./intent-edit.component.css']
})
export class IntentEditComponent implements OnInit {

  name: string = null;
  intent: Intent = null;

  constructor(private route: ActivatedRoute,
              private nluService: NluService) { }

  ngOnInit() {
    this.name = this.route.snapshot.paramMap.get('name');
    this.nluService.intentService.getIntent(this.name).subscribe(
      value => this.intent = value
    );
  }


}
