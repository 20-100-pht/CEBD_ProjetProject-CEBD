-- ########  TABLE  ########

CREATE TABLE LesDisciplines (
  nomDi VARCHAR2(20) PRIMARY KEY
);

CREATE TABLE LesSportifs_base (
  numSp NUMBER(4) PRIMARY KEY,
  nomSp VARCHAR2(20),
  prenomSp VARCHAR2(20),
  pays VARCHAR2(100),
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  CONSTRAINT SPB_CK1 CHECK(numSp >= 1000 AND numSp <= 1500),
  CONSTRAINT SPB_CK2 CHECK(categorieSp IN ('feminin','masculin')),
  CONSTRAINT SPB_U1 UNIQUE(nomSp, prenomSp)
);

CREATE TABLE LesEquipes_base (
  numEq NUMBER(4) PRIMARY KEY,
  CONSTRAINT EB_CK1 CHECK(numEq > 0 AND numEq <= 100 )
);

CREATE TABLE LesMembresEquipes (
  numEq NUMBER(4),
  numSp NUMBER(4),
  CONSTRAINT ME_P1 PRIMARY KEY (numEq, numSp),
  CONSTRAINT ME_FK1 FOREIGN KEY (numEq) REFERENCES LesEquipes_base (numEq) ON DELETE CASCADE,
  CONSTRAINT ME_FK2 FOREIGN KEY (numSp) REFERENCES LesSportifs_base (numSp) ON DELETE CASCADE
);

CREATE TABLE LesParticipants (
  numP NUMBER(4) PRIMARY KEY,
  CONSTRAINT LP_CK1 CHECK(numP > 0 AND numP <= 1500 )
);

CREATE TABLE LesEpreuves (
  numEp NUMBER(3) PRIMARY KEY,
  nomEp VARCHAR2(20),
  forme VARCHAR2(13),
  nomDi VARCHAR2(25),
  categorieEp VARCHAR2(10),
  nbSportifsEp NUMBER(2),
  dateEp DATE,
  numPOr NUMBER(4),
  numPArgent NUMBER(4),
  numPBronze NUMBER(4),
  CONSTRAINT EP_CK1 CHECK (forme IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 0),
  CONSTRAINT EP_CK1 CHECK(numPOr <> numPArgent <> numPBronze),
  CONSTRAINT EP_CK1 CHECK(numPOr > 0 AND numPOr <= 1500 ),
  CONSTRAINT EP_CK1 CHECK(numPArgent > 0 AND numPArgent <= 1500 ),
  CONSTRAINT EP_CK1 CHECK(numPBronze > 0 AND numPBronze <= 1500 ),
  CONSTRAINT EP_FK1 FOREIGN KEY (nomDi) REFERENCES LesDisciplines (nomDi) ON DELETE CASCADE,
  CONSTRAINT EP_FK2 FOREIGN KEY (numPOr) REFERENCES LesParticipants (numP) ON DELETE CASCADE,
  CONSTRAINT EP_FK3 FOREIGN KEY (numPArgent) REFERENCES LesParticipants (numP) ON DELETE CASCADE,
  CONSTRAINT EP_FK4 FOREIGN KEY (numPBronze) REFERENCES LesParticipants (numP) ON DELETE CASCADE
);

CREATE TABLE LesParticipations (
  numP NUMBER(4),
  numEp NUMBER(4),
  CONSTRAINT P_P1 PRIMARY KEY (numP, numEp),
  CONSTRAINT P_FK1 FOREIGN KEY (numP) REFERENCES LesParticipants (numP) ON DELETE CASCADE,
  CONSTRAINT P_FK2 FOREIGN KEY (numEp) REFERENCES LesEpreuves (numEp) ON DELETE CASCADE
);

-- ########  VIEW  ########

CREATE VIEW IF NOT EXISTS LesSportifs
AS
SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, TRUNC((julianday('now') - julianday(dateNaisSp))/365) AS ageSp
FROM LesSportifs_base;

CREATE VIEW IF NOT EXISTS LesEquipes
AS
SELECT numEq, COUNT(numSp) As nbEquipiersEq
FROM LesEquipes_base JOIN LesMembresEquipes USING(numEq)
GROUP BY numEq;
