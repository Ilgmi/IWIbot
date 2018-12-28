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


  private checkJson(content){
    // TODO: Check content for valid Objects
  }

  public useFile(files: File[]) {
    console.log(files);
    if(files.length > 0){
      const file = files[0];
      const fileReader = new FileReader();
      fileReader.onload = (e) => {
        this.checkJson(JSON.parse(<string>fileReader.result));
      };
      fileReader.readAsText(file);
    }
  }
}
