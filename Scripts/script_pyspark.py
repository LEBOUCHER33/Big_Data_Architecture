"""
Script to run PySpark with TensorFlow and Keras for image processing.

"""


# Initial setup and imports

print('Starting script_pyspark.py')

import pandas as pd
from PIL import Image
import numpy as np
import io
import os
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras import Model
from pyspark.sql.functions import col, pandas_udf, PandasUDFType, element_at, split
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors
from pyspark.sql.functions import udf
from pyspark.ml.linalg import VectorUDT, Vectors
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import PCA


print('All imports done successfully in script_pyspark.py !!!!!!!!!!!!!!!!!!!')

# 1- Define paths

# data directory
data_dir = "s3://aws-bucket-p9/fruits/" 
print(f"Data directory set to: {data_dir}") 

# results directory
path_results = "s3://aws-bucket-p9/results/"
print(f"Results directory set to: {path_results}")


# 2-Initialize Spark session

# création d'une session spark = pt d'entrée dans les fonctionnalités spark
# nécessaire pour contruire un dataframe spark
spark = (SparkSession
             .builder
             .appName('P9_Big_Data_Architecture')
             .config("spark.sql.parquet.writeLegacyFormat", 'true')
             .getOrCreate()
)
print('Spark session created successfully in script_pyspark.py')

# instance d'un sparkcontext
sc = spark.sparkContext

print(f"Spark session: {spark}")
print(f"Spark context: {sc}")

# Spark configuration settings
spark.conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", 1024)
spark.conf.set("spark.sql.shuffle.partitions", 4)



# 3- Load and preprocess data

# lecture des images stockées dans s3
images = spark.read.format("binaryFile") \
  .option("pathGlobFilter", "*.jpg") \
  .option("recursiveFileLookup", "true") \
  .load(data_dir) \
  .limit(10)

print(f"Number of images loaded: {images.count()}, \nimages variable: {type(images)}, \nschema of images dataframe: {images.printSchema()}")

# extraction du label depuis le path
images = images.withColumn('label', element_at(split(images['path'], '/'),-2))
print(f"Schema after adding label: {images.printSchema()}")
print(images.select('path','label').show(5,False))



# 4- Feature extraction using pre-trained MobileNetV2 model

# charger le modèle MobileNetV2
# loading du modèle pré-entrainé
model = MobileNetV2(weights='imagenet',
                    include_top=True,
                    input_shape=(224, 224, 3))

# suppression de la dernière couche de classification
new_model = Model(inputs=model.input,
                  outputs=model.layers[-2].output)
# 4- Broadcast the model weights to worker nodes
brodcast_weights = sc.broadcast(new_model.get_weights())

def model_fn():
    """
    Returns a MobileNetV2 model with top layer removed
    and broadcasted pretrained weights.
    """
    model = MobileNetV2(weights='imagenet',
                        include_top=True,
                        input_shape=(224, 224, 3))
    for layer in model.layers:
        layer.trainable = False
    new_model = Model(inputs=model.input,
                  outputs=model.layers[-2].output)
    new_model.set_weights(brodcast_weights.value)
    return new_model

def preprocess(content):
    """
    Preprocesses raw image bytes for prediction.
    """
    img = Image.open(io.BytesIO(content)).resize([224, 224])
    arr = img_to_array(img)
    return preprocess_input(arr)

def featurize_series(model, content_series):
    """
    Featurize a pd.Series of raw images using the input model.
    :return: a pd.Series of image features
    """
    input = np.stack(content_series.map(preprocess))
    preds = model.predict(input)
    # For some layers, output features will be multi-dimensional tensors.
    # We flatten the feature tensors to vectors for easier storage in Spark DataFrames.
    output = [p.flatten() for p in preds]
    return pd.Series(output)


# définition d'un pandas UDF scalaire itératif (le format pandas spark)

@pandas_udf('array<float>', PandasUDFType.SCALAR_ITER) # active pandas + Arrow // batch + iterateur
# distribue sur les workers, chaque elt de sortie est un batch de données
def featurize_udf(content_series_iter): # batch spark
    '''
    This method is a Scalar Iterator pandas UDF wrapping our featurization function.
    The decorator specifies that this returns a Spark DataFrame column of type ArrayType(FloatType).

    :param content_series_iter: This argument is an iterator over batches of data, where each batch
                              is a pandas Series of image data.
    '''
    # With Scalar Iterator pandas UDFs, we can load the model once and then re-use it
    # for multiple data batches.  This amortizes the overhead of loading big models.
    model = model_fn()
    for content_series in content_series_iter:
        yield featurize_series(model, content_series) # charge le modèle une fois et renvoie un batch


# 5- PCA dimensionality reduction


# modification des vecteurs
array_to_vector = udf(lambda x: Vectors.dense(x), VectorUDT())

# application de l'udf pour extraire les features
df = images.withColumn(
    "features_array",
    featurize_udf("content")
)

# conversion des arrays en vecteurs
df = df.withColumn(
    "features",
    array_to_vector("features_array")
)

print(f"Schema after feature extraction: {df.printSchema()}")

df = df.cache()
df.count()  # action pour forcer le calcul et le cache
print("Dataframe cached after feature extraction.")
print(df.select('path','label','features').show(5,False))



scaler = StandardScaler(
    inputCol="features",
    outputCol="features_scaled",
    withMean=False,   # centre les données (moyenne 0)
    withStd=True     # met à l'échelle avec écart-type 1
)


scaler_model = scaler.fit(df).transform(df)



pca = PCA(
    k=100,  # nombre de composantes principales
    inputCol="features_scaled",
    outputCol="features_pca"
)

pca_model = pca.fit(scaler_model)
df_pca = pca_model.transform(scaler_model)

df_pca.select("features_pca").show(truncate=False)
print(df_pca.select("features_pca").first()[0].size)

# on check la taille du vecteur
df_pca.select("features_pca").head()[0].size
print(f"Schema after PCA: {df_pca.printSchema()}")

