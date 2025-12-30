from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from streams.vars import FLOWBITE_ICONS
from school.blocks import AcademicCalendarBlock, ScheduleBlock

class QuestionAnswerBlock(blocks.StructBlock):
    """a singleton blocks for Question/Answer."""
    question = blocks.CharBlock(
        max_length=255,
        label="Pertanyaan (FAQ Title)",
        help_text="Judul yang akan diklik pengguna"
    )

    answer = blocks.RichTextBlock(
        label="Jawaban (FAQ Content)",
        features=['bold', 'italic', 'link'],
        help_text="Isi jawaban lengkap"
    )

    class Meta:
        icon = 'comment'
        label = 'Item Pertanyaan & Jawaban'


class FAQBlock(blocks.StructBlock):
    """Block container to display FAQ list."""
    heading = blocks.CharBlock(
        max_length=100,
        required=False,
        label="Judul Bagian FAQ"
    )

    # 🌟 Menggunakan ListBlock untuk mengulang QuestionAnswerBlock 🌟
    items = blocks.ListBlock(
        QuestionAnswerBlock(),
        label="Daftar Pertanyaan",
        help_text="Tambahkan dan susun pertanyaan FAQ di sini."
    )

    class Meta:
        icon = 'list-ul'
        label = 'Daftar FAQ'
        template = 'blocks/faq-sections.html'


class HeadingBlock(blocks.StructBlock):
    """heading block for heading sections"""
    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
    background_image = ImageChooserBlock(required=False)
    icon_choice = blocks.ChoiceBlock(
        choices=[(value, key) for key, value in FLOWBITE_ICONS.items()],
        required=False,
        default= FLOWBITE_ICONS["calendar"]
    )

    class Meta:
        template = "blocks/heading-section.html"
        icon = "image"
        label = "Heading Block"


class CarouselBlock(blocks.StructBlock):
    """Caraousel Block for block with panels"""
    images = blocks.ListBlock(
        ImageChooserBlock(),
        help_text="Add images to display in the carousel."
    )

    class Meta:
        template = "blocks/carousel-section.html"
        icon = "image"
        label = "Carousel"


class HeroBlock(blocks.StructBlock):
    """Block for the main hero section."""
    hero_title = blocks.RichTextBlock(required=False, features=['bold', 'italic', 'br'], help_text="Judul utama. Gunakan Shift+Enter untuk baris baru." )
    hero_subtitle = blocks.RichTextBlock(required=False,features=['bold', 'italic', 'br'], help_text="Subjudul atau deskripsi singkat." )
    hero_image = ImageChooserBlock(required=False, help_text="Gambar latar belakang atau gambar utama.")

    class Meta:
        template = "blocks/hero-section.html"
        icon = "home"
        label = "Hero Section"


class CardBlock(blocks.StructBlock):
    """A single card with an optional image, title, and description."""
    image = ImageChooserBlock(required=False, help_text="Gambar untuk kartu (opsional).")
    title = blocks.CharBlock(required=False, max_length=96, help_text="Judul kartu.")
    description = blocks.TextBlock(required=False, help_text="Deskripsi singkat kartu.")

    class Meta:
        icon = "form"
        label = "Card"


class TitledCardSectionBlock(blocks.StructBlock):
    """A section with a title, subtitle, and a list of cards."""
    title = blocks.CharBlock(required=False, max_length=96, help_text="Judul untuk seksi ini (misal: 'Profil Sekolah').")
    subtitle = blocks.TextBlock(required=False, help_text="Subjudul atau deskripsi untuk seksi ini (opsional).")
    cards = blocks.StreamBlock([
        ('card', CardBlock())
    ], use_json_field=True, required=False)

    class Meta:
        template = "blocks/titled-card-section.html"
        icon = "table"
        label = "Titled Card Section"


class MapsEmbedBlock(blocks.StructBlock):
    """A section for placing embedding maps"""
    title = blocks.CharBlock(required=False, max_length=32, help_text="Judul Lokasi (misal: 'Lokasi Sekolah Kami')")
    subtitle = blocks.TextBlock(required=False, max_length=255, help_text="deskripsi text (misal: 'Temukan lokasi Sekolah kami dengan mudah dan cepat')")
    element = blocks.RawHTMLBlock(required=False, help_text="Tempat section untuk menaruh peta lokasi")

    class Meta:
        template = "blocks/maps-section.html"
        label = "Maps Sections"


class timelineItem(blocks.StructBlock):
    """singular item inside timeline"""
    title = blocks.CharBlock(required=False, max_length=32, help_text="title item")
    date = blocks.DateBlock(required=False, max_length=10, help_text="tahun item")
    description = blocks.RichTextBlock(required=False, help_text="deskripsi item",
        features=["image","bold","italic","embed","link"]
    )

    class Meta:
        icon = "form"
        label = "Timeline Sections"


class timelineBlocks(blocks.StructBlock):
    """sections for displaying timeline blocks"""
    title = blocks.CharBlock(required=False, max_length=32, help_text="timeline heading")
    subtitle = blocks.TextBlock(required=False, max_length=255, help_text="subtitle dari timeline ")
    items = blocks.ListBlock(
        timelineItem(),
        help_text = "isi dari timeline items"
    )

    class Meta:
        template = "blocks/timeline-sections.html"
        label = "Timeline Sections"


class BodyContentBlock(blocks.StreamBlock):
    """group of multiple blocks for use in standard pages"""
    # blocks for standard pages
    hero_section = HeroBlock()
    card_section = TitledCardSectionBlock()
    maps_section = MapsEmbedBlock()
    heading_sections = HeadingBlock()
    carousel_sections = CarouselBlock()
    faq_sections = FAQBlock()
    timeline_sections = timelineBlocks()

    # school related blocks
    academic_sections = AcademicCalendarBlock()
    schedule_sections = ScheduleBlock()
