from django.db.models.fields import return_None
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from .forms import CategorieForm, ArticleForm, ArticleFormM, ClientForm

from .models import Categorie, Article, Client, Panier


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
            categorie = Categorie(titre=titre, description=description, image=image)
            categorie.save()
            messages.success(request, "Catégorie ajoutée avec succès !")
            return redirect('listeCategorie')  # Redirection vers la page de liste des catégories
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = CategorieForm()

    return render(request, 'ajoutCategorie.html', {'form': form})
#LA VUE POUR SUPPRIMER UNE CATEGORIE
def supprimerCateegorie(request, id):
    if request.method == 'GET':
        categorie = get_object_or_404(Categorie, id=id)
        categorie.delete()
        messages.success(request, f"{categorie.titre} a été supprimé avec succès")
        return redirect('listeCategorie')  # Assure-toi que 'listeProduit' est bien défini dans urls.py
    else:
        return HttpResponse("Méthode non autorisée", status=405)


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

    context = {"articles": articles}
    if not articles.exists:
        message = "Aucun produit n'est enregistré"

        return render(request, "listeArticle.html", {"message": message})

    return render(request, "listeArticle.html", context)


#LA VUE POUR AFFICHER LES CATEGORIE
def listeCategorie(request):
    categories = Categorie.objects.all()

    context = {"categories": categories}
    if not categories.exists:
        message = "Aucun produit n'est enregistré"

        return render(request, 'listeCategorie.html', {"message": message})

    return render(request, 'listeCategorie.html', context)


#LA VUE POUR SUPPRIMER UN ARTICLE
def supprimerArticle(request, id):
    if request.method == 'GET':
        article = get_object_or_404(Article, id=id)
        article.delete()
        messages.success(request, f"{article.nom} a été supprimé avec succès")
        return redirect('listeArticle')  # Assure-toi que 'listeProduit' est bien défini dans urls.py
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
                categorie.image = request.FILES['image']


            categorie.save()

            messages.success(request,  f" Catégorie ' {categorie.titre} ' a été  mis à jour  avec succès !")
            #return redirect('listeCategorie', idCate = categorie.id )  # Redirection vers la page de liste des catégories

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


#Views pour modifier
def modifierArticle(request, idArticle):
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
            messages.success(request, f"{article.nom} a été modifié avec succès")
            return redirect('listeArticle')  # Redirection vers la page de liste des produits
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
            messages.success(request, f"Client {client.nomClient} ajoutée avec succès !")
            return redirect('acceuil')  # Redirection vers la page de liste des catégories
        else:
            for field, errors in formClient.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        formClient = ClientForm()

    return render(request, 'ajoutClient.html', {'formClient': formClient})