import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {IntentListComponent} from './intent/intent-list/intent-list.component';
import {IntentEditComponent} from './intent/intent-edit/intent-edit.component';
import {HomeComponent} from './home/home.component';
import {EntityListComponent} from './entity/entity-list/entity-list.component';
import {EntityEditComponent} from './entity/entity-edit/entity-edit.component';
import {ImportComponent} from './import/import/import.component';
import {TrainingComponent} from './training/training.component';
import {SentenceComponent} from './sentence/sentence.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'intents',  component: IntentListComponent },
  { path: 'intent/:name', component: IntentEditComponent },
  { path: 'entities', component: EntityListComponent},
  { path: 'entity/:name', component: EntityEditComponent},
  { path: 'import', component: ImportComponent},
  { path: 'training', component: TrainingComponent},
  { path: 'sentences', component: SentenceComponent},
  ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NluManageRoutingModule { }
