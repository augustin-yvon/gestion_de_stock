import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import ttk

# Connexion à la base de données
db = mysql.connector.connect(host="localhost", user="root", password="Troll1394@@@@", database="boutique")

# Création de la fenêtre
window = tk.Tk()
window.title("Liste des produits")

# Récupération des produits depuis la base de données
cursor = db.cursor()
cursor.execute("select * from produits")
produits = cursor.fetchall()

# Création du tableau pour afficher les produits
tableau = ttk.Treeview(window, columns=("nom", "description", "prix", "quantite", "categorie"))

# Initialisation des colonnes
tableau.heading("#0", text="ID", anchor='w')
tableau.column("#0", width=0, stretch=tk.NO)

tableau.heading("nom", text="Nom", anchor='w')
tableau.column("nom", width=150)

tableau.heading("description", text="Description", anchor='w')
tableau.column("description", width=300)

tableau.heading("prix", text="Prix", anchor='w')
tableau.column("prix", width=75)

tableau.heading("quantite", text="Quantité en stock", anchor='w')
tableau.column("quantite", width=125)

tableau.heading("categorie", text="Catégorie", anchor='w')
tableau.column("categorie", width=125)

tableau.pack()

# Ajout des produits au tableau
for produit in produits:
    id_produit = produit[0]
    nom = produit[1]
    description = produit[2]
    prix = produit[3]
    quantite = produit[4]
    id_categorie = produit[5]
    cursor.execute("select nom from categorie where id = '{}'".format(id_categorie))
    categorie = cursor.fetchone()[0]
    tableau.insert("", tk.END, text=id_produit, values=(nom, description, prix, quantite, categorie))

"""Fonction pour ajouter un produit
   Dans un premier temps la fonction créée une nouvelle fenêtre avec des entré pour écrire les information du produit
   Ensuite une seconde fonction est créée qui récupère les information entrée, puis les affiche dans les tableau et
   les mets à jour dans la base de données."""
def ajouter_produit():
    # Création de la fenêtre d'ajout de produit
    ajout_window = tk.Toplevel()
    ajout_window.title("Ajouter un produit")

    # Champ pour le nom du produit
    nom_label = tk.Label(ajout_window, text="Nom :")
    nom_label.grid(column=0, row=0, padx=5, pady=5)
    nom_entry = tk.Entry(ajout_window)
    nom_entry.grid(column=1, row=0, padx=5, pady=5)

    # Champ pour la description du produit
    description_label = tk.Label(ajout_window, text="Description :")
    description_label.grid(column=0, row=1, padx=5, pady=5)
    description_entry = tk.Entry(ajout_window)
    description_entry.grid(column=1, row=1, padx=5, pady=5)

    # Champ pour le prix du produit
    prix_label = tk.Label(ajout_window, text="Prix :")
    prix_label.grid(column=0, row=2, padx=5, pady=5)
    prix_entry = tk.Entry(ajout_window)
    prix_entry.grid(column=1, row=2, padx=5, pady=5)

    # Champ pour la quantité du produit
    quantite_label = tk.Label(ajout_window, text="Quantité :")
    quantite_label.grid(column=0, row=3, padx=5, pady=5)
    quantite_entry = tk.Entry(ajout_window)
    quantite_entry.grid(column=1, row=3, padx=5, pady=5)

    # Liste des catégories pour le choix
    cursor.execute("select * from categorie")
    categories = cursor.fetchall()
    categorie_choices = [c[1] for c in categories]
    categorie_label = tk.Label(ajout_window, text="Catégorie :")
    categorie_label.grid(column=0, row=4, padx=5, pady=5)
    categorie_choice = ttk.Combobox(ajout_window, values=categorie_choices)
    categorie_choice.grid(column=1, row=4, padx=5, pady=5)

    def ajouter():
        # Récupération des informations saisies
        nom = nom_entry.get()
        description = description_entry.get()
        prix = float(prix_entry.get())
        quantite = int(quantite_entry.get())
        categorie_nom = categorie_choice.get()

        # Récupération de l'id de la catégorie
        cursor.execute("select id from categorie where nom = '{}'".format(categorie_nom))
        categorie_id = cursor.fetchone()[0]

        # Màj de la base de données
        cursor.execute("insert into produits (nom, description, prix, quantite, id_categorie) values (%s, %s, %s, %s, %s)", (nom, description, prix, quantite, categorie_id))
        db.commit()

        # Affichage du produit dans le tableau
        cursor.execute("select * from produits where nom = '{}'".format(nom))
        produit = cursor.fetchone()
        id_produit = produit[0]
        categorie_id = produit[5]
        cursor.execute("select nom from categorie where id = '{}'".format(categorie_id))
        categorie = cursor.fetchone()[0]
        tableau.insert("", tk.END, text=id_produit, values=(nom, description, prix, quantite, categorie))

        # Destruction de la fenêtre
        ajout_window.destroy()

    # Création du bouton de Ajouter
    ajouter_btn = tk.Button(ajout_window, text="Ajouter", command=ajouter)
    ajouter_btn.grid(row=5, column=1, padx=5, pady=5)

"""Fonction pour supprimer un produit
   Cette fonction prend en argument id_produit, qui est l'id de sélection de la ligne du tableau"""
def supprimer_produit(id_produit):
    # Récupère le nom du produit pour le supprimer de la base de données
    nom = tableau.item(id_produit, "values")[0]
    cursor.execute("delete from produits where nom = '{}'".format(nom))
    db.commit()
    # Suppression de la ligne du tableau avec l'id de la ligne 
    tableau.delete(id_produit)

