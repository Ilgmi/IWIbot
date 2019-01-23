import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {NluService} from '../../../services/nlu.service';
import {Intent} from '../../../model/intent/intent';
import {Entity} from '../../../model/entity/entity';
import {EntityData} from '../../../model/entity/entity-data';
import {formatNumber} from '@angular/common';

@Component({
  selector: 'app-entity-edit',
  templateUrl: './entity-edit.component.html',
  styleUrls: ['./entity-edit.component.css']
})
export class EntityEditComponent implements OnInit {

  oldName: string;
  name: string = null;

  entity: Entity = null;

  constructor(private route: ActivatedRoute,
              private router: Router,
              private nluService: NluService) { }

  ngOnInit() {
    this.name = this.route.snapshot.paramMap.get('name');
    this.oldName = this.name;
    this.router.routeReuseStrategy.shouldReuseRoute = function () {
      return false;
    };
    this.nluService.entityService.getEntity(this.name).subscribe(
      value => {
        this.entity = value;
        console.log(this.entity);
      }
    );
  }

  public updateSynonym(synonyms, index, value){
    synonyms[index] = value;
  }

  public updateName() {
    this.nluService.entityService.createEntity(this.name, this.entity).subscribe(
      value => this.nluService.entityService.deleteEntity(this.oldName).subscribe(
        value1 => this.router.navigate(['/entity/', this.name])
      )
    );
  }

  public save() {
    this.nluService.entityService.updateEntity(this.name, this.entity).subscribe();
  }

  addSynonym(data: EntityData) {
    data.synonyms.push('');
  }

  deleteSynonym(data: EntityData, index: number) {
    const synonyms = data.synonyms;
    if (index < synonyms.length && index >= 0 ) {
      synonyms.splice(index, 1);
    }
  }

  addEntityData(entity: Entity) {
    entity.data.push(new EntityData());
  }

  deleteEntityData(entity: Entity, data: EntityData) {
    const index = entity.data.indexOf(data);
    if (index >= 0) {
      entity.data.splice(index, 1);
    }
  }
}
