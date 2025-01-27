#! /usr/bin/python
# -*- coding:utf-8 -*-
# mysql --user=bdidier3 --host=serveurmysql --password=mdp --database=BDD_bdidier3_tp
from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

                                    ## à ajouter
from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="localhost",                 # à modifier
            user="bdidier3",                     # à modifier
            password="mdp",                # à modifier
            database="BDD_bdidier3_tp",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')


#PAGE DE BASE
@app.route('/maraicher/layout')
def show_layout_maraicher():
    return render_template('layout.html')


#PAGE BAPTISTE (TYPE-MARCHE)
@app.route('/type-marche/show')
def show_typemarche():

    mycursor = get_db().cursor()
    sql = """SELECT typem.id_type_marche, typem.Libelle_type_marche, typem.nombre_place_type_marche, 
               typem.surface_type_marche, lieu.id_lieu, lieu.Libelle_lieu
        FROM type_marche typem
        JOIN Lieu lieu ON typem.id_lieu = lieu.id_lieu
    """
    mycursor.execute(sql)
    typemarche = mycursor.fetchall()

    return render_template('typemarche/show_typemarche.html', typemarche=typemarche)

@app.route('/type-marche/add', methods=['GET'])
def add_typemarche():

    mycursor = get_db().cursor()

    sql = "SELECT * FROM type_marche ORDER BY id_type_marche"
    mycursor.execute(sql)
    type_marche = mycursor.fetchall()
    print(type_marche)

    sql = "SELECT * FROM Lieu ORDER BY id_lieu"
    mycursor.execute(sql)
    lieux = mycursor.fetchall()
    print(lieux)

    return render_template('typemarche/add_typemarche.html', type_marche=type_marche, lieux=lieux)

@app.route('/type-marche/add', methods=['POST'])
def valid_add_typemarche():
        mycursor = get_db().cursor()

        Libelle_type_marche = request.form.get('Libelle_type_marche', '')
        id_type_marche = request.form.get('id_type_marche','')
        id_lieu = request.form.get('id_lieu', '')
        nombre_place_type_marche = request.form.get('nombre_place_type_marche', '')
        surface_type_marche = request.form.get('surface_type_marche', '')
        tuple_insert = (Libelle_type_marche, id_lieu, nombre_place_type_marche, surface_type_marche)
        sql = "INSERT INTO type_marche (Libelle_type_marche, id_lieu, nombre_place_type_marche, surface_type_marche) VALUES (%s, %s, %s, %s);"
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        message = u'type ajouté , libellé :' + Libelle_type_marche + 'id type_marche : ' + id_type_marche + ' nombre_place_type_marche : ' + nombre_place_type_marche + ' surface_type_marche' + surface_type_marche
        flash(message, 'alert-success')
        return redirect('/type-marche/show')

@app.route('/type-marche/delete', methods=['GET'])
def delete_typemarche():
    mycursor = get_db().cursor()

    sql = """SELECT typem.id_type_marche, typem.Libelle_type_marche, typem.nombre_place_type_marche, 
               typem.surface_type_marche, lieu.id_lieu, lieu.Libelle_lieu
        FROM type_marche typem
        JOIN Lieu lieu ON typem.id_lieu = lieu.id_lieu
    """
    mycursor.execute(sql)
    typemarche = mycursor.fetchall()
    return render_template('typemarche/delete_typemarche.html', typemarche=typemarche)
@app.route('/type-marche/delete', methods=['POST'])
def valid_delete_typemarche():
    id_type_marche = request.form.get('id_type_marche', '')
    mycursor = get_db().cursor()

    sql_del_fk_participation = """ DELETE FROM participation WHERE id_type_marche = %s;"""
    mycursor.execute(sql_del_fk_participation, id_type_marche)

    sql_del_qv = """ DELETE FROM Quantitee_vendue WHERE id_type_marche = %s;"""
    mycursor.execute(sql_del_qv, (id_type_marche,))

    sql_delete_se_deroule = """ DELETE FROM se_deroule WHERE id_type_marche = %s;"""
    mycursor.execute(sql_delete_se_deroule, (id_type_marche,))

    sql_delete_type_marche = """ DELETE FROM type_marche WHERE id_type_marche = %s;"""
    mycursor.execute(sql_delete_type_marche, (id_type_marche,))

    get_db().commit()
    return redirect('/type-marche/delete')



