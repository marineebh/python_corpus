#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 08:10:33 2022

@author: jvelcin
"""

import json

with open("data/evg_esp_veg.envpdiprboucle.json", "r") as f:
    d_json = json.load(f)
    
#La variable que vous venez de charger est un dictionnaire, vous pouvez le vérifier avec la commande type.
#Observez les clefs et essayez d'avoir accès aux champs du jeu de données et à la liste des randonnées.

print(f"Type de la variable : {type(d_json)}")

print(f"Valeurs : {d_json.keys()}")

#Enregistrez la liste des champs dans une variable var et les randonnées dans une variable rando.
#Vérifiez le nombre d'enregistrements et essayez d'avoir accès aux valeurs.

var = d_json['fields']
rando = d_json['values']

#Quelle est la taille du jeu de données, càd le nombre de lignes ?
#Quel est le nom de la randonnée de la ligne 10 ?

print(f"Nombre de randonnées : {len(rando)}")
print(rando[10]["nom"])

#Pour rendre ces données pleinement utilisables, nous allons convertir le fichier json en format tabulaire avec la librairie pandas.
#Il vous suffit de créer un DataFrame à partir de la variable rando à l'aide de la fonction from_dict.

import pandas as pd

df_rando = pd.DataFrame.from_dict(rando)

df_rando.shape

df_rando.head()

#df_rando.loc[0:2, "longueur"]
df_rando.iloc[0:2, 1:2]

df_rando["difficulte"].value_counts()

df_rando["temps_parcours"]

# première solution : on garde les 4 premiers caractères
r_clean = [int(r[0:3]) for r in df_rando["temps_parcours"]]
# deuxième solution : on supprimer les dernier caractères
#r_clean = [int(r[:-4]) for r in df_rando["temps_parcours"]]
df_rando["temps_parcours"] = pd.Series(r_clean)

# à noter la solution plus longue avec une boucle explicite :
#temps = df_rando["temps_parcours"]
#serie_nettoyee = []
#for t in temps:
#    t_clean = t[0:3]
#    t_clean = int(t_clean)
#    serie_nettoyee.append(t_clean)
# df_rando["temps_parcours"] = serie_nettoyee


df_rando["temps_parcours"].mean()

# on peut spécifier la précision de la valeur numérique, par ex. :
print("Moyenne du temps de parcours : {:.2f}".format(df_rando["temps_parcours"].mean()))


dif_moyennes = df_rando.groupby('difficulte')
dif_moyennes[['difficulte', 'temps_parcours']].mean()


# Troisième partie : visualisation avec Matplotlib

import matplotlib

#df_rando["difficulte"].value_counts()
df_rando["difficulte"].value_counts().plot.bar()

df_rando["difficulte"].value_counts().sort_index().plot.bar()

df_rando["difficulte"].value_counts().plot.pie()

#s = df_rando["longueur"][0]
#s_clean = s[:-2]
#s_clean = s_clean.replace(",", ".")
#float(s_clean)

r_clean = [float(r[:-3].replace(',','.')) for r in df_rando["longueur"]]
df_rando["longueur"] = pd.Series(r_clean)
df_rando["longueur"]

df_rando.plot.scatter(x = 'longueur', y = 'temps_parcours')

ax = df_rando.plot.scatter(x = 'longueur', y = 'temps_parcours')
ax.set_title("croisement entre la longueur d'un parcours et le temps nécessaire")
ax.set_xlabel("longueur (km)")
ax.set_ylabel("temps (min)")

# dernier exo sur calcul de R

df_rando["longueur"].corr(df_rando["temps_parcours"])

# Cinquième partie : lier plusieurs tables

with open("data/ACC-caracteristiques-2018.csv", "r") as f:
    caracs = pd.read_csv(f, sep=",")
with open("data/ACC-lieux-2018.csv", "r") as f:
    lieux = pd.read_csv(f, sep=",")
with open("data/ACC-usagers-2018.csv", "r") as f:
    usagers = pd.read_csv(f, sep=",")
with open("data/ACC-vehicules-2018.csv", "r") as f:
    vehicules = pd.read_csv(f, sep=",")

# toutes les lignes correspondant aux accidents ayant lieu sur Lyon

caracs_lyon = caracs[caracs["dep"] == 690]

print(f"{len(caracs_lyon)} accidents à Lyon 2018")

# toutes les lignes correspondant aux accidents de vélo

velo = vehicules[vehicules["catv"] == 1]

print(f"{len(velo)} accidents de vélo sur la France en 2018")

# nombre d'accidents de vélo à Lyon en 2018

acc_velo_lyon = caracs_lyon.join(
    velo.set_index('Num_Acc'), on="Num_Acc", how="inner")

acc_velo_lyon_2 = caracs_lyon.merge(
    velo, on="Num_Acc", how="inner")

print(f"Nombre d'accidents de vélo à Lyon : {len(acc_velo_lyon)} avec la fonction join et {len(acc_velo_lyon_2)} avec la fonction merge")