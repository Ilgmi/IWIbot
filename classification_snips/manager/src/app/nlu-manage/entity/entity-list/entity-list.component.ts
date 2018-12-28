import { Component, OnInit } from '@angular/core';
import {NluService} from '../../../services/nlu.service';
import {DataContainer} from '../../../model/data-container';
import {Entity} from '../../../model/entity/entity';

@Component({
  selector: 'app-entity-list',
  templateUrl: './entity-list.component.html',
  styleUrls: ['./entity-list.component.css']
})
export class EntityListComponent implements OnInit {

  public entities: DataContainer<Entity> = null;

  constructor(private nluService: NluService) {
    this.nluService.entityService.getEntities().subscribe( value => {
      this.entities = value;
    });
  }

  ngOnInit() {
  }

  private updateList(){
    this.nluService.entityService.getEntities().subscribe( value => this.entities = value);
  }

  deleteEntity(entityKey: string) {
    if(this.entities.keyExists(entityKey)){
      this.nluService.entityService.deleteEntity(entityKey).subscribe(
        value => this.updateList()
      );
    }
  }

  addNewEntity(name: string) {
    if(!this.entities.keyExists(name)){
      this.nluService.entityService.createEntity(name, new Entity()).subscribe(
        value => this.updateList(),
        error1 => console.log(error1)
      )
    }
  }
}
