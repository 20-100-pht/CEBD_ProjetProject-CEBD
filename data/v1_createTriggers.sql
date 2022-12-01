-- ########  TRIGGER ########

CREATE TRIGGER triggerUniquementSportifs BEFORE INSERT ON LesParticipations
WHEN EXISTS(SELECT * FROM LesEpreuves WHERE numEp=NEW.numEp AND forme='individuelle' AND NEW.numP < 1000)
BEGIN
  SELECT RAISE (ABORT,'Pas déquipe dans les épreuves individuelles');
END;
