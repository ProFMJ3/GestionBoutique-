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
- Liste Achats(FK)




"""

#Model catégorie

class Categorie(models.Models):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    dateAjout = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"
        ordering("-dateAjout")
    def __init__(self):
        return self.titre

class Article(models.Models):
    nom = models.CharField(max_length=255)
    quantite = models.IntegerField()
    image = models.ImageField(upload_to="imagesArticles/")
    prixUnitaire = models.DecimalField(max_digits=10, decimal_places=2)
    dateAjout = models.DateTimeField(auto_now_add=True)
    dateModification = models.DateTimeField(auto_now=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        #ordering("-dateAjout")
        ordering=['-dateAjout']
    def __str__(self):
        return self.nom

class Client(models.Models):
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    dateInscription = models.DateTimeField(auto_now_add=True)


class Panier(models.Model):
    dateAjout = models.DateTimeField(auto_now_add=True)
    dateModification = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    Achats = models.ManyToManyField(Client, trough="achats")


class achats(models.Model):
    dateCommande = models.DateTimeField(auto_now_add=True)
    quantite = models.IntegerField()
    prixTotal = models.DecimalField(max_digits=10, decimal_places=2)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering["-dateCommande"]


    def __str__(self):
        return self.article.nom
