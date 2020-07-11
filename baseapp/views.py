from django.shortcuts import render
import logging
from baseapp.management.predictbreed import predict_breed
from baseapp.models import Breed, Dog

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    # logger.debug("baseapp.views.home")
    if request.method == 'POST':
        logger.debug(request.POST)
        postValues = request.POST.copy()
        adaptability = int(postValues['adaptabilitySelect'])
        energy = int(postValues['energySelect'])
        friendliness = int(postValues['friendlinessSelect'])
        health_grooming = int(postValues['health_groomingSelect'])
        trainability = int(postValues['trainabilitySelect'])
        size = int(postValues['sizeSelect'])
        breeds_predicted = predict_breed(adaptability, energy, friendliness, health_grooming, trainability, size)
        top_breed = Breed.objects.filter(name=breeds_predicted[0])[0]

        topbar_values = {
            "adaptability": int((top_breed.adaptability / 5) * 100),
            "energy": int((top_breed.energy / 5) * 100),
            "friendliness": int((top_breed.friendliness / 5) * 100),
            "health_grooming": int((top_breed.health_grooming / 5) * 100),
            "trainability": int((top_breed.trainability / 5) * 100),
            "size": int((top_breed.size / 5) * 100)
        }

        breed_result = Breed.objects.filter(name__in=breeds_predicted)
        breed_result_ids = [breed_result_id.pk for breed_result_id in breed_result]
        primary_result = Dog.objects.filter(breed_one_id__in=breed_result_ids)
        secondary_result = Dog.objects.filter(breed_two__in=breed_result_ids)
        adoptable_result = primary_result.union(secondary_result)
        breeds_predicted.pop(0)
        other_breeds = Breed.objects.filter(name__in=breeds_predicted)
        return render(request, 'recommend.html', {
            'topbreed': top_breed,
            'topbar_values': topbar_values,
            'other_breeds': other_breeds,
            'breedpredicted': breed_result,
            'dogs': adoptable_result
        })

    return render(request, 'home.html', {

    })
