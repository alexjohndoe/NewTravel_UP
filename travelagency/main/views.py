from django.shortcuts import render, get_object_or_404
from .models import BlogPost, TourPackage, Driver, Testimonial, Destination,  Booking, CustomUser, TourPackage
from .forms import ContactForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.utils import timezone
from .models import GalleryCategory, GalleryImage

from django.core.mail import send_mail
from django.contrib import messages

from django.templatetags.static import static

from .models import FAQ

from django.views.generic import ListView
from .models import Destination

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'  # Update with your template path
    context_object_name = 'destinations'
    
def home(request):
    context = {
        'featured_tours': TourPackage.objects.filter(is_featured=True)[:3],
        'popular_tours': TourPackage.objects.filter(is_popular=True)[:4],
        'recent_posts': BlogPost.objects.filter(is_published=True).order_by('-published_at')[:3],
        'destinations': Destination.objects.all()[:4],
        'faqs': FAQ.objects.all().order_by('order'),
        #'destinations': Destination.objects.all().order_by('-id')[:4]
        'hero_images': [
            'main/images/hero/hero1.jpg',
            'main/images/hero/hero2.jpg',
            'main/images/hero/hero3.jpg'
        ],
    }
    return render(request, 'main/home.html', context)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Correct booking query
    bookings = Booking.objects.filter(user=request.user).select_related('tour')
    
    # Remove testimonial query if not needed, or use correct relation
    context = {
        'bookings': bookings,
        'user_profile': request.user.userprofile
    }
    return render(request, 'dashboard/dashboard.html', context)

def tour_detail(request, slug):
    tour = get_object_or_404(TourPackage, slug=slug)
    
    # Safely handle missing itinerary
    itinerary = getattr(tour, 'itinerary', '')
    itinerary_lines = itinerary.split('\n') if itinerary else []
    
    return render(request, 'main/tours/detail.html', {
        'tour': tour,
        'itinerary_lines': itinerary_lines
    })

def tour_list(request):
    tours = TourPackage.objects.exclude(slug__exact='')  # Exclude empty slugs
    return render(request, 'main/tours/list.html', {'tours': tours})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send email
        send_mail(
            f'New Message from {name} (Travel Agency Contact Form)',
            f"From: {name} <{email}>\n\n{message}",
            'noreply@yourdomain.com',  # From email
            ['admin@email.net'],       # To email
            fail_silently=False,
        )
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    
    return render(request, 'main/contact.html')

def testimonial_list(request):
    testimonials = Testimonial.objects.filter(approved=True)
    return render(request, 'main/testimonials/list.html', {'testimonials': testimonials})

def blog_list(request):
    # Filter only published posts and order by publication date
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'blog/list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id).order_by('-published_at')[:3]
    return render(request, 'blog/detail.html', {
        'post': post,
        'recent_posts': recent_posts
    })

def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'main/drivers/list.html', {'drivers': drivers})

def search(request):
    query = request.GET.get('q', '')
    results = {
        'tours': TourPackage.objects.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ),
        'blog_posts': BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    }
    return render(request, 'search/results.html', {
        'results': results,
        'query': query
    })

def gallery(request):
    categories = GalleryCategory.objects.prefetch_related('galleryimage_set').all()
    return render(request, 'main/gallery.html', {'categories': categories})

def gallery_category(request, slug):
    category = get_object_or_404(GalleryCategory, slug=slug)
    images = GalleryImage.objects.filter(category=category)
    return render(request, 'main/gallery_category.html', {
        'category': category,
        'images': images
    })

@login_required
def dashboard(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-booking_date')
    testimonials = Testimonial.objects.filter(user=user)
    
    context = {
        'bookings': bookings,
        'testimonials': testimonials,
        'user_profile': user.userprofile
    }
    
    if user.user_type in ['ADMIN', 'STAFF']:
        context['pending_bookings'] = Booking.objects.filter(status='PENDING')
        context['pending_testimonials'] = Testimonial.objects.filter(approved=False)
    
    return render(request, 'dashboard/index.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'dashboard/edit_profile.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send email
        send_mail(
            f'Contact Form Submission from {name}',
            message,
            email,
            ['admin@email.net'],  # Recipient list
            fail_silently=False,
        )
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    
    return render(request, 'main/contact.html')

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    related_tours = destination.tours.all()[:5]  # Get first 5 related tours
    
    return render(request, 'destinations/detail.html', {
        'destination': destination,
        'related_tours': related_tours
    })