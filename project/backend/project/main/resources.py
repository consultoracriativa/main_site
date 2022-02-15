from import_export import resources

from .models import ContentContent


class ContentResource(resources.ModelResource):
    class Meta:
        model = ContentContent
