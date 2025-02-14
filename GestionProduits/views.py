from itertools import count

from django.db.models.fields import return_None
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from .forms import CategorieForm, ArticleForm, ArticleFormM, ClientForm

from .models import Categorie, Article, Client, Panier
from  django.db.models import Count
from django.core.exceptions import ValidationError


# git config --global core.autocrlf true

# Create your views here

#LA VUE POUR AFFICHER ACCEUIL
def acceuil(request):
    return render(request, 'acceuil.html')

#
def dash(request):
    return render(request, 'dash.html')


#LA VUE POUR AJOUTER UNE NOUVELLE CATEGORIE
def ajoutCategorie(request):

    if request.method == 'POST':

        form = CategorieForm(request.POST, request.FILES)

        if form.is_valid():
            
            titre = form.cleaned_data['titre']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            try:


                #categorie = form.save(commit =False)
                categorie = Categorie(titre=titre, description=description, image=image)
                categorie.full_clean()
                categorie.save()
                messages.success(request, "Catégorie ajoutée avec succès !")
                return redirect('listeCategorie')  # Redirection vers la page de liste des catégories
            except ValidationError as e:
                form.add_error('titre', e.message_dict.get('titre',"Erreur !! Le titre ne doit être pas un nombre"))


    else:
        form = CategorieForm()

    return render(request, 'ajoutCategorie.html', {'form': form})


#LA VUE POUR AJOUTER UNE NOUVELLE ARTICLE

def ajoutArticle(request):
    if request.method == 'POST':
        formArticle = ArticleForm(request.POST, request.FILES)
        if formArticle.is_valid():
            nom = formArticle.cleaned_data['nom']
            prixUnitaire = formArticle.cleaned_data['prixUnitaire']
            categorie = formArticle.cleaned_data['categorie']
            image = formArticle.cleaned_data['image']
            stock = formArticle.cleaned_data['stock']

            article = Article(nom=nom,  stock=stock,  image=image, prixUnitaire=prixUnitaire, categorie=categorie)
            article.save()
            messages.success(request, f"{article.nom} a été Ajouté avec succès")
            return redirect('listeArticle')  # Redirection vers la page de liste des produits
        else:
            for field, errors in formArticle.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")


    else:
        formArticle = ArticleForm()
    return render(request, 'ajoutArticle.html', {'formArticle': formArticle})

#LA VUE POUR AFFICHER LES ARTICLES
def listeArticle(request):
    articles = Article.objects.all()
    total = articles.count()

    context = {"articles": articles, 'total':total}
    if not articles.exists():
        message = "Aucune article n'est enregistré"
        total =0

        return render(request, "listeArticle.html", {"message": message, 'total':total})

    return render(request, "listeArticle.html", context)

def articles(request):
    articles = Article.objects.all()
    total = articles.count()

    context = {"articles": articles, 'total':total}
    if not articles.exists():
        message = "Aucune article n'est enregistré"
        total =0

        return render(request, "articles.html", {"message": message, 'total':total})

    return render(request, "articles.html", context)


#Views pour modifier article
def modifierArticle(request, idArticle):

    #Récuperation de la ligne dans la table catégorie
    article = get_object_or_404(Article, id=idArticle)

    if request.method == "POST":


        formArticle = ArticleFormM(request.POST, request.FILES)

        if formArticle.is_valid():

            article.nom = formArticle.cleaned_data['nom']
            article.prixUnitaire = formArticle.cleaned_data['prixUnitaire']
            article.categorie = formArticle.cleaned_data['categorie']

            #article.image = formArticle.cleaned_data.get('image', article.image)  # Garde l'ancienne image si non modifiée
            article.stock = formArticle.cleaned_data['stock']
            if 'image' in request.FILES:
                article.image = request.FILES['image']

            article.save()
            messages.success(request, f"Mis à jour de l'article {article.nom} !!")
            return redirect('articles')  # Redirection vers la page de liste des produits
        else:
            for field, errors in formArticle.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        formArticle = ArticleFormM(initial={
            'nom': article.nom,
            'prixUnitaire': article.prixUnitaire,
            'categorie': article.categorie,
            'stock': article.stock,
        })
    return render(request, 'modifierArticle.html', {'formArticle': formArticle, 'article':article })


#LA VUE POUR SUPPRIMER UN ARTICLE
def supprimerArticle(request, id):
    if request.method == 'GET':
        article = get_object_or_404(Article, id=id)
        article.delete()
        messages.success(request, f"{article.nom} a été supprimé avec succès")
        return redirect('articles')  # Assure-toi que 'listeProduit' est bien défini dans urls.py
    else:
        return HttpResponse("Méthode non autorisée", status=405)



