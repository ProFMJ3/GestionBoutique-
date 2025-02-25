from django import forms
from django.forms.widgets import TextInput

from .models import Categorie, Client, Article
import  re



class CategorieForm(forms.Form):
    titre = forms.CharField(label="Nom de la catégorie :", max_length=128, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Entrez le nom de la catégorie',

    }))
    description = forms.CharField(label="Description :", required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Entrez une description',

        'rows': 5,
    }))

    image = forms.ImageField(label="Vous pouvez ajouter une image du produit :", required=False,
                             widget=forms.ClearableFileInput(attrs={
                                 'accept': 'image/*',

                             }))



class ArticleForm(forms.Form):

    categorie = forms.ModelChoiceField(label="Selectionnez la categorie :", queryset=Categorie.objects.all())


    nom = forms.CharField(label="Nom du produit :", max_length=128, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Entrez le nom du produit',
    }))
    image = forms.ImageField(label="Vous pouvez ajouter une image du produit :", required=False,
                             widget=forms.ClearableFileInput(attrs={
                                 'accept': 'image/*',

                             }))
    prixUnitaire = forms.DecimalField(label="Prix Unitaire du produit :", initial=0, required=True,
                                    widget=forms.NumberInput(attrs={
                                        'placeholder': 'Entrez le prix du produit',
                                    }))


    stock = forms.IntegerField(label="Le stock du Produit  :", initial=0, required=True,
                               widget=forms.NumberInput(attrs={
                                   'placeholder': 'Le nombre de stock disponible'
                               }))



class ArticleFormM(forms.Form):

    categorie = forms.ModelChoiceField(label="Selectionnez la categorie :", queryset=Categorie.objects.all())


    nom = forms.CharField(label="Nom du produit :", max_length=128, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Entrez le nom du produit',
    }))
    image = forms.ImageField(label="Vous pouvez ajouter une image du produit :", required=False,
                             widget=forms.ClearableFileInput(attrs={
                                 'accept': 'image/*',

                             }))
    prixUnitaire = forms.DecimalField(label="Prix Unitaire du produit :", initial=0, required=True,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'Entrez le prix du produit',
                                    }))


    stock = forms.IntegerField(label="Le stock du Produit  :", initial=0, required=True,
                               widget=forms.NumberInput(attrs={
                                   'placeholder': 'Le nombre de stock disponible'
                               }))



class ClientForm(forms.Form):
        nomClient = forms.CharField(label="Nom du client :", max_length=128, required=True,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Ex : Jules FOLLYKOE',
                                    'class': 'form-control'

                                }))
        telephone = forms.CharField(label="Numéro de téléphone du client(optionnel) :", required=False, widget=forms.TextInput(attrs={
            'placeholder': 'Ex : +22879405199',
            'class':'form-control',
        }))

        adresse = forms.CharField(label="Domicile du Client(optionnel) :", required=False,
                                 widget=TextInput(attrs={
                                     'placeholder':'EX : Agoe Fiovi',
                                     'class': 'form-control',


                                 }))


class PanierForm(forms.Form):

    client = forms.ModelChoiceField(label="Selectionnez le client", required=False, queryset = Client.objects.all())
    NouveauNomClient = forms.CharField(label="Entrez le nom du client s'il n'existe pas(Optionnel) ", required=False, widget=forms.TextInput(attrs={
                                   'placeholder': "Ce champ sera remplir a cas où le nom du client dans la liste"

                               }))
    #NouveauTelephoneClient = forms.CharField(label="Entrez le contact du nouveau client (Optionnel) ",  required= False, widget= forms.TextInput(attrs={
                               #    'placeholder': 'Ex : +22879405199 .Ce champ peut être rempli quand celui du nom est rempli',

                               #}))







class TransactionForm(forms.Form):
    operateur_Choix = (
        ('Moov', 'Moov'),
        ('Yas', 'Yas'),
    )
    operation_Choix = (
        ('Retrait', 'Retrait'),
        ('Dépot', 'Dépot'),
    )

    #client = forms.ModelChoiceField(label="Sélectionnez le client :", required=False, queryset=Client.objects.all(),
                               #widget=forms.Select(attrs={
                                  # 'placeholder': 'Ex : +22879405199',
                                  # 'class': 'form-control',
                               #}))

    telephone = forms.CharField(label="Numéro de téléphone du client :", required=False,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Ex : +22879405199',
                                   'class': 'form-control',
                               }))
    operateur = forms.ChoiceField(choices=operateur_Choix,required=True,
                                widget=forms.Select(attrs={
                                    'class': 'form-select',
                                }))
    operation = forms.ChoiceField(choices=operation_Choix, required=True,
                                widget=forms.Select(attrs={
                                    'class': 'form-select',
                                }))

    montant = forms.DecimalField(label="Montant :", required=False,
                                widget=forms.NumberInput(attrs={
                                    'placeholder': 'Ex : 100000',
                                    'class': 'form-control',
                                }))

class AchatForm(forms.Form):
    article = forms.ModelChoiceField(label="Selectionnez l'article", required=True, queryset=Article.objects.all(), widget=forms.Select(attrs={
                'class':'form-control',})
    )

    quantite = forms.IntegerField(label="La quantité ",
                                                 required=True, widget=forms.TextInput(attrs={
                'class':'form-control',
            }))

    def clean_quantite(self):
        quantite = self.cleaned_data.get('quantite')
        article = self.cleaned_data.get('article')

        if article and quantite:
            # Vérifiez si la quantité dépasse le stock disponible
            if quantite > article.stock:
                raise forms.ValidationError(
                    f"Attention ❌🚫!! Le stock est insuffissant pour cet article. Stock disponible : {article.stock}.")

        return quantite






