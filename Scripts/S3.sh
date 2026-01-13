"""

Script Bash pour interagir avec Amazon S3

"""

# Variables d'environnement pour AWS S3
export AWS_ACCESS_KEY_ID="votre_access_key_id"
export AWS_SECRET_ACCESS_KEY="votre_secret_access_key"
export AWS_DEFAULT_REGION="votre_region"

# installation de l'AWS CLI (si nécessaire)
# pip install awscli --upgrade --user
# redémarrer le terminal après l'installation

# configuration de l'AWS CLI
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set default.region $AWS_DEFAULT_REGION
aws configure set default.output json

# Commande pour lister les buckets S3
aws s3 ls

# Commande pour créer un bucket S3
aws s3 mb s3://votre-bucket-nom

# Commande pour télécharger un fichier depuis S3
aws s3 cp s3://votre-bucket-nom/fichier.txt ./fichier.txt
aws s3 cp ./mon-dossier-local s3://nom-de-votre-bucket-unique/ --recursive # si multiple files +++

# Commande pour supprimer un fichier S3
aws s3 rm s3://votre-bucket-nom/fichier.txt

# Commande pour supprimer un bucket S3
aws s3 rb s3://votre-bucket-nom --force

# Commande pour checker la configuration AWS
aws configure list

# commande pour afficher les buckets S3
aws s3 ls