import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {IntentListComponent} from "./intent/intent-list/intent-list.component";
import {IntentEditComponent} from "./intent/intent-edit/intent-edit.component";
import {HomeComponent} from "./home/home.component";

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'intents',  component: IntentListComponent },
  { path: 'intent/:name', component: IntentEditComponent }
  ];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NluManageRoutingModule { }
