from django import template
from django.db.models import Sum
from GestionProduits.models import Article

register = template.Library()


@register.simple_tag
def artilesLesPlusPendus():
    articles = Article.objects.annotate(total_quantite=Sum('achat__quantite'),total_ventes=Sum('achat__prixAchat')).filter(total_ventes__gt=0).order_by('-total_ventes')[:10]
    return [(article.nom, article.total_quantite , article.total_ventes ) for article in articles]

