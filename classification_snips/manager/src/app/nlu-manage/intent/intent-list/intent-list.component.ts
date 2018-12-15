import { Component, OnInit } from '@angular/core';
import {NluService} from "../../../services/nlu.service";
import {DataContainer} from "../../../model/data-container";
import {Intent} from "../../../model/intent/intent";

@Component({
  selector: 'app-intent-list',
  templateUrl: './intent-list.component.html',
  styleUrls: ['./intent-list.component.css']
})
export class IntentListComponent implements OnInit {

  intents: DataContainer<Intent>;

  constructor(private nluService: NluService) {

    this.nluService.intentService.getIntents().subscribe(
      value => {
        this.intents = value;
      }
    );

  }

  ngOnInit() {
  }


  deleteIntent(intentKey: string) {
    if(this.intents.keyExists(intentKey)){
      // Modal

      // Soll Gelöscht werden
      this.nluService.intentService.deleteIntent(intentKey);
    }
  }
}
