
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from reportlab.lib.colors import black
from django.db.models import Sum
import matplotlib.pyplot as plt
import io
import urllib
import base64
from datetime import  timedelta
from  django.utils import  timezone

from .forms import CategorieForm, ArticleForm, ArticleFormM, ClientForm, PanierForm, TransactionForm

from .models import Categorie, Article, Client, Panier, Achat,Transactions, Facture
from  django.db.models import Count
from django.core.exceptions import ValidationError

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

import os
import datetime

# git config --global core.autocrlf true

# Create your views here

#LA VUE POUR AFFICHER ACCEUIL
def acceuil(request):
    return render(request, 'acceuil.html')

#La vue du dashboard
def dashboard(request):
    totalArticle = Article.objects.count()
    totalAchat = Achat.objects.count()
    paniers = Panier.objects.filter(valide=True)
    totalPV = paniers.count()
    totalPN = Panier.objects.filter(valide=False).count()

    # Optimisation de la somme des ventes
    totalVente = paniers.aggregate(Sum('totalAchat'))['totalAchat__sum'] or 0

    """
        Vue qui affiche le tableau de bord avec la courbe des ventes et les ventes récentes.
        
        
        """

    ventes = ventesParPeriode()
    #articles_ventes = artilesLesPlusPendus()

    context = {
        "totalArticle": totalArticle,
        "totalVente": totalVente,
        "totalPV": totalPV,
        "totalPN": totalPN,
        'totalAchat': totalAchat,
        'ventes_aujourdhui': ventes['ventes_aujourdhui'],
        'ventes_mois_precedent': ventes['ventes_mois_precedent'],
        'ventes_semaine_derniere': ventes['ventes_semaine_derniere'],
        #'articles_ventes': articles_ventes,



    }



    return render(request, 'dash.html', context)



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
            try:

                nom = formArticle.cleaned_data['nom']
                prixUnitaire = formArticle.cleaned_data['prixUnitaire']
                categorie = formArticle.cleaned_data['categorie']
                image = formArticle.cleaned_data['image']
                stock = formArticle.cleaned_data['stock']

                article = Article(nom=nom,  stock=stock,  image=image, prixUnitaire=prixUnitaire, categorie=categorie)
                article.save()

                messages.success(request, f"{article.nom} a été Ajouté avec succès")
                return redirect('listeArticle')  # Redirection vers la page de liste des produits

            except ValidationError as e:
                # Gestion des erreurs de validation

                for field, errors in e.message_dict.items():
                    formArticle.add_error(field, errors)
                #messages.error(request, "Erreur lors de l'ajout d'article, veuillez vérifier les informations.")

            except Exception as e:
                # Gestion des erreurs inattendues
                messages.error(request, f"Une erreur inattendue s'est produite: {str(e)}")

        else:
            messages.error(request, f"Une erreur s'est produite!! Veuillez vérifier le formulaire .")

    else:
        formArticle = ArticleForm()
    return render(request, 'ajoutArticle.html', {'formArticle': formArticle})

#LA VUE POUR AFFICHER LES ARTICLES
def listeArticle(request):
    articles = Article.objects.all()
    #total = articles.count()
    #paniers = Panier.objects.filter(valide=False)

    context = {"articles": articles}


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

"""
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

"""

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
            #return JsonResponse({"success": False, "message": "Article introuvable"}, status=400)
            messages.error(request, "Article est introuvale !!")

            # client = Client.objects.get(id=client_id)
        if not panierId:
            messages.error(request, "Veuillez selectionnez le panier avant de cliquer le boutton Panier +!!")
            return  redirect("articlePanier")
        try:
            panier = get_object_or_404(Panier, id=int(panierId), valide=False)
        except ValueError:
            messages.error(request, "ID de panier invalide.")
            return redirect('articlePanier')

        #panier = Panier.objects.get(id=panierId, valide=False)


        achat_existant = Achat.objects.filter(panier=panier, article=article).first()

        if achat_existant:
            if achat_existant.quantite + quantite > article.stock:
                #return JsonResponse({"success": False, "message": "Stock insuffisant"}, status=400)
                messages.error(request,
                               f"Le stock est insuffisant. Veuillez ajouter du stock !! Ou soit diminué la quantité d'achat")
            else:


                achat_existant.quantite += quantite
                achat_existant.prixAchat = achat_existant.quantite * article.prixUnitaire
                achat_existant.save()

                article.stock -= quantite
                article.save()
                panier.calculeTotal()
                messages.success(request, f"La quantité d'achat de {article.nom} est bien augmenté au panier {panier.numero}")

        else:
            if quantite > article.stock:
               #return JsonResponse({"success": False, "message": "Stock insuffisant"}, status=400)
                messages.error(request, f"Le stock est insuffisant. Veuillez ajouter du stock !! Ou soit diminué la quantité d'achat")
            else:
                Achat.objects.create(
                    panier=panier,
                    article=article,
                    quantite=quantite,
                    prixAchat=quantite * article.prixUnitaire
                )


                article.stock -= quantite
                article.save()
                panier.calculeTotal()
                messages.success(request, f"{article.nom} est bien ajouté au panier {panier.numero}")




        return redirect('articlePanier')

