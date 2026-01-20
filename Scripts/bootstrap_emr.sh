#!/bin/bash
set -x # Affiche chaque commande avant son exécution

echo "=== Début du Bootstrap ==="

# 3. Installation des librairies
echo "=== Installation des dépendances système pour Pillow ==="
sudo yum install -y \
    gcc \
    python3-devel \
    zlib-devel \
    libjpeg-devel \
    freetype-devel \
    lcms2-devel \
    libtiff-devel \
    openjpeg2-devel


# Mise à jour de pip pour l'utilisateur root et hadoop
sudo python3 -m pip install --upgrade pip


echo "=== Installation des dépendances système pour keras ==="
sudo yum install -y \
    hdf5-devel

# Installation de Pillow avant les autres librairies pour éviter des conflits
echo "=== Installation de Pillow ==="
sudo python3 -m pip install Pillow

# Installation d'optree avant TensorFlow pour éviter des conflits
echo "=== Installation d'optree ==="
sudo python3 -m pip install optree

# Installation de rich pour une meilleure expérience en ligne de commande
echo "=== Installation de rich ==="
sudo python3 -m pip install rich 

echo "=== Installation des librairies Python ==="
sudo python3 -m pip install \
    numpy==1.24.4 \
    tensorflow==2.13.1 \
    ml-dtypes==0.2.0 \
    pandas \
    scikit-learn \
    pyarrow \
    boto3 \
    s3fs \
    matplotlib \
    h5py 


# 4. Vérification TensorFlow
echo "=== Vérification TensorFlow ==="
python3 -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

echo "=== Bootstrap terminé avec succès ==="

