from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock


from streams.vars import FLOWBITE_ICONS
from school.models import AcademicCalendar


class AcademicCalendarBlock(blocks.StructBlock):
    """block for the academic calendars"""
    title = blocks.CharBlock(default="Jadwal Kegiatan Akademik", required=False)
    subtitle = blocks.CharBlock(required=False)
    limit = blocks.IntegerBlock(default=50, required=False)
    show_description = blocks.BooleanBlock(default=False, required=False)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        qs = AcademicCalendar.objects.all()
        if value["limit"]:
            qs = qs[:value["limit"]]

        context["events"] = qs
        return context

    class Meta:
        template = "blocks/calendar-section.html"
        icon = "date"
        label = "Academic Calendar"


class HeadingBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    subtitle = blocks.CharBlock(required=False)
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

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)

        return context

class ScheduleBlock(blocks.StructBlock):
    """Schedule Block F=for Searching Schedule"""

    class Meta:
        template = "blocks/schedule-section.html"
        icon = "date"
        label = "schedule search"


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
    subtitle = blocks.TextBlock(required=False, max_length=64, help_text="deskripsi text (misal: 'Temukan lokasi Sekolah kami dengan mudah dan cepat')")
    element = blocks.RawHTMLBlock(required=False, help_text="Tempat section untuk menaruh peta lokasi")

    class Meta:
        template = "blocks/maps-section.html"
        label = "Maps Sections"
        

class BodyContentBlock(blocks.StreamBlock):
    """group of multiple blocks for use in standard pages"""
    # blocks for standard pages
    hero_section = HeroBlock()
    card_section = TitledCardSectionBlock()
    maps_section = MapsEmbedBlock()
    heading_sections = HeadingBlock()
    carousel_sections = CarouselBlock()
    
    # school related blocks
    academic_sections = AcademicCalendarBlock()
    schedule_sections = ScheduleBlock()

