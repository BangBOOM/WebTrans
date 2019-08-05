from django.db.models import Lookup

class SimilarLookup(Lookup):
    lookup_name = 'similar_lookup'

