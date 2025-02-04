from django import forms

from .models import Categorie


class CategorieForm(forms.Form):
    titre = forms.CharField(label="Nom de la catégorie :", max_length=128, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Entrez le nom de la catégorie',

    }))
    description = forms.CharField(label="Description :", required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Entrez une description',
        'rows': 5,
    }))

    image = forms.ImageField(label="Vous pouvez ajouter une image du produit :", required=True,
                             widget=forms.ClearableFileInput(attrs={
                                 'accept': 'image/*',

                             }))



class ArticleForm(forms.Form):
    nom = forms.CharField(label="Nom du produit :", max_length=128, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Entrez le nom du produit',
    }))
    prixUnitaire = forms.DecimalField(label="Prix Unitaire du produit :", initial=0, required=True,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Entrez le prix du produit',
                                    }))

    categorie = forms.ModelChoiceField(label="Selectionnez la categorie :", queryset=Categorie.objects.all())
    image = forms.ImageField(label="Vous pouvez ajouter une image du produit :", required=True,
                             widget=forms.ClearableFileInput(attrs={
                                 'accept': 'image/*',

                             }))
    stock = forms.IntegerField(label="Le stock du Produit  :", initial=0, required=True,
                               widget=forms.NumberInput(attrs={
                                   'placeholder': 'Le nombre de stock disponible'
                               }))


