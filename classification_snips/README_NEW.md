#**IWIbot Classifier mit Snips NLU**
**Voraussetzungen**
Folgende Komponenten werden benötigt:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
    * [Cloud Object Storage](https://www.ibm.com/de-de/cloud/object-storage)
        * [ibm-cos-sdk-python](https://github.com/IBM/ibm-cos-sdk-python)
    * [Cloudant](https://www.ibm.com/de-de/cloud/cloudant)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)
* [SnipsNLU](https://snips-nlu.readthedocs.io/)
* [PyCharm](https://www.jetbrains.com/pycharm/) (optional)

#### Cloud Object Storage
**Cloud Object Storage (COS)** ist ein günstiger, skalierbarer Speicher bei IBM, wo fast unbegrenzte Mengen an Daten sicher gespeichert werden können.
COS unterstützt geografische Skalierung und Verschlüsselung von Daten, die per _HTTP_ mithilfe _REST API_ zugreifbar sind.
Folgende Lösung wird häufig für die Datenarchivierung und -sicherung, Webanwendungen und mobile Anwendungen  benutzt.

Während des Trainings mit neuesten Daten werden immer neue Versionen von SNIPS NLU Engine erstellt. Es entsteht die Notwendigkeit, eine Lösung zu finden, den Engine automatisch zu persistieren und die Wiederherstellung auf vorherige Version optional gewährzuleisten, falls neue Lerndaten zur fehlerhaften Ergebnissen führen würden. 
   
 **COS** wird für die Speicherung und Wiederherstellung des NLU-Engines benutzt. Für die Implementierung wird ein Fork von boto3 Bibliothek bei AWS - [ibm-cos-sdk-python](https://github.com/IBM/ibm-cos-sdk-python) benutzt, der Amazon S3 ähnliche APIs (kompartibel mit IBM Cloud) unterstützt.
 #####Voraussetzungen:
+ Eine Instanz von COS in Cloud (**Location: Frankfurt, public**)
+ API key von IBM Cloud Identity und Access Management (Writer permissions)
+ ID von COS
+ Token/Service endpoint
 #####Verbindungsaufbau
 Es soll zuerst eine laufende COS Instanz auf IBM Cloud erstellt werden. Es ist wichtig Location: Frankfurt bei der Estellung des Services zu benutzen, andere Einstellungen können default sein.
 
 Für den Verbindungsaufbau werden Credentials laufender Instanz benötigt: 
 + ibm_api_key_id = api_key (aus Credentials)
 + ibm_service_instance_id = resource_instance_id (aus Credentials)
 + ibm_auth_endpoint <-- [IAM token service](https://console.bluemix.net/docs/services/Cloudant/guides/iam.html#ibm-cloud-identity-and-access-management-iam-), Authentifizierung per HTTP 
 + endpoint_url <-- definiert Region, wo die Buckets erstellt werden. Es ist ganz wichtig zwischen den privaten und public Endpoints zu unterscheiden, da der Zugriff aus Cloud Foundry **nur auf public** Endpoints möglich ist! 
   + [Die Liste von Regionen und Endpoints(public&private)](https://console.bluemix.net/docs/services/cloud-object-storage/basics/endpoints.html#select-regions-and-endpoints)
   
 #####Implementierung 
Es gibt 2 Clients: high- und low-level APIs(resource und client), um den Object Storage zuzugreifen.
**_cos_context.py_** ist verantwortlich für die I/O Operationen und Verwaltung von Buckets in COS.
Die Verwaltung von Buckets ist automatisiert: es wird automatisch geprüft, ob bereits Bucket **"engine"**(default) in COS existiert, falls nein - wird eine neue Instanz erstellt.(d.h. es soll nur die Verbindung zu COS hergestellt werden)


_upload_file(), download_file(), remove_file(), rename_file(), remove_bucket()_ - sind die Standartfunktionen, die für hoch-, herunterladen des Engines verantwortlich sind.

__file_exist_in_bucket(),_ _bucket_exist(), get_buckets()_ - sind die Hilfsfunktionen.






 