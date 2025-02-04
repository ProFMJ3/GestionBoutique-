from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from .forms import CategorieForm, ArticleForm

from .models import Categorie, Article


# git config --global core.autocrlf true

# Create your views here

#LA VUE POUR AFFICHER ACCEUIL
def acceuil(request):
    return render(request, 'acceuil.html')

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
            print(form.errors)

    else:
        form = CategorieForm()

    return render(request, 'ajoutCategorie.html', {'form': form})
#LA VUE POUR SUPPRIMER UNE CATEGORIE
def supprimerCateegorie(request, id):
    if request.method == 'GET':
        categorie = get_object_or_404(Categorie, id=id)
        categorie.delete()
        messages.success(request, f"{categorie.titre} a été supprimé avec succès")
        return redirect('listeArticle')  # Assure-toi que 'listeProduit' est bien défini dans urls.py
    else:
        return HttpResponse("Méthode non autorisée", status=405)


#LA VUE POUR AJOUTER UN NOUVEAU ARTICLE

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
            print(formArticle.errors)


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



def modifierArticle(request, id):
    pass