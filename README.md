#M2 Yue GUO
# 深度学习项目
推荐系统｜简历-职位匹配：
1.爬取法国劳工局招聘启事+领英对应简历
2.基于 Sentence-BERT 做文本向量化，余弦相似度 Top-K 召回，孪生网络Siamese驱动的简历-职位自动配对。

# Processus d'automatisation du recrutement

Ce document détaille le processus automatisé de récupération, de nettoyage et d'analyse des données pour le recrutement à l'aide du scraping web et de l'apprentissage automatique.

## Extraction des données

### Récupération des CV
1. Le script `getCVdata.py` est exécuté pour accéder aux profils des candidats sur le site de LinkedIn en utilisant le fichier `cvUrlIT.csv`.
2. Il utilise ensuite l'API Proxycurl avec la clé d'API stockée dans `api_key.text` pour automatiser la collecte des informations.
3. Les données collectées sont sauvegardées sous forme de 10 fichiers JSON contenant les CV.

Commande pour exécuter le script :
```bash
subprocess.run(["python", "getCVdata.py"])
```
###Récupération des annonces d'emploi
1. Le script getAnnounceEmploi.py emploie Selenium pour imiter les actions humaines de recherche d'annonces d'emploi, recueillant des informations pertinentes.
2. Les données récupérées sont enregistrées dans le fichier `announce.csv`.

```bash
subprocess.run(["python", "getAnnounceEmploi.py"])
```

###Nettoyage des données
Les notebooks `dataCleanAnnonce.ipynb` et `dataCleanProfileLinkedin.ipynb` sont utilisés pour nettoyer les données récupérées respectivement.

Après nettoyage, les descriptions pertinentes sont combinées et l'expérience requise ou possédée est compilée en mois.

Fichiers de données nettoyées :
```bash
df_announce=pd.read_csv('./dataDownloadSelenium/data_announce_propre.csv')
df_cv=pd.read_csv('./dataDownloadSelenium/data_cv_propre.csv')
```

###Apprentissage et Analyse
Le notebook `TrainingDataEmployCV.ipynb` détaille le processus d'apprentissage machine.
Calcul de la similarité cosinus entre chaque CV et annonce de recrutement.
Construction d'un modèle de réseau siamois pour l'extraction des caractéristiques.
Identification des CV idéaux correspondant aux annonces.


