from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from .forms import CategorieForm, ArticleForm

from .models import Categorie, Article


# git config --global core.autocrlf true

# Create your views here
def acceuil(request):
    return render(request, 'acceuil.html')


def ajoutCategorie(request):
    if request.method == 'POST':
        forms = CategorieForm(request.POST, request.FILES)
        if forms.is_valid():
            titre = forms.cleaned_data['titre']
            description = forms.cleaned_data['description']
            image = forms.cleaned_data['image']
            categorie = Categorie(titre=titre, description=description, image=image)
            categorie.save()
            return redirect('listeCategorie')  # Redirection vers la page de liste des catégories
        else:
            print(forms.errors)

    else:
        forms = CategorieForm()

    return render(request, 'ajoutCategorie.html', {'forms': forms})



def ajoutArticle(request):
    if request.method == 'POST':
        forms = ArticleForm(request.POST, request.FILES)
        if forms.is_valid():
            nom = forms.cleaned_data['nom']
            prixUnitaire = forms.cleaned_data['prixUnitaire']
            categorie = forms.cleaned_data['categorie']
            image = forms.cleaned_data['image']
            stock = forms.cleaned_data['stock']

            produit = ArticleForm(nom=nom, prixUnitaire=prixUnitaire, categorie=categorie, image=image, stock=stock)
            produit.save()
            return redirect('listeProduit')  # Redirection vers la page de liste des produits

    else:
        forms = ArticleForm()
    return render(request, 'ajoutArticle.html', {'forms': forms})


def listeArticle(request):
    articles = Article.objects.all()

    context = {"articles": articles}
    if not articles.exists:
        message = "Aucun produit n'est enregistré"

        return render(request, "listeArticle.html", {"message": message})

    return render(request, "listeArticle.html", context)


def listeCategorie(request):
    categories = Categorie.objects.all()

    context = {"categories": categories}
    if not categories.exists:
        message = "Aucun produit n'est enregistré"

        return render(request, 'listeCategorie.html', {"message": message})

    return render(request, 'listeCategorie.html', context)


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