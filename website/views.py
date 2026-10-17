from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import (
    NewsArticle, ManifestoItem, ContactMessage,
    CoreValue, KabaleFeature, GalleryImage, KabaleStatistic
)
from .forms import ContactForm


def home(request):
    """Homepage view"""
    # Get featured news articles for homepage display
    featured_articles = NewsArticle.objects.filter(
        is_published=True,
        is_featured=True
    ).order_by('-published_date')[:6]

    # Fall back to all recent articles if no featured ones
    all_articles = NewsArticle.objects.filter(
        is_published=True
    ).order_by('-published_date')[:6]

    # Get manifesto items
    manifesto_items = ManifestoItem.objects.filter(is_active=True).order_by('order')

    # Get core values
    core_values = CoreValue.objects.filter(is_active=True).order_by('order')

    # Get Kabale features
    kabale_features = KabaleFeature.objects.filter(is_active=True).order_by('order')

    # Get hero/about gallery images
    hero_images = GalleryImage.objects.filter(is_active=True, section='hero').order_by('order')
    gallery_images = GalleryImage.objects.filter(is_active=True, section='gallery').order_by('order')[:8]

    context = {
        'featured_articles': featured_articles,
        'all_articles': all_articles,
        'manifesto_items': manifesto_items,
        'core_values': core_values,
        'kabale_features': kabale_features,
        'hero_images': hero_images,
        'gallery_images': gallery_images,
        'news_count': NewsArticle.objects.filter(is_published=True).count(),
    }

    return render(request, 'website/home.html', context)


def article_detail(request, slug):
    """Individual article detail view"""
    article = get_object_or_404(NewsArticle, slug=slug, is_published=True)

    # Get related articles (same category, excluding current)
    related_articles = NewsArticle.objects.filter(
        is_published=True,
        category=article.category
    ).exclude(slug=slug).order_by('-published_date')[:3]

    context = {
        'article': article,
        'related_articles': related_articles,
    }

    return render(request, 'website/article_detail.html', context)


def news_list(request):
    """News listing page with category filter"""
    category = request.GET.get('category', '')
    articles = NewsArticle.objects.filter(is_published=True).order_by('-published_date')

    if category:
        articles = articles.filter(category=category)

    # Pagination
    paginator = Paginator(articles, 9)  # 9 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Category choices for filter
    from .models import NewsArticle as NA
    categories = NA.CATEGORY_CHOICES

    context = {
        'page_obj': page_obj,
        'articles': page_obj,
        'categories': categories,
        'current_category': category,
        'total_articles': NewsArticle.objects.filter(is_published=True).count(),
    }

    return render(request, 'website/news_list.html', context)


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('website:contact')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }

    return render(request, 'website/contact.html', context)


def about(request):
    """About page view"""
    core_values = CoreValue.objects.filter(is_active=True).order_by('order')
    about_images = GalleryImage.objects.filter(
        is_active=True,
        section__in=['about', 'campaign', 'community']
    ).order_by('section', 'order')[:6]

    context = {
        'core_values': core_values,
        'about_images': about_images,
    }

    return render(request, 'website/about.html', context)


def manifesto(request):
    """Manifesto page view"""
    manifesto_items = ManifestoItem.objects.filter(is_active=True).order_by('order')

    context = {
        'manifesto_items': manifesto_items,
        'nrm_website_url': 'https://nrm.ug',
    }

    return render(request, 'website/manifesto.html', context)


def kabale(request):
    """Kabale District page view — comprehensive with UBOS data"""
    kabale_features = KabaleFeature.objects.filter(is_active=True).order_by('order')

    # Get statistics by category
    population_stats = KabaleStatistic.objects.filter(
        is_active=True, category='population'
    ).order_by('order')
    health_stats = KabaleStatistic.objects.filter(
        is_active=True, category='health'
    ).order_by('order')
    education_stats = KabaleStatistic.objects.filter(
        is_active=True, category='education'
    ).order_by('order')
    infrastructure_stats = KabaleStatistic.objects.filter(
        is_active=True, category='infrastructure'
    ).order_by('order')
    economy_stats = KabaleStatistic.objects.filter(
        is_active=True, category='economy'
    ).order_by('order')
    tourism_stats = KabaleStatistic.objects.filter(
        is_active=True, category='tourism'
    ).order_by('order')

    context = {
        'kabale_features': kabale_features,
        'population_stats': population_stats,
        'health_stats': health_stats,
        'education_stats': education_stats,
        'infrastructure_stats': infrastructure_stats,
        'economy_stats': economy_stats,
        'tourism_stats': tourism_stats,
        'kabale_website_url': 'https://kabale.go.ug',
    }

    return render(request, 'website/kabale.html', context)


def gallery(request):
    """Photo gallery page"""
    gallery_images = GalleryImage.objects.filter(is_active=True).order_by('section', 'order')

    context = {
        'gallery_images': gallery_images,
    }

    return render(request, 'website/gallery.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_ajax(request):
    """AJAX contact form submission"""
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.'
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })


def sitemap(request):
    """Generate sitemap for SEO"""
    articles = NewsArticle.objects.filter(is_published=True).order_by('-published_date')
    context = {
        'articles': articles,
    }
    return render(request, 'website/sitemap.xml', context, content_type='application/xml')


def robots_txt(request):
    """Generate robots.txt for SEO"""
    return render(request, 'website/robots.txt', content_type='text/plain')