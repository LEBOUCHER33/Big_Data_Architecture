"""
Script pour mettre à jour et installer toutes les librairies nécessaires à l'environnement d'éxecution
"""
#!/bin/bash
set -e # Arrête le script en cas d'erreur

echo "=== Début du Bootstrap ==="

# 1. Mise à jour système (optionnel, peut ralentir le démarrage)
yum update -y

# 2. Mise à jour de pip
python3 -m pip install --upgrade pip

# 3. Installation des librairies

echo "=== Installation des librairies Python ==="
python3 -m pip install \
    pandas \
    pillow \
    scikit-learn \
    tensorflow \
    keras \
    pyarrow \
    boto3 \
    s3fs \
    matplotlib

# 4. Vérification TensorFlow
echo "=== Vérification TensorFlow ==="
python3 -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

echo "=== Bootstrap terminé avec succès ==="