from django.db import models

# Create your models here.


"""
Acteur du système:
- Administrateur
- Client ?? optionnel juste rechercher les catalogues de produits

- Gérant du boutique


Les classes de modèles:
. Catégories de produits(Alimentaires, Cosmétiques, Fouritures Scolaires, Produits Electro-Ménagères)
    - Nom
    - Description
    -date Ajout
    -date Modification


. Articles 
    - Nom
    - quantite en stock
    - image
    - prixUnitaire
    - date Ajout
    - date de modification
    - categorie(FK)

NB:Si on prends une catégorie, on va avoir plusieurs articles et un article appartient à une seule catégorie.
    - On peut savoir pour une catégorie total des articles qu'elle contient

.Achats:
    - date
    - quantite
    - prixTotal
    - article(FK)
    - client(FK)
    - gérer les articles en stock

.Factures:
    - date
    - prixTotal
    - client(FK)
    - achat(FK)
    - gérer les achats effectués par un client

.Client:
    - nom
    - prenom
    - adresse
    - telephone
    - dateInscription
    

.Panier:
- dateAjout
- dateModification
- quantite
- prixTotal
- client(FK)
- article(FK)




"""
