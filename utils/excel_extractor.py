import sqlite3
from sqlite3 import IntegrityError

import pandas

def read_excel_file_V0(data:sqlite3.Connection, file):
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert into V0_LesSportifsEQ values ({},'{}','{}','{}','{}','{}',{})".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'], row['numEq'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            #print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Lecture de l'onglet LesEpreuves du fichier excel, en interprétant toutes les colonnes comme des string
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert into V0_LesEpreuves values ({},'{}','{}','{}','{}',{},".format(
                row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'])

            if (row['dateEp'] != 'null'):
                query = query + "'{}')".format(row['dateEp'])
            else:
                query = query + "null)"
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            #print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

#TODO 1.3a : modifier la lecture du fichier Excel pour lire l'ensemble des données et les intégrer dans le schéma de la BD V1
def read_excel_file_V1(data:sqlite3.Connection, file):
    # Lecture de l'onglet du fichier excel LesSportifs_base, LesEquipes_base et LesMembres, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert into LesSportifs_base values ('{}','{}','{}','{}','{}','{}')".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            #print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)
            
        try:
            query = "insert into LesEquipes_base values ('{}')".format(row['numEq'])
            #print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)
            
        if(row['numEq'] != 'null'):
            try:
                query = "insert into LesMembresEquipes values ('{}', '{}')".format(row['numEq'], row['numSp'])
                #print(query)
                cursor.execute(query)
            except IntegrityError as err:
                print(err)
            
        # Insertion LesParticipants
        
        if(row['numEq'] != 'null'):
            try:
                query = "insert into LesParticipants values ('{}')".format(row['numEq'])
                #print(query)
                cursor.execute(query)
            except IntegrityError as err:
                print(err)
            
        if(row['numSp'] != 'null'):
            try:
                query = "insert into LesParticipants values ('{}')".format(row['numSp'])
                #print(query)
                cursor.execute(query)
            except IntegrityError as err:
                print(err)


            
            
    # Lecture de l'onglet du fichier excel LesEpreuves, en interprétant toutes les colonnes comme des string
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')
    
    df_resultat = pandas.read_excel(file, sheet_name='LesResultats', dtype=str)
    df_resultat = df_resultat.where(pandas.notnull(df_resultat), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert into LesDisciplines values ('{}')".format(row['nomDi'])
            #print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

        medailles = df_resultat.loc[df_resultat['numEp'] == row['numEp']]

        if(len(medailles['gold'].array) != 0):
            goldP = medailles['gold'].array[0]
            silverP = medailles['silver'].array[0]
            bronzeP = medailles['bronze'].array[0]
        else:
            goldP = 'null'
            silverP = 'null'
            bronzeP = 'null'

        try:
            query = "insert into LesEpreuves values ({},'{}','{}','{}','{}', '{}', '{}', '{}', '{}', '{}')".format(
                row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'], row['dateEp'], goldP, silverP, bronzeP)

            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            #print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")
            
    # Insertion LesParticipants
            
    df_epreuves = pandas.read_excel(file, sheet_name='LesInscriptions', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert into LesParticipations values ({}, {})".format(row['numIn'], row['numEp'])
            #print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")