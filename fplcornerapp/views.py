from django.shortcuts import render
from .models import Fpldata

# Create your views here.


def test_view(request):
    data = Fpldata.objects.order_by('-import_date')
    out = data[0]
    return render(request, 'fplcornerapp/test.html', {'out': out})
