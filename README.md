# Big_Data_Architecture

## Objectif 

Réaliser un traitement de données un environnement Big Data.

La chaine de traitement des données comprendra un preprocessing des données pour les formater à un modèle pré-entrainé et une réduction de dimension par PCA.

Les scripts seront développés en Pyspark pour ensuite être déployés dans un environnement Big Data AWS et permettre du calcul distribué.

## Prérequis

- environnement PySpark pour executer le code sur le cluster Spark (AWS / EMR)
- environnement AWS pour l'infrastructure Big Data

## Modèle utilisé

On utilisera le modèle entrainé MobileNetV2.
On réalisera du transfert learning pour utiliser ses performances et l'ajuster à notre problématique de classification multiclasses en supprimant la dernière couche du modèle.

## Concept du projet

le volume important de données implicite un environnement big data afin que le stockage des données et les calculs soient distribués sur un cluster de machines.

Apach Spark est un moteur de calcul distribué qui va gérer la complexité Big Data. 
PySpark est l'API python de Spark.

## outils AWS

On utilisera le prestataire web AWS comme fournisseur de ressources et accéder à l'infrastructure nécessaire :

- stockage des données (S3)

- serveurs (EC2)

- cluster Spark pour coordonner, scaler et executer les jobs (EMR = driver + workers)

- réseau

- sécurité et permisssions (IAM)



## Process

1- tester le processing des données en local

2- configurer les outils AWS : IAM / S3 / EC2 / EMR

3- déployer les calculs sur le cloud

## Workflow 

Images (S3)
   ↓
Cluster EMR (Spark)
   ↓
Feature extraction (MobileNetV2)
   ↓
StandardScaler + PCA (Spark MLlib)
   ↓
Features réduites / modèles / résultats (S3)


### 1- configurer un compte AWS

1- création d'un compte root AWS
2- sécurisation du compte root MFA (Multi Factor Authentification)
3- création d'un compte IAM (Identity and Access Management)
4- définir les clés d'accès API et les droits pour S3/EC2/EMR :

    - créer un groupe IAM = conteneur pour les droits
    - rattacher un user IAM à ce groupe
    - donner les droits full access avec la politique AdministratorAccess ou ajuster la politique d'accès aux différents services
    - créer les clés pour utiliser les web services via un terminal CLI, des scripts ou des clusters EMR


### 2- configurer le stockage S3

- création d'un bucket S3 (compartiment)
- loading des data dans le bucket via le terminal CLI:
```bash
aws s3 sync /nom_dossier_local/ s3://nom_bucket/nom_dossier_s3/
```
- création des droits d'accès à ce bucket = définir la politique d'accès à la ressource (bucket policy)


### 3- configurer EMR

EC2 AWS = serveur virtuel sur le cloud / cluster de machines
EMR = Cluster Big Data clé en mais basé sur plusieurs EC2 déjà configuré pour Spark

1- développer un script bash pour configurer l'environnement d'execution (mise à jour et installation des libs)
Ce script bootstrap garantira que les noeuds (machines) disposent des mêmes lib / configurations au lancement

2- loader les scripts bash et pyspark dans le stockage S3

3-créer le cluster EMR et le configurer :
   - définir les applications 
   - accès et sécurité
      - paramétrer les rôles IAM : définir deux rôles et leur attribuer des policies
         1- Fonction EMR : EMR_DefaultRole (AmazonEMRServicePolicy_v2 + AmazonElasticMapReduceRole)
         2- Fonction EC2 : EMR_EC2_DefaultRole (AmazonElasticMapReduceforEC2Role + AmazonSSMManagedInstanceCore)
      - s'assurer que les subnets soient bien publics avec un enregistrement DNS A au lancement
      - définir la résiliation (manuelle ou automatique)
      - créer une paire de clés SSH pour suivre les logs en lignes de commandes (AWSCli)
      ```ssh -i "votre-clef.pem" hadoop@votre-dns-public-master```
   
   - définir une fonction d'amorçage pour le bootsptrapping : associer un script bash pour configurer l'environnement d'execution (MAJ et installation des libs)

   - associer des steps : ajouter les scripts d'éxecution pyspark

4- connexion au cluster EMR pour suivi SSH : PuTTy
Téléchargez PuTTY.exe sur votre ordinateur à partir de : https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html 
Démarrez PuTTY.
Dans la liste Category (Catégorie), sélectionnez Session.
Dans le champ Host Name (Nom d'hôte), entrez hadoop@ec2-##-##-##.eu-north-1.compute.amazonaws.com
Dans la liste Category, développez Connection (Connexion) > SSH, puis sélectionnez Auth.
Pour Private key file for authentication (Fichier de clé privée pour l'authentification), sélectionnez Browse (Parcourir) et le fichier de clé privée (p9-key.ppk) que vous avez utilisé pour lancer le cluster.
Cliquez sur Open (Ouvrir).
Sélectionnez Yes (Oui) pour ignorer l'alerte de sécurité.

5- lancement des jobs depuis S3

   5-1 Suivi de l'action d'amorçage

```
# Pour voir l'erreur de votre script bash
cat /var/log/bootstrap-actions/1/stderr

# Pour voir ce que votre script a affiché (les echo)
cat /var/log/bootstrap-actions/1/stdout
```

   5-2 Suivi de l'execution du script pyspark

```
spark-submit --master yarn --deploy-mode client s3://aws-bucket-p9/script_pyspark.py 

spark-submit --master yarn --deploy-mode client s3://aws-bucket-p9/script_pyspark.py > logs_output.txt 2>&1
grep "DEBUG >>>" logs_output.txt
``` 


## 4- Relier un notebook à un cluster

- créer un studio personnalisé :
   - lui définir un rôle 
   - créer les règles entrantes et sortantes pour que le studio et l'EMR puisse communiquer
   
- créer un workspace 

- le relier à un cluster



