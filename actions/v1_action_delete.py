
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppDelete(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_delete.ui", self)
        self.data = data

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_delete_info, "")
        display.refreshLabel(self.ui.label_fct_delete_query, "")
        if (not self.ui.lineEdit_delete_from.text().strip()) or ((not self.ui.lineEdit_where.text().strip()) and (self.ui.checkBox_condition.isChecked())):
            display.refreshLabel(self.ui.label_fct_delete_info, "Veuillez completer avec une suppression valide")
        else:
            try:
                cursor = self.data.cursor()
                query = "DELETE FROM "+self.ui.lineEdit_delete_from.text().strip()
                if self.ui.checkBox_condition.isChecked():
                    query = query+" WHERE "+self.ui.lineEdit_where.text().strip()
                cursor.execute(query)
            except Exception as e:
                display.refreshLabel(self.ui.label_fct_delete_query, query)
                display.refreshLabel(self.ui.label_fct_delete_info, "Impossible de supprimer : " + repr(e))
            else:
                display.refreshLabel(self.ui.label_fct_delete_query, query)
                display.refreshLabel(self.ui.label_fct_delete_info, "Suppression effectuée avec succes !")
                self.data.commit()