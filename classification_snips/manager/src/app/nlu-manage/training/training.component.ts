import { Component, OnInit } from '@angular/core';
import {NluService} from '../../services/nlu.service';

@Component({
  selector: 'app-training',
  templateUrl: './training.component.html',
  styleUrls: ['./training.component.css']
})
export class TrainingComponent implements OnInit {

  constructor(private nluService: NluService) { }

  ngOnInit() {
  }

  trainNlu(){
    this.nluService.trainNLU();
  }

  roleBack(){
    this.nluService.roleBack();
  }

}
