import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { CdkTableModule } from '@angular/cdk/table';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {MatButtonModule,
        MatCheckboxModule,
        MatToolbarModule,
        MatIconModule,
        MatDialogModule,
        MatFormFieldModule,
        MatInputModule,
        MatSelectModule,
        MatSidenavModule
      } from '@angular/material';
import { FlexLayoutModule } from '@angular/flex-layout';
import { AppComponent } from './app.component';
import { SpeechToTextService } from './shared/services/speech-to-text-service.service';
import { ChatComponent } from './chat/chat.component';
import { ConversationService } from './shared/services/conversation.service';
import { Conversation} from './shared/models/conversation';
import { TextToSpeechService } from './shared/services/text-to-speech.service';
import { LoginDialogComponent } from './login-dialog/login-dialog.component';
import { LoginService } from './shared/services/login.service';
import { ToolbarComponent } from './toolbar/toolbar.component';


@NgModule({
  declarations: [
    AppComponent,
    ChatComponent,
    LoginDialogComponent,
    ToolbarComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    CdkTableModule,
    FlexLayoutModule,
    MatButtonModule,
    MatCheckboxModule,
    MatToolbarModule,
    MatIconModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatSidenavModule,
  ],
  providers: [
    SpeechToTextService,
    ConversationService,
    Conversation,
    TextToSpeechService,
    LoginService
  ],
  bootstrap: [
    AppComponent,
  ],
  entryComponents: [
    LoginDialogComponent
  ],
})
export class AppModule { }