def categorieArticle(request, idCategorie):

    #categorie = Categorie.objects.filter(id =idCategorie)
    categorie = get_object_or_404(Categorie ,id =idCategorie)
    categorieArticles = Article.objects.filter(categorie=categorie)
    totalArticle = categorieArticles.count()

    context = {"categorieArticles": categorieArticles, "categorie":categorie, 'totalArticle':totalArticle}
    if not categorieArticles.exists():
        message = "Aucune article n'est enregistré"
        totalArticle = 0

        return render(request,  "categorieArticle.html", {"message": message, 'totalArticle':totalArticle})

    return render(request, "categorieArticle.html", context)


#LA VUE POUR AFFICHER LES CATEGORIE

def listeCategorie(request):

    categories = Categorie.objects.annotate(totalArticles = Count('article')).order_by('-dateAjout')
    totalCategorie = categories.count()


    context = {"categories": categories,'totalCategorie':totalCategorie }
    if not categories.exists():
        message = "Aucun produit n'est enregistré"
        totalCategorie = 0

        return render(request, 'listeCategorie.html', {"message": message},'totalCategorie',totalCategorie)

    return render(request, 'listeCategorie.html', context)



#LA VUE POUR SUPPRIMER UNE CATEGORIE
def supprimerCateegorie(request, id):
    if request.method == 'GET':
        categorie = get_object_or_404(Categorie, id=id)
        categorie.delete()
        messages.success(request, f"{categorie.titre} a été supprimé avec succès")
        return redirect('listeCategorie')  # Assure-toi que 'listeProduit' est bien défini dans urls.py
    else:
        return HttpResponse("Méthode non autorisée", status=405)




def modifierCategorie(request, idCate):
    categorie = get_object_or_404(Categorie, id=idCate)

    if request.method == 'POST':

        formCategorie = CategorieForm(request.POST, request.FILES)

        if formCategorie.is_valid():

            categorie.titre = formCategorie.cleaned_data['titre']
            categorie.description = formCategorie.cleaned_data['description']

            if 'image' in request.FILES:
                categorie.save()
    
                messages.success(request,  f" Catégorie ' {categorie.titre} ' a été  mis à jour  avec succès !")
                #return redirect('listeCategorie', idCate = categorie.id)  # Redirection vers la page de liste des catégories
    
                return redirect('listeCategorie')  # Redirection vers la page de liste des catégories

        else:
            for field, errors in formCategorie.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        formCategorie = CategorieForm(initial={
            'titre': categorie.titre,
            'description': categorie.description,
        })
    return render(request, 'modifierCategorie.html', {'formCategorie':formCategorie, 'categorie':categorie})




# LA VUE POUR AJOUTER UNE NOUVELLE CATEGORIE
def ajoutClient(request):
    if request.method == 'POST':

        formClient = ClientForm(request.POST)

        if formClient.is_valid():

            nomClient  = formClient.cleaned_data['nomClient']
            adresse = formClient.cleaned_data['adresse']
            tel = formClient.cleaned_data['telephone']
            client = Client(nomClient=nomClient, adresse=adresse, telephone=tel)
            client.save()
            messages.success(request, f"Client {client.nomClient} ajouté avec succès !")
            return redirect('listeClient')  # Redirection vers la page de liste des catégories
        else:
            for field, errors in formClient.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        formClient = ClientForm()

    return render(request, 'ajoutClient.html', {'formClient': formClient})


#Client 
def listeClient(request):
    clients = Client.objects.all()
    totalClient = clients.count()

    context = {"clients": clients, 'totalClient':totalClient}
    if not clients.exists():
        message = "Aucun client n'est enregistré"
        totalClient =0

        return render(request, "listeClient.html", {"message": message, 'totalClient':totalClient})

    return render(request, "listeClient.html", context)


#Views pour modifier
def modifierClient(request, idClient):

    #Récupération de la ligne dans la table Cleint
    client = get_object_or_404(Client, id=idClient)

    if request.method == "POST":


        formClient = ClientForm(request.POST)

        if formClient.is_valid():

            client.nomClient = formClient.cleaned_data['nomClient']
            client.adresse = formClient.cleaned_data['adresse']
            client.tel = formClient.cleaned_data['telephone']

            client.save()
            messages.success(request, f"Mis à jour du client {client.nomClient}!")
            return redirect('listeClient')  # Redirection vers la page de liste des catégories

        else:
            for field, errors in formClient.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        formClient = ClientForm(initial={
            'nomClient': client.nomClient,
            'adresse': client.adresse,
            'tel': client.telephone,
        })
    return render(request, 'modifierClient.html', {'formClient': formClient, 'client':client})



#LA VUE POUR SUPPRIMER UN client
def supprimerClient(request, id):
    if request.method == 'GET':
        client = get_object_or_404(Client, id=id)
        client.delete()
        messages.success(request, f"{client.nomClient} a été supprimé avec succès")
        return redirect('listeClient')  # Assure-toi que 'listeProduit' est bien défini dans urls.py
    else:
        return HttpResponse("Méthode non autorisée", status=405)


def ajoutPanier(request):
    pass

