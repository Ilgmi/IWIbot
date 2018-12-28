import {Component, Input, OnInit, Type} from '@angular/core';
import {IntentSentence} from '../../../../model/intent/intent-sentence';
import {IntentTextInterface} from '../../../../model/intent/intent-text-interface';
import {IntentText} from '../../../../model/intent/intent-text';
import {IntentTextWithEntity} from '../../../../model/intent/intent-text-with-entity';

@Component({
  selector: 'app-sentence-edit',
  templateUrl: './sentence-edit.component.html',
  styleUrls: ['./sentence-edit.component.css']
})
export class SentenceEditComponent implements OnInit {

  @Input() sentence: IntentSentence;

  public trainingSentence = '';
  public oldSentence = '';

  // entities laden
  entities = [];

  IntentText: Type<IntentText> = IntentText;
  IntentTextWithEntity: Type<IntentTextWithEntity> = IntentTextWithEntity;

  constructor() { }

  ngOnInit() {
    this.sentence.data.forEach( item => {
      this.trainingSentence += item.text;
      this.oldSentence += item.text;
    });
  }

  isInstanceOf(object, type: Type<any>) {
    return object instanceof type;
  }

  asIntentText(intent: IntentTextInterface): IntentText {
    return <IntentText>intent;
  }

  asIntentTextWithEntity(intent: IntentTextInterface): IntentTextWithEntity {
    return <IntentTextWithEntity>intent;
  }

  // Vielleicht ein Modal

  addText() {
    this.sentence.data.push(new IntentText());
  }

  addTextWithEntity() {
    this.sentence.data.push(new IntentTextWithEntity());
  }

  delete(text: IntentTextInterface) {
    const index = this.sentence.data.indexOf(text);
    if (index >= 0) {
      this.sentence.data.splice(index, 1);
    }
  }

  public intentSentenceChanged(){
    this.sentence.data.forEach( item => {
      this.trainingSentence += item.text;
      this.oldSentence += item.text;
    });
  }

  public sentenceChanged(sentence: string) {

  }
}
