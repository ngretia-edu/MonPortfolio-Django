# debug_urls.py
# Script pour diagnostiquer les problèmes d'URLs Django

import os
import sys
import django
from django.conf import settings

# Configuration minimale pour Django
if not settings.configured:
    # Remplacez 'portfolio_project.settings' par le chemin vers vos settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
    django.setup()

def check_urls_recursion():
    """Vérifie les URLs pour détecter les récursions"""
    
    print("=== DIAGNOSTIC DES URLs ===\n")
    
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        print("✅ Resolver principal chargé avec succès")
        print(f"URL patterns: {len(resolver.url_patterns)}")
        
        # Affichage des patterns principaux
        for i, pattern in enumerate(resolver.url_patterns):
            print(f"{i+1}. {pattern.pattern} -> {pattern}")
            
    except Exception as e:
        print(f"❌ Erreur lors du chargement du resolver: {e}")
        return False
    
    return True

def check_error_handlers():
    """Vérifie les gestionnaires d'erreurs personnalisés"""
    
    print("\n=== VÉRIFICATION DES GESTIONNAIRES D'ERREURS ===\n")
    
    try:
        from django.conf.urls import handler404, handler500, handler403, handler400
        
        handlers = {
            'handler400': handler400,
            'handler403': handler403, 
            'handler404': handler404,
            'handler500': handler500,
        }
        
        for name, handler in handlers.items():
            if handler:
                print(f"✅ {name}: {handler}")
            else:
                print(f"➖ {name}: Non défini (utilise le défaut)")
                
    except ImportError as e:
        print(f"❌ Erreur d'import des handlers: {e}")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

def check_views_imports():
    """Vérifie les imports de vues"""
    
    print("\n=== VÉRIFICATION DES IMPORTS DE VUES ===\n")
    
    try:
        from portfolio import views
        print("✅ Import portfolio.views réussi")
        
        # Vérification de la fonction index
        if hasattr(views, 'index'):
            print("✅ Fonction views.index existe")
            
            # Test de la signature
            import inspect
            sig = inspect.signature(views.index)
            print(f"✅ Signature views.index: {sig}")
        else:
            print("❌ Fonction views.index manquante")
            
    except Exception as e:
        print(f"❌ Erreur import portfolio.views: {e}")

def main():
    """Fonction principale de diagnostic"""
    
    print("DIAGNOSTIC DJANGO - PROBLÈME DE RÉCURSION")
    print("=" * 50)
    
    # Vérifications
    check_views_imports()
    check_error_handlers() 
    check_urls_recursion()
    
    print("\n" + "=" * 50)
    print("DIAGNOSTIC TERMINÉ")

if __name__ == "__main__":
    main()