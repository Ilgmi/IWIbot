import {Component, Input, OnInit} from '@angular/core';
import {Intent} from '../../../model/intent/intent';
import {NluService} from '../../../services/nlu.service';
import {ActivatedRoute, Router} from '@angular/router';
import {IntentSentence} from '../../../model/intent/intent-sentence';

@Component({
  selector: 'app-intent-edit',
  templateUrl: './intent-edit.component.html',
  styleUrls: ['./intent-edit.component.css']
})
export class IntentEditComponent implements OnInit {

  oldName: string;
  name: string = null;
  intent: Intent = null;

  constructor(private route: ActivatedRoute,
              private router: Router,
              private nluService: NluService) { }

  ngOnInit() {
    this.name = this.route.snapshot.paramMap.get('name');
    this.oldName = this.name;
    this.router.routeReuseStrategy.shouldReuseRoute = function () {
      return false;
    };
    this.nluService.intentService.getIntent(this.name).subscribe(
      value => this.intent = value
    );
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
}
