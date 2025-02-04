from django.urls import path
from . import views

urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('ajoutCategorie/', views.ajoutCategorie, name='ajoutCategorie'),
    path('ajoutArticle/', views.ajoutArticle, name='ajoutArticle'),
    path('listeArticle/', views.listeArticle, name='listeArticle'),
    path('listeCategorie/', views.listeCategorie, name='listeCategorie'),

    path('supprimerArticle/<int:id>/', views.supprimerArticle, name='supprimerArticle'),
    path('supprimerCategorie/<int:id>/', views.supprimerCateegorie, name='supprimerCategorie'),

]
