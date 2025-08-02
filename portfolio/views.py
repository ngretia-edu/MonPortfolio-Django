# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Competence, Projet, Experience, Contact
import json

def index(request):
    """Vue principale pour afficher la page d'accueil"""
    return render(request, 'index.html')

def api_portfolio_data(request):
    """API pour récupérer toutes les données du portfolio"""
    try:
        # Récupérer le profil principal (le premier actif)
        profile = Profile.objects.filter(actif=True).first()
        
        # Récupérer les compétences par catégorie
        competences = Competence.objects.filter(actif=True).order_by('ordre', 'nom')
        
        # Récupérer les projets actifs, avec les featured en premier
        projets = Projet.objects.filter(actif=True).order_by('-featured', 'ordre', '-date_debut')
        
        # Récupérer les expériences actives, les plus récentes en premier
        experiences = Experience.objects.filter(actif=True).order_by('-date_debut')
        
        # Préparer les données pour JSON
        data = {
            'success': True,
            'profile': None,
            'competences': [],
            'projets': [],
            'experiences': []
        }
        
        # Sérialiser le profil
        if profile:
            data['profile'] = {
                'nom': profile.nom,
                'titre': profile.titre,
                'email': profile.email,
                'telephone': profile.telephone,
                'bio': profile.bio,
                'description_longue': profile.description_longue,
                'ville': profile.ville,
                'pays': profile.pays,
                'photo': profile.photo.url if profile.photo else None,
                'cv': profile.cv.url if profile.cv else None,
                'linkedin': profile.linkedin,
                'github': profile.github,
                'twitter': profile.twitter,
                'website': profile.website,
            }
        
        # Sérialiser les compétences
        for competence in competences:
            data['competences'].append({
                'id': competence.id,
                'nom': competence.nom,
                'categorie': competence.categorie,
                'categorie_display': competence.get_categorie_display(),
                'niveau': competence.niveau,
                'icone': competence.icone,
                'couleur': competence.couleur,
                'ordre': competence.ordre
            })
        
        # Sérialiser les projets
        for projet in projets:
            data['projets'].append({
                'id': projet.id,
                'titre': projet.titre,
                'description_courte': projet.description_courte,
                'description_longue': projet.description_longue,
                'image_principale': projet.image_principale.url if projet.image_principale else None,
                'image_2': projet.image_2.url if projet.image_2 else None,
                'image_3': projet.image_3.url if projet.image_3 else None,
                'technologies': [{'nom': tech.nom, 'couleur': tech.couleur} for tech in projet.technologies.all()],
                'url_demo': projet.url_demo,
                'url_code': projet.url_code,
                'url_case_study': projet.url_case_study,
                'statut': projet.statut,
                'statut_display': projet.get_statut_display(),
                'date_debut': projet.date_debut.isoformat() if projet.date_debut else None,
                'date_fin': projet.date_fin.isoformat() if projet.date_fin else None,
                'featured': projet.featured,
                'vues': projet.vues
            })
        
        # Sérialiser les expériences
        for experience in experiences:
            data['experiences'].append({
                'id': experience.id,
                'type_experience': experience.type_experience,
                'type_display': experience.get_type_experience_display(),
                'titre': experience.titre,
                'entreprise': experience.entreprise,
                'lieu': experience.lieu,
                'date_debut': experience.date_debut.isoformat() if experience.date_debut else None,
                'date_fin': experience.date_fin.isoformat() if experience.date_fin else None,
                'est_en_cours': experience.est_en_cours,
                'description': experience.description,
                'competences_acquises': [comp.nom for comp in experience.competences_acquises.all()]
            })
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur lors du chargement des données: {str(e)}'
        }, status=500)

@csrf_exempt
def api_contact(request):
    """API pour traiter les messages de contact"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            contact = Contact.objects.create(
                nom=data.get('nom'),
                email=data.get('email'),
                sujet=data.get('sujet'),
                message=data.get('message')
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Message envoyé avec succès!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Erreur lors de l\'envoi: {str(e)}'
            }, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def increment_project_views(request, project_id):
    """Incrémenter le nombre de vues d'un projet"""
    try:
        projet = Projet.objects.get(id=project_id, actif=True)
        projet.increment_views()
        return JsonResponse({'success': True, 'views': projet.vues})
    except Projet.DoesNotExist:
        return JsonResponse({'error': 'Projet non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)