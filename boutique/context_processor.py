from boutique.models import Categorie

def categories_context(request):
    
    categories = Categorie.objects.all().order_by('nom')
    return {'categories': categories}