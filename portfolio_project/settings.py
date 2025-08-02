# portfolio_project/settings.py
# Configuration principale de Django pour le portfolio

import os
from pathlib import Path
from decouple import config

# Répertoire de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète - À garder privée en production
SECRET_KEY = config('SECRET_KEY', default='django-insecure-votre-cle-secrete-temporaire')

# Mode debug - Mettre à False en production
DEBUG = config('DEBUG', default=True, cast=bool)

# Hosts autorisés - Ajouter votre domaine en production
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',        # Interface d'administration Django
    'django.contrib.auth',         # Système d'authentification
    'django.contrib.contenttypes', # Framework de types de contenu
    'django.contrib.sessions',     # Framework de sessions
    'django.contrib.messages',     # Framework de messages
    'django.contrib.staticfiles',  # Gestion des fichiers statiques
    'django_filters',
    
    # Applications tierces
    'rest_framework',              # API REST Framework
    'corsheaders',                 # Gestion des CORS pour React
    
    # Applications locales
    'portfolio',                   # Notre application portfolio
]

# Middlewares - Traitent les requêtes/réponses
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',          # CORS pour React
    'django.middleware.security.SecurityMiddleware',  # Sécurité
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',      # Protection CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuration des URLs principales
ROOT_URLCONF = 'portfolio_project.urls'

# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Dossier des templates HTML
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuration WSGI pour le déploiement
WSGI_APPLICATION = 'portfolio_project.wsgi.application'

# Configuration de la base de données SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Fichier de base de données
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuration de l'internationalisation
LANGUAGE_CODE = 'fr-fr'  # Français
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuration des fichiers statiques (CSS, JS, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Pour le déploiement
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Dossier des fichiers statiques de développement
]

# Configuration des fichiers média (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Type de champ de clé primaire par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration de Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Accès libre pour les APIs publiques
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Rendu JSON pour les APIs
    ],
    'PAGE_SIZE': 20  # Pagination par défaut
}

# Configuration CORS pour permettre à React de communiquer avec Django
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Serveur de développement React
    "http://127.0.0.1:3000",
]

# Dans settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,  # Ou la valeur que vous avez déjà
    # ... vos autres configurations REST Framework
}

CORS_ALLOW_CREDENTIALS = True

# En développement, autorise toutes les origines CORS
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True