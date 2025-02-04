
from django.contrib import admin
from django.urls import path, include
from  django.conf.urls.static import static
from django.conf import  settings

urlpatterns = [
   #Urls pour l'
    path('', include('GestionProduits.urls')),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # Seulement en mode développement
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
