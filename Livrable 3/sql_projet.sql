/*  mysql -u bdidier3 -p BDD_bdidier3_tp <  sql_projet.sql */
DROP TABLE IF EXISTS se_deroule;
DROP TABLE IF EXISTS participation;
DROP TABLE IF EXISTS Quantitee_vendue;
DROP TABLE IF EXISTS Produit;
DROP TABLE IF EXISTS Jour_Semaine;
DROP TABLE IF EXISTS type_marche;
DROP TABLE IF EXISTS Lieu;
DROP TABLE IF EXISTS Saison;
DROP TABLE IF EXISTS Maraicher;

CREATE TABLE Maraicher(
                          id_maraicher INT AUTO_INCREMENT,
                          nom VARCHAR(50),
                          prenom VARCHAR(50),
                          age VARCHAR(50),
                          numero VARCHAR(20),
                          mail VARCHAR(50),
                          PRIMARY KEY(id_maraicher)
);

CREATE TABLE Saison(
                       id_saison INT AUTO_INCREMENT,
                       libelle_saison VARCHAR(50),
                       PRIMARY KEY(id_saison)
);

CREATE TABLE Lieu(
                     id_lieu INT AUTO_INCREMENT,
                     Libelle_lieu VARCHAR(50),
                     PRIMARY KEY(id_lieu)
);

CREATE TABLE type_marche(
                            id_type_marche INT AUTO_INCREMENT,
                            Libelle_type_marche VARCHAR(50),
                            id_lieu INT NOT NULL,
                            nombre_place_type_marche INT,
                            surface_type_marche DECIMAL(10,2),
                            PRIMARY KEY(id_type_marche),
                            FOREIGN KEY(id_lieu) REFERENCES Lieu(id_lieu)
);

CREATE TABLE Jour_Semaine(
                             id_jour INT AUTO_INCREMENT,
                             libelle_jour VARCHAR(50),
                             PRIMARY KEY(id_jour)
);

CREATE TABLE Produit(
                        id_produit INT AUTO_INCREMENT,
                        libelle_produit VARCHAR(50),
                        prix_au_kilo DECIMAL(15,2),
                        id_saison INT NOT NULL,
                        PRIMARY KEY(id_produit),
                        FOREIGN KEY(id_saison) REFERENCES Saison(id_saison)
);

CREATE TABLE Quantitee_vendue(
                                id_vente INT AUTO_INCREMENT,
                                id_maraicher INT,
                                date_vente DATE,
                                id_produit INT,
                                id_type_marche INT,
                                quantitee DECIMAL(15,2),
                                recette DECIMAL(15,2),
                                PRIMARY KEY(id_vente),
                                FOREIGN KEY(id_maraicher) REFERENCES Maraicher(id_maraicher),
                                FOREIGN KEY(id_produit) REFERENCES Produit(id_produit),
                                FOREIGN KEY(id_type_marche) REFERENCES type_marche(id_type_marche)
);


CREATE TABLE participation(
   id_participation INT AUTO_INCREMENT,
   id_maraicher INT,
   id_type_marche INT,
   date_participation DATE,
   duree VARCHAR(255),
   prix_place DECIMAL(10, 2),
   PRIMARY KEY(id_participation),
   FOREIGN KEY(id_maraicher) REFERENCES Maraicher(id_maraicher),
   FOREIGN KEY(id_type_marche) REFERENCES type_marche(id_type_marche)
);

CREATE TABLE se_deroule(
                           id_type_marche INT,
                           id_jour INT,
                           PRIMARY KEY(id_type_marche, id_jour),
                           FOREIGN KEY(id_type_marche) REFERENCES type_marche(id_type_marche),
                           FOREIGN KEY(id_jour) REFERENCES Jour_Semaine(id_jour)
);

INSERT INTO Lieu(Libelle_lieu) VALUES
                                           ('Nices'),
                                           ('Lyon'),
                                           ('Brest');

INSERT INTO Saison(id_saison,libelle_saison) VALUES
                                                 (NULL,'ete'),
                                                 (NULL,'printemps'),
                                                 (NULL,'automne'),
                                                 (NULL,'hiver');

