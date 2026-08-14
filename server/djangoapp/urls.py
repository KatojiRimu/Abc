from django.urls import path
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Auth endpoints
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_request, name='logout'),
    path(route='register', view=views.registration, name='register'),
    
    # Car Makes & Models endpoint
    path(route='get_cars', view=views.get_cars, name='getcars'),
    
    # Dealers endpoints
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='get_dealer/<int:dealer_id>', view=views.get_dealer_details, name='get_dealer_by_id'),
    
    # Reviews & Sentiment endpoints
    path(route='get_reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='get_dealer_reviews'),
    path(route='add_review', view=views.add_review, name='add_review'),
    path(route='analyze/<str:text>', view=views.analyze_review_sentiment, name='analyze_review'),
]
