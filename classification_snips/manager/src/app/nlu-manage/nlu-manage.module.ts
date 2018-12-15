import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { NluManageRoutingModule } from './nlu-manage-routing.module';
import { EntityListComponent } from './entity/entity-list/entity-list.component';
import { EntityEditComponent } from './entity/entity-edit/entity-edit.component';
import { IntentListComponent } from './intent/intent-list/intent-list.component';
import { IntentEditComponent } from './intent/intent-edit/intent-edit.component';
import { SentenceEditComponent } from './intent/intent-edit/sentence-edit/sentence-edit.component';
import {FormsModule} from "@angular/forms";
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import { HomeComponent } from './home/home.component';

@NgModule({
  declarations: [
    EntityListComponent,
    EntityEditComponent,
    IntentListComponent,
    IntentEditComponent,
    SentenceEditComponent,
    HomeComponent
  ],
  exports: [
    IntentEditComponent,
    SentenceEditComponent
  ],
  imports: [
    CommonModule,
    NluManageRoutingModule,
    FormsModule,
    NgbModule,
  ]
})
export class NluManageModule { }
