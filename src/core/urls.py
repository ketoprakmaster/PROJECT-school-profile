from django.conf import settings
from django.urls import include, path
from django.contrib import admin



from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("django-cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),

    path("api/school/", include("school.urls")),
    path("api/chat", include("chatbot.urls")),


    # Wagtail's router will handle all other page URLs
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
