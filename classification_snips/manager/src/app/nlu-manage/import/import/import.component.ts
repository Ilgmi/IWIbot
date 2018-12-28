import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-import',
  templateUrl: './import.component.html',
  styleUrls: ['./import.component.css']
})
export class ImportComponent implements OnInit {

  private jsonData: string = null;

  public hasValidJson = false;

  constructor() { }

  ngOnInit() {
  }

  useFile(files: File[]) {
    if(files.length > 0){
      const file = files[0];
      
    }
  }
}
