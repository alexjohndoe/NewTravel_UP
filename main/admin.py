from django.contrib import admin

from .models import (
    CustomUser, 
    BlogPost, 
    TourPackage,
    Destination, 
    Driver, 
    Testimonial, 
    GalleryCategory,  # Add this
    GalleryImage,     # Add this
    Booking,          # Add this if needed
    Payment           # Add this if needed
)
from .models import FAQ

# Register your models here.
@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'category', 'date_taken')
    list_filter = ('category',)
    search_fields = ('caption',)

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration', 'is_featured', 'slug')
    list_filter = ('is_featured', 'duration')
    search_fields = ('title', 'overview')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'is_featured')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration')
        }),
        ('Content', {
            'fields': ('overview', 'itinerary', 'featured_image')  # Added itinerary
        }),
    )
    
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at', 'created_at')
    list_filter = ('is_published', 'published_at')
    list_editable = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'featured_image')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Publication', {
            'fields': ('is_published', 'published_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('question', 'answer')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'best_time_to_visit')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'image')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'full_description')
        }),
        ('Details', {
            'fields': ('location', 'best_time_to_visit', 'popular_activities')
        }),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'rating')
    search_fields = ('user_name', 'comment')