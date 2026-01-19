#!/bin/bash
set -x # Affiche chaque commande avant son exécution

echo "=== Début du Bootstrap ==="

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