"""Fonction pour modifier le produit    
   La fonction modifier ne fonctionne pas, au lieu de modifier la ligne sélectionné, 
   elle créé une nouvelle ligne dans le tableau je préfère le rendre maintenant afin
   d'éviter de prendre du retard"""
def modifier_produit():
    # Création de la fenêtre de modification de produit
    ajout_window = tk.Toplevel()
    ajout_window.title("Ajouter un produit")

    # Champ pour le nom du produit
    nom_label = tk.Label(ajout_window, text="Nom :")
    nom_label.grid(column=0, row=0, padx=5, pady=5)
    nom_entry = tk.Entry(ajout_window)
    nom_entry.grid(column=1, row=0, padx=5, pady=5)

    # Champ pour la description du produit
    description_label = tk.Label(ajout_window, text="Description :")
    description_label.grid(column=0, row=1, padx=5, pady=5)
    description_entry = tk.Entry(ajout_window)
    description_entry.grid(column=1, row=1, padx=5, pady=5)

    # Champ pour le prix du produit
    prix_label = tk.Label(ajout_window, text="Prix :")
    prix_label.grid(column=0, row=2, padx=5, pady=5)
    prix_entry = tk.Entry(ajout_window)
    prix_entry.grid(column=1, row=2, padx=5, pady=5)

    # Champ pour la quantité du produit
    quantite_label = tk.Label(ajout_window, text="Quantité :")
    quantite_label.grid(column=0, row=3, padx=5, pady=5)
    quantite_entry = tk.Entry(ajout_window)
    quantite_entry.grid(column=1, row=3, padx=5, pady=5)

    # Liste des catégories pour le choix    
    cursor.execute("select * from categorie")
    categories = cursor.fetchall()
    categorie_choices = [c[1] for c in categories]
    categorie_label = tk.Label(ajout_window, text="Catégorie :")
    categorie_label.grid(column=0, row=4, padx=5, pady=5)
    categorie_choice = ttk.Combobox(ajout_window, values=categorie_choices)
    categorie_choice.grid(column=1, row=4, padx=5, pady=5)

    def modifier():
        # id_produit prend pour valeur l'id de la ligne sélectionné
        id_produit = tableau.focus()

        # Essai de récupérer l'information entrée
        try:
            nom = nom_entry.get()
            # Si le champ est vide, l'information prend la valeur correspondante dans le tableau
            if nom == '':
                nom = tableau.item(id_produit, "values")[0]
        except:
            nom = tableau.item(id_produit, "values")[0]
        
        try:
            description = description_entry.get()
            if description == '':
                description = tableau.item(id_produit, "values")[1]
        except:
            description = tableau.item(id_produit, "values")[1]
        
        try:
            prix = float(prix_entry.get())
            if prix == '':
                prix = tableau.item(id_produit, "values")[2]
        except:
            prix = tableau.item(id_produit, "values")[2]
        try:
            quantite = int(quantite_entry.get())
            if quantite == '':
                quantite = tableau.item(id_produit, "values")[3]
        except:
            quantite = tableau.item(id_produit, "values")[3]
        try:
            categorie_nom = categorie_choice.get()
            if categorie_nom == '':
                categorie_nom = tableau.item(id_produit, "values")[4]
        except:
            categorie_nom = tableau.item(id_produit, "values")[4]
        
        # Màj de la base de données
        cursor.execute("select id from categorie where nom = '{}'".format(categorie_nom))
        categorie_id = cursor.fetchone()[0]
        cursor.execute("insert into produits (nom, description, prix, quantite, id_categorie) values ('{}', '{}', {}, {}, '{}')".format(nom, description, prix, quantite, categorie_id))
        db.commit()

        # Affichage du produit dans le tableau
        cursor.execute("select * from produits where nom = '{}'".format(nom))
        produit = cursor.fetchone()
        id_produit = produit[0]
        categorie_id = produit[5]
        cursor.execute("select nom from categorie where id = {}".format(categorie_id))
        categorie = cursor.fetchone()[0]
        tableau.insert("", tk.END, text=id_produit, values=(nom, description, prix, quantite, categorie))
        supprimer_produit(id_produit)

        # Fermeture de la fenêtre d'ajout de produit
        ajout_window.destroy()

    modifier_btn = tk.Button(ajout_window, text="Modifier", command=modifier)
    modifier_btn.grid(row=5, column=1, padx=5, pady=5)

# Création de la bopite contenant les boutons
boutons_frame = tk.Frame(window)

# Création des boutons Ajouter produit, Mofifier et Supprimer

bouton_ajouter = tk.Button(boutons_frame, text="Ajouter produit", command=ajouter_produit)
bouton_ajouter.pack(side=tk.LEFT, padx=5, pady=5)

bouton_modifier = tk.Button(boutons_frame, text="Modifier", command = lambda: modifier_produit())
bouton_modifier.pack(side=tk.LEFT, padx=5, pady=5)

supprimer_btn = tk.Button(boutons_frame, text="Supprimer", command = lambda: supprimer_produit(tableau.focus()))
supprimer_btn.pack(side=tk.LEFT, padx=5, pady=5)

boutons_frame.pack(side=tk.BOTTOM, pady=10)

# Boucle principale de la fenêtre
window.mainloop()

# Fermeture de la connexion à la base de données
db.close()
