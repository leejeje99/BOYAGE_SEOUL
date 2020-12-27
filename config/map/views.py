from django.shortcuts import render
from .models import *
import csv, io
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings



def place_upload(request):
    # declaring template
    template = "map/place_upload.html"
    data = Place.objects.all()
    data2 = Seoul_detail.objects.all()
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, lat, lng, gu',
        'profiles': data,
        'profiles2': data2,
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if csv_file.name.startswith('1'):
        # messages.error(request, 'THIS IS NOT A CSV FILE')
        dataset = csv_file.read().decode('UTF-8')

        io_string = io.StringIO(dataset)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Place.objects.update_or_create(
                name=column[0],
                lat=column[1],
                lng=column[2],
                gu=column[3],
                image=column[4],
                description=column[5],

                formainlat=column[6],
                formainlng=column[7],
            )
        context = {}
        return render(request,template,context)

def main(request):
    places = Place.objects.all()
    print(settings.GOOGLE_MAPS_API_KEY)
    api = "https://maps.googleapis.com/maps/api/js?key=" + settings.GOOGLE_MAPS_API_KEY + "&language=en&callback=initMap&libraries=&v=weekly"
    context = {
        'places': places,
        'api_key' : api,
    }

    return render(request,'map/main.html',context=context)

def map_contents(request, pk):
    place = Place.objects.get(pk=pk)
    # placeimg = place.image
    placelat = place.lat
    placelng = place.lng
    placegu = place.gu
    _trip_url = place.trip_url


    youtubes = YoutubeData.objects.filter(place=place.id)
    tour_places = Seoul_detail.objects.filter(place=place.id)
    routes = detail_route.objects.filter(place=place.id)
    trips = TourReview.objects.filter(place=place.id)

    context = {
        'routes': routes,
        'tour_places': tour_places,
        'youtubes': youtubes,
        'placelat': placelat,
        'placelng': placelng,
        'placegu': placegu,
        'trips' : trips,
        'trip_url' : _trip_url,
    }
    return render(request, 'map/map_contents.html', context=context)

def search(request):
    words = request.POST.get("searchwords")

    places = Place.objects.filter(name__contains=words)
    search_result =[]
    name = []

    for place in places:
        if words in place.name:
            search_result.append(place.id)
            name = place.name

    context ={
        "search_result" : search_result,
        "name" : name,
    }

    return JsonResponse(context)