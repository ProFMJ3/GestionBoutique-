from django.db import models
from django.utils import  timezone

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
    dateModification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =['-dateAjout']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if self.pk is not None:  # Si l'article existe déjà (modification)
            self.dateModification = timezone.now()
        super().save(*args, **kwargs)


#Classe Article 
class Article(models.Model):
    nom = models.CharField(max_length=128)
    stock = models.PositiveBigIntegerField(default=1)
    image = models.ImageField(upload_to="imagesArticles/", null=True, blank=True)
    prixUnitaire = models.DecimalField(max_digits=10, decimal_places=2)
    dateAjout = models.DateTimeField(auto_now_add=True)
    dateModification = models.DateTimeField(auto_now=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering=['-dateAjout']



    def __str__(self):
        return f"L'article {self.nom} a {self.stock} stock"

    def mise_a_jour_disponibilite(self):
        if self.stock <= 0:
            self.disponible = False

    def save(self, *args, **kwargs):
        if self.pk is not None:  # Si l'article existe déjà (modification)
            self.dateModification = timezone.now()
        super().save(*args, **kwargs)


class Client(models.Model):
    nomClient = models.CharField(max_length=128, null=False)
    adresse = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    dateInscription = models.DateTimeField(auto_now_add=True)


"""
#classe Panier
class Panier(models.Model):
    client = models.ManyToManyField(Client, through="Achat", related_name="panierClient")

    dateAjout = models.DateTimeField(auto_now_add=True)
    dateModification = models.DateTimeField(auto_now=True) 
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"Panier de {self.client.nomClient} - {'Validé' if self.valide else 'En cours'}"

#classe Achat
class Achat(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="achatClient")
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name="achatClient")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="achats")
    dateCommande = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveBigIntegerField(default=1)
    prixTotal = models.DecimalField(max_digits=10, decimal_places=2)

    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["dateCommande"]


    def __str__(self):
        return f"{self.client.nomClient} a acheté {self.quantite} de {self.article.nom} le {self.dateCommande}"
"""