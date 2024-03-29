
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppPart2_1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part2_1.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_part2_1, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT numEq, AVG(ageSp) as moyenneAge FROM LesMembresEquipes JOIN LesEpreuves ON(numEq = numPOr) JOIN LesSportifs USING(numSp) GROUP BY numEq;")
        except Exception as e:
            self.ui.table_fct_part2_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_part2_1, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_part2_1, result)