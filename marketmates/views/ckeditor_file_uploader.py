import os
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.views import get_storage_class, image_verify, \
    NoImageException

storage = get_storage_class()


def overrided_handle_uploaded_file(file):
    """Handles file uploads by renaming the file to a UUID while preserving its extension."""
    file_storage = storage()
    ext = os.path.splitext(file.name)[1]
    file_uuid = f"{uuid.uuid4()}{ext}"
    upload_path = os.path.join("uploads", file_uuid)
    filename = file_storage.save(upload_path, file)
    return file_storage.url(filename)


@require_POST
def ckeditor_file_uploader(request):
    """Handles the upload request for CKEditor 5."""
    form = UploadFileForm(request.POST, request.FILES)
    allow_all_file_types = getattr(settings, "CKEDITOR_5_ALLOW_ALL_FILE_TYPES",
                                   False)

    if not allow_all_file_types:
        try:
            image_verify(request.FILES["upload"])
        except NoImageException as ex:
            return JsonResponse({"error": {"message": f"{ex}"}}, status=400)

    if form.is_valid():
        url = overrided_handle_uploaded_file(request.FILES["upload"])
        return JsonResponse({"url": url})

    if form.errors["upload"]:
        return JsonResponse(
            {"error": {"message": form.errors["upload"][0]}},
            status=400,
        )

    return JsonResponse({"error": {"message": _("Invalid form data")}},
                        status=400)
