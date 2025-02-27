from django.urls import path
from . import views
from .views import DestinationListView

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tours/<slug:slug>/', views.tour_detail, name='tour_detail'),
    path('drivers/', views.driver_list, name='driver_list'),
    path('testimonials/', views.testimonial_list, name='testimonial_list'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<slug:slug>/', views.gallery_category, name='gallery_category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/edit-profile/', views.edit_profile, name='edit_profile'),
    path('destinations/', DestinationListView.as_view(), name='destination_list'),
    path('destinations/<slug:slug>/', views.destination_detail, name='destination_detail'),
]