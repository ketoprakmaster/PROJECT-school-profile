from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock


class HeroBlock(blocks.StructBlock):
    """Block for the main hero section."""
    hero_title = blocks.RichTextBlock(required=False, features=['bold', 'italic', 'br'], help_text="Judul utama. Gunakan Shift+Enter untuk baris baru." )
    hero_subtitle = blocks.TextBlock(required=False, help_text="Subjudul atau deskripsi singkat." )
    hero_image = ImageChooserBlock(required=False, help_text="Gambar latar belakang atau gambar utama.")

    class Meta:
        template = "home/blocks/hero_block.html"
        icon = "home"
        label = "Hero Section"


class CardBlock(blocks.StructBlock):
    """A single card with an optional image, title, and description."""
    image = ImageChooserBlock(required=False, help_text="Gambar untuk kartu (opsional).")
    title = blocks.CharBlock(required=False, max_length=255, help_text="Judul kartu.")
    description = blocks.TextBlock(required=False, help_text="Deskripsi singkat kartu.")

    class Meta:
        icon = "form"
        label = "Card"


class TitledCardSectionBlock(blocks.StructBlock):
    """A section with a title, subtitle, and a list of cards."""
    title = blocks.CharBlock(required=False, max_length=255, help_text="Judul untuk seksi ini (misal: 'Profil Sekolah').")
    subtitle = blocks.TextBlock(required=False, help_text="Subjudul atau deskripsi untuk seksi ini (opsional).")
    cards = blocks.StreamBlock([
        ('card', CardBlock())
    ], use_json_field=True, required=False)

    class Meta:
        template = "home/blocks/titled_card_section_block.html"
        icon = "table"
        label = "Titled Card Section"

class MapsEmbedBlock(blocks.StructBlock):
    """A section for placing embedding maps"""
    title = blocks.CharBlock(required=False, max_length=32, help_text="Judul Lokasi (misal: 'Lokasi Sekolah Kami')")
    subtitle = blocks.TextBlock(required=False, max_length=64, help_text="deskripsi text (misal: 'Temukan lokasi Sekolah kami dengan mudah dan cepat')")
    element = blocks.RawHTMLBlock(required=False, help_text="Tempat section untuk menaruh peta lokasi")

    class Meta:
        template = "home/blocks/maps_block.html"
        label = "Maps Sections"


body = StreamField([
    ('hero_section', HeroBlock()),
    ('card_section', TitledCardSectionBlock()),
    ('maps_section', MapsEmbedBlock())
], use_json_field=True, blank=True, null=True)