def panier_view(request):
    clients = Client.objects.all()
    articles = Article.objects.all()
    return render(request, "ajoutPanier.html", {"clients": clients, "articles": articles})

def listePanier(request):
    paniers = Panier.objects.filter(valide=True)
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
            date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            NouveauNomClient = formPanier.cleaned_data['NouveauNomClient']
            NouveauTelephoneClient = formPanier.cleaned_data['NouveauTelephoneClient']
            if client :
                panier = Panier(client=client, dateCreation=date)
                panier.save()
                messages.success(request, f"Panier de {client.nomClient} est crée avec succès")


            elif NouveauNomClient and NouveauTelephoneClient :

                client = Client(nomClient=NouveauNomClient, telephone=NouveauTelephoneClient)
                client.save()

                panier = Panier(client=client, dateCreation=date)
                panier.save()
                messages.success(request, f"Panier de {client.nomClient} est crée avec succès")


            else:
                panier = Panier(dateCreation=date)
                panier.save()
                messages.success(request, f"Panier de numéro {panier.numero} est crée avec succès")



            return redirect('articlePanier')

            #return redirect('listeArticle')

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


#Vue menant vers la page permettant d'ajouter les articles au panier
def articlePanier(request):

    paniers = Panier.objects.filter(valide=False)
    articles = Article.objects.all()
    context = {'articles': articles, 'paniers': paniers, }
    return render(request, 'articlePanier.html', context)

def panierNonValide(request):
    paniersEnCours = Panier.objects.filter(valide=False).prefetch_related("achatClient__article")


    if not paniersEnCours.exists():  # Vérification correcte
        return render(request, 'panierNonvalide.html', {'message': "Aucun panier en cours"})

    return render(request, 'panierNonvalide.html', {'paniersEnCours': paniersEnCours})

def validerPanier(request, id):
    panier = get_object_or_404(Panier, id=id)
    if request.method== "POST":
        valide = request.POST.get("valide")
        #panier = Panier.objects.update(id =id, valide=valide)
        panier.valide = valide
        panier.save()

        return redirect('listePanier')


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

def modifierTransation(request, id):
    pass


def supprimerTransation(request, id):
    if request.method == 'GET':
        trans = get_object_or_404(Transactions, id=id)
        trans.delete()
        messages.success(request, f"Suppression du transation a été éffectué avec  avec succès")
        return redirect('listeTransaction')
    else:
        return HttpResponse("Méthode non autorisée", status=405)





def genererFacture(request, panier_id):
    panier = get_object_or_404(Panier, id=panier_id)
    facture = Facture(panier=panier)

    response = HttpResponse(content_type='application/pdf')
    #numero_facture = f"FACT-{panier.dateCreation.strftime('%Y%m%d')}-{panier.id:05d}"
    numero_facture = f"FACT-{panier.numero}"
    response['Content-Disposition'] = f'attachment; filename="{numero_facture}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Ajout du logo


    #logo_path = os.path.join(settings.BASE_DIR, "static", "img", "log.png")
    #logo_path = os.path.join("static", "img", "log.png")

    logo_path = os.path.abspath(os.path.join("GestionProduits", "static", "img", "log.png"))
    #print("Chemin du logo :", logo_path)
    #print("Le fichier existe :", os.path.exists(logo_path))

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=100, height=50)  # Ajuste la taille du logo


        nom_entreprise = Paragraph('<font color="white"><b>Raïssa Shop</b></font>', styles['Title'])

        # Informations de contact à droite
        info_contact = Paragraph(
            '<font color="white"><b>Adresse : Agoe Nyivé non loin d\'Institut SIVOP<br/></b></font>'
            '<font color="white"><b>Téléphone : +228 90326791</b></font>',
            styles['Normal']
        )

        # Créer un tableau avec 3 colonnes pour aligner le tout à droite
        header_table = Table([[logo, nom_entreprise, info_contact]], colWidths=[70, 150, 280])

        # Appliquer un style pour aligner au centre verticalement
        header_table.setStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.blue),  # Fond bleu
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrer verticalement
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Logo aligné à droite
            ('ALIGN', (2, 0), (2, 0), 'LEFT'),  # Nom aligné à gauche après le logo
            ('ALIGN', (3, 0), (3, 0), 'RIGHT'),  # Contact aligné à droite
            ('TEXTCOLOR', (1, 0), (1, 0), colors.whitesmoke),  # Texte en blanc
            #('LEFTPADDING', (0, 0), (-1, -1), 0),  # Supprime l’espace à gauche
            #('RIGHTPADDING', (0, 0), (-1, -1), 0),  # Supprime l’espace à droite
        ])

        elements.append(header_table)  # Ajoute le tableau au document
        elements.append(Spacer(1, 10))
    # Titre de la facture
    #styles['Title'].alignment = 0
    elements.append(Paragraph(f"<b>{numero_facture}</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Infos du vendeur
    #elements.append(Paragraph("<b>Gérant:Tata Raïssa,</b> Adresse :Agoe Nyivé non loin d'Institut SIVOP, Téléphone:+228 90326791", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Infos du client
    if panier.client:  # Vérifie que le client existe
        if panier.client.nomClient:
            elements.append(Paragraph(f"<b>Client :</b> {panier.client.nomClient} -- Tel : {panier.client.telephone}",
                                      styles['Normal']))
        else:
            elements.append(Paragraph("<b>Client :</b> Information manquante", styles['Normal']))
    else:
        elements.append(Paragraph("<b>Client :</b> Non spécifié", styles['Normal']))

    elements.append(Paragraph(f"<b>Date et Heure :</b> {panier.dateCreation.strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Récupération des articles
    achats = panier.achatClient.all()
    data = [["Article", "Quantité", "Prix Unitaire (FCFA)", "Total (FCFA)"]]
    total = 0

    for achat in achats:
        total_article = achat.quantite * achat.article.prixUnitaire
        data.append([achat.article.nom, achat.quantite, achat.article.prixUnitaire, total_article])
        total += total_article

    #data.append(["", "", "Total :", total])


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
    elements.append(table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f'<font color="black"> <b> Total Achat :  {total} CFFA </b> </font>',styles['Title']))
    elements.append(Spacer(1,20))

    # Signature électronique
    elements.append(Paragraph("Signature du vendeur: ________________________", styles['Normal']))

    doc.build(elements)
    return response





def ajoutStock(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":

        stock = int(request.POST.get("Stock"))

        article.stock = article.stock + stock
        article.save()

        messages.success(request, f"Le stock de {article.nom} est augmenté à {stock}")

        return redirect('listeArticle')
    else:
        messages.error(request, "Une erreur s'est survenue, le stock n'a pu ajouter . Réessayez plus tard !!")



def modifierAchat(request):
    pass

def supprimerAchat(request, id):

    if request.method == 'GET':
        achat = get_object_or_404(Achat, id=id)
        achat.delete()
        messages.success(request, f"Suppression de l'achat a été éffectué avec  avec succès")
        return redirect('listePanier')
    else:
        return HttpResponse("Méthode non autorisée", status=405)




def ventesParPeriode():
    today = timezone.now()

    # Total des ventes aujourd'hui
    ventes_aujourdhui = \
    Panier.objects.filter(dateCreation__date=today.date(), valide=True).aggregate(Sum('totalAchat'))[
        'totalAchat__sum'] or 0

    # Ventes du mois dernier
    debut_mois_precedent = today.replace(day=1) - timedelta(days=1)
    debut_mois_precedent = debut_mois_precedent.replace(day=1)
    ventes_mois_precedent = \
    Panier.objects.filter(dateCreation__gte=debut_mois_precedent, dateCreation__lt=today.replace(day=1),
                          valide=True).aggregate(Sum('totalAchat'))['totalAchat__sum'] or 0

    # Ventes de la semaine dernière
    debut_semaine_derniere = today - timedelta(days=today.weekday() + 7)  # Lundi de la semaine dernière
    fin_semaine_derniere = debut_semaine_derniere + timedelta(days=6)  # Dimanche de la semaine dernière
    ventes_semaine_derniere = \
    Panier.objects.filter(dateCreation__gte=debut_semaine_derniere, dateCreation__lte=fin_semaine_derniere,
                          valide=True).aggregate(Sum('totalAchat'))['totalAchat__sum'] or 0



    return {
        'ventes_aujourdhui': ventes_aujourdhui,
        'ventes_mois_precedent': ventes_mois_precedent,
        'ventes_semaine_derniere': ventes_semaine_derniere,

    }



def artilesLesPlusPendus():
    articles = Article.objects.annotate(total_ventes=Sum('achat__prixAchat')).filter(total_ventes__gt=0).order_by('-total_ventes')[:5]
    articles_ventes = [(article.nom, article.total_ventes or 0) for article in articles]
    return articles_ventes