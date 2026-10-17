from django.contrib import admin
from django.utils.html import format_html
from .models import (
    NewsArticle, ManifestoItem, ContactMessage,
    SiteConfiguration, CoreValue, KabaleFeature,
    GalleryImage, KabaleStatistic
)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'is_published', 'is_featured', 'published_date']
    list_filter = ['category', 'is_published', 'is_featured', 'published_date']
    list_editable = ['is_published', 'is_featured']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ['-published_date']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Categorization', {
            'fields': ('category', 'location')
        }),
        ('Media', {
            'fields': ('featured_image', 'image_alt_text')
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_date')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order', 'is_active', 'image_preview']
    list_filter = ['section', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'caption']
    ordering = ['section', 'order']

    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'image', 'alt_text', 'caption')
        }),
        ('Display Settings', {
            'fields': ('section', 'order', 'is_active')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px; height:60px; object-fit:cover; border-radius:4px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"


@admin.register(ManifestoItem)
class ManifestoItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'icon', 'description', 'points'),
            'description': 'For "points" field, enter a JSON list like: ["Point 1", "Point 2", "Point 3"]'
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'phone', 'message', 'created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🌐 Site Information', {
            'fields': ('site_name', 'tagline', 'subtitle', 'hero_description'),
            'description': 'Main headline text shown on the homepage hero section'
        }),
        ('📞 Contact Information', {
            'fields': ('phone', 'email', 'location', 'whatsapp')
        }),
        ('📱 Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'tiktok_url', 'youtube_url'),
            'description': 'Enter full URLs (e.g. https://facebook.com/YourPage)'
        }),
        ('👤 About / Biography', {
            'fields': (
                'about_title', 'about_subtitle',
                'about_bio',
                'education_background', 'professional_background',
                'why_running', 'vision',
                'profile_image', 'about_image_2'
            ),
            'description': 'This controls everything displayed on the About page'
        }),
        ('🗺️ Kabale District Section', {
            'fields': ('kabale_title', 'kabale_subtitle', 'kabale_description', 'kabale_website_url'),
            'description': 'Text for the Kabale District overview section'
        }),
        ('📌 Footer', {
            'fields': ('footer_description', 'copyright_text')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one configuration instance
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of configuration
        return False


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'icon', 'description'),
            'description': 'For "icon", use FontAwesome icon names without "fa-" (e.g. "heart", "star", "users")'
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(KabaleFeature)
class KabaleFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'icon', 'description'),
            'description': 'For "icon", use FontAwesome icon names without "fa-" (e.g. "mountain", "users")'
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(KabaleStatistic)
class KabaleStatisticAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'unit', 'category', 'source', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    list_editable = ['value', 'order', 'is_active']
    search_fields = ['label', 'value', 'source']
    ordering = ['category', 'order']

    fieldsets = (
        ('Statistic Data', {
            'fields': ('label', 'value', 'unit', 'source', 'icon'),
            'description': 'Examples — label: "Total Population", value: "285,588", unit: "people", source: "UBOS NPHC 2024"'
        }),
        ('Display', {
            'fields': ('category', 'order', 'is_active')
        }),
    )


# Customize admin site header and branding
admin.site.site_header = "Hon. Enid Origumisiriza Atuheire — Campaign Admin"
admin.site.site_title = "Aunt Enid Admin"
admin.site.index_title = "Welcome to the Campaign Administration Panel"