
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenêtre de visualisation des données
class AppTablesDataV1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/v1_tablesData.ui", self)
        self.data = data

        # On met à jour l'affichage avec les données actuellement présentes dans la base
        self.refreshAllTablesV1()

    ####################################################################################################################
    # Méthodes permettant de rafraichir les différentes tables
    ####################################################################################################################

    # Fonction de mise à jour de l'affichage d'une seule table
    def refreshTable(self, label, table, query):
        display.refreshLabel(label, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            table.setRowCount(0)
            display.refreshLabel(label, "Impossible d'afficher les données de la table : " + repr(e))
        else:
            display.refreshGenericData(table, result)


    # Fonction permettant de mettre à jour toutes les tables
    @pyqtSlot()
    def refreshAllTablesV1(self):

        self.refreshTable(self.ui.label_LesEpreuves, self.ui.tableEpreuves, "SELECT numEp, nomEp, forme, nomDi, categorieEp, nbSportifsEp, dateEp, numPOr, numPArgent, numPBronze FROM LesEpreuves")
        self.refreshTable(self.ui.label_LesSportifs_base, self.ui.tableSportifs, "SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp FROM LesSportifs_base")
        self.refreshTable(self.ui.label_LesEquipes_base, self.ui.tableEquipes, "SELECT numEq FROM LesEquipes_base")
        self.refreshTable(self.ui.label_LesMembresEquipes, self.ui.tableMembresEquipes, "SELECT numEq, numSp FROM LesMembresEquipes")
        self.refreshTable(self.ui.label_LesParticipants, self.ui.tableParticipants, "SELECT numP FROM LesParticipants")
        self.refreshTable(self.ui.label_LesDisciplines, self.ui.tableDisciplines, "SELECT nomDi FROM LesDisciplines")
        self.refreshTable(self.ui.label_LesParticipations, self.ui.tableParticipations, "SELECT numP, numEp FROM LesParticipations")
        self.refreshTable(self.ui.label_LesSportifs, self.ui.tableSportifsView, "SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, ageSp FROM LesSportifs")
        self.refreshTable(self.ui.label_LesEquipes, self.ui.tableEquipesView, "SELECT numEq, nbEquipiersEq FROM LesEquipes")

