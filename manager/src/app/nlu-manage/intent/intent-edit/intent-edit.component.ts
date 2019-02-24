import {Component, Input, OnInit} from '@angular/core';
import {Intent} from '../../../model/intent/intent';
import {NluService} from '../../../services/nlu.service';
import {ActivatedRoute, Router} from '@angular/router';
import {IntentSentence} from '../../../model/intent/intent-sentence';
import {DataContainer} from '../../../model/data-container';
import {Entity} from '../../../model/entity/entity';
import {Observable} from 'rxjs';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {ConfirmModalComponent} from '../../../modal/confirm-modal/confirm-modal.component';

@Component({
  selector: 'app-intent-edit',
  templateUrl: './intent-edit.component.html',
  styleUrls: ['./intent-edit.component.css']
})
export class IntentEditComponent implements OnInit {


  constructor(private route: ActivatedRoute,
              private router: Router,
              private nluService: NluService,
              private modalService: NgbModal) { }

  oldName: string;
  name: string = null;

  intent: Intent = null;
  intentCopy: Intent = null;

  listOfEntities: string[] = [];

  private function;
  ngOnInit() {
    this.name = this.route.snapshot.paramMap.get('name');
    this.oldName = this.name;
    this.router.routeReuseStrategy.shouldReuseRoute = function () {
      return false;
    };
    this.nluService.intentService.getIntent(this.name).subscribe(
      value => {
        this.intent = value;
        this.intentCopy = <Intent>this.deepCopy(value);
      }
    );
    this.nluService.entityService.getEntities().subscribe( entities => {
      console.log(entities.getKeys());
      this.listOfEntities = entities.getKeys();
    });
  }

  public updateName() {
    this.nluService.intentService.createIntent(this.name, this.intent).subscribe(
      value => this.nluService.intentService.deleteIntent(this.oldName).subscribe(
        value1 => this.router.navigate(['/intent/', this.name])
      )
    );
  }

  private prepareSentences() {
    this.intent.utterances.forEach( sentence => {
      sentence.data.forEach( (item, index, s) => {
        if (index === 0) {

        } else if ((index === s.length - 1)) {

        } else {

        }
      });
    });
  }

  public save() {
    this.nluService.intentService.updateIntent(this.name, this.intent).subscribe();
  }

  addSentence() {
    this.intent.utterances.push(new IntentSentence());
  }

  private deepCopy(obj) {
    let copy;

    // Handle the 3 simple types, and null or undefined
    if (null == obj || 'object' !== typeof obj) { return obj; }

    // Handle Date
    if (obj instanceof Date) {
      copy = new Date();
      copy.setTime(obj.getTime());
      return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
      copy = [];
      for (let i = 0, len = obj.length; i < len; i++) {
        copy[i] = this.deepCopy(obj[i]);
      }
      return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
      copy = {};
      for (const attr in obj) {
        if (obj.hasOwnProperty(attr)) { copy[attr] = this.deepCopy(obj[attr]); }
      }
      return copy;
    }

    throw new Error('Unable to copy obj! Its type isn\'t supported.');
  }

  deleteSentence(sentence: IntentSentence) {
    const index = this.intent.utterances.indexOf(sentence);
    if (index > -1) {

      const modalRef = this.modalService.open(ConfirmModalComponent);
      (<ConfirmModalComponent>modalRef.componentInstance).text = 'Wollen Sie den Satz wirklich löschen ?';

      (<Promise<boolean>>modalRef.result).then( (reason) => {
        this.intent.utterances.splice(index, 1);
      });


    }
  }
}
