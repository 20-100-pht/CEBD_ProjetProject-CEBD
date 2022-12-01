
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppAdd(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_add.ui", self)
        self.data = data

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_add_info, "")
        display.refreshLabel(self.ui.label_fct_add_query, "")
        if (not self.ui.lineEdit_insert.text().strip()) or (not self.ui.lineEdit_values.text().strip()) :
            display.refreshLabel(self.ui.label_fct_add_info, "Veuillez completer avec un insert valide")
        else:
            try:
                cursor = self.data.cursor()
                query = "INSERT INTO "+self.ui.lineEdit_insert.text().strip()+" VALUES "+self.ui.lineEdit_values.text().strip()
                cursor.execute(query)
            except Exception as e:
                display.refreshLabel(self.ui.label_fct_add_query, query)
                display.refreshLabel(self.ui.label_fct_add_info, "Impossible d'inserer : " + repr(e))
            else:
                display.refreshLabel(self.ui.label_fct_add_query, query)
                display.refreshLabel(self.ui.label_fct_add_info, "Insertion effectuée avec succes !")
                self.data.commit()