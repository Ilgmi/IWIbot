import { Component, OnInit } from '@angular/core';
import {NluService} from '../../services/nlu.service';
import {HttpErrorResponse} from '@angular/common/http';

@Component({
  selector: 'app-training',
  templateUrl: './training.component.html',
  styleUrls: ['./training.component.css']
})
export class TrainingComponent implements OnInit {
  public status: string;

  public showSpinner = false;

  constructor(private nluService: NluService) { }

  ngOnInit() {
  }

  trainNlu(){
    this.showSpinner = true;
    this.nluService.trainNLU().subscribe( value => {
      console.log(value);
      this.status = value;
      this.showSpinner = false;
    }, error =>  {
      console.log(error);
      this.status = error.message;
      this.showSpinner = false;
    });
  }

  roleBack(){
    this.nluService.roleBack().subscribe(value => {
      console.log(value);
      this.status = value;
      this.showSpinner = false;
    }, error =>  {
      console.log(error);
      this.status = error.message;
      this.showSpinner = false;
    });
  }

  setSuccess(s: string){
    this.status = s;
  }
  setError(error: HttpErrorResponse){
    console.log(error);
    this.status = error.message;
    console.log(this.status);
  }

}
