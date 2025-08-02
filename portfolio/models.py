# portfolio/models.py
# Définition des modèles de données pour le portfolio

from django.db import models
from django.core.validators import URLValidator
from django.utils import timezone

class Profile(models.Model):
    """Modèle pour les informations personnelles du portfolio"""
    
    # Informations de base
    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    titre = models.CharField(max_length=200, verbose_name="Titre professionnel", 
                           default="Développeur Full Stack")
    email = models.EmailField(verbose_name="Adresse email")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    
    # Informations détaillées
    bio = models.TextField(verbose_name="Biographie", 
                          help_text="Description courte de votre parcours")
    description_longue = models.TextField(verbose_name="Description détaillée", 
                                        help_text="Description complète de vos compétences")
    
    # Localisation
    ville = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    pays = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    
    # Photo de profil
    photo = models.ImageField(upload_to='profile/', blank=True, null=True,
                             verbose_name="Photo de profil")
    
    # CV téléchargeable
    cv = models.FileField(upload_to='documents/', blank=True, null=True,
                         verbose_name="CV (PDF)")
    
    # Réseaux sociaux
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    github = models.URLField(blank=True, verbose_name="GitHub")
    twitter = models.URLField(blank=True, verbose_name="Twitter")
    website = models.URLField(blank=True, verbose_name="Site web personnel")
    
    # Métadonnées
    cree_le = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    modifie_le = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    actif = models.BooleanField(default=True, verbose_name="Profil actif")
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"
    
    def __str__(self):
        return self.nom

class Competence(models.Model):
    """Modèle pour les compétences techniques"""
    
    CATEGORIES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Base de données'),
        ('devops', 'DevOps'),
        ('design', 'Design'),
        ('ia', 'Intelligence Artificielle'),
        ('autres', 'Autres'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom de la compétence")
    categorie = models.CharField(max_length=20, choices=CATEGORIES, 
                               verbose_name="Catégorie")
    niveau = models.IntegerField(default=50, verbose_name="Niveau (%)",
                               help_text="Niveau de maîtrise en pourcentage (0-100)")
    icone = models.CharField(max_length=100, blank=True, 
                           help_text="Classe CSS pour l'icône (ex: fab fa-python)")
    couleur = models.CharField(max_length=7, default='#007bff',
                             help_text="Couleur en hexadécimal (ex: #FF5733)")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    # Métadonnées
    cree_le = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True, verbose_name="Compétence active")
    
    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
        ordering = ['ordre', 'nom']  # Tri par ordre puis par nom
    
    def __str__(self):
        return f"{self.nom} ({self.get_categorie_display()})"

class Projet(models.Model):
    """Modèle pour les projets du portfolio"""
    
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('pause', 'En pause'),
        ('archive', 'Archivé'),
    ]
    
    # Informations principales
    titre = models.CharField(max_length=200, verbose_name="Titre du projet")
    description_courte = models.CharField(max_length=300, 
                                        verbose_name="Description courte")
    description_longue = models.TextField(verbose_name="Description détaillée")
    
    # Images du projet
    image_principale = models.ImageField(upload_to='projects/', 
                                       verbose_name="Image principale")
    image_2 = models.ImageField(upload_to='projects/', blank=True, null=True,
                              verbose_name="Image secondaire")
    image_3 = models.ImageField(upload_to='projects/', blank=True, null=True,
                              verbose_name="Image tertiaire")
    
    # Technologies utilisées
    technologies = models.ManyToManyField(Competence, 
                                        verbose_name="Technologies utilisées",
                                        help_text="Sélectionnez les compétences utilisées")
    
    # Liens du projet
    url_demo = models.URLField(blank=True, verbose_name="URL de démonstration")
    url_code = models.URLField(blank=True, verbose_name="URL du code source")
    url_case_study = models.URLField(blank=True, verbose_name="Étude de cas")
    
    # Statut et dates
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                            default='termine', verbose_name="Statut")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(blank=True, null=True, verbose_name="Date de fin")
    
    # Métadonnées pour l'affichage
    featured = models.BooleanField(default=False, 
                                 verbose_name="Projet mis en avant")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    vues = models.PositiveIntegerField(default=0, verbose_name="Nombre de vues")
    
    # Métadonnées système
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True, verbose_name="Projet actif")
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-featured', 'ordre', '-date_debut']  # Projets featured en premier
    
    def __str__(self):
        return self.titre
    
    def increment_views(self):
        """Méthode pour incrémenter le nombre de vues"""
        self.vues += 1
        self.save(update_fields=['vues'])

class Experience(models.Model):
    """Modèle pour l'expérience professionnelle et formations"""
    
    TYPES = [
        ('travail', 'Expérience professionnelle'),
        ('formation', 'Formation'),
        ('projet', 'Projet personnel'),
        ('benevolat', 'Bénévolat'),
    ]
    
    type_experience = models.CharField(max_length=20, choices=TYPES, 
                                     verbose_name="Type d'expérience")
    titre = models.CharField(max_length=200, verbose_name="Titre du poste/formation")
    entreprise = models.CharField(max_length=200, verbose_name="Entreprise/École")
    lieu = models.CharField(max_length=100, blank=True, verbose_name="Lieu")
    
    # Dates
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(blank=True, null=True, 
                              verbose_name="Date de fin (laisser vide si en cours)")
    
    # Détails
    description = models.TextField(verbose_name="Description des tâches/apprentissages")
    competences_acquises = models.ManyToManyField(Competence, blank=True,
                                                verbose_name="Compétences acquises")
    
    # Métadonnées
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    cree_le = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True, verbose_name="Expérience active")
    
    class Meta:
        verbose_name = "Expérience"
        verbose_name_plural = "Expériences"
        ordering = ['-date_debut']  # Plus récent en premier
    
    def __str__(self):
        return f"{self.titre} - {self.entreprise}"
    
    @property
    def est_en_cours(self):
        """Propriété pour vérifier si l'expérience est en cours"""
        return self.date_fin is None

class Contact(models.Model):
    """Modèle pour les messages de contact"""
    
    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Adresse email")
    sujet = models.CharField(max_length=200, verbose_name="Sujet du message")
    message = models.TextField(verbose_name="Message")
    
    # Métadonnées
    envoye_le = models.DateTimeField(auto_now_add=True, verbose_name="Envoyé le")
    lu = models.BooleanField(default=False, verbose_name="Message lu")
    repondu = models.BooleanField(default=False, verbose_name="Réponse envoyée")
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-envoye_le']  # Plus récent en premier
    
    def __str__(self):
        return f"{self.nom} - {self.sujet}"