@app.route('/type-marche/edit', methods=['GET'])
def edit_typemarche():
    mycursor = get_db().cursor()
    id_type_marche = request.args.get('id_type_marche', '')
    sql = """
        SELECT id_type_marche, Libelle_type_marche, nombre_place_type_marche, surface_type_marche, id_lieu 
        FROM type_marche 
        WHERE id_type_marche = %s
        """
    mycursor.execute(sql, (id_type_marche,))
    type_marche = mycursor.fetchone()
    sql_lieux = "SELECT id_lieu, Libelle_lieu FROM Lieu"
    mycursor.execute(sql_lieux)
    lieux = mycursor.fetchall()
    return render_template('typemarche/edit_typemarche.html', type_marche=type_marche, lieux=lieux)

@app.route('/type-marche/edit', methods=['POST'])
def valid_edit_typemarche():
    mycursor = get_db().cursor()
    Libelle_type_marche = request.form.get('Libelle_type_marche', '')
    id_type_marche = request.form.get('id_type_marche', '')  # Utilisez form pour récupérer la valeur depuis le formulaire
    id_lieu = request.form.get('id_lieu', '')
    nombre_place_type_marche = request.form.get('nombre_place_type_marche', '')
    surface_type_marche = request.form.get('surface_type_marche', '')
    tuple_update = (Libelle_type_marche, id_lieu, nombre_place_type_marche, surface_type_marche, id_type_marche)
    sql = "UPDATE type_marche SET Libelle_type_marche = %s, id_lieu = %s, nombre_place_type_marche = %s, surface_type_marche = %s WHERE id_type_marche = %s;"
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type de marché modifié, id : ' + id_type_marche + "libelle : " + Libelle_type_marche + " id_lieu : " + id_lieu + "nombre de place : " + nombre_place_type_marche + "surface : " + surface_type_marche, 'alert-success')
    return redirect('/type-marche/show')

@app.route('/type-marche/etat', methods=["GET"])
def show_etat():

    mycursor = get_db().cursor()

    sql = """SELECT typem.id_type_marche, typem.Libelle_type_marche, typem.nombre_place_type_marche, 
                   typem.surface_type_marche, lieu.id_lieu, lieu.Libelle_lieu
            FROM type_marche typem
            JOIN Lieu lieu ON typem.id_lieu = lieu.id_lieu
        """
    mycursor.execute(sql)
    typemarche = mycursor.fetchall()

    sql_nb_place_total_tm = ''' SELECT
    SUM(nombre_place_type_marche) AS nb_place_tot,
    SUM(surface_type_marche) AS nb_surface_tot,
    COUNT(DISTINCT id_type_marche) AS type_marche_tot
FROM
    type_marche; '''

    mycursor.execute(sql_nb_place_total_tm)
    nb_place_total_tm = mycursor.fetchone()


    sql_nb_surface_total_tm = ''' SELECT surface_type_marche, id_type_marche FROM type_marche '''
    mycursor.execute(sql_nb_surface_total_tm)
    nb_surface_total_tm = mycursor.fetchone()

    return render_template('typemarche/etat_typemarche.html', nb_surface_total_tm=nb_surface_total_tm, nb_place_total_tm=nb_place_total_tm, typemarche=typemarche)





#PAGE MATHIS (PARTICIPATION)
@app.route('/participations/show')
def show_participations():
    mycursor = get_db().cursor()
    sql = '''
        SELECT participation.id_participation, Maraicher.nom, Maraicher.prenom, type_marche.Libelle_type_marche, participation.date_participation, participation.duree, participation.prix_place
        FROM participation
        JOIN Maraicher ON Maraicher.id_maraicher = participation.id_maraicher
        JOIN type_marche ON type_marche.id_type_marche = participation.id_type_marche
        ORDER BY participation.id_participation;
        '''
    mycursor.execute(sql)
    participations = mycursor.fetchall()
    return render_template('participation/show_participation.html', participations=participations)

@app.route('/participation/add', methods=['GET'])
def add_participation():
    mycursor = get_db().cursor()

    sql = "SELECT * FROM participation ORDER BY id_participation"
    mycursor.execute(sql)
    participation = mycursor.fetchall()
    print(participation)

    sql = "SELECT * FROM Maraicher ORDER BY id_maraicher"
    mycursor.execute(sql)
    maraicher = mycursor.fetchall()
    print(maraicher)

    sql = "SELECT * FROM type_marche ORDER BY id_type_marche"
    mycursor.execute(sql)
    type_marche = mycursor.fetchall()
    print(type_marche)

    return render_template('participation/add_participation.html', participation=participation, maraicher=maraicher, type_marche=type_marche)

@app.route('/participation/delete', methods=['GET'])
def delete_participation():
    id_participation = request.args.get('id_participation', '')
    # Suppression
    mycursor = get_db().cursor()
    tuple_delete = (id_participation,)
    sql = "DELETE FROM participation WHERE id_participation=%s;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message = u'id : ' + id_participation + ' deleted'
    flash(message)
    return redirect('/participations/show')

@app.route('/participation/add', methods=['POST'])
def valid_add_participation():
    mycursor = get_db().cursor()
    id_maraicher = request.form.get('id_maraicher') or None
    id_type_marche = request.form.get('id_type_marche') or None
    date_participation = request.form.get('date_participation') or None
    duree = request.form.get('duree') or None
    prix_place = request.form.get('prix_place') or None
    tuple_insert = (id_maraicher, id_type_marche, date_participation, duree, prix_place)
    sql = '''
            INSERT INTO participation (id_maraicher, id_type_marche, date_participation, duree, prix_place) 
            VALUES (%s, %s, %s, %s, %s);
        '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/participations/show')

@app.route('/participation/edit', methods=['GET'])
def edit_participation():
    mycursor = get_db().cursor()
    id_participation = request.args.get('id_participation', '')
    sql = '''
        SELECT id_participation, id_maraicher, id_type_marche, date_participation, duree, prix_place
        FROM participation
        WHERE id_participation=%s;
    '''
    mycursor.execute(sql, (id_participation,))
    participation = mycursor.fetchone()
    sql_maraicher = "SELECT id_maraicher, nom, prenom FROM Maraicher"
    mycursor.execute(sql_maraicher)
    maraicher = mycursor.fetchall()
    sql_type_marche = "SELECT id_type_marche, Libelle_type_marche  FROM type_marche"
    mycursor.execute(sql_type_marche)
    type_marche = mycursor.fetchall()
    return render_template('participation/edit_participation.html', participation=participation, maraicher=maraicher, type_marche=type_marche)

@app.route('/participation/edit', methods=['POST'])
def valid_edit_participation():
    mycursor = get_db().cursor()
    id_participation = request.form.get('id_participation', '')
    id_maraicher = request.form.get('id_maraicher', '')
    id_type_marche = request.form.get('id_type_marche', '')
    date_participation = request.form.get('date_participation')
    duree = request.form.get('duree', '')
    prix_place = request.form.get('prix_place', '')
    tuple_update = (id_maraicher, id_type_marche, date_participation, duree, prix_place, id_participation)
    sql = '''
        UPDATE participation 
        SET id_maraicher=%s, id_type_marche=%s, date_participation=%s, duree=%s, prix_place=%s 
        WHERE id_participation=%s;
    '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'vente modifié, id : ' + id_participation + "id maraicher : " + id_maraicher + "id type marche : " + id_type_marche + 'date_participation :' + date_participation + ' - duree :' + duree + ' - prix_place :' + prix_place,'alert-success')
    return redirect('/participations/show')

@app.route('/participations/etat', methods=["GET"])
def show_etat_participation():
    mycursor = get_db().cursor()
    sql = '''
        SELECT participation.id_participation, Maraicher.nom, Maraicher.prenom, type_marche.Libelle_type_marche, participation.date_participation, participation.duree, participation.prix_place
        FROM participation
        JOIN Maraicher ON Maraicher.id_maraicher = participation.id_maraicher
        JOIN type_marche ON type_marche.id_type_marche = participation.id_type_marche
        ORDER BY participation.id_participation;
        '''
    mycursor.execute(sql)
    participation = mycursor.fetchall()

    sql_prix_total = ''' 
        SELECT COUNT(participation.id_participation) AS nb_marche,sum(participation.prix_place) as prix_total
        FROM participation
         '''
    mycursor.execute(sql_prix_total)
    sql_prix_total = mycursor.fetchone()
    return render_template('participation/etat_participation.html', sql_prix_total=sql_prix_total, participation=participation)






#PAGE ANTOINE (VENTES)
@app.route('/ventes/show')
def show_ventes():
    mycursor = get_db().cursor()
    sql = ("""SELECT Quantitee_vendue.id_vente ,Maraicher.nom ,Quantitee_vendue.date_vente, type_marche.Libelle_type_marche, Produit.libelle_produit, Quantitee_vendue.quantitee
           FROM Quantitee_vendue 
           JOIN Maraicher ON Maraicher.id_maraicher = Quantitee_vendue.id_maraicher
           JOIN type_marche ON type_marche.id_type_marche = Quantitee_vendue.id_type_marche
           JOIN Produit ON Produit.id_produit = Quantitee_vendue.id_produit
           ORDER BY Quantitee_vendue.id_maraicher""")
    mycursor.execute(sql)
    ventes = mycursor.fetchall()
    return render_template('ventes/show_ventes.html', ventes=ventes )

@app.route('/ventes/delete', methods=['GET'])
def delete_ventes():

    id_vente = request.args.get('id_vente','')
    mycursor = get_db().cursor()
    tuple_delete = (id_vente,)
    sql = "DELETE FROM Quantitee_vendue WHERE id_vente = %s ;"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message = u'id : ' + id_vente + ' deleted'
    flash(message)
    return redirect('/ventes/show')

@app.route('/ventes/add', methods=['GET'])
def add_vente():

    mycursor = get_db().cursor()

    sql_qv = "SELECT * FROM Quantitee_vendue ORDER BY id_vente"
    mycursor.execute(sql_qv)
    ventes = mycursor.fetchall()
    print(ventes)

    sql_m = "SELECT * FROM Maraicher ORDER BY id_maraicher"
    mycursor.execute(sql_m)
    maraicher = mycursor.fetchall()
    print(maraicher)

    sql_tm = "SELECT * FROM type_marche ORDER BY id_type_marche"
    mycursor.execute(sql_tm)
    type_marche = mycursor.fetchall()
    print(type_marche)

    sql_prod = "SELECT * FROM Produit ORDER BY id_produit"
    mycursor.execute(sql_prod)
    produit = mycursor.fetchall()
    print(produit)

    return render_template('ventes/add_ventes.html', ventes=ventes, maraicher=maraicher, type_marche=type_marche, produit=produit)

@app.route('/ventes/add', methods=['POST'])
def valid_add_vente():
        mycursor = get_db().cursor()

        id_maraicher = request.form.get('id_maraicher') or None
        id_type_marche = request.form.get('id_type_marche') or None
        id_produit = request.form.get('id_produit') or None
        quantitee = request.form.get('quantitee') or None
        date_vente = request.form.get('date_vente')
        tuple_insert = (id_maraicher, date_vente, id_type_marche, id_produit, quantitee)
        sql = "INSERT INTO Quantitee_vendue (id_maraicher , date_vente , id_type_marche, id_produit, quantitee) VALUES ( %s, %s, %s, %s, %s);"
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        return redirect('/ventes/show')

@app.route('/ventes/edit', methods=['GET'])
def edit_ventes():
    mycursor = get_db().cursor()
    id_vente = request.args.get('id_vente', '')
    sql = """
        SELECT id_vente, id_maraicher, date_vente, id_produit, id_type_marche, quantitee, recette 
        FROM Quantitee_vendue 
        WHERE id_vente = %s
        """
    mycursor.execute(sql, (id_vente,))
    ventes = mycursor.fetchone()
    sql_maraicher = "SELECT id_maraicher, nom FROM Maraicher"
    mycursor.execute(sql_maraicher)
    maraicher = mycursor.fetchall()
    sql_produit = "SELECT id_produit, libelle_produit FROM Produit"
    mycursor.execute(sql_produit)
    produit = mycursor.fetchall()
    sql_type_marche = "SELECT id_type_marche,Libelle_type_marche  FROM type_marche"
    mycursor.execute(sql_type_marche)
    type_marche = mycursor.fetchall()
    return render_template('ventes/edit_ventes.html', ventes=ventes, maraicher=maraicher, type_marche=type_marche, produit=produit)

@app.route('/ventes/edit', methods=['POST'])
def valid_edit_ventes():
    mycursor = get_db().cursor()
    id_vente = request.form.get('id_vente', '')  # Utilisez form pour récupérer la valeur depuis le formulaire
    id_maraicher = request.form.get('id_maraicher', '')
    date_vente = request.form.get('date_vente')
    id_type_marche = request.form.get('id_type_marche', '')
    id_produit = request.form.get('id_produit', '')
    quantitee = request.form.get('quantitee', '')
    tuple_update = (id_maraicher, date_vente,id_type_marche, id_produit, quantitee,id_vente)
    sql = "UPDATE Quantitee_vendue SET id_maraicher = %s, date_vente = %s,id_type_marche = %s, id_produit = %s, quantitee = %s WHERE id_vente = %s;"
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'vente modifié, id : ' + id_vente + "id maraicher : " + id_maraicher + " date : " + date_vente + "id produit : " + id_produit + "quantitee : " + quantitee, 'alert-success')
    return redirect('/ventes/show')

@app.route('/ventes/etat', methods=["GET"])
def show_etat_ventes():

    mycursor = get_db().cursor()

    sql_v = """SELECT Quantitee_vendue.id_vente ,Maraicher.nom ,Quantitee_vendue.date_vente, type_marche.Libelle_type_marche, Produit.libelle_produit, Quantitee_vendue.quantitee
           FROM Quantitee_vendue 
           JOIN Maraicher ON Maraicher.id_maraicher = Quantitee_vendue.id_maraicher
           JOIN type_marche ON type_marche.id_type_marche = Quantitee_vendue.id_type_marche
           JOIN Produit ON Produit.id_produit = Quantitee_vendue.id_produit
           ORDER BY Quantitee_vendue.id_maraicher
        """
    mycursor.execute(sql_v)
    ventes = mycursor.fetchall()

    sql_p = """  SELECT id_produit AS id, libelle_produit AS nom, prix_au_kilo AS prix, id_saison AS id_saison
    FROM Produit
    ORDER BY nom DESC; 
            """
    mycursor.execute(sql_p)
    produit = mycursor.fetchall()

    sql_prix_total = ''' 
    SELECT q.id_vente,p.libelle_produit,p.prix_au_kilo,q.quantitee,sum(p.prix_au_kilo * q.quantitee) AS prix_total_calcule,sum(q.quantitee) as nb_quantitee
    FROM Quantitee_vendue q
    JOIN Produit p ON q.id_produit = p.id_produit; '''

    mycursor.execute(sql_prix_total)
    nb_prix_total = mycursor.fetchone()


    sql_nb_ventes = ''' SELECT count(id_vente) as nb_de_ventes FROM Quantitee_vendue '''
    mycursor.execute(sql_nb_ventes)
    nb_ventes = mycursor.fetchone()

    return render_template('ventes/etat_ventes.html', ventes=ventes, nb_prix_total=nb_prix_total, nb_ventes=nb_ventes, produit=produit)




#ETHAN PRODUIT

#ETHAN PRODUIT

@app.route('/produit/show')
def show_produit():
    mycursor = get_db().cursor()
    id_saison = request.form.get('id_saison')
    sql = '''   SELECT id_produit AS id_produit, libelle_produit AS libelle_produit, prix_au_kilo AS prix_au_kilo, id_saison AS id_saison
    FROM Produit
    ORDER BY id_produit DESC;      '''
    mycursor.execute(sql)

    produits = mycursor.fetchall()
    return render_template('produit/show_produit.html', produit = produits )


@app.route('/produit/add', methods=['GET'])
def add_produit():

    mycursor = get_db().cursor()
    sql = '''SELECT id_saison, libelle_saison FROM Saison'''
    mycursor.execute(sql)
    saisons = mycursor.fetchall()
    prix = mycursor.fetchall()
    produit = {}
    return render_template('produit/add_produit.html', produit=produit, saisons=saisons, prix = prix)



@app.route('/produit/add', methods=['POST'])
def valid_add_produit():
    print('''ajout du produit dans le tableau''')
    nom = request.form.get('libelle_produit')
    id_saison = request.form.get('id_saison')
    prix = request.form.get('prix')
    print(f'nom : {nom} - id_saison : {id_saison}')




    # insert
    mycursor = get_db().cursor()
    sql = '''INSERT INTO Produit (id_produit, libelle_produit, id_saison, prix_au_kilo) 
    VALUES (NULL, %s, %s, %s);'''
    tuple_param = (nom, id_saison, prix)
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/produit/show')


@app.route('/produit/edit', methods=['GET'])
def edit_produit():
    id = request.args.get('id_produit')
    if id and id.isnumeric():
        mycursor = get_db().cursor()


        produit_sql = '''
            SELECT id_produit, libelle_produit, id_saison, prix_au_kilo
            FROM Produit
            WHERE id_produit = %s
        '''
        mycursor.execute(produit_sql, (id,))
        produit = mycursor.fetchone()


        saisons_sql = 'SELECT id_saison, libelle_saison FROM Saison'
        mycursor.execute(saisons_sql)
        saisons = mycursor.fetchall()


        print("Produit récupéré :", produit)
        print("Saisons récupérées :", saisons)
    else:
        produit = None
        saisons = []

    return render_template('produit/edit_produit.html', produit=produit, saisons=saisons)


@app.route('/produit/edit', methods=['POST'])
def valid_edit_produit():
    print('Modification du produit dans le tableau')


    id = request.form.get('id_produit')
    nom = request.form.get('libelle_produit')
    groupe = request.form.get('id_saison')
    prix = request.form.get('prix_au_kilo')


    mycursor = get_db().cursor()
    sql = '''UPDATE Produit 
             SET libelle_produit = %s, id_saison = %s, prix_au_kilo = %s 
             WHERE id_produit = %s;'''


    tuple_param = (nom, groupe, prix, id)


    mycursor.execute(sql, tuple_param)
    get_db().commit()


    return redirect('/produit/show')


@app.route('/produit/delete', methods=['GET'])
def delete_produit():
    mycursor = get_db().cursor()

    sql = """SELECT prod.id_produit, prod.libelle_produit, prod.prix_au_kilo, prod.id_saison
        FROM Produit prod
        JOIN Saison saison ON prod.id_saison = saison.id_saison 
        ORDER BY id_produit DESC; """
    mycursor.execute(sql)
    produit = mycursor.fetchall()
    return render_template('produit/delete_produit.html', produit=produit)



@app.route('/produit/delete', methods=['POST'])
def valid_delete_produit():
    id_produit = request.form.get('id_produit', '')
    mycursor = get_db().cursor()


    sql_del_qv = """ 
    DELETE FROM Quantitee_vendue WHERE id_produit = %s;
    """
    mycursor.execute(sql_del_qv, (id_produit,))


    sql_del_produit = """ 
    DELETE FROM Produit WHERE id_produit = %s;
    """
    mycursor.execute(sql_del_produit, (id_produit,))

    get_db().commit()
    return redirect('/produit/delete')



@app.route('/produit/etat', methods=["GET"])
def etat_produit():
    mycursor = get_db().cursor()


    sql_totals = """
    SELECT 
        COUNT(*) AS total_produits,
        SUM(prix_au_kilo) AS total_prix,
        AVG(prix_au_kilo) AS prix_moyen
    FROM 
        Produit;
    """
    mycursor.execute(sql_totals)
    totals = mycursor.fetchone()


    sql_rentable = """
  SELECT 
    Produit.libelle_produit, 
    SUM(COALESCE(Quantitee_vendue.quantitee, 0) * COALESCE(Produit.prix_au_kilo, 0)) AS recette_totale
FROM 
    Quantitee_vendue
JOIN 
    Produit ON Quantitee_vendue.id_produit = Produit.id_produit
GROUP BY 
    Produit.libelle_produit
ORDER BY 
    recette_totale DESC;
    """
    mycursor.execute(sql_rentable)
    produit_rentable = mycursor.fetchone()

    return render_template('produit/etat_produit.html', totals=totals, produit_rentable=produit_rentable)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