INSERT INTO Jour_Semaine(id_jour, libelle_jour) VALUES
                                                    (NULL,'Lundi'),
                                                    (NULL,'Mardi'),
                                                    (NULL,'Mercredi'),
                                                    (NULL,'Jeudi'),
                                                    (NULL,'Vendredi'),
                                                    (NULL,'Samedi'),
                                                    (NULL,'Dimanche');

INSERT INTO type_marche(id_type_marche, Libelle_type_marche, id_lieu, nombre_place_type_marche, surface_type_marche) VALUES
                                                                          (NULL,'Wazemmes',  1, 2, 10.2),
                                                                          (NULL,'Lices',  2, 5 , 84.2),
                                                                          (NULL,'Halles',  1, 10 , 100.2);

INSERT INTO Produit(id_produit,libelle_produit, prix_au_kilo, id_saison) VALUES
                                                                             (NULL,'Tomate', 5.5, 1),
                                                                             (NULL,'Fraise', 2.5, 4),
                                                                             (NULL,'Banane', 6, 4);

INSERT INTO Maraicher(id_maraicher, nom, prenom, age, numero, mail) VALUES
                                                                        (NULL,'Dupont', 'Francis', 42, '06 75 29 38 56', 'francisdupont@gmail.com'),
                                                                        (NULL,'Legrand', 'Claude', 31, '07 47 21 26 79', 'claude.legrand@outlook.fr'),
                                                                        (NULL,'Bernard', 'Michel', 56, '06 56 38 05 96', 'bernard.michel@gmail.com');


INSERT INTO Quantitee_vendue(id_maraicher, date_vente, id_produit, id_type_marche, quantitee, recette) VALUES
                                                                                                         (1, '2024-12-23', 1, 1, 25.2, 12),
                                                                                                         (2, '2024-12-24', 2, 3, 18.2, 16.35),
                                                                                                         (1, '2024-12-24', 2, 2, 38.9, 22.35),
                                                                                                         (1, '2024-12-24', 3, 3,  24.25, 23.35),
                                                                                                         (2, '2024-12-22', 1, 1, 24.5, 29.4),
                                                                                                         (1, '2024-12-22', 3, 1, 22.5, 19.6);

INSERT INTO participation(id_maraicher, id_type_marche, date_participation, duree, prix_place) VALUES
                                                                                                         (1, 2, '2024-12-23', '1h00', 12.50),
                                                                                                         (2, 1, '2024-06-12', '2h30', 16.35),
                                                                                                         (1, 2, '2024-04-26', '1h30', 22.35),
                                                                                                         (3, 3, '2024-01-16', '3h30',  23.35),
                                                                                                         (2, 1, '2024-10-06', '2h00', 29.40),
                                                                                                         (3, 3, '2024-09-11', '4h00', 19.60);

INSERT INTO se_deroule(id_type_marche, id_jour) VALUES
                                                    (1,3),
                                                    (3,2);


# Donne le nom des marches qui sont à Nices
SELECT Libelle_type_marche
FROM type_marche
         JOIN  Lieu on type_marche.id_lieu = Lieu.id_lieu
WHERE Lieu.Libelle_lieu = 'Nices';

# Donne la moyenne du prix au kilo des produits qui sont recolte en hiver
SELECT AVG(Produit.prix_au_kilo) AS moyenne_prix_au_kilo
FROM Produit
         JOIN Saison on Produit.id_saison = Saison.id_saison
WHERE Saison.id_saison = 4;

# Renvoie la somme des recettes produit par Monsieur Dupont le 24 decembre 2024
SELECT SUM(recette) AS 'Recette'
FROM Quantitee_vendue
         JOIN Maraicher on Quantitee_vendue.id_maraicher = Maraicher.id_maraicher
WHERE date_vente = '2024-12-24' and nom='Dupont' ;

# Renvoie les differents produits qui etait present le 12 dècembre 2024 dans les marches ayant lieu un mardi
SELECT DISTINCT Produit.libelle_produit
FROM type_marche
         JOIN se_deroule on type_marche.id_type_marche = se_deroule.id_type_marche
         JOIN Jour_Semaine on se_deroule.id_jour = Jour_Semaine.id_jour
         JOIN Quantitee_vendue on type_marche.id_type_marche = Quantitee_vendue.id_type_marche
         JOIN Produit on Quantitee_vendue.id_produit = Produit.id_produit
WHERE se_deroule.id_jour = 2 and date_vente='2024-12-24';