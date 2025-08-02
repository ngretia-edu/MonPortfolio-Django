# portfolio/admin.py
# Configuration de l'interface d'administration Django

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Profile, Competence, Projet, Experience, Contact

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Profile"""
    
    # Champs affichés dans la liste
    list_display = ['nom', 'titre', 'email', 'ville', 'actif', 'modifie_le']
    
    # Champs modifiables directement dans la liste
    list_editable = ['actif']
    
    # Filtres sur le côté
    list_filter = ['actif', 'ville', 'pays', 'cree_le']
    
    # Champ de recherche
    search_fields = ['nom', 'email', 'titre', 'bio']
    
    # Organisation des champs dans le formulaire
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'titre', 'email', 'telephone')
        }),
        ('Localisation', {
            'fields': ('ville', 'pays')
        }),
        ('Description', {
            'fields': ('bio', 'description_longue')
        }),
        ('Fichiers', {
            'fields': ('photo', 'cv')
        }),
        ('Réseaux sociaux', {
            'fields': ('linkedin', 'github', 'twitter', 'website'),
            'classes': ('collapse',)  # Section pliable
        }),
        ('Métadonnées', {
            'fields': ('actif',),
            'classes': ('collapse',)
        })
    )
    
    # Champs en lecture seule
    readonly_fields = ['cree_le', 'modifie_le']
    
    def has_add_permission(self, request):
        """Limite à un seul profil"""
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Competence"""
    
    list_display = ['nom', 'categorie', 'niveau', 'colored_bar', 'ordre', 'actif']
    list_editable = ['niveau', 'ordre', 'actif']
    list_filter = ['categorie', 'actif']
    search_fields = ['nom']
    ordering = ['ordre', 'nom']
    
    # Organisation par onglets
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom', 'categorie', 'niveau')
        }),
        ('Apparence', {
            'fields': ('icone', 'couleur', 'ordre')
        }),
        ('Statut', {
            'fields': ('actif',)
        })
    )
    
    def colored_bar(self, obj):
        """Affiche une barre de progression colorée pour le niveau"""
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0; border-radius: 3px;">'
            '<div style="width: {}%; height: 20px; background-color: {}; border-radius: 3px; text-align: center; color: white; font-size: 12px; line-height: 20px;">'
            '{}%</div></div>',
            obj.niveau, obj.couleur, obj.niveau
        )
    colored_bar.short_description = 'Niveau'
    colored_bar.admin_order_field = 'niveau'

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Projet"""
    
    list_display = ['titre', 'statut', 'featured', 'date_debut', 'vues', 'actif']
    list_editable = ['statut', 'featured', 'actif']
    list_filter = ['statut', 'featured', 'actif', 'date_debut', 'technologies']
    search_fields = ['titre', 'description_courte', 'description_longue']
    date_hierarchy = 'date_debut'  # Navigation par date
    ordering = ['-featured', 'ordre', '-date_debut']
    
    # Relations many-to-many avec widget amélioré
    filter_horizontal = ['technologies']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'description_courte', 'description_longue')
        }),
        ('Images', {
            'fields': ('image_principale', 'image_2', 'image_3')
        }),
        ('Technologies et liens', {
            'fields': ('technologies', 'url_demo', 'url_code', 'url_case_study')
        }),
        ('Dates et statut', {
            'fields': ('statut', 'date_debut', 'date_fin')
        }),
        ('Affichage', {
            'fields': ('featured', 'ordre', 'actif'),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('vues',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['vues', 'cree_le', 'modifie_le']
    
    def get_queryset(self, request):
        """Optimise les requêtes avec prefetch_related"""
        return super().get_queryset(request).prefetch_related('technologies')
    
    # Actions personnalisées
    actions = ['mark_as_featured', 'mark_as_not_featured', 'mark_as_finished']
    
    def mark_as_featured(self, request, queryset):
        """Action pour marquer comme featured"""
        queryset.update(featured=True)
        self.message_user(request, f"{queryset.count()} projet(s) marqué(s) comme mis en avant.")
    mark_as_featured.short_description = "Marquer comme mis en avant"
    
    def mark_as_not_featured(self, request, queryset):
        queryset.update(featured=False)
        self.message_user(request, f"{queryset.count()} projet(s) retiré(s) de la mise en avant.")
    mark_as_not_featured.short_description = "Retirer de la mise en avant"
    
    def mark_as_finished(self, request, queryset):
        queryset.update(statut='termine')
        self.message_user(request, f"{queryset.count()} projet(s) marqué(s) comme terminé(s).")
    mark_as_finished.short_description = "Marquer comme terminé"

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Experience"""
    
    list_display = ['titre', 'entreprise', 'type_experience', 'date_debut', 'est_en_cours_display', 'actif']
    list_editable = ['actif']
    list_filter = ['type_experience', 'actif', 'date_debut']
    search_fields = ['titre', 'entreprise', 'description']
    date_hierarchy = 'date_debut'
    ordering = ['-date_debut']
    
    filter_horizontal = ['competences_acquises']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('type_experience', 'titre', 'entreprise', 'lieu')
        }),
        ('Période', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Compétences', {
            'fields': ('competences_acquises',)
        }),
        ('Affichage', {
            'fields': ('ordre', 'actif'),
            'classes': ('collapse',)
        })
    )
    
    def est_en_cours_display(self, obj):
        """Affiche si l'expérience est en cours"""
        if obj.est_en_cours:
            return format_html('<span style="color: green;">✓ En cours</span>')
        return format_html('<span style="color: red;">✗ Terminée</span>')
    est_en_cours_display.short_description = 'Statut'
    est_en_cours_display.admin_order_field = 'date_fin'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Configuration admin pour le modèle Contact"""
    
    list_display = ['nom', 'email', 'sujet', 'envoye_le', 'lu', 'repondu']
    list_editable = ['lu', 'repondu']
    list_filter = ['lu', 'repondu', 'envoye_le']
    search_fields = ['nom', 'email', 'sujet', 'message']
    date_hierarchy = 'envoye_le'
    ordering = ['-envoye_le']
    
    # Champs en lecture seule (ne pas modifier les messages reçus)
    readonly_fields = ['nom', 'email', 'sujet', 'message', 'envoye_le']
    
    fieldsets = (
        ('Informations du contact', {
            'fields': ('nom', 'email', 'envoye_le')
        }),
        ('Message', {
            'fields': ('sujet', 'message')
        }),
        ('Gestion', {
            'fields': ('lu', 'repondu')
        })
    )
    
    # Actions personnalisées
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        queryset.update(lu=True)
        self.message_user(request, f"{queryset.count()} message(s) marqué(s) comme lu(s).")
    mark_as_read.short_description = "Marquer comme lu"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(lu=False)
        self.message_user(request, f"{queryset.count()} message(s) marqué(s) comme non lu(s).")
    mark_as_unread.short_description = "Marquer comme non lu"
    
    def mark_as_replied(self, request, queryset):
        queryset.update(repondu=True, lu=True)
        self.message_user(request, f"{queryset.count()} message(s) marqué(s) comme répondu(s).")
    mark_as_replied.short_description = "Marquer comme répondu"
    
    def has_add_permission(self, request):
        """Empêche l'ajout manuel de messages de contact"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Empêche la suppression des messages (pour archivage)"""
        return False

# Personnalisation globale de l'admin
admin.site.site_header = "Portfolio - Administration"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Tableau de bord du portfolio"

# Message d'aide personnalisé
admin.site.site_url = "/"  # Lien vers le site
admin.site.enable_nav_sidebar = True  # Sidebar de navigation