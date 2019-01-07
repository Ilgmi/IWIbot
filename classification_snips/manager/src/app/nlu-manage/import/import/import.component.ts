import { Component, OnInit } from '@angular/core';
import {main} from '@angular/compiler-cli/src/main';
import {Entity} from '../../../model/entity/entity';
import {Intent} from '../../../model/intent/intent';
import {TrainingsData} from '../../../model/trainings-data';
import {NluService} from '../../../services/nlu.service';

@Component({
  selector: 'app-import',
  templateUrl: './import.component.html',
  styleUrls: ['./import.component.css']
})
export class ImportComponent implements OnInit {

  private jsonData: string = null;

  public hasValidJson = false;

  public label = 'Snips Json File';

  public errorMessage: string;

  private data: TrainingsData = null;

  constructor(private nluService: NluService) { }

  ngOnInit() {
  }

  private checkEntity(entity: Entity) {
    if (entity.data.length === 0) {
      throw new Error('Entity has no Data');
    }

    return true;
  }

  private checkIntent(intent: Intent) {
    intent.utterances.forEach( item => {
      if (item.data.length === 0) {
        throw new Error('Intent :' + intent + ' Error');
      }
    });
    return true;
  }

  private checkJson(content): boolean {
    try {
      const trainingsData = new TrainingsData().deserialize(content);
      const keys = Object.keys(content);
      console.log(keys);
      if (keys.length !== 3) {
        return false;
      }

      const mainKeys = ['entities', 'intents', 'language'];

      let i = 0;
      for (i = 0; i < mainKeys.length; i++) {
        if (keys.indexOf(mainKeys[i]) === -1) {
          return false;
        }
      }

      trainingsData.intents.getKeys().forEach( (intentKey) => {
        try {
          this.checkIntent(trainingsData.intents.getValue(intentKey));
        } catch (e) {
          throw new Error('Error in Intent:' + intentKey + ' Message: ' + e.message);
        }
      });

      trainingsData.entities.getKeys().forEach( (entityKeys) => {
        try {
          const snipsEntities = ['snips/datetime'];
          if (snipsEntities.indexOf(entityKeys) === -1) {
            this.checkEntity(trainingsData.entities.getValue(entityKeys));
          }
        } catch (e) {
          throw new Error('Error in Entity:' + entityKeys + ' Message: ' + e.message);
        }
      });


      this.data = trainingsData;


    } catch (e) {
      this.errorMessage = e.meaning;
      console.log(e);
      return false;
    }

    return true;
  }

  public useFile(files: File[]) {
    console.log(files);
    if (files.length > 0) {
      const file = files[0];
      this.label = file.name;
      const fileReader = new FileReader();
      fileReader.onload = (e) => {
        this.hasValidJson = this.checkJson(JSON.parse(<string>fileReader.result));
      };
      fileReader.readAsText(file);
    }
  }

  replaceData() {
    // TODO: Add Modal
    this.nluService.entityService.getEntities().subscribe( entities => {
      entities.getKeys().forEach( entity => {
        this.nluService.entityService.deleteEntity(entity).subscribe();
      });
      this.data.entities.getKeys().forEach( entity => {
        if (entity.includes('snips/')) {
          this.nluService.entityService.addBuildInEntity(entity.replace('snips/', '')).subscribe();
        } else {
          this.nluService.entityService.createEntity(entity, this.data.entities.getValue(entity)).subscribe();
        }
      });
    });

    this.nluService.intentService.getIntents().subscribe( intents => {
      intents.getKeys().forEach( intent => {
        this.nluService.intentService.deleteIntent(intent).subscribe();
      });
      this.data.intents.getKeys().forEach( intent => {
        this.nluService.intentService.createIntent(intent, this.data.intents.getValue(intent)).subscribe();
      });
    });



    // TODO: Create Intents and Entities and replace current data
  }

  addData() {
    // TODO: Add Modal

    this.data.intents.getKeys().forEach( intentKey => {
      this.nluService.intentService.createIntent(intentKey, this.data.intents.getValue(intentKey)).subscribe();
    });

    this.data.entities.getKeys().forEach( entity => {
      if (entity.includes('snips/')) {
        this.nluService.entityService.addBuildInEntity(entity.replace('snips/', '')).subscribe();
      } else {
        this.nluService.entityService.createEntity(entity, this.data.entities.getValue(entity)).subscribe();
      }
    });

  }
}
