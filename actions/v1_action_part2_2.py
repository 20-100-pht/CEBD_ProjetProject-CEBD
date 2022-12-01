
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

class AppPart2_2(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_part2_2.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_part2_2, "")
        try:
            cursor = self.data.cursor()
            query="""WITH relPaysDesEquipes AS (
    SELECT DISTINCT numEq, pays FROM LesMembresEquipes JOIN LesSportifs_base USING(numSp)
),
relPaysDesParticipants AS (
    SELECT numSp AS numP, pays FROM LesSportifs_base
    UNION
    SELECT numEq AS numP, pays FROM relPaysDesEquipes
),
relNOrParPays AS (
  SELECT COUNT(*) AS NOr, pays FROM LesEpreuves JOIN relPaysDesParticipants ON(numP=numPOr)
  GROUP BY pays
),
relNArgentParPays AS (
  SELECT COUNT(*) AS NArgent, pays FROM LesEpreuves JOIN relPaysDesParticipants ON(numP=numPArgent)
  GROUP BY pays
),
relNBronzeParPays AS (
  SELECT COUNT(*) AS NBronze, pays FROM LesEpreuves JOIN relPaysDesParticipants ON(numP=numPBronze)
  GROUP BY pays
),
relTousLesPays AS (
  SELECT DISTINCT pays FROM LesSportifs_base
)
SELECT DISTINCT relTousLesPays.pays, NOr, NArgent, NBronze FROM relTousLesPays LEFT JOIN relNOrParPays USING(pays) LEFT JOIN relNArgentParPays USING(pays) LEFT JOIN relNBronzeParPays USING(pays)
ORDER BY NOr DESC, NArgent DESC, NBronze DESC;"""
            result = cursor.execute(query)
        except Exception as e:
            self.ui.table_fct_part2_2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_part2_2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_part2_2, result)