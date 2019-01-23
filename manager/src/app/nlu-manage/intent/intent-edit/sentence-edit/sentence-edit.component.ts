import {Component, EventEmitter, Input, OnInit, Output, Type} from '@angular/core';
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
  @Input() listOfEntities: string[];

  @Output() deleteSentence = new EventEmitter<IntentSentence>();

  public trainingSentence = '';
  public oldSentence = '';

  // entities laden
  entities = [];

  IntentText: Type<IntentText> = IntentText;
  IntentTextWithEntity: Type<IntentTextWithEntity> = IntentTextWithEntity;

  constructor() { }

  ngOnInit() {
    this.updateSentence();
    console.log(this.listOfEntities);
  }

  public updateSentence(){
    this.sentence.data.forEach( item => {

      if (item instanceof IntentText) {
        this.trainingSentence += item.text;
      } else if (item instanceof IntentTextWithEntity) {
        this.trainingSentence += '[' + item.slot_name + ':' + item.entity + '](' + item.text + ')';
      }
    });
    this.oldSentence = this.trainingSentence;
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
    this.intentSentenceChanged();
  }

  addTextWithEntity() {
    this.sentence.data.push(new IntentTextWithEntity());
    this.intentSentenceChanged();
  }

  onDeleteSentence(){
    this.deleteSentence.next(this.sentence);
  }

  delete(text: IntentTextInterface) {
    const index = this.sentence.data.indexOf(text);
    if (index >= 0) {
      this.sentence.data.splice(index, 1);
      this.intentSentenceChanged();
    }
  }

  public intentSentenceChanged() {
    this.trainingSentence = '';
    this.oldSentence = '';
    this.updateSentence();
  }

  public sentenceChanged() {

    let _sentence = this.trainingSentence;
    const entities = [];
    let match = _sentence.match(/\[.*].*\(.*\)/);
    do {
      if (match !== null && match.length > 0) {
        _sentence = _sentence.split(match[0]).join('');
        const entityString = match[0];
        const slot_name = entityString.match(/\[.*:/)[0];
        const entity = entityString.match(/:.*\]/)[0];
        const text = entityString.match(/\(.*\)/)[0];
        console.log(match);

        const e = new IntentTextWithEntity();
        e.slot_name = slot_name.slice(1, slot_name.length - 1);
        e.entity = entity.slice(1, entity.length - 1);
        e.text = text.slice(1, text.length - 1);

        const prevE = new IntentText();
        prevE.text = match.input.slice(0, match.index);
        entities.push(prevE);
        entities.push(e);
        _sentence = match.input.slice(match.index + match[0].length, match.input.length);
      }
      match = _sentence.match(/\[.*].*\(.*\)/);
      console.log(_sentence);
    }while (match !== null);

    if(_sentence.length > 0){
      const e = new IntentText();
      e.text = _sentence.slice(0, _sentence.length);
      entities.push(e);
    }

    console.log(entities);

    this.sentence.data.splice(0, this.sentence.data.length);
    this.sentence.data.push(...entities);



  }
}
