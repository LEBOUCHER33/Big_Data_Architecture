"""
Script pour mettre à jour et installer toutes les librairies nécessaires à l'environnement d'éxecution
"""

#!/bin/bash
set -e

echo "=== Mise à jour système ==="
sudo yum update -y

echo "=== Installation Python libs ==="
sudo python3 -m pip install --upgrade pip

sudo python3 -m pip install \
    pandas \
    pillow \
    scikit-learn \
    tensorflow \
    keras \
    pyarrow \
    boto3 \
    s3fs \
    matplotlib \
    pyspark

echo "=== Vérification TensorFlow ==="
python3 - <<EOF
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
EOF

echo "=== Bootstrap terminé ==="
