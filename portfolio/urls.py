# portfolio/urls.py (dans ton app portfolio)
from django.urls import path
from . import views

urlpatterns = [
    # Page principale
    path('', views.index, name='index'),
    
    # API endpoints
    path('api/portfolio/', views.api_portfolio_data, name='api_portfolio_data'),
    path('api/contact/', views.api_contact, name='api_contact'),
    path('api/project/<int:project_id>/views/', views.increment_project_views, name='increment_project_views'),
]