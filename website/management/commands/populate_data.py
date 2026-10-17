from django.core.management.base import BaseCommand
from django.utils import timezone
from website.models import (
    NewsArticle, ManifestoItem, CoreValue, 
    KabaleFeature, SiteConfiguration, GalleryImage, KabaleStatistic
)


class Command(BaseCommand):
    help = 'Populate the database with up-to-date data for Hon. Enid Origumisiriza Atuheire and Kabale District'

    def handle(self, *args, **options):
        self.stdout.write('Starting comprehensive data update...')
        
        # 1. Update or create site configuration
        config, created = SiteConfiguration.objects.get_or_create(id=1)
        config.site_name = "Hon. Enid Origumisiriza Atuheire"
        config.tagline = "Woman Member of Parliament — Kabale District"
        config.subtitle = "NRM FLAG BEARER | 12th Parliament of Uganda (2026–2031)"
        config.hero_description = (
            "A compassionate leader who empowers, connects, and transforms communities. "
            "Dedicated to servant leadership, quality healthcare, youth empowerment, and rural development in Kabale District."
        )
        config.phone = "0764195740"
        config.email = "auntenidoa@gmail.com"
        config.location = "Kabale District, Uganda"
        config.whatsapp = "+256 705 357149"
        config.twitter_url = "https://x.com/auntenid"
        config.facebook_url = "https://facebook.com/auntenid"
        config.tiktok_url = "https://tiktok.com/@auntenid"
        config.about_title = "Hon. Enid Origumisiriza Atuheire"
        config.about_subtitle = "Woman Member of Parliament, Kabale District | 12th Parliament of Uganda"
        config.about_bio = (
            "Hon. Enid Origumisiriza Atuheire was born in Kashumurizi village, Kabale District. "
            "She attended Bishop Kivigyere Girls' School for primary education, then proceeded to "
            "the historic Kigezi High School for both O-Level and A-Level studies. She completed her professional teacher "
            "training at National Teachers' College (NTC) Kabale before obtaining her Bachelor of Education (B.Ed) degree from "
            "Bishop Barham University College.\n\n"
            "Prior to entering competitive politics, she served with distinction as a teacher and rose to become the "
            "Senior Woman Teacher at Kigezi High School — an experience that cemented her dedication to girl-child protection, "
            "youth mentorship, and household education.\n\n"
            "In 2021, she contested for the Kabale District Woman Member of Parliament seat as an independent candidate. "
            "In 2025, she won the hotly contested National Resistance Movement (NRM) primary elections, defeating the incumbent. "
            "In the February 2026 General Elections, she clinched a resounding victory with 46,797 votes, winning the confidence "
            "and mandate of the people of Kabale. She was officially sworn into the 12th Parliament of Uganda in May 2026."
        )
        config.education_background = (
            "Bishop Kivigyere Girls' School (Primary) | "
            "Kigezi High School (UCE & UACE) | "
            "National Teachers' College, Kabale (Diploma in Education) | "
            "Bishop Barham University College (Bachelor of Education)"
        )
        config.professional_background = (
            "Educator | Senior Woman Teacher (Kigezi High School) | "
            "Community Broadcaster | Patron, Children of the Word | Member of Parliament"
        )
        config.why_running = (
            "As a woman leader deeply rooted in Kabale District, I believe in the power of inclusive governance "
            "that uplifts every voice, especially those often unheard. Our community deserves leadership that understands "
            "our rugged terrain, our economic potential, and has the compassion to address household poverty with wisdom and persistence."
        )
        config.vision = (
            "I envision a Kabale District where every mother delivers safely in a well-equipped health center, "
            "every youth possesses practical marketable skills, farmers receive premium prices for their produce through cooperatives, "
            "and government initiatives like the Parish Development Model (PDM) genuinely transform families at the grassroots."
        )
        config.kabale_title = "Kabale District"
        config.kabale_subtitle = "The Switzerland of Africa — Gateway to Tourism, Agriculture & Regional Trade"
        config.kabale_description = (
            "Kabale District, situated in the Kigezi Sub-Region of South-Western Uganda, is widely celebrated as the "
            "'Switzerland of Africa' owing to its cool temperate climate and scenic terraced green highlands. "
            "According to official Uganda Bureau of Statistics (UBOS) 2024 Census figures, Kabale is home to 285,588 residents "
            "(164,365 females and 121,223 males) with an average household size of 4.2 persons and a high population density of ~509 people/km².\n\n"
            "Known as Uganda's potato basket, Kabale farmers have tamed the steep mountainous hills into productive terraced steps. "
            "Bordered by Rwanda at the Katuna border crossing (just 25 km from Kabale Town), the district serves as an indispensable trade artery "
            "and the tourism gateway to Lake Bunyonyi and the mountain gorillas of the Kigezi landscape."
        )
        config.kabale_website_url = "https://kabale.go.ug"
        config.footer_description = "Serving Kabale District with transparent leadership, compassion, and inclusive community empowerment."
        config.copyright_text = "2026 Hon. Enid Origumisiriza Atuheire. All rights reserved."
        config.save()
        self.stdout.write(self.style.SUCCESS("[OK] Site Configuration updated successfully!"))

        # 2. Populate / Update UBOS Kabale Statistics
        stats_data = [
            # Population
            {'label': 'Total Population', 'value': '285,588', 'unit': 'people', 'category': 'population', 'icon': 'users', 'source': 'UBOS NPHC 2024', 'order': 1},
            {'label': 'Female Population', 'value': '164,365', 'unit': 'women (57.6%)', 'category': 'population', 'icon': 'female', 'source': 'UBOS NPHC 2024', 'order': 2},
            {'label': 'Male Population', 'value': '121,223', 'unit': 'men (42.4%)', 'category': 'population', 'icon': 'male', 'source': 'UBOS NPHC 2024', 'order': 3},
            {'label': 'Total Households', 'value': '66,752', 'unit': 'households', 'category': 'population', 'icon': 'home', 'source': 'UBOS NPHC 2024', 'order': 4},
            {'label': 'Average Household Size', 'value': '4.2', 'unit': 'persons/household', 'category': 'population', 'icon': 'user-friends', 'source': 'UBOS NPHC 2024', 'order': 5},
            {'label': 'Population Density', 'value': '509.1', 'unit': 'persons/km²', 'category': 'population', 'icon': 'expand-arrows-alt', 'source': 'UBOS NPHC 2024', 'order': 6},
            {'label': 'Land Area', 'value': '561.4', 'unit': 'square kilometers', 'category': 'population', 'icon': 'map', 'source': 'UBOS Statistical Abstract', 'order': 7},
            # Health
            {'label': 'Kabale Regional Referral', 'value': '280+', 'unit': 'inpatient beds', 'category': 'health', 'icon': 'hospital', 'source': 'Ministry of Health 2024', 'order': 1},
            {'label': 'Major Referral Hospitals', 'value': '3', 'unit': 'facilities', 'category': 'health', 'icon': 'hospital-alt', 'source': 'Kabale RRH, Rushoroza, Rugarama', 'order': 2},
            {'label': 'Sub-County Health Centres', 'value': '15+', 'unit': 'HC III & IV units', 'category': 'health', 'icon': 'clinic-medical', 'source': 'District Health Office', 'order': 3},
            # Infrastructure & Roads
            {'label': 'Kampala-Kabale Highway', 'value': '410', 'unit': 'kilometers (Tarmac)', 'category': 'infrastructure', 'icon': 'road', 'source': 'UNRA Transport Network', 'order': 1},
            {'label': 'Katuna Border Distance', 'value': '25', 'unit': 'kilometers', 'category': 'infrastructure', 'icon': 'exchange-alt', 'source': 'Uganda-Rwanda Border Highway', 'order': 2},
            {'label': 'Sub-counties & Divisions', 'value': '15', 'unit': 'local councils', 'category': 'governance', 'icon': 'landmark', 'source': 'Kabale Local Government', 'order': 1},
            {'label': 'Parishes & Wards', 'value': '79', 'unit': 'PDM beneficiary parishes', 'category': 'governance', 'icon': 'sitemap', 'source': 'Parish Development Model Register', 'order': 2},
            # Education
            {'label': 'Kabale University', 'value': 'Public', 'unit': 'Chartered University', 'category': 'education', 'icon': 'university', 'source': 'Ministry of Education', 'order': 1},
            {'label': 'Govt Aided Secondary Schools', 'value': '15+', 'unit': 'secondary institutions', 'category': 'education', 'icon': 'school', 'source': 'District Education Department', 'order': 2},
        ]
        
        KabaleStatistic.objects.all().delete()
        for stat in stats_data:
            KabaleStatistic.objects.create(**stat)
        self.stdout.write(self.style.SUCCESS(f"[OK] Populated {len(stats_data)} UBOS Kabale District statistics!"))

        # 3. Create or Update Core Values
        core_values_data = [
            {'title': 'Compassion', 'icon': 'heart', 'description': 'Listening to vulnerable households, widows, and youth with empathy and practical relief.', 'order': 1},
            {'title': 'Integrity', 'icon': 'handshake', 'description': 'Transparent, accountable, and corruption-free advocacy for Kabale resources in Parliament.', 'order': 2},
            {'title': 'Inclusivity', 'icon': 'users', 'description': 'Uniting all sub-counties, religions, and backgrounds without political bias or favoritism.', 'order': 3},
            {'title': 'Hard Work & Resilience', 'icon': 'mountain', 'description': 'Drawing inspiration from the Bakiga spirit to conquer steep challenges and deliver real progress.', 'order': 4},
            {'title': 'Innovation & Skills', 'icon': 'lightbulb', 'description': 'Empowering youth and women with modern agricultural value addition and trade technologies.', 'order': 5},
        ]
        CoreValue.objects.all().delete()
        for cv in core_values_data:
            CoreValue.objects.create(**cv)
        self.stdout.write(self.style.SUCCESS(f"[OK] Created {len(core_values_data)} core values!"))

        # 4. Create or Update Manifesto Pillars (NRM 2026-2031 aligned)
        manifesto_data = [
            {
                'title': 'Healthcare & Maternal Survival',
                'icon': 'heartbeat',
                'description': 'Upgrading rural health infrastructure and saving mothers and newborns across Kigezi.',
                'points': [
                    'Ensure all Health Centre IIIs have functioning maternity wards and solar power',
                    'Advocate for medicine availability and specialized equipment at Kamukira HC IV and Kabale RRH',
                    'Provide community ambulance facilitation for difficult mountain terrain',
                    'Aggressive nutrition drives to reduce childhood stunting across all 79 parishes'
                ],
                'order': 1
            },
            {
                'title': 'Education, Youth Skills & Employment',
                'icon': 'graduation-cap',
                'description': 'Equipping young people with marketable technical skills and stem school dropouts.',
                'points': [
                    'Sponsor vocational training programs (carpentry, tailoring, salon, ICT, driving)',
                    'Combat boy-child and girl-child school dropout rates in rural sub-counties',
                    'Support Kabale University student innovations and community research fellowships',
                    'Establish Aunt Enid talent incubators and sports leagues to inspire young leaders'
                ],
                'order': 2
            },
            {
                'title': 'Women Economic Empowerment',
                'icon': 'female',
                'description': 'Elevating women from subsistence farming into business ownership and cooperative wealth.',
                'points': [
                    'Link women savings SACCOs directly to low-interest seed capital and Emyooga funds',
                    'Provide financial literacy and value-addition training for market vendors',
                    'Defend widow land rights and combat domestic gender-based violence',
                    'Support women-led craft, pottery, and tourist souvenir micro-enterprises at Lake Bunyonyi'
                ],
                'order': 3
            },
            {
                'title': 'Agriculture, PDM & Food Security',
                'icon': 'leaf',
                'description': 'Maximizing returns from terraced farming in Uganda’s premier potato and vegetable basket.',
                'points': [
                    'Ensure 100% transparent disbursement of Parish Development Model (PDM) funds in every parish',
                    'Supply certified Irish potato seeds, fertilizer subsidies, and modern terrace conservation techniques',
                    'Establish post-harvest cold storage and packaging facilities in Kabale Municipality',
                    'Eliminate middlemen exploitation through district agricultural marketing cooperatives'
                ],
                'order': 4
            },
            {
                'title': 'Roads, Bridges & Tourism Infrastructure',
                'icon': 'road',
                'description': 'Unlocking connectivity across steep hills and tapping the Lake Bunyonyi tourism economy.',
                'points': [
                    'Lobby central government and UNRA for tarmacking tourism circuits around Lake Bunyonyi',
                    'Procure heavy district road maintenance equipment for clearing landslides and opening farm access roads',
                    'Construct durable footbridges over mountain rivers to keep school children safe during rains',
                    'Expand rural electrification and solar street lighting across commercial trading centers'
                ],
                'order': 5
            },
            {
                'title': 'Clean Water & Environmental Protection',
                'icon': 'tint',
                'description': 'Safeguarding mountain ecosystems while providing clean gravity water to highland homes.',
                'points': [
                    'Expand Gravity Flow Schemes (GFS) from highland springs to water-scarce hilltops',
                    'Promote tree planting and bamboo planting on steep slopes to prevent soil erosion and fatal landslides',
                    'Protect Lake Bunyonyi wetlands from siltation while preserving eco-tourism livelihoods',
                    'Drill deep-water solar boreholes in hard-to-reach sub-counties'
                ],
                'order': 6
            }
        ]
        ManifestoItem.objects.all().delete()
        for item in manifesto_data:
            ManifestoItem.objects.create(**item)
        self.stdout.write(self.style.SUCCESS(f"[OK] Created {len(manifesto_data)} NRM manifesto pillars!"))

        # 5. Populate and Sync Up-to-date Live News Stories
        articles_data = [
            {
                'title': 'Hon. Enid Origumisiriza Takes Oath in the 12th Parliament of Uganda',
                'slug': 'hon-enid-origumisiriza-takes-oath-12th-parliament',
                'excerpt': 'Following her decisive victory in the general election, Hon. Enid Origumisiriza Atuheire was sworn in as Kabale District Woman MP, pledging selfless advocacy and grassroots development.',
                'content': '''Hon. Enid Origumisiriza Atuheire has officially taken her oath of allegiance as the Woman Member of Parliament representing Kabale District in the 12th Parliament of Uganda.

Dressed in radiant traditional attire and accompanied by family members, religious leaders, and party mobilizers, Hon. Enid placed her hand on the Holy Bible at the parliamentary grounds in Kampala, swearing to preserve, protect, and defend the Constitution of the Republic of Uganda.

Her swearing-in comes on the back of an overwhelming general election victory in February, where she garnered 46,797 votes on the National Resistance Movement (NRM) ticket.

Speaking to journalists shortly after the ceremony, Hon. Enid outlined her top legislative agenda:
1. Championing Maternal and Infant Health: Ensuring that health centers like Kamukira HC IV, Buhara HC III, and Maziba HC III receive emergency delivery kits, reliable water, and solar backups.
2. Overseeing the Parish Development Model (PDM): Safeguarding PDM funding across Kabale's 79 parishes so that funds directly reach vulnerable households without bureaucratic deductions.
3. Quality Education & Youth Retainment: Addressing the alarming school dropout rates among boys and girls and expanding vocational training.
4. Infrastructure & Tourism: Lobbying for the completion and upgrading of the Lake Bunyonyi tourism circuit roads and district feeder connections.

"I stand here not just as a legislator, but as a servant of Kabale. The trust that mothers, youths, and elders placed in me will be honored through active, fearless, and results-driven representation," she declared.''',
                'category': 'parliament',
                'location': 'Parliament of Uganda, Kampala',
                'published_date': timezone.datetime(2026, 5, 20),
                'is_featured': True,
                'is_published': True
            },
            {
                'title': 'Kabale Community Welcomes Hon. Enid with Grand Thanksgiving Service',
                'slug': 'kabale-community-welcomes-hon-enid-thanksgiving',
                'excerpt': 'Thousands of residents from Ndorwa and Kabale Municipality gathered for an inter-denominational thanksgiving service celebrating unity and leadership for the district.',
                'content': '''A massive crowd gathered in Kabale Town as religious leaders from the Catholic Church, Church of Uganda, and Muslim community joined thousands of supporters in a grand thanksgiving service honoring Hon. Enid Origumisiriza Atuheire's assumption of parliamentary duties.

Leaders commended her steadfast commitment to non-partisan community development. Clergy speakers reminded the congregation that Aunt Enid had spent years mentoring young girls as Senior Woman Teacher at Kigezi High School and supporting widows long before seeking political office.

During her address, Hon. Enid expressed heartfelt gratitude to the voters of Kabale:
"This victory belongs to every household that desires progress. Election season is behind us; now is the time to build together. Whether you voted yellow or held another view, I am the Woman MP for all people of Kabale District."

The thanksgiving ceremony featured performances by youth groups, testimonies from women SACCO leaders who have benefited from her mentorship, and an agricultural exhibition by local Irish potato farmers.''',
                'category': 'community',
                'location': 'Kabale Town',
                'published_date': timezone.datetime(2026, 6, 12),
                'is_featured': True,
                'is_published': True
            },
            {
                'title': 'Advancing PDM Funds: Hon. Enid Inspects Beneficiary Farmer Groups in Buhara and Maziba',
                'slug': 'advancing-pdm-funds-hon-enid-inspects-buhara-maziba',
                'excerpt': 'In her oversight role, Hon. Enid conducted an extensive inspection tour of agricultural projects benefiting from the Parish Development Model in rural sub-counties.',
                'content': '''Hon. Enid Origumisiriza Atuheire has concluded a three-day working tour across Buhara, Maziba, and Kyanamira sub-counties to evaluate the implementation of the Parish Development Model (PDM).

The Woman MP met with parish chiefs, SACCO leaders, and individual farming beneficiaries engaged in potato seed multiplication, zero-grazing dairy farming, and poultry projects.

Key takeaways from the field monitoring tour:
• Transparency in selection: Beneficiaries praised the improved vetting process, ensuring that the poorest households (the 39% in subsistence) receive their 1 million shillings entitlement.
• Seed Quality: Hon. Enid intervened on complaints regarding seed quality, directing district agricultural officers to provide disease-resistant certified potato varieties suited for Kabale's volcanic soils.
• Extension Services: She called on the Ministry of Agriculture, Animal Industry and Fisheries to increase veterinary and crop extension officers deployed in Kigezi.

"PDM is the bedrock of President Museveni's vision to transition Uganda into middle-income status. In Kabale, we will not allow a single shilling to be siphoned away from the intended grassroots beneficiaries," Hon. Enid told gathering residents at Buhara trading center.''',
                'category': 'empowerment',
                'location': 'Buhara & Maziba Sub-counties',
                'published_date': timezone.datetime(2026, 8, 5),
                'is_featured': True,
                'is_published': True
            },
            {
                'title': 'The Lasting Case for Aunt Enid: A Legacy Built on Service and Mentorship',
                'slug': 'the-lasting-case-for-aunt-enid',
                'excerpt': 'Before she ever took her seat in Parliament, Hon. Enid Origumisiriza — fondly called Aunt Enid — had already written her story in the hearts of many through community projects and school mentorship.',
                'content': '''Long before the title "Honourable" was added before her name, Enid Origumisiriza was already known in villages, homes, and marketplaces as a beacon of service. To the mothers who had once struggled silently, she was the one who came with listening ears and practical solutions. To the youth wandering without direction, she was the one who saw not only their struggles but also their potential.

Her work began humbly — reaching out to families in need, supporting widows, and creating safe spaces where women could learn skills and find empowerment. As Senior Woman Teacher at Kigezi High School, she instilled discipline, high academic ambition, and spiritual strength into generations of girls who are today doctors, engineers, and educators.

On community radio, her voice became a constant companion in homes across Kigezi. Through programs filled with encouragement, advice, and practical wisdom, listeners found a trusted sister, mentor, and guide.

Now in the 12th Parliament, Aunt Enid continues this sacred calling with the same humility, accessibility, and unwavering love for the people of Kabale.''',
                'category': 'leadership',
                'location': 'Kabale District',
                'published_date': timezone.datetime(2026, 3, 1),
                'is_featured': True,
                'is_published': True
            },
            {
                'title': 'President Museveni Nomination & Historic NRM Unity Rally',
                'slug': 'president-museveni-historic-nomination',
                'excerpt': 'Hon. Enid Origumisiriza Atuheire joined thousands of NRM supporters at Kololo to celebrate the party\'s strategic roadmap under the leadership of President Yoweri Kaguta Museveni.',
                'content': '''Hon. Enid Origumisiriza Atuheire joined thousands of jubilant supporters and party delegates at Kololo Independence Grounds to celebrate the official nomination of H.E. President Yoweri Kaguta Museveni as the NRM presidential flag bearer.

Draped in iconic party yellow, delegates reaffirmed the party's historic mission: peace, national security, infrastructure development, and economic transformation under the 2026–2031 Manifesto.

Hon. Enid emphasized that Kabale District stands to gain tremendously from the national development priorities, particularly in industrial value addition for agricultural goods, road connectivity to Rwanda and DRC, and healthcare revitalization.

"Our unity as NRM is our greatest strength. Under President Museveni's visionary stewardship, Kabale will continue to rise," she noted.''',
                'category': 'nrm_event',
                'location': 'Kololo Independence Grounds',
                'published_date': timezone.datetime(2025, 9, 23),
                'is_featured': True,
                'is_published': True
            },
            {
                'title': 'Clarification on False Reports Circulating Online Regarding Buhara',
                'slug': 'clarification-on-false-reports-circulating-online',
                'excerpt': 'Official clarification: Disregarding fabricated social media claims and reiterating commitment to peaceful, lawful, and dignified leadership.',
                'content': '''We wish to clarify that information circulated on certain online blogs regarding alleged incidents at Buhara Police Post was entirely fabricated and malicious.

At no point did Hon. Enid Origumisiriza Atuheire or her team engage in any unlawful activity. All engagements by Aunt Enid and her campaign remain strictly peaceful, lawful, and anchored on mutual respect and due process.

We urge supporters and the public to disregard propaganda intended to distract from genuine development work. We remain focused on unity, service delivery, and uplifting Kabale District.''',
                'category': 'clarification',
                'location': 'Buhara, Kabale District',
                'published_date': timezone.datetime(2025, 9, 24),
                'is_featured': False,
                'is_published': True
            }
        ]

        for art_data in articles_data:
            art, _ = NewsArticle.objects.update_or_create(
                slug=art_data['slug'],
                defaults=art_data
            )
            self.stdout.write(f"[OK] Synced story: {art.title}")

        self.stdout.write(self.style.SUCCESS("All database records successfully populated and updated!"))
