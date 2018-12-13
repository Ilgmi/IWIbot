import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NluManageRoutingModule } from './nlu-manage-routing.module';
import { EntityListComponent } from './entity/entity-list/entity-list.component';
import { EntityEditComponent } from './entity/entity-edit/entity-edit.component';
import { IntentListComponent } from './intent/intent-list/intent-list.component';
import { IntentEditComponent } from './intent/intent-edit/intent-edit.component';

@NgModule({
  declarations: [EntityListComponent, EntityEditComponent, IntentListComponent, IntentEditComponent],
  imports: [
    CommonModule,
    NluManageRoutingModule
  ]
})
export class NluManageModule { }
