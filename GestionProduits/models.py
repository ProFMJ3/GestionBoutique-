from django.db import models
from django.utils import  timezone
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.core.validators import  RegexValidator

import random

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

#class catégorie : un ensemble d'articles

class Categorie(models.Model):
    titre = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to="ImagesCategories/", null=True, blank=True )
    dateAjout = models.DateTimeField(auto_now_add=True)
    dateModification = models.DateTimeField(null=True, blank=True)



    class Meta:
        ordering =['-dateAjout']


    def controleTitre(self):
        self.titre = self.titre.strip()
        if self.titre.replace(".", "", 1).replace(",", "",1).replace(";","",1) .isdigit():
            raise ValidationError("Le titre ne doit pas être un nombre entier ou décimal. Il doit contenir des lettres.")

        self.titre = capfirst(self.titre)

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if self.pk is not None:  # Si l'article existe déjà (modification)
            self.dateModification = timezone.now()
        else :
            self.dateModification = None

        self.full_clean()
        super().save(*args, **kwargs)


#Classe Article : composition d'une catégorie
class Article(models.Model):
    nom = models.CharField(max_length=128)
    stock = models.PositiveBigIntegerField(default=1)
    image = models.ImageField(upload_to="imagesArticles/", null=True, blank=True)
    prixUnitaire = models.DecimalField(max_digits=10, decimal_places=2)
    dateAjout = models.DateTimeField(auto_now_add=True)
    dateModification = models.DateTimeField(null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering=['-dateAjout']

    def controleNom(self):
        if self.titre.replace(".", "", 1).replace(",", "", 1).replace(";", "", 1).isdigit():

            raise  ValidationError ("Le nom du produit ne doit pas un nombre. Plutôt un caractère !!")
        else:
            return self.nom



    def __str__(self):
        return f"L'article {self.nom} a {self.stock} stock"

    def mise_a_jour_disponibilite(self):
        if self.stock <= 0:
            self.disponible = False

    def save(self, *args, **kwargs):
        if self.pk is not None:  # Si l'article existe déjà (modification)
            self.dateModification = timezone.now()
        else:
            self.dateModification =None
        self.full_clean()
        super().save(*args, **kwargs)


phone_validateur = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Le numéro doit être au format international (+123456789)"
)

#class Client : celui qui va faire les achats 
class Client(models.Model):
    nomClient = models.CharField(max_length=128, null=False)
    adresse = models.TextField(null=True, blank=True)
    telephone = models.CharField(validators=[phone_validateur], unique=True, null=True, blank=True)
    dateInscription = models.DateTimeField(auto_now_add=True)




#classe Panier : un ensemble d'achats d'un client spécifique à un moment spécifique(date)
class Panier(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="panier")
    dateCreation = models.DateTimeField(auto_now_add=True)
    #dateModification = models.DateTimeField(null=True)
    valide = models.BooleanField(default=False)
    totalAchat =models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)

    def calculeTotal (self):
        self.totalAchat=0
        for achat in self.achatClient.all():
            self.totalAchat += achat.quantite * achat.article.prixUnitaire
            self.save()
        return self.totalAchat


    def __str__(self):
        return f"Panier de {self.client.nomClient }- crée le {self.dateCreation} - {'Validé' if self.valide else 'En cours'} et total à payer est {self.totalAchat}"





#classe Achat : composition de panier
class Achat(models.Model):
    #client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="achatClient")
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name="achatClient")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="achat")
    dateCommande = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveBigIntegerField(default=1)
    prixAchat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:

        ordering = ["dateCommande"]


    def __str__(self):
        return f"{self.panier.client.nomClient} a acheté {self.quantite} de {self.article.nom} le {self.dateCommande} et le prix de cet achat est {self.prixAchat}"


    def save(self, *args, **kwargs):
        if self.article and self.quantite:
        #Calcule le prix total de l'achat en fonction du prix unitaire de l'article.
            self.prixAchat = self.quantite * self.article.prixUnitaire
        super().save(*args, **kwargs)




"""
class ModePaiement(models.Model):
    type = models.CharField()

#class Facture
class Facture(models.Model):

    panier = models.ForeignKey(Panier, related_name="facture", on_delete=models.CASCADE)
    numero = random.randint(0, 9999)
    prixTotalAchat = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.BooleanField(default=False)
    dateFacture = models.DateTimeField(auto_now_add=True)

"""