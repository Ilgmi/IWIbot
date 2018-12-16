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

  public intents: DataContainer<Intent> = new DataContainer<Intent>();

  constructor(private nluService: NluService) {

    this.intents = new DataContainer<Intent>();
    this.nluService.intentService.getIntents().subscribe(
      value => {
        value.getKeys().forEach( key =>{
          this.intents.setValue(key, value.getValue(key));
        });
      }
    );

  }

  ngOnInit() {
  }

  deleteIntent(intentKey: string) {
    if(this.intents.keyExists(intentKey)){
      // Modal

      // Soll Gelöscht werden
      this.nluService.intentService.deleteIntent(intentKey).subscribe(
        success => this.updateList()
      );
    }
  }

  private updateList(){
    this.nluService.intentService.getIntents().subscribe(resultV => {
      this.intents = resultV;
    });
  }

  addNewIntent(value: string) {
    console.log(value);
    console.log((this.intents));
    if(!this.intents.keyExists(value)){
      this.nluService.intentService.createIntent(value, new Intent()).subscribe(
        value1 => this.updateList(),
        error1 => console.log(error1)
      );

    }
  }
}
