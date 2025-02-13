from django.db import models
from django.utils import  timezone
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.core.validators import  RegexValidator

import uuid
import re

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

    def clean(self):
        """ Vérifie que le titre n'est pas un nombre, même avec des séparateurs. """
        self.titre = self.titre.strip()

        # Supprime tous les séparateurs (.,;: et espaces) pour ne garder que les caractères
        titre_sans_separateurs = re.sub(r'[.,;:\s]', '', self.titre)

        # Vérifie si après suppression des séparateurs, il ne reste que des chiffres
        if titre_sans_separateurs.isdigit():
            raise ValidationError(
                {"titre": "Le titre ne doit pas être un nombre entier ou décimal. Il doit contenir des lettres."})

        # S'assure que le titre commence par une majuscule
        self.titre = capfirst(self.titre)

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if self.pk:  # Si l'objet est mis à jour
            self.dateModification = timezone.now()
        else:
            self.dateModification = None

        self.full_clean()  # Exécute `clean()` pour valider les données
        super().save(*args, **kwargs)

#Classe Article : composition d'une catégorie
class Article(models.Model):
    nom = models.CharField(max_length=128)
    stock = models.PositiveBigIntegerField(default=1)
    image = models.ImageField(upload_to="imagesArticles/", null=True, blank=True)
    prixUnitaire = models.DecimalField(max_digits=10, decimal_places=2)
    dateAjout = models.DateTimeField(auto_now_add=True)
    dateModification = models.DateTimeField(null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='article')
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering=['-dateAjout']

    def controleNom(self):
        if self.nom.replace(".", "", 1).replace(",", "", 1).replace(";", "", 1).isdigit():

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

    class Meta:
        ordering = ['-dateInscription']


#classe Panier : un ensemble d'achats d'un client spécifique à un moment spécifique(date)
class Panier(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="paniers", null=True,blank=True)
    NouveautNomClient = models.CharField(max_length=128, null=True, blank=True)
    NouveauTelephoneClient =  models.CharField(validators=[phone_validateur], unique=True, null=True, blank=True)
    dateCreation = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False)
    totalAchat = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)

    class Meta:
        ordering = ['-dateCreation']
    #Fonction pour calculer le total des
    def calculeTotal(self):
        """ Calcule et mis à jour le total des achats dU panier """
        total = sum(achat.quantite * achat.article.prixUnitaire for achat in self.achatClient.all())
        self.totalAchat = total  # Stocke le total dans le champ totalAchat
        self.save()  # Enregistre la mise à jour dans la base de données
        return self.totalAchat  # Retourne la valeur mise à jour

    def __str__(self):
        status = "Validé" if self.valide else "En cours"
        return f"Panier de {self.client.nomClient} - {self.dateCreation.strftime('%Y-%m-%d %H:%M')} - {status} - Total : {self.totalAchat}FCFA"






#classe Achat : composition de panier
class Achat(models.Model):
    #client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="achatClient")
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name="achatClient")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="achat")
    dateCommande = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveBigIntegerField(default=1)
    prixAchat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:

        ordering = ["-dateCommande"]


    def __str__(self):
        return f"{self.panier.client.nomClient} a acheté {self.quantite} de {self.article.nom} le {self.dateCommande} et le prix de cet achat est {self.prixAchat}"


    def save(self, *args, **kwargs):
        if self.article and self.quantite:
        #Calcule le prix total de l'achat en fonction du prix unitaire de l'article.
            self.prixAchat = self.quantite * self.article.prixUnitaire
        super().save(*args, **kwargs)


        #Ajout du prix d'achat au total d'achat du panier au panier
        self.panier.calculeTotal()





class Facture(models.Model):
    panier = models.ForeignKey(Panier, related_name="factures", on_delete=models.CASCADE)

    # Numéro unique généré automatiquement
    numero = models.CharField(max_length=36, unique=True, default=uuid.uuid4, editable=False)

    prixTotalAchat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    statut = models.BooleanField(default=False)
    dateFacture = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Facture {self.numero} - {self.panier} - {self.prixTotalAchat}FCFA"



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