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

class Categorie(models.Model):
    titre = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to="ImagesCategories/", null=True, blank=True )
    dateAjout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-dateAjout']

    def __str__(self):
        return self.titre


#Classe Article 
class Article(models.Model):
    nom = models.CharField(max_length=128)
    stock = models.PositiveBigIntegerField(default=1)
    image = models.ImageField(upload_to="imagesArticles/", null=True, blank=True)
    prixUnitaire = models.DecimalField(max_digits=10, decimal_places=2)
    dateAjout = models.DateTimeField(auto_now_add=True)
    #dateModification = models.DateTimeField(auto_now=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    class Meta:
        ordering=['-dateAjout']

    def __str__(self):
        return f"L'article {self.nom} a {self.stock} stock"


class Client(models.Model):
    nomClient = models.CharField(max_length=128, null=False)
    adresse = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    dateInscription = models.DateTimeField(auto_now_add=True)



#classe Panier
class Panier(models.Model):
    dateAjout = models.DateTimeField(auto_now_add=True)
    dateModification = models.DateTimeField(auto_now=True) 
    achats = models.ManyToManyField(Client, through="Achat", related_name="panierClient")

#classe Achat
class Achat(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="achatClient")
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name="achatClient")
    dateCommande = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveBigIntegerField(default=1)
    prixTotal = models.DecimalField(max_digits=10, decimal_places=2)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="achats")
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["dateCommande"]


    def __str__(self):
        return f"{self.Client.nomClient} a acheté {self.quantite} de {self.Article.nom} le {self.dateCommande}"
