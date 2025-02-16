
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .forms import CategorieForm, ArticleForm, ArticleFormM, ClientForm, PanierForm, TransactionForm

from .models import Categorie, Article, Client, Panier, Achat,Transactions
from  django.db.models import Count
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from reportlab.pdfgen import canvas




from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
import  os


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



# LA VUE POUR AFFICHER LES CATEGORIE

def listeCategorie(request):
    categories = Categorie.objects.annotate(totalArticles=Count('article')).order_by('-dateAjout')
    totalCategorie = categories.count()

    context = {"categories": categories, 'totalCategorie': totalCategorie}
    if not categories.exists():
        message = "Aucun produit n'est enregistré"
        totalCategorie = 0

        return render(request, 'listeCategorie.html', {"message": message}, 'totalCategorie', totalCategorie)

    return render(request, 'listeCategorie.html', context)


# LA VUE POUR AFFICHER LES  ARTICLES POUR UNE CATEGORIE
def categorieArticle(request, idCategorie):
    # categorie = Categorie.objects.filter(id =idCategorie)
    categorie = get_object_or_404(Categorie, id=idCategorie)
    categorieArticles = Article.objects.filter(categorie=categorie)
    totalArticle = categorieArticles.count()

    context = {"categorieArticles": categorieArticles, "categorie": categorie, 'totalArticle': totalArticle}
    if not categorieArticles.exists():
        message = "Aucune article n'est enregistré"
        totalArticle = 0

        return render(request, "categorieArticle.html", {"message": message, 'totalArticle': totalArticle})

    return render(request, "categorieArticle.html", context)


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

            messages.success(request, f" Catégorie ' {categorie.titre} ' a été  mis à jour  avec succès !")
            # return redirect('listeCategorie', idCate = categorie.id) # Redirection vers la page de liste des catégories
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
    return render(request, 'modifierCategorie.html', {'formCategorie': formCategorie, 'categorie': categorie})


# LA VUE POUR SUPPRIMER UNE CATEGORIE
def supprimerCateegorie(request, id):
    if request.method == 'GET':
        categorie = get_object_or_404(Categorie, id=id)
        categorie.delete()
        messages.success(request, f"{categorie.titre} a été supprimé avec succès")
        return redirect('listeCategorie')
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
    total = articles.count()
    paniers = Panier.objects.filter(valide=False)

    context = {"articles": articles, 'total':total, 'paniers':paniers,}


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

def ajoutStock(request, idArticle):
    # Récuperation de la ligne dans la table catégorie
    article = get_object_or_404(Article, id=idArticle)

    if request.method == "POST":

        formArticle = ArticleFormM(request.POST)

        if formArticle.is_valid():


            article.stock = formArticle.cleaned_data['stock']

            article.save()
            messages.success(request, f"Quantité {article.stock} est ajoutée à {article.nom} !!")
            return redirect('articles')  # Redirection vers la page de liste des produits
        else:
            for field, errors in formArticle.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        formArticle = ArticleFormM()
    return render(request, 'modifierArticle.html', {'formArticle': formArticle, 'article': article})


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
        return redirect('articles')
    else:
        return HttpResponse("Méthode non autorisée", status=405)




# LA VUE POUR AJOUTER UN NOUVEAU CLIENT
def ajoutClient(request):
    if request.method == 'POST':

        formClient = ClientForm(request.POST)

        if formClient.is_valid():
            try:

                nomClient  = formClient.cleaned_data['nomClient']
                adresse = formClient.cleaned_data['adresse']
                tel = formClient.cleaned_data['telephone']

                client = Client(nomClient=nomClient, adresse=adresse, telephone=tel)
                client.full_clean()
                client.save()
                messages.success(request, f"Client {client.nomClient} ajouté avec succès !")
                return redirect('listeClient')  # Redirection vers la page de liste des catégories
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    formClient.add_error(field, errors)
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
        return redirect('listeClient')  
    else:
        return HttpResponse("Méthode non autorisée", status=405)




def ajoutPanier(request):

    if request.method == "POST":

        """
            quantite = request.POST.get("quantite")
            panier_id = request.POST.get("panierId")

            try:
                panier = Panier.objects.get(id=panier_id)
                quantite = int(quantite)

                # Ajouter l'achat au panier...
                messages.success(request, "Article ajouté au panier avec succès !")
        """

        #data = json.loads(request.body)
        article_id = request.POST.get("article_id")
        panierId = request.POST.get("panierId")
        quantite = int((request.POST.get("quantite")))

        try:
            article = Article.objects.get(id=article_id)

        except Article.DoesNotExist:
            return JsonResponse({"success": False, "message": "Article introuvable"}, status=400)

        #client = Client.objects.get(id=client_id)

        panier = Panier.objects.get(id=panierId, valide=False)

        achat_existant = Achat.objects.filter(panier=panier, article=article).first()

        if achat_existant:
            if achat_existant.quantite + quantite > article.stock:
                return JsonResponse({"success": False, "message": "Stock insuffisant"}, status=400)

            achat_existant.quantite += quantite
            achat_existant.prixAchat = achat_existant.quantite * article.prixUnitaire
            achat_existant.save()
        else:
            if quantite > article.stock:
                return JsonResponse({"success": False, "message": "Stock insuffisant"}, status=400)

            Achat.objects.create(
                panier=panier,
                article=article,
                quantite=quantite,
                prixAchat=quantite * article.prixUnitaire
            )


        article.stock -= quantite
        article.save()

        panier.calculeTotal()

        messages.success(request, f"{article.nom} est bien ajouté au panier {panier.client.nomClient}")
        return redirect('listeArticle')

