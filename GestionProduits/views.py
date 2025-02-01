from django.shortcuts import render

# Create your views here.

"""
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

"""