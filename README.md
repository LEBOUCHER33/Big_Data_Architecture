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
Ce script bootstrap garantira que les noeuds (machines) disposent des mêmes lib configurations au lancement

2- loader le script bash dans le stockage S3

3-créer le cluster EMR et le configurer :
   - accès et sécurité
   - bootstrap actions

4- connexion au cluster EMR

5- lancement des jobs depuis S3

