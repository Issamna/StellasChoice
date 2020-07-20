from django.shortcuts import render
import logging
from baseapp.management.predictbreed import predict_breed
from baseapp.models import Breed, Dog
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from baseapp.management.predictadoptionspeed import predict_speed

logger = logging.getLogger(__name__)


def home(request):
    # logger.debug("baseapp.views.home")

    # Form submit
    if request.method == 'POST':
        logger.info(request.POST)
        # Get values
        postValues = request.POST.copy()
        adaptability = int(postValues['adaptabilitySelect'])
        energy = int(postValues['energySelect'])
        friendliness = int(postValues['friendlinessSelect'])
        health_grooming = int(postValues['health_groomingSelect'])
        trainability = int(postValues['trainabilitySelect'])
        size = int(postValues['sizeSelect'])
        # Predict breed using values
        breeds_predicted = predict_breed(adaptability, energy, friendliness, health_grooming, trainability, size)
        # Get top breed predicted
        top_breed = Breed.objects.filter(name=breeds_predicted[0])[0]
        # Convert top breed predicted data to percentage for bar
        topbar_values = {
            "adaptability": int((top_breed.adaptability / 5) * 100),
            "energy": int((top_breed.energy / 5) * 100),
            "friendliness": int((top_breed.friendliness / 5) * 100),
            "health_grooming": int((top_breed.health_grooming / 5) * 100),
            "trainability": int((top_breed.trainability / 5) * 100),
            "size": int((top_breed.size / 5) * 100)
        }
        # Find breed data from database
        breed_result = Breed.objects.filter(name__in=breeds_predicted)
        # Get primary keys of predicted breeds
        breed_result_ids = [breed_result_id.pk for breed_result_id in breed_result]
        # Get adoptable dogs matching its first breeds matching predicted
        primary_result = Dog.objects.filter(breed_one_id__in=breed_result_ids)
        # Get adoptable dogs matching its second breeds matching predicted
        secondary_result = Dog.objects.filter(breed_two_id__in=breed_result_ids)
        # Union both
        adoptable_result = primary_result.union(secondary_result)
        # Remove top breed
        breeds_predicted.pop(0)
        # Other four breeds
        other_breeds = Breed.objects.filter(name__in=breeds_predicted)
        # Return recommend page with data
        return render(request, 'recommend.html', {
            'topbreed': top_breed,
            'topbar_values': topbar_values,
            'other_breeds': other_breeds,
            'breedpredicted': breed_result,
            'dogs': adoptable_result
        })

    return render(request, 'home.html', {

    })


def datavisual(request):
    # Get all breed data
    all_breeds = Breed.objects.all()
    # Create empty arrays to transfer data
    adaptability_count = [0, 0, 0, 0, 0]
    adaptability_lists = [[], [], [], [], []]
    energy_count = [0, 0, 0, 0, 0]
    energy_lists = [[], [], [], [], []]
    friendliness_count = [0, 0, 0, 0, 0]
    friendliness_lists = [[], [], [], [], []]
    health_grooming_count = [0, 0, 0, 0, 0]
    health_grooming_lists = [[], [], [], [], []]
    trainability_count = [0, 0, 0, 0, 0]
    trainability_lists = [[], [], [], [], []]
    size_count = [0, 0, 0, 0, 0]
    size_lists = [[], [], [], [], []]
    # Loop through data and fill arrays
    for breed in all_breeds:
        adaptability_count[breed.adaptability - 1] += 1
        adaptability_lists[breed.adaptability - 1].append(breed.name)
        energy_count[breed.energy - 1] += 1
        energy_lists[breed.energy - 1].append(breed.name)
        friendliness_count[breed.friendliness - 1] += 1
        friendliness_lists[breed.friendliness - 1].append(breed.name)
        health_grooming_count[breed.health_grooming - 1] += 1
        health_grooming_lists[breed.health_grooming - 1].append(breed.name)
        trainability_count[breed.trainability - 1] += 1
        trainability_lists[breed.trainability - 1].append(breed.name)
        size_count[breed.size - 1] += 1
        size_lists[breed.size - 1].append(breed.name)

    # Get all adoptable dogs
    all_dogs = Dog.objects.all()
    # Create empty arrays to transfer data
    adoption_speed_count = [0, 0]
    # Loop through data and fill arrays
    for dog in all_dogs:
        adoption_speed_count[dog.adoption_speed - 1] += 1
    adoption_speed_count = [adoption_speed_count[1],adoption_speed_count[0]]
    # Return datavisual page with data
    return render(request, 'datavisual.html', {
        'adaptability_count': adaptability_count,
        'energy_count': energy_count,
        'friendliness_count': friendliness_count,
        'health_grooming_count': health_grooming_count,
        'trainability_count': trainability_count,
        'size_count': size_count,
        'adaptability_lists': adaptability_lists,
        'energy_lists': energy_lists,
        'friendliness_lists': friendliness_lists,
        'health_grooming_lists': health_grooming_lists,
        'trainability_lists': trainability_lists,
        'size_lists': size_lists,
        'adoption_speed_count': adoption_speed_count
    })


def about(request):
    return render(request, 'about.html', {

    })


def alldogs(request):
    # Get all dog data
    all_dogs = Dog.objects.all()
    return render(request, 'alldogs.html', {
        'all_dogs': all_dogs
    })


def pdf_view(request):
    # Request file and return for download
    fs = FileSystemStorage()
    filename = 'baseapp/static/Capstone Document.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Capstone Document.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')


@csrf_exempt
def ajax_adoption_speed(request):
    logger.info("baseapp.views.ajax_adoption_speed: POST")
    logger.info(request.POST)
    json_data = {}
    json_data['answer'] = "over"
    try:
        json_data = {}
        # Get data from frontend
        postValues = request.POST.copy()
        age = int(postValues['age'])
        breed2 = int(postValues['mixed'])
        gender = int(postValues['gender'])
        size = int(postValues['size'])
        dewormed = int(postValues['dewormed'])
        health = int(postValues['health'])
        # predict speed
        adoption_speed = predict_speed(age, breed2, gender, size, dewormed, health)
        if adoption_speed == 0:
            adoption_speed_return = "under"
        else:
            adoption_speed_return = "over"
        # Return answer
        json_data['answer'] = adoption_speed_return
    except Exception as e:
        logger.info('%s (%s)' % (e.message, type(e)))
    return JsonResponse(json_data, safe=False)

