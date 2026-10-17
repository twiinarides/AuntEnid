from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


class NewsArticle(models.Model):
    """Model for news articles"""
    CATEGORY_CHOICES = [
        ('leadership', 'Leadership'),
        ('politics', 'Politics'),
        ('campaign', 'Campaign'),
        ('empowerment', 'Empowerment'),
        ('youth', 'Youth'),
        ('clarification', 'Clarification'),
        ('nrm_event', 'NRM Event'),
        ('women_empowerment', 'Women Empowerment'),
        ('youth_development', 'Youth Development'),
        ('parliament', 'Parliament'),
        ('community', 'Community'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=500, help_text="Short description for news preview")
    content = models.TextField(help_text="Full article content")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100, default="Kabale District")
    featured_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    image_alt_text = models.CharField(max_length=200, blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:article_detail', kwargs={'slug': self.slug})


class GalleryImage(models.Model):
    """Model for photo gallery images"""
    SECTION_CHOICES = [
        ('hero', 'Hero / Homepage'),
        ('about', 'About Page'),
        ('gallery', 'Photo Gallery'),
        ('campaign', 'Campaign Events'),
        ('community', 'Community Work'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/', help_text="Upload photo")
    alt_text = models.CharField(max_length=200, blank=True, help_text="Describe the image for accessibility")
    caption = models.TextField(blank=True, help_text="Optional caption displayed under the image")
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, default='gallery')
    order = models.PositiveIntegerField(default=0, help_text="Lower number = shown first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return f"{self.title} ({self.get_section_display()})"


class ManifestoItem(models.Model):
    """Model for manifesto items"""
    ICON_CHOICES = [
        ('graduation-cap', 'Education & Youth'),
        ('female', 'Women Empowerment'),
        ('leaf', 'Agriculture'),
        ('road', 'Infrastructure'),
        ('chart-line', 'Economic Development'),
        ('shield-alt', 'Community Security'),
        ('heartbeat', 'Healthcare'),
        ('tint', 'Water & Sanitation'),
        ('bolt', 'Energy'),
        ('landmark', 'Governance'),
        ('tree', 'Environment'),
        ('wifi', 'ICT & Connectivity'),
    ]

    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    description = models.TextField()
    points = models.JSONField(default=list, help_text="List of bullet points")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Manifesto Item"
        verbose_name_plural = "Manifesto Items"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Model for contact form submissions"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"


class SiteConfiguration(models.Model):
    """Model for site-wide configuration — all editable from admin panel"""
    site_name = models.CharField(max_length=100, default="Hon. Enid Origumisiriza Atuheire")
    tagline = models.CharField(max_length=200, default="Woman Member of Parliament — Kabale District")
    subtitle = models.CharField(max_length=200, default="NRM FLAG BEARER | 12th Parliament of Uganda")
    hero_description = models.TextField(
        default="A compassionate leader who empowers, connects, and transforms communities. "
                "Serving Kabale District with integrity, dedication and a clear vision."
    )

    # Contact Information
    phone = models.CharField(max_length=20, default="0764195740")
    email = models.EmailField(default="auntenidoa@gmail.com")
    location = models.CharField(max_length=100, default="Kabale District, Uganda")
    whatsapp = models.CharField(max_length=20, default="+256 705 357149")

    # Social Media Links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True, help_text="X (Twitter) profile URL")
    instagram_url = models.URLField(blank=True)
    tiktok_url = models.URLField(default="https://tiktok.com/@auntenid")
    youtube_url = models.URLField(blank=True)

    # About Section — Bio
    about_title = models.CharField(max_length=100, default="Hon. Enid Origumisiriza Atuheire")
    about_subtitle = models.CharField(
        max_length=200,
        default="Woman Member of Parliament, Kabale District | 12th Parliament of Uganda"
    )
    about_bio = models.TextField(
        default=(
            "Hon. Enid Origumisiriza Atuheire was born in Kashumurizi village, Kabale District. "
            "She attended Bishop Kivigyere Girls' School for primary education, then proceeded to "
            "Kigezi High School for both O-Level and A-Level studies. She later trained at "
            "National Teachers' College (NTC) Kabale before earning her Bachelor of Education "
            "degree from Bishop Barham University College.\n\n"
            "Before entering active politics, she served as a teacher and rose to the position of "
            "Senior Woman Teacher at Kigezi High School — a role that honed her commitment to "
            "nurturing the next generation.\n\n"
            "In 2021, she first contested for the Kabale District Woman MP seat as an independent "
            "candidate. In 2025, she won the hotly contested NRM primary elections, defeating the "
            "incumbent Catherine Atwakiire Ndamira. In the February 2026 general elections, she "
            "secured a decisive victory with 46,797 votes, earning the trust of the people of "
            "Kabale District. She was officially sworn into the 12th Parliament of Uganda in "
            "May 2026."
        ),
        help_text="Full biography displayed on the About page"
    )
    why_running = models.TextField(
        default=(
            "As a woman leader deeply rooted in Kabale District, I believe in the power of "
            "inclusive governance that uplifts every voice — especially those often unheard. "
            "Our community deserves leadership that understands the unique challenges we face "
            "and has the compassion to address them with wisdom and determination."
        )
    )
    vision = models.TextField(
        default=(
            "I envision a Kabale District where every family thrives, where women and youth "
            "are empowered, where education is accessible to all, and where our natural resources "
            "benefit our entire community. My work in Parliament is anchored in healthcare, "
            "maternal health, youth economic empowerment, and the Parish Development Model (PDM)."
        )
    )
    education_background = models.TextField(
        blank=True,
        default=(
            "Bishop Kivigyere Girls' School (Primary) | "
            "Kigezi High School (O & A-Level) | "
            "National Teachers' College, Kabale | "
            "Bishop Barham University College — Bachelor of Education"
        ),
        help_text="Educational background (displayed on About page)"
    )
    professional_background = models.TextField(
        blank=True,
        default="Teacher | Senior Woman Teacher at Kigezi High School | Community Leader | NRM Flag Bearer",
        help_text="Professional/career background"
    )
    profile_image = models.ImageField(
        upload_to='profile/', blank=True, null=True,
        help_text="Main profile photo for hero and about page"
    )
    about_image_2 = models.ImageField(
        upload_to='profile/', blank=True, null=True,
        help_text="Secondary about page image (e.g., in community/parliament)"
    )

    # Kabale Section
    kabale_title = models.CharField(max_length=100, default="Kabale District")
    kabale_subtitle = models.CharField(
        max_length=200,
        default="The Switzerland of Africa — Our beautiful home with unlimited potential"
    )
    kabale_description = models.TextField(
        default=(
            "Kabale District, often called the 'Switzerland of Africa' for its cool climate and "
            "breathtaking rolling green hills, is located in the Kigezi Sub-region of South-Western "
            "Uganda. With a population of 285,588 people (UBOS NPHC 2024), Kabale is one of Uganda's "
            "most densely populated districts at approximately 509 persons per square kilometre.\n\n"
            "The Bakiga people of Kabale — known for their resilience, hard work, and vibrant culture "
            "— have transformed steep hillsides into productive terrace farms, making Kabale Uganda's "
            "potato basket. The district borders Rwanda to the south (Katuna border), making it a "
            "strategic gateway for trade, tourism, and regional integration."
        )
    )
    kabale_website_url = models.URLField(
        default="https://kabale.go.ug",
        blank=True,
        help_text="Link to the official Kabale District Government website"
    )

    # Footer
    footer_description = models.TextField(
        default="Empowering Kabale District through compassionate leadership and inclusive development."
    )
    copyright_text = models.CharField(
        max_length=200,
        default="2026 Hon. Enid Origumisiriza Atuheire. All rights reserved."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"

    def save(self, *args, **kwargs):
        # Ensure only one configuration instance exists
        if not self.pk and SiteConfiguration.objects.exists():
            return
        super().save(*args, **kwargs)


class CoreValue(models.Model):
    """Model for core values section"""
    title = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class (without 'fa-')")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Core Value"
        verbose_name_plural = "Core Values"

    def __str__(self):
        return self.title


class KabaleFeature(models.Model):
    """Model for Kabale District features"""
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class (without 'fa-')")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Kabale Feature"
        verbose_name_plural = "Kabale Features"

    def __str__(self):
        return self.title


class KabaleStatistic(models.Model):
    """Model for Kabale District key statistics (UBOS data)"""
    CATEGORY_CHOICES = [
        ('population', 'Population'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('infrastructure', 'Infrastructure / Roads'),
        ('economy', 'Economy'),
        ('tourism', 'Tourism'),
        ('governance', 'Governance'),
    ]

    label = models.CharField(max_length=100, help_text="e.g. Total Population")
    value = models.CharField(max_length=100, help_text="e.g. 285,588")
    unit = models.CharField(max_length=50, blank=True, help_text="e.g. people, km, hospitals")
    icon = models.CharField(max_length=50, default="chart-bar", help_text="FontAwesome icon class (without 'fa-')")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='population')
    source = models.CharField(
        max_length=200, blank=True,
        default="UBOS NPHC 2024",
        help_text="Data source, e.g. UBOS NPHC 2024"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'order']
        verbose_name = "Kabale Statistic"
        verbose_name_plural = "Kabale Statistics"

    def __str__(self):
        return f"{self.label}: {self.value}"