# portfolio/serializers.py
# Sérialiseurs pour convertir les modèles Django en JSON pour l'API REST

from rest_framework import serializers
from .models import Profile, Competence, Projet, Experience, Contact

class ProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Profile - convertit en JSON"""
    
    # Champs calculés (read-only)
    photo_url = serializers.SerializerMethodField()  # URL complète de la photo
    cv_url = serializers.SerializerMethodField()     # URL complète du CV
    
    class Meta:
        model = Profile
        fields = [
            'id', 'nom', 'titre', 'email', 'telephone',
            'bio', 'description_longue', 'ville', 'pays',
            'photo', 'photo_url', 'cv', 'cv_url',
            'linkedin', 'github', 'twitter', 'website',
            'cree_le', 'modifie_le', 'actif'
        ]
        read_only_fields = ['id', 'cree_le', 'modifie_le']  # Champs non modifiables
    
    def get_photo_url(self, obj):
        """Méthode pour obtenir l'URL complète de la photo"""
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
        return None
    
    def get_cv_url(self, obj):
        """Méthode pour obtenir l'URL complète du CV"""
        if obj.cv:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cv.url)
        return None

class CompetenceSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Competence"""
    
    # Affichage du nom de la catégorie au lieu de la valeur
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    
    class Meta:
        model = Competence
        fields = [
            'id', 'nom', 'categorie', 'categorie_display',
            'niveau', 'icone', 'couleur', 'ordre', 'actif'
        ]
        read_only_fields = ['id']

class CompetenceSimpleSerializer(serializers.ModelSerializer):
    """Sérialiseur simplifié pour les compétences (utilisé dans les projets)"""
    
    class Meta:
        model = Competence
        fields = ['id', 'nom', 'couleur', 'icone']

class ProjetSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Projet"""
    
    # Relations avec d'autres modèles
    technologies = CompetenceSimpleSerializer(many=True, read_only=True)
    
    # Champs calculés
    image_principale_url = serializers.SerializerMethodField()
    image_2_url = serializers.SerializerMethodField()
    image_3_url = serializers.SerializerMethodField()
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    duree_projet = serializers.SerializerMethodField()  # Durée calculée
    
    class Meta:
        model = Projet
        fields = [
            'id', 'titre', 'description_courte', 'description_longue',
            'image_principale', 'image_principale_url',
            'image_2', 'image_2_url', 'image_3', 'image_3_url',
            'technologies', 'url_demo', 'url_code', 'url_case_study',
            'statut', 'statut_display', 'date_debut', 'date_fin',
            'featured', 'ordre', 'vues', 'duree_projet', 'actif'
        ]
        read_only_fields = ['id', 'vues', 'cree_le', 'modifie_le']
    
    def get_image_principale_url(self, obj):
        """URL complète de l'image principale"""
        if obj.image_principale:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_principale.url)
        return None
    
    def get_image_2_url(self, obj):
        """URL complète de l'image 2"""
        if obj.image_2:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_2.url)
        return None
    
    def get_image_3_url(self, obj):
        """URL complète de l'image 3"""
        if obj.image_3:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_3.url)
        return None
    
    def get_duree_projet(self, obj):
        """Calcule la durée du projet en mois"""
        if obj.date_fin:
            delta = obj.date_fin - obj.date_debut
            return round(delta.days / 30)  # Conversion approximative en mois
        return None

class ProjetSimpleSerializer(serializers.ModelSerializer):
    """Sérialiseur simplifié pour l'aperçu des projets (liste)"""
    
    image_principale_url = serializers.SerializerMethodField()
    technologies = CompetenceSimpleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Projet
        fields = [
            'id', 'titre', 'description_courte', 'image_principale_url',
            'technologies', 'featured', 'vues', 'statut'
        ]
    
    def get_image_principale_url(self, obj):
        if obj.image_principale:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_principale.url)
        return None

class ExperienceSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Experience"""
    
    # Relations et champs calculés
    competences_acquises = CompetenceSimpleSerializer(many=True, read_only=True)
    type_display = serializers.CharField(source='get_type_experience_display', read_only=True)
    est_en_cours = serializers.ReadOnlyField()  # Propriété du modèle
    duree = serializers.SerializerMethodField()
    
    class Meta:
        model = Experience
        fields = [
            'id', 'type_experience', 'type_display', 'titre', 'entreprise', 'lieu',
            'date_debut', 'date_fin', 'est_en_cours', 'duree',
            'description', 'competences_acquises', 'ordre', 'actif'
        ]
        read_only_fields = ['id']
    
    def get_duree(self, obj):
        """Calcule la durée de l'expérience"""
        from datetime import date
        
        date_fin = obj.date_fin if obj.date_fin else date.today()
        delta = date_fin - obj.date_debut
        
        # Calcul en mois
        mois = round(delta.days / 30)
        
        if mois < 12:
            return f"{mois} mois"
        else:
            annees = mois // 12
            mois_restants = mois % 12
            if mois_restants == 0:
                return f"{annees} an{'s' if annees > 1 else ''}"
            else:
                return f"{annees} an{'s' if annees > 1 else ''} et {mois_restants} mois"

class ContactSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le modèle Contact"""
    
    class Meta:
        model = Contact
        fields = [
            'id', 'nom', 'email', 'sujet', 'message',
            'envoye_le', 'lu', 'repondu'
        ]
        read_only_fields = ['id', 'envoye_le', 'lu', 'repondu']
    
    def validate_email(self, value):
        """Validation personnalisée de l'email"""
        if not value:
            raise serializers.ValidationError("L'adresse email est requise.")
        return value
    
    def validate_message(self, value):
        """Validation personnalisée du message"""
        if len(value) < 10:
            raise serializers.ValidationError("Le message doit contenir au moins 10 caractères.")
        return value

class ContactCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur spécialisé pour la création de messages de contact"""
    
    class Meta:
        model = Contact
        fields = ['nom', 'email', 'sujet', 'message']
    
    def create(self, validated_data):
        """Méthode personnalisée de création"""
        # Le message est automatiquement marqué comme non lu
        return Contact.objects.create(**validated_data)

# Sérialiseur pour les statistiques du portfolio
class PortfolioStatsSerializer(serializers.Serializer):
    """Sérialiseur pour les statistiques générales du portfolio"""
    
    total_projets = serializers.IntegerField()
    projets_featured = serializers.IntegerField()
    total_competences = serializers.IntegerField()
    total_experiences = serializers.IntegerField()
    messages_non_lus = serializers.IntegerField()
    total_vues_projets = serializers.IntegerField()
    
    # Pas de méta car ce n'est pas basé sur un modèle Django