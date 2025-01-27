DROP TABLE IF EXISTS se_déroule;
DROP TABLE IF EXISTS Participe;
DROP TABLE IF EXISTS Quantité_vendue;
DROP TABLE IF EXISTS Produit;
DROP TABLE IF EXISTS Jour_Semaine;
DROP TABLE IF EXISTS type_marché;
DROP TABLE IF EXISTS Lieu;
DROP TABLE IF EXISTS Saison;
DROP TABLE IF EXISTS Maraicher;

CREATE TABLE Maraicher(
                          id_maraicher INT AUTO_INCREMENT,
                          nom VARCHAR(50),
                          prenom VARCHAR(50),
                          age VARCHAR(50),
                          numéro VARCHAR(20),
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

CREATE TABLE type_marché(
                            id_type_marché INT AUTO_INCREMENT,
                            Libelle_type_marché VARCHAR(50),
                            id_lieu INT NOT NULL,
                            PRIMARY KEY(id_type_marché),
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

CREATE TABLE Quantité_vendue(
                                id_maraicher INT,
                                JJ_MM_AAAA DATE,
                                id_produit INT,
                                id_type_marché INT,
                                quantite DECIMAL(15,2),
                                recette DECIMAL(15,2),
                                PRIMARY KEY(id_maraicher, JJ_MM_AAAA, id_produit, id_type_marché),
                                FOREIGN KEY(id_maraicher) REFERENCES Maraicher(id_maraicher),
                                FOREIGN KEY(id_produit) REFERENCES Produit(id_produit),
                                FOREIGN KEY(id_type_marché) REFERENCES type_marché(id_type_marché)
);

CREATE TABLE Participe(
                          id_maraicher INT,
                          JJ_MM_AAAA DATE,
                          id_type_marché INT,
                          PRIMARY KEY(id_maraicher, JJ_MM_AAAA, id_type_marché),
                          FOREIGN KEY(id_maraicher) REFERENCES Maraicher(id_maraicher),
                          FOREIGN KEY(id_type_marché) REFERENCES type_marché(id_type_marché)
);

CREATE TABLE se_déroule(
                           id_type_marché INT,
                           id_jour INT,
                           PRIMARY KEY(id_type_marché, id_jour),
                           FOREIGN KEY(id_type_marché) REFERENCES type_marché(id_type_marché),
                           FOREIGN KEY(id_jour) REFERENCES Jour_Semaine(id_jour)
);

INSERT INTO Lieu(id_lieu,Libelle_lieu) VALUES
                                           (NULL,'Nices'),
                                           (NULL,'Lyon'),
                                           (NULL,'Brest');

INSERT INTO Saison(id_saison,libelle_saison) VALUES
                                                 (NULL,'été'),
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

INSERT INTO type_marché(id_type_marché, Libelle_type_marché, id_lieu) VALUES
                                                                          (NULL,'Wazemmes',  1),
                                                                          (NULL,'Lices',  2),
                                                                          (NULL,'Halles',  1);

INSERT INTO Produit(id_produit,libelle_produit, prix_au_kilo, id_saison) VALUES
                                                                             (NULL,'Tomate', 5.5, 1),
                                                                             (NULL,'Fraise', 2.5, 4),
                                                                             (NULL,'Banane', 6, 4);

INSERT INTO Maraicher(id_maraicher, nom, prenom, age, numéro, mail) VALUES
                                                                        (NULL,'Dupont', 'Francis', 42, '06 75 29 38 56', 'francisdupont@gmail.com'),
                                                                        (NULL,'Legrand', 'Claude', 31, '07 47 21 26 79', 'claude.legrand@outlook.fr'),
                                                                        (NULL,'Bernard', 'Michel', 56, '06 56 38 05 96', 'bernard.michel@gmail.com');


INSERT INTO Quantité_vendue(id_maraicher, JJ_MM_AAAA, id_produit, id_type_marché, quantite, recette) VALUES
                                                                                                         (1, '2024-12-23', 1, 1, 25.2, 12),
                                                                                                         (2, '2024-12-24', 2, 3, 18.2, 16.35),
                                                                                                         (1, '2024-12-24', 2, 2, 38.9, 22.35),
                                                                                                         (1, '2024-12-24', 3, 3,  24.25, 23.35),
                                                                                                         (2, '2024-12-22', 1, 1, 24.5, 29.4),
                                                                                                         (1, '2024-12-22', 3, 1, 22.5, 19.6);

INSERT INTO se_déroule(id_type_marché, id_jour) VALUES
                                                    (1,3),
                                                    (3,2);


# Donne le nom des marchés qui sont à Nices
SELECT Libelle_type_marché
FROM type_marché
         JOIN  Lieu on type_marché.id_lieu = Lieu.id_lieu
WHERE Lieu.Libelle_lieu = 'Nices';

# Donne la moyenne du prix au kilo des produits qui sont récolté en hiver
SELECT AVG(Produit.prix_au_kilo) AS moyenne_prix_au_kilo
FROM Produit
         JOIN Saison on Produit.id_saison = Saison.id_saison
WHERE Saison.id_saison = 4;

# Renvoie la somme des recettes produit par Monsieur Dupont le 24 décembre 2024
SELECT SUM(recette) AS 'Recette'
FROM Quantité_vendue
         JOIN Maraicher on Quantité_vendue.id_maraicher = Maraicher.id_maraicher
WHERE JJ_MM_AAAA = '2024-12-24' and nom='Dupont' ;

# Renvoie les différents produits qui était présent le 12 dècembre 2024 dans les marchés ayant lieu un mardi
SELECT DISTINCT Produit.libelle_produit
FROM type_marché
         JOIN se_déroule on type_marché.id_type_marché = se_déroule.id_type_marché
         JOIN Jour_Semaine on se_déroule.id_jour = Jour_Semaine.id_jour
         JOIN Quantité_vendue on type_marché.id_type_marché = Quantité_vendue.id_type_marché
         JOIN Produit on Quantité_vendue.id_produit = Produit.id_produit
WHERE se_déroule.id_jour = 2 and JJ_MM_AAAA='2024-12-24';