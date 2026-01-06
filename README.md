# Big_Data_Architecture

## Objectif 

Réaliser un traitement de données un environnement Big Data.

La chaine de traitement des données comprendra un preprocessing des données pour les formater à un modèle pré-entrainé et une réduction de dimension par PCA.

Les scripts seront développés en Pyspark pour ensuite être déployés dans un environnement Big Data AWS et permettre du calcul distribué.

## Prérequis

- environnement PySpark
- environnement AWS


## Modèle utilisé

On utilisera le modèle entrainé MobileNetV2.
On réalisera du transfert learning pour utiliser ses performances et l'ajuster à notre problématique de classification multiclasses.

