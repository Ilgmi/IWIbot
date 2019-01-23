import { Component, OnInit } from '@angular/core';
import {Intent} from '../../model/intent/intent';
import {DataContainer} from '../../model/data-container';
import {IntentSentence} from '../../model/intent/intent-sentence';
import {IntentText} from '../../model/intent/intent-text';
import {NluService} from '../../services/nlu.service';
import {observable, Observable} from 'rxjs';

@Component({
  selector: 'app-sentence',
  templateUrl: './sentence.component.html',
  styleUrls: ['./sentence.component.css']
})
export class SentenceComponent implements OnInit {

  intents: DataContainer<Intent>;
  sentences: string[];

  public isLoaded = false;

  constructor(private nluService: NluService) {

  }

  ngOnInit() {
    this.nluService.sentenceService.getSentences().subscribe( value => {this.sentences = value; this.isLoaded = this.intents !== undefined; });
    this.nluService.intentService.getIntents().subscribe( value => {this.intents = value; this.isLoaded = this.sentences !== undefined; });
  }

  private updateSentence() {
    this.nluService.sentenceService.updateSentences(this.sentences).subscribe( value => this.sentences = value);
  }

  deleteSentence(index: number) {
    this.sentences.splice(index, 1);
    this.updateSentence();
  }

  sentenceToIntent(intentKey: string, sentence: string, index: number) {
    const newIntent = new IntentSentence();
    newIntent.data.push(new IntentText(sentence));
    this.intents.getValue(intentKey).utterances.push(newIntent);
    this.nluService.intentService.updateIntent(intentKey, this.intents.getValue(intentKey)).subscribe();
    this.sentences.splice(index);
    this.updateSentence();
  }


}
