import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import {HttpClientModule} from '@angular/common/http';
import {NluManageModule} from './nlu-manage/nlu-manage.module';
import {FormsModule} from '@angular/forms';
import { SidenavComponent } from './sidenave/sidenav.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { AppRoutingModule } from './app-routing.module';
import { ConfirmModalComponent } from './modal/confirm-modal/confirm-modal.component';



@NgModule({
  declarations: [
    AppComponent,
    SidenavComponent,
    NotFoundComponent,
    ConfirmModalComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    NluManageModule,
    FormsModule,
    AppRoutingModule
  ],
  entryComponents: [ConfirmModalComponent],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
