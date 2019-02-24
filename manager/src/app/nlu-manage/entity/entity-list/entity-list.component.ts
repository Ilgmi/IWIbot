import { Component, OnInit } from '@angular/core';
import {NluService} from '../../../services/nlu.service';
import {DataContainer} from '../../../model/data-container';
import {Entity} from '../../../model/entity/entity';
import {InformationMessageService} from '../../../services/information-message.service';
import {HttpErrorResponse} from '@angular/common/http';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {ConfirmModalComponent} from '../../../modal/confirm-modal/confirm-modal.component';

@Component({
  selector: 'app-entity-list',
  templateUrl: './entity-list.component.html',
  styleUrls: ['./entity-list.component.css']
})
export class EntityListComponent implements OnInit {

  public buildInEntities: string[];

  public entities: DataContainer<Entity> = null;

  constructor(private nluService: NluService, private infoMessageService: InformationMessageService, private modalService: NgbModal) {
    this.nluService.entityService.getEntities().subscribe( value => {
      this.entities = value;
    },
    error => {
      const e = <HttpErrorResponse>error;
      if(e.status >= 400 && e.status < 500){
        this.infoMessageService.errorMessage.emit(e.message);
        console.log(e);
      }else if(e.status >= 500 && e.status < 600){
        this.infoMessageService.errorMessage.emit('Server Error');
      }
    });

    this.nluService.entityService.getBuildInEntities().subscribe( entities => this.buildInEntities = entities);
  }

  ngOnInit() {
  }

  addBuildIn(name: string){
    this.nluService.entityService.addBuildInEntity(name).subscribe( v => this.updateList());
  }

  isBuildIn(name: string){
    return name.includes('snips/');
  }

  private updateList() {
    this.nluService.entityService.getEntities().subscribe( value => this.entities = value);
  }

  deleteEntity(entityKey: string) {

    const modalRef = this.modalService.open(ConfirmModalComponent);
    (<ConfirmModalComponent>modalRef.componentInstance).text = 'Wollen Sie den Entity ' + entityKey + ' wirklich löschen ?';

    (<Promise<boolean>>modalRef.result).then( (reason) => {
      if (this.entities.keyExists(entityKey)) {
        this.nluService.entityService.deleteEntity(entityKey).subscribe(
          value => this.updateList()
        );
      }
    });
  }

  addNewEntity(name: string) {
    if (!this.entities.keyExists(name)) {
      this.nluService.entityService.createEntity(name, new Entity()).subscribe(
        value => this.updateList(),
        error1 => console.log(error1)
      );
    }
  }
}
