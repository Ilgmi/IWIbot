import { Component, OnInit } from '@angular/core';
import {NluService} from "../../../services/nlu.service";
import {DataContainer} from "../../../model/data-container";
import {Intent} from "../../../model/intent/intent";
import {InformationMessageService} from '../../../services/information-message.service';
import {HttpErrorResponse} from '@angular/common/http';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {ConfirmModalComponent} from '../../../modal/confirm-modal/confirm-modal.component';

@Component({
  selector: 'app-intent-list',
  templateUrl: './intent-list.component.html',
  styleUrls: ['./intent-list.component.css']
})
export class IntentListComponent implements OnInit {

  public intents: DataContainer<Intent> = new DataContainer<Intent>();

  constructor(private nluService: NluService, private informationMessageService: InformationMessageService, private modalService: NgbModal) {

    this.intents = new DataContainer<Intent>();
    this.nluService.intentService.getIntents().subscribe(
      value => {
        value.getKeys().forEach( key =>{
          this.intents.setValue(key, value.getValue(key));
        });
      },
      error => {
        const e = <HttpErrorResponse>error;
        if(e.status >= 400 && e.status < 500){
          this.informationMessageService.errorMessage.emit(e.message);
          console.log(e);
        }else if(e.status >= 500 && e.status < 600){
          this.informationMessageService.errorMessage.emit('Server Error');
        }
      }
    );

  }

  ngOnInit() {
  }

  deleteIntent(intentKey: string) {
    if(this.intents.keyExists(intentKey)){
      // Modal

      const modalRef = this.modalService.open(ConfirmModalComponent);
      (<ConfirmModalComponent>modalRef.componentInstance).text = 'Wollen Sie den Intent ' + intentKey + ' wirklich löschen ?';

      (<Promise<boolean>>modalRef.result).then( (reason) => {
        this.nluService.intentService.deleteIntent(intentKey).subscribe(
          success => this.updateList()
        );
      });

    }
  }

  private updateList(){
    this.nluService.intentService.getIntents().subscribe(resultV => {
      this.intents = resultV;
    });
  }

  addNewIntent(value: string) {
    if(!this.intents.keyExists(value)){
      this.nluService.intentService.createIntent(value, new Intent()).subscribe(
        value1 => this.updateList(),
        error1 => console.log(error1)
      );

    }
  }
}
