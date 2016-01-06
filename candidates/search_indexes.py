from haystack import indexes

from popolo.models import Person


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
