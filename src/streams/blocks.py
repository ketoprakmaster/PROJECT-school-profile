from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from streams.vars import FLOWBITE_ICONS
from school.blocks import AcademicCalendarBlock, ScheduleBlock

# --- BASE BLOCKS ---

class BaseTitledBlock(blocks.StructBlock):
    """
    Base block to provide title and subtitle fields
    consistently across all other blocks.
    """
    title = blocks.CharBlock(
        required=False, 
        max_length=255, 
        label="Judul/Title"
    )
    subtitle = blocks.TextBlock(
        required=False, 
        label="Sub-judul/Deskripsi"
    )

    class Meta:
        abstract = True


# --- ITEM BLOCKS (Small Components) ---

class QuestionAnswerBlock(blocks.StructBlock):
    question = blocks.CharBlock(max_length=255, label="Pertanyaan")
    answer = blocks.RichTextBlock(features=['bold', 'italic', 'link'], label="Jawaban")

    class Meta:
        icon = 'comment'
        label = 'Item FAQ'


class BasicCardBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    title = blocks.CharBlock(required=False, max_length=96)
    description = blocks.TextBlock(required=False)

    class Meta:
        template = "components/basic-card.html"
        icon = "form"
        label = "Card"


class ProfileCardBlock(BasicCardBlock):
    contact = blocks.TextBlock(required=False, help_text="Nomor atau link kontak")

    class Meta:
        template = "components/profile-card.html"
        icon = "user"
        label = "Profile Card"


class TimelineItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=128)
    date = blocks.DateBlock(required=False)
    description = blocks.RichTextBlock(
        required=False, 
        features=["image", "bold", "italic", "embed", "link"]
    )

    class Meta:
        icon = "date"
        label = "Timeline Item"


# --- MAIN SECTION BLOCKS (Refactored using BaseTitledBlock) ---

class FAQBlock(BaseTitledBlock):
    items = blocks.ListBlock(QuestionAnswerBlock(), label="Daftar Pertanyaan")

    class Meta:
        template = 'blocks/faq-sections.html'
        icon = 'list-ul'
        label = 'Daftar FAQ'


class HeadingBlock(BaseTitledBlock):
    background_image = ImageChooserBlock(required=False)
    icon_choice = blocks.ChoiceBlock(
        choices=[(value, key) for key, value in FLOWBITE_ICONS.items()],
        required=False,
        default=FLOWBITE_ICONS.get("calendar", "")
    )

    class Meta:
        template = "blocks/heading-section.html"
        icon = "title"
        label = "Heading Block"


class HeroBlock(BaseTitledBlock):
    # Overriding title/subtitle untuk menggunakan RichText khusus di Hero Section
    title = blocks.RichTextBlock(required=False, features=['bold', 'italic', 'br'])
    subtitle = blocks.RichTextBlock(required=False, features=['bold', 'italic', 'br'])
    image = ImageChooserBlock(required=False, label="Hero Image")

    class Meta:
        template = "blocks/hero-section.html"
        icon = "home"
        label = "Hero Section"


class TitledCardSectionBlock(BaseTitledBlock):
    cards = blocks.StreamBlock([
        ('card', BasicCardBlock()),
        ('profile_card', ProfileCardBlock()),
    ], use_json_field=True, required=False)

    class Meta:
        template = "blocks/titled-card-section.html"
        icon = "table"
        label = "Titled Card Section"


class HorizontalCardSectionBlock(TitledCardSectionBlock):
    class Meta:
        template = "blocks/horizontal-card-section.html"
        icon = "table"
        label = "Horizontal Card Sections"


class MapsEmbedBlock(BaseTitledBlock):
    element = blocks.RawHTMLBlock(required=False, help_text="Embed code dari Google Maps")

    class Meta:
        template = "blocks/maps-section.html"
        icon = "site"
        label = "Maps Sections"


class TimelineBlocks(BaseTitledBlock):
    items = blocks.ListBlock(TimelineItemBlock())

    class Meta:
        template = "blocks/timeline-sections.html"
        icon = "history"
        label = "Timeline Sections"


class CarouselBlock(blocks.StructBlock):
    # Carousel biasanya tidak butuh title/subtitle global, tapi bisa ditambah jika mau
    images = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        template = "blocks/carousel-section.html"
        icon = "image"
        label = "Carousel"


# --- FINAL STREAMBLOCK ---

class BodyContentBlock(blocks.StreamBlock):
    hero_section = HeroBlock()
    card_section = TitledCardSectionBlock()
    horizontal_card_section = HorizontalCardSectionBlock()
    maps_section = MapsEmbedBlock()
    heading_sections = HeadingBlock()
    carousel_sections = CarouselBlock()
    faq_sections = FAQBlock()
    timeline_sections = TimelineBlocks()
    
    academic_sections = AcademicCalendarBlock()
    schedule_sections = ScheduleBlock()