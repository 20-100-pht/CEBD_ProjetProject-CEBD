
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppUpdate(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_update.ui", self)
        self.data = data

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_update_info, "")
        display.refreshLabel(self.ui.label_fct_update_query, "")
        if (not self.ui.lineEdit_update.text().strip()) or (not self.ui.lineEdit_set.text().strip()) or ((not self.ui.lineEdit_where.text().strip()) and (self.ui.checkBox_condition.isChecked())):
            display.refreshLabel(self.ui.label_fct_update_info, "Veuillez completer avec un update valide")
        else:
            try:
                cursor = self.data.cursor()
                query = "UPDATE "+self.ui.lineEdit_update.text().strip()+" SET "+self.ui.lineEdit_set.text().strip()
                if self.ui.checkBox_condition.isChecked():
                    query = query+" WHERE "+self.ui.lineEdit_where.text().strip()
                cursor.execute(query)
            except Exception as e:
                display.refreshLabel(self.ui.label_fct_update_query, query)
                display.refreshLabel(self.ui.label_fct_update_info, "Impossible d'update : " + repr(e))
            else:
                display.refreshLabel(self.ui.label_fct_update_query, query)
                display.refreshLabel(self.ui.label_fct_update_info, "Update effectuée avec succes !")
                self.data.commit()