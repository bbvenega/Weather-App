
from django.shortcuts import render
from django.http import HttpResponse
from weatherApp import main


def index(request):
    return render(request, 'index.html')

def weather_result(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        forecast_type = request.POST.get('forecast_type')
        if address and forecast_type: 
            periods = main(address, forecast_type)
            return render(request, 'weather_result.html', {'periods': periods})
        else:
            return HttpResponse('Please provide an address.')
    else:
        return HttpResponse('Method not allowed')
        
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')

