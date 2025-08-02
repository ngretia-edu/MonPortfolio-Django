# portfolio_project/urls.py
# Configuration finale avec API + Interface React

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from portfolio import views

urlpatterns = [
    # Interface d'administration
    path('admin/', admin.site.urls),
    
    # API pour React
    path('api/', include('portfolio.urls')),
    
    # Interface React - Page d'accueil
    path('', views.index, name='index'),
    
    # Catch-all pour React Router (toutes les autres routes)
    re_path(r'^(?!admin|api|static|media).*/$', views.index, name='react-app'),
]

# Configuration pour servir les fichiers média et statiques en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personnalisation de l'interface admin
admin.site.site_header = "Administration Portfolio"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Gestion du Portfolio"