from django.urls import path
from . import views

urlpatterns = [

#URL MENANT VERS LA PAGE ACCEUIL #LA VUE POUR AFFICHER ACCEUIL
    path('acceuil/', views.acceuil, name='acceuil'),

    #URL MENANT VERS LE DASHBOARD
    path('dash/', views.dash, name='dash'),

# URL MENANT VERS LE FORMULAIRE D'AJOUT DE CATEGORIE
    path('ajoutCategorie/', views.ajoutCategorie, name='ajoutCategorie'),

# URL MENANT VERS LE FORMULAIRE D'AJOUT DES CLIENTS
    path('ajoutArticle/', views.ajoutArticle, name='ajoutArticle'),
    path('ajoutStock/', views.ajoutStock, name='ajoutStock'),

    path('ajoutClient/', views.ajoutClient, name='ajoutClient'),

#URL MENANT VERS LA PAGE DE LISTE ARTICLE
    path('', views.listeArticle, name='listeArticle'),
    path('articles/', views.articles, name='articles'),

#URL MENANT VERS LA PAGE DE LISTE CATEGORIE
    path('listeCategorie/', views.listeCategorie, name='listeCategorie'),

    #path('categorieArticle/', views.categorieArticle, name='categorieArticle'),

#URL MENANT VERS LA PAGE DE LISTE DES ARTICLES D'UNE CATEGORIE SPECIFIQUE
    path('categorieArticle/<int:idCategorie>/', views.categorieArticle, name='categorieArticle'),

    #URL MENANT VERS LA PAGE DE LISTE CLIENT
    path('listeClient/', views.listeClient, name='listeClient'),

#URL MENANT POUR LA SUPPRESSION
    path('supprimerArticle/<int:id>/', views.supprimerArticle, name='supprimerArticle'),
    path('supprimerCategorie/<int:id>/', views.supprimerCateegorie, name='supprimerCategorie'),
    path('supprimerClient/<int:id>/', views.supprimerClient, name='supprimerClient'),
    path('modifierCategorie/<int:idCate>/', views.modifierCategorie, name='modifierCategorie'),
    path('modifierArticle/<int:idArticle>/', views.modifierArticle, name='modifierArticle'),
    path('modifierClient/<int:idClient>/', views.modifierClient, name='modifierClient'),


    path("ajoutPanier/", views.ajoutPanier, name="ajoutPanier"),
    path("panier_view/", views.panier_view, name="panier_view"),
    path("listePanier/", views.listePanier, name="listePanier"),
    path("listeAchat/", views.listeAchat, name="listeAchat"),

    path("newPanier/", views.newPanier, name="newPanier"),
    path("articleAuPanier/", views.articleAuPanier, name="articleAuPanier"),
    path("panierNonValide/", views.panierNonValide, name="panierNonValide"),

    path('supprimerPanier/<int:id>',views.supprimerPanier, name='supprimerPanier'),


]
