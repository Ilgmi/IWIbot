# IWIbot Classifier

IWIbot Classifier ist ein Text Classification Module, das Neuronale Netzwerke benutzt. Es basiert auf den Algorithmen aus [Text Classification using Neural Networks](https://machinelearnings.co/text-classification-using-neural-networks-f5cd7b8765c6) und ist Teil des IWIbot Projekts der [Hochschule Karlsruhe](https://hs-karlsruhe.de). Das Classification Module wird als eine Python Flask App bereitgestellt und kann auf die IBM Cloud deployed werden.

Dieses Dokument soll dabei helfen die Entwicklungsumgebung für den IWIbot Classifier aufzusetzen und soll hilfreiche Tipps geben für die weitere Entwicklung. 

## Voraussetzungen

Folgende Komponenten werden benötigt:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)
* [Angular 7.1](https://angular.io/guide/quickstart)
* [PyCharm](https://www.jetbrains.com/pycharm/) (optional)

## 1. Clone die IWIbot App

Clone das IWIBot Repository und gehe in das Verzeichnis in dem sich der IWIBot Classifier befindet.

  ```
git clone https://github.com/HSKA-IWI-VSYS/IWIbot
cd IWIbot/classification
  ```

## 2. NLU Manager bauen
Im Ordern ```IWIBot/manager``` finden Sie den NLU Manager. Nachdem Sie Angular installiert haben,
könen Sie den Manager mit folgenden Befehl bauen: 
  ```
npm run build:Cloud Prod
  ```

Danach ist im Ordner ```IWIBot/classification_snips/static ``` eine lauffähige Angular Anwendung.

## 3. Führe den Classifier lokal aus

Installiere die Abhängigkeiten die in der [requirements.txt](https://pip.readthedocs.io/en/stable/user_guide/#requirements-files) gelistet sind um den Classifier lokal ausführen zu können.

Es ist möglich optional eine [virtuelle Umgebung](https://packaging.python.org/installing/#creating-and-using-virtual-environments) zu erstellen um zu verhindern das die Abhängigkeiten mit anderen Python Projekten oder dem Betriebssystem kollidieren.
  ```
pip install -r requirements.txt
  ```

Führe den Classifier aus.
  ```
python rest.py
  ```
  
In PyCharm kann die **rest.py** auch einfach gestartet und debugged werden.  

 Eine Webtest-Oberfläche befindet sich unter: http://localhost:8000

## 4. Bereite den Classifier für das Deployment vor


 

Um in die IBM Cloud zu deployen, ist es wichtig das manifest.yml richtig zu konfigurieren. Der Classifier kommt mit einem bereits vorkonfigurierten Manifest.

Das manifest.yml beinhaltet Basis-Informationen über die zu den Classifier, wie den Namen in der Cloud, wie viel Speicher für pro Instanz alloziert werden soll und die Route. Im aktuellen manifest.yml **random-route: false** generiert den Classifier immer unter der gleichen Route. Sollen mehrere Classifier Instanz deployen werden kann dies in **random-route: true** geändert werden und es wird eine zufällige Route erzeugt die einen Konflikt mit anderen verhindert.  Es ist auch möglich **random-route: false** mit **host: IWIbotChosenHostName**, um einen Hostnamen selbst zu wählen. [Weitere Informationen...](https://console.bluemix.net/docs/manageapps/depapps.html#appmanifest)
 ```
 applications:
 - name: IWIBotClassifier
   random-route: false
   memory: 128M
 ```

## 5. Deployment des Classifier

Es ist möglich den Classifier über die Cloud Foundry CLI zu deployen.

Wähle den passenden API Endpunkt
   ```
cf api <API-endpoint>
   ```

Ersetze das *API-endpoint* im Befehl mit einem API endpoint aus der folgenden Liste.

|URL                             |Region          |
|:-------------------------------|:---------------|
| https://api.ng.bluemix.net     | US South       |
| https://api.us-east.bluemix.net| US East        |
| https://api.eu-de.bluemix.net  | Germany        |
| https://api.eu-gb.bluemix.net  | United Kingdom |
| https://api.au-syd.bluemix.net | Sydney         |


Loge in deinen IBM Cloud Account

  ```
cf login
  ```

Aus dem *classification* Verzeichnis heraus pushe den Classifier in die IBM Cloud
  ```
cf push IWIBotClassifier -b https://github.com/cloudfoundry/buildpack-python.git
  ```
Der Classifier wird immer mit der aktuellen Python Version deployed in der **runtime.txt** kann die Python Version angepasst werden.

Das Deployen kann einige Minuten dauern. Kommt es zu Fehlern im Deployment Prozess kann mit dem Befehl `cf logs IWIBotClassifier --recent` der Fehler gesucht werden.

Nach abgeschlossenem Deployment sollte eine Meldung anzeigen das der Classifier läuft.  Nun ist es möglich den Classifier unter der gelisteten URL in der Ausgabe des push Befehls anzusprechen.  Es ist auch möglich den Befehl
  ```
cf apps
  ```
  auszuführen um eine Übersicht über den Status des Classifiers einzusehen und um die URL zu sehen.

## 6. Eine Datenbank hinzufügen

Der Classifier benötigt eine NoSQL Datenbank zum persistieren seiner Daten. Aus diesem Grund wird der IBM Cloud ein Service hinzugefügt der diese bereitstellt und es findet die Konfiguration diese Datenbank in der IBM Cloud als auch lokal zu verwenden. 

1. Öffne IBM Cloud in deinem Browser. Öffne das `Dashboard`. Wähle den Classifier aus durch klicken auf den Namen in der `Name` Spalte.
2. Wähle `Connections`/`Verbindungen` aus und dann `Connect new`/`Neue verbdinen`. (Optional kann auch eine bereits erstelle verbunden werden)
2. Im `Data & Analytics` Bereich, wähle `Cloudant NoSQL DB` und `Create` den Service.
3. Wähle `Restage` wenn gefragt wird. Die IBM Cloud wird den Classifier neu starten und die Datenbank Credentials für den Classifier bereitstellen mit der`VCAP_SERVICES` Umgebungsvariable. Diese Umgebungsvariable ist nur verfügbar wenn der Classifier auf der IBM Cloud ausgeführt wird.

Umgebungsvariablen ermöglichen es die Deployment Einstellungen vom Quellcode zu separieren, es ist also nicht nötig ein Datenbank Passwort im COde zu setzen, es ist auch mögliche diese Umgebungsvariable im Quellcode zu speichern.

## 7. Benutze die Datenbank lokal

Um den Classifier lokal auszuführen ist es nötig lokal eine Verbindung mit der Datenbank aufzubauen. Dafür wird eine JSON Datei die die Credentials für den zu benutzenden Datenbank Service speichert. Diese Datei wird NUR verwendet wenn der Classifier lokal ausgeführt wird. Falls es in der IBM Cloud ausgeführt wird, werden die Credentials aus der VCAP_SERVICES Umgebungsvariable gelesen.

1. Erstelle eine Datei mit Namen `vcap-local.json` im `IWIbotClassifier` Verzeichnis mit dem folgenden Inhalt:
  ```
  {
    "services": {
      "cloudantNoSQLDB": [
        {
          "credentials": {
            "username":"CLOUDANT_DATABASE_USERNAME",
            "password":"CLOUDANT_DATABASE_PASSWORD",
            "host":"CLOUDANT_DATABASE_HOST"
          },
          "label": "cloudantNoSQLDB"
        }
      ]
    }
  }
  ```

2. In der IBM Cloud UI, wähle den Classifier -> Connections/Verbindungen -> Cloudant -> View Credentials

3. Kopiere und ersetze die `username`, `password`, und `host` aus den Credentials in das selbe Feld als in der `vcap-local.json` Datei und ersetze **CLOUDANT_DATABASE_USERNAME**, **CLOUDANT_DATABASE_PASSWORD**, und **CLOUDANT_DATABASE_URL**.

4. Führe den Classifier local aus.
  ```
python rest.py
  ```

oder starte den Classifier in PyCharm.

  Der Classifier kann unter: http://localhost:8000 getestet werden. Der Text der in das Feld eingeben wird, wird dann klassifiziert und das Resultat wird ausgegeben.

5. Mache die Änderungen die du willst und deploye erneut zur IBM Cloud!
  ```
cf push IWIBotSnips -b https://github.com/cloudfoundry/buildpack-python.git
  ```

Schaue die Instanz an unter der gelisteten URL in der Ausgabe des push Befehls, zum Beispiel, *iwibotclassifier.mybluemix.net*.

## 8. Datenbank füllen

Nach dem ersten Start des Classifiers ist die Datenbank noch leer. Um den Classifier mit Daten zu füllen, können Sie dies über die Oberläche mache, 
oder sie importieren eine Snips NLU Json Datei. Hierzu können Sie auch das beiligende ```data.json``` verwenden.

## 9. Hilfreiche Links

* [IBM-Cloud Get-Started-Python](https://github.com/IBM-Cloud/get-started-python)
* [Cloudant Client Dokumentation](https://github.com/cloudant/python-cloudant)
* [Text Classification using Neural Networks](https://machinelearnings.co/text-classification-using-neural-networks-f5cd7b8765c6)

## Aufbau 
## Übersicht Bild

Der Classifier besteht aus Fünf Komponenten:, Trainer, Classifier, Datenbank, Cloud-Storage und REST-Schnittstelle

* **Trainer:** Ist für das Trainieren und sichern der Snips NLU zuständig. Verwendet den Cloud-Storage um das Backup in einem Bucket zu sichern.

* **Classifier:** Verwendet die Snips NLU um anhand eines Satzen den Intent und den Entity zu berechnen.

* **Datenbank** Speichert die Intents und Entities mit ihren Beispielsätzen. Sichert auch Sätze, welche durch die NLU nicht erkannt wurden. Dadurch sollen neue Daten hinzugefügt werden. 

* **Cloud-Storage** Sichert die Trainierte Snips NLU in einem Bucket. Dazu wird auch der zuvor trainierte NLU gesichert, um gegebenen Falls ein Role Back durchzufüghen.

* **REST:** Ist die Schnittstelle des Classifiers nach außen Anwendungen können die Services die diese Schnittstelle bereitstellt aufrufen. Die Schnittstelle beinhaltet Endpunkte für das erhalten von Intends und Entities als auch Endpunkte zum modifizieren und trainieren der Snips NLU.

## REST Schnittstelle

#### Intent und Entity Json
Der Aufbau der Intent und Entities orientiert sich an der Snips NLU. 


Endpunkte:

* **POST: /api/getIntent** Gibt den Intent eines Satzes zurück. Erwartet ein JSON im Request Body. Dieses JSON muss einen Satz beinhalten unter dem Schlüssel "sentence". Gibt als Response zurück den erhaltenen Request Body ohne den Satz und mit einer Classification, die einen Intent beinhaltet.

* **POST: /api/getEntity** Gibt eine Entity eines Satzes zurück basierend auf den mitgegebenen vorherigen Intent. Erwartet ein JSON im Request Body. Dieses JSON muss einen Satz beinhalten unter dem Schlüssel "sentence" und einen vorherigen Intent unter dem Pfad "/context/priorIntent/intent". Gibt als Response zurück den erhaltenen Request Body ohne den Satz und mit einer Classification, die eine Entity beinhaltet.

* **GET: /api/trainEngine** Löst das Trainieren der NLU aus.

* **GET: /api/rollbackEngine** Falls eine vorherige NLU existiert, wird als neue NLU verwedet.

* **Intent:**  Verwendet die Json Intent Objekte der Snips NLU

* **GET: /api/intent/<string:name>** Gibt einen Intent mit dem angegebenen Namen zurück.
* **POST: /api/intent/<string:name>** Erstellt einen neuen Intent mit dem angegebenen Namen.
* **PUT: /api/intent/<string:name>**  Aktualisert einen Intent.
* **DELETE: /api/intent/<string:name>** Löscht einen Intent.

* **GET: /api/entity** Gibt eine Liste von Entities zurück.
* **GET: /api/entity/<string:name>** Gibt einen Entity zurück.
* **POST: /api/entity/<string:name>** Erstellt einen Entity.
* **PUT: /api/entity/<string:name>** Aktualisiert einen Entity.
* **DELETE: /api/entity/<string:name>** Löscht einen Entity.

* **GET: /api/entity/snips/** Gibt eine Liste von Snips internen Entities zurück.
* **POST: /api/entity/snips/<string:name>** Erstellt einen Snips Entity.
* **DELETE: /api/entity/snips/<string:name>** Löscht einen Snips Entity.

* **GET: /api/sentence/** Gibt eine Liste von Sätzen zurück.
* **PUT: /api/sentence/** Aktualisiert die Liste von Sätzen.



##  Ausblick

* **Conversation Management:**  Der Nlu Manager könnte durch einen Converstaiton Manager erweitert werden um eigenen Konversationen für den IWIBot zu erstellen. 