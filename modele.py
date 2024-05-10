from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import GBTClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import StringIndexer

# Créer une session Spark
spark = SparkSession.builder \
    .appName("Predictive Maintenance") \
    .getOrCreate()

# Charger les données dans un DataFrame Spark
data_path = "predictive_maintenance.csv"
spark_df = spark.read.csv(data_path, header=True, inferSchema=True)

# Supprimer les lignes contenant des valeurs nulles dans les colonnes pertinentes
relevant_cols = ['Rotational speed', 'Torque', 'Process temperature', 'Air temperature', 'Tool wear']
for col in relevant_cols:
    spark_df = spark_df.filter(spark_df[col].isNotNull())

# Ajouter l'attribut Power
spark_df = spark_df.withColumn("Power", 2 * 3.14 * spark_df['Rotational speed'] * spark_df['Torque'] / 60)

# Ajouter l'attribut temp_diff
spark_df = spark_df.withColumn("temp_diff", spark_df['Process temperature'] - spark_df['Air temperature'])

# Supprimer les colonnes inutiles
spark_df = spark_df.drop('UDI', 'Product ID', 'Air temperature', 'Process temperature', 'Rotational speed', 'Torque', 'Failure Type')

# Convertir la colonne 'Type' en une représentation numérique
indexer = StringIndexer(inputCol="Type", outputCol="TypeIndex")
indexed_df = indexer.fit(spark_df).transform(spark_df)

# Assembler les colonnes d'entités
feature_cols = ['Power', 'Tool wear', 'temp_diff', 'TypeIndex']
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
data_prepared = assembler.transform(indexed_df)

# Diviser les données en ensembles de formation et de test
train_data, test_data = data_prepared.randomSplit([0.7, 0.3], seed=42)

# Créer un classificateur Gradient Boosting
gbt = GBTClassifier(featuresCol="features", labelCol="features", maxIter=10)  # You can adjust parameters like maxIter if needed

# Créer un pipeline sans l'assembler stage
pipeline = Pipeline(stages=[gbt])

# Entraîner le modèle sur les données d'entraînement
model = pipeline.fit(train_data)

# Faire des prédictions sur les données de test
predictions = model.transform(test_data)

# Évaluer les performances du modèle
evaluator = BinaryClassificationEvaluator(labelCol="features")
auc = evaluator.evaluate(predictions, {evaluator.metricName: "areaUnderROC"})
print("AUC:", auc)

# Enregistrer le modèle
model_path = "predictive_maintenance_spark"
model.save(model_path)

# Arrêter la session Spark
spark.stop()
