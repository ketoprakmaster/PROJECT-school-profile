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
        label="Judul",
        help_text="Masukkan judul utama untuk bagian ini."
    )
    subtitle = blocks.TextBlock(
        required=False,
        label="Sub-judul/Deskripsi",
        help_text="Tambahkan keterangan tambahan di bawah judul (opsional)."
    )

    class Meta:
        abstract = True


# --- ITEM BLOCKS (Small Components) ---

class QuestionAnswerBlock(blocks.StructBlock):
    question = blocks.CharBlock(
        max_length=255,
        label="Pertanyaan",
        help_text="Tuliskan pertanyaan yang sering diajukan."
    )
    answer = blocks.RichTextBlock(
        features=['bold', 'italic', 'link'],
        label="Jawaban",
        help_text="Tuliskan jawaban lengkap secara singkat dan jelas."
    )

    class Meta:
        icon = 'comment'
        label = 'Item FAQ'


class BasicCardBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=False,
        label="Gambar",
        help_text="Gunakan gambar dengan rasio 4:3 untuk hasil terbaik."
    )
    title = blocks.CharBlock(
        required=False,
        max_length=96,
        label="Judul Kartu",
        help_text="Judul singkat untuk kartu ini."
    )
    description = blocks.TextBlock(
        required=False,
        label="Deskripsi",
        help_text="Isi konten utama dari kartu."
    )

    class Meta:
        template = "components/streams-basic-card.html"
        icon = "form"
        label = "Kartu Standar"


class ProfileCardBlock(BasicCardBlock):
    contact = blocks.TextBlock(
        required=False,
        label="Kontak",
        help_text="Masukkan nomor telepon, email, atau link profil sosial media."
    )

    class Meta:
        template = "components/streams-profile-card.html"
        icon = "user"
        label = "Kartu Profil"


class TimelineItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        max_length=128,
        label="Nama Agenda/Event"
    )
    date = blocks.DateBlock(
        required=False,
        label="Tanggal",
        help_text="Pilih tanggal kejadian untuk urutan waktu."
    )
    description = blocks.RichTextBlock(
        required=False,
        features=["image", "bold", "italic", "embed", "link"],
        label="Keterangan",
        help_text="Detail informasi mengenai agenda/event ini."
    )

    class Meta:
        icon = "date"
        label = "Item Lini Masa"


# --- MAIN SECTION BLOCKS (Refactored using BaseTitledBlock) ---

class FAQBlock(BaseTitledBlock):
    items = blocks.ListBlock(
        QuestionAnswerBlock(),
        label="Daftar Pertanyaan",
        help_text="Tambahkan satu atau lebih tanya-jawab ke dalam daftar."
    )

    class Meta:
        template = 'blocks/faq-sections.html'
        icon = 'list-ul'
        label = 'Bagian FAQ'


class HeadingBlock(BaseTitledBlock):
    background_image = ImageChooserBlock(
        required=False,
        label="Gambar Latar",
        help_text="Gambar ini akan muncul sebagai latar belakang heading."
    )
    icon_choice = blocks.ChoiceBlock(
        choices=[(value, key) for key, value in FLOWBITE_ICONS.items()],
        required=False,
        label="Ikon",
        default=FLOWBITE_ICONS.get("calendar", ""),
        help_text="Pilih ikon visual untuk mendampingi judul."
    )

    class Meta:
        template = "blocks/heading-section.html"
        icon = "title"
        label = "Bagian Judul (Heading)"


class HeroBlock(BaseTitledBlock):
    title = blocks.RichTextBlock(
        required=False,
        features=['bold', 'italic', 'br'],
        label="Judul Hero",
        help_text="Judul besar di bagian atas halaman (mendukung baris baru)."
    )
    subtitle = blocks.RichTextBlock(
        required=False,
        features=['bold', 'italic', 'br'],
        label="Sub-judul Hero",
        help_text="Penjelasan singkat di bawah judul utama."
    )
    image = ImageChooserBlock(
        required=False,
        label="Gambar Hero",
        help_text="Gambar utama yang akan ditampilkan di section Hero."
    )

    class Meta:
        template = "blocks/hero-section.html"
        icon = "home"
        label = "Bagian Hero"


class TitledCardSectionBlock(BaseTitledBlock):
    cards = blocks.StreamBlock([
        ('card', BasicCardBlock(label="Kartu Biasa")),
        ('profile_card', ProfileCardBlock(label="Kartu Profil")),
    ], use_json_field=True, required=False, label="Kumpulan Kartu")

    class Meta:
        template = "blocks/titled-card-section.html"
        icon = "table"
        label = "Bagian Kartu Berjudul"


class HorizontalCardSectionBlock(TitledCardSectionBlock):
    class Meta:
        template = "blocks/horizontal-card-section.html"
        icon = "table"
        label = "Bagian Kartu Horizontal"


class MapsEmbedBlock(BaseTitledBlock):
    element = blocks.RawHTMLBlock(
        required=False,
        label="Kode Embed Maps",
        help_text="Salin kode iframe dari Google Maps (Share > Embed a map)."
    )

    class Meta:
        template = "blocks/maps-section.html"
        icon = "site"
        label = "Bagian Google Maps"


class TimelineBlocks(BaseTitledBlock):
    items = blocks.ListBlock(
        TimelineItemBlock(),
        label="Daftar Agenda Lini Masa"
    )

    class Meta:
        template = "blocks/timeline-sections.html"
        icon = "history"
        label = "Bagian Lini Masa"


class CarouselBlock(blocks.StructBlock):
    images = blocks.ListBlock(
        ImageChooserBlock(),
        label="Slide Gambar",
        help_text="Tambahkan beberapa gambar untuk slide yang berputar otomatis."
    )

    class Meta:
        template = "blocks/carousel-section.html"
        icon = "image"
        label = "Carousel/Slide"


# --- FINAL STREAMBLOCK ---

class BodyContentBlock(blocks.StreamBlock):
    hero_section = HeroBlock(label="Bagian Hero")
    card_section = TitledCardSectionBlock(label="Bagian Kartu Vertikal")
    horizontal_card_section = HorizontalCardSectionBlock(label="Bagian Kartu Horizontal")
    maps_section = MapsEmbedBlock(label="Peta Lokasi")
    heading_sections = HeadingBlock(label="Judul Halaman/Header")
    carousel_sections = CarouselBlock(label="Slide Gambar (Carousel)")
    faq_sections = FAQBlock(label="Tanya Jawab (FAQ)")
    timeline_sections = TimelineBlocks(label="Lini Masa/Sejarah")

    academic_sections = AcademicCalendarBlock(label="Kalender Akademik")
    schedule_sections = ScheduleBlock(label="Jadwal Pelajaran")

    class Meta:
        label = "Konten Halaman"