def panier_view(request):
    clients = Client.objects.all()
    articles = Article.objects.all()
    return render(request, "ajoutPanier.html", {"clients": clients, "articles": articles})

def listePanier(request):
    paniers = Panier.objects.all()
    totalPanier = paniers.count()

    context = {"paniers": paniers, 'totalPanier': totalPanier}
    if not paniers.exists():
        message = "Aucun client n'est enregistré"
        totalPanier = 0

        return render(request, "listePanier.html", {"message": message, 'totalPanier': totalPanier})

    return render(request, "listePanier.html", context)

def listeAchat(request):
    achats = Achat.objects.all()
    totalAchat = achats.count()

    context = {"achats":  achats, 'totalAchat': totalAchat}

    return render(request, "listeAchat.html", context)

#Créer un nouveau panier
def newPanier(request):
    if request.method == "POST":
        formPanier = PanierForm(request.POST)

        if formPanier.is_valid():
            client = formPanier.cleaned_data['client']

            #NouveauNomClient = formPanier.cleaned_data['NouveauNomClien']
            #NouveauTelephoneClient = formPanier.cleaned_data['NouveauTelephoneClient']
            #if NouveauNomClient :
                #Client.objects.C
                #client = Client(nomClient=NouveauNomClient, Telephone=NouveauTelephoneClient)
                #client.save()

            panier = Panier(client=client)
            panier.save()
            messages.success(request, f"Panier de {client.nomClient} est crée avec succès")
            return redirect('listeArticle')

    else:
        formPanier = PanierForm()

    return  render(request, 'newPanier.html', {'formPanier':formPanier})
"""
def listePanierNonValide(request):

    paniers = Panier.objects.filter(valide=False).prefetch_related("achatClient__article")
    context={'paniers':paniers}
    if not paniers.exists():
        context['message'] = "Aucun panier en cours"

    return render(request, 'listeArticle.html', context)
"""
def panierNonValide(request):
    paniersEnCours = Panier.objects.filter(valide=False).prefetch_related("achatClient__article")


    if not paniersEnCours.exists():  # Vérification correcte
        return render(request, 'panierNonvalide.html', {'message': "Aucun panier en cours"})

    return render(request, 'panierNonvalide.html', {'paniersEnCours': paniersEnCours})



def supprimerPanier(request, id):
    if request.method == 'GET':
        panier = get_object_or_404(Panier, id=id)
        panier.delete()
        messages.success(request, f"Suppression du panier a été éffectué avec  avec succès")
        return redirect('listePanier')
    else:
        return HttpResponse("Méthode non autorisée", status=405)



# LA VUE POUR AJOUTER UNE NOUVELLE CATEGORIE
def ajoutTransaction(request):
    if request.method == 'POST':

        formTransaction = TransactionForm(request.POST)

        if formTransaction.is_valid():
            try:

                telephone  = formTransaction.cleaned_data['telephone']
                operateur = formTransaction.cleaned_data['operateur']
                operation = formTransaction.cleaned_data['operation']
                montant = formTransaction.cleaned_data['montant']

                transaction = Transactions(telephone=telephone, operateur=operateur,operation=operation, montant=montant)

                transaction.save()
                messages.success(request, f"Transaction : {operation} de {montant} du client {transaction.telephone} : {transaction.dateTransaction} est ajouté avec succès !")
                return redirect('listeTransaction')  # Redirection vers la page de liste des catégories
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    formTransaction.add_error(field, errors)
        else:
            for field, errors in formTransaction.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        formTransaction = TransactionForm()

    return render(request, 'ajoutTransaction.html', {'formTransaction': formTransaction})

def listeTransaction(request):
    transactions = Transactions.objects.all()
    totalTrans = transactions.count()

    context = {"transactions":  transactions, 'totalTrans': totalTrans}

    return render(request, "listeTransatcion.html", context)




def genererFacture(request, panier_id):
    panier = get_object_or_404(Panier, id=panier_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{panier.id}.pdf"'

    # Définition du document PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Ajouter un logo
    logo_path = os.path.join("static", "images", "logo.png")  # Change selon ton chemin réel
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        p.drawImage(logo, 50, height - 100, width=100, height=100, mask='auto')

    # Titre de la facture
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 80, f"Facture - Panier #{panier.id}")

    # Infos du client
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 120, f"Client : {panier.client.nomClient}")
    p.drawString(50, height - 140, f"Date : {panier.dateCreation.strftime('%d/%m/%Y:%H:%M:%s')}")  # Ajoute la date

    # Récupération des articles
    achats = panier.achatClient.all()
    data = [["Article", "Quantité", "Prix Unitaire (FCFA)", "Total (FCFA)"]]  # En-têtes du tableau
    total = 0

    for achat in achats:
        total_article = achat.quantite * achat.article.prixUnitaire
        data.append([achat.article.nom, achat.quantite, achat.article.prixUnitaire, total_article])
        total += total_article

    # Ajout de la ligne du total
    data.append(["", "", "Total :", total])

    # Création du tableau
    table = Table(data, colWidths=[200, 80, 100, 100])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    # Position du tableau
    table.wrapOn(p, width, height)
    table.drawOn(p, 50, height - 300)

    # Finalisation et enregistrement du fichier PDF
    p.showPage()
    p.save()
    return response

