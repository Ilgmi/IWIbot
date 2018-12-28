import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-import',
  templateUrl: './import.component.html',
  styleUrls: ['./import.component.css']
})
export class ImportComponent implements OnInit {

  private jsonData: string = null;

  public hasValidJson = false;

  public label = 'Snips Json File';

  constructor() { }

  ngOnInit() {
  }


  private checkJson(content){
    // TODO: Check content for valid Objects

    this.hasValidJson = true;
  }

  public useFile(files: File[]) {
    console.log(files);
    if(files.length > 0){
      const file = files[0];
      this.label = file.name;
      const fileReader = new FileReader();
      fileReader.onload = (e) => {
        this.checkJson(JSON.parse(<string>fileReader.result));
      };
      fileReader.readAsText(file);
    }
  }

  replaceData() {
    // TODO: Add Modal


    // TODO: Create Intents and Entities and replace current data
  }

  addData() {
    // TODO: Add Modal


    // TODO: Create Intents an Entities and add Data to current Trainings-Data
  }
}
