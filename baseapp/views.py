from django.shortcuts import render
import logging
from baseapp.management.predictbreed import predict_breed
from baseapp.models import Breed, Dog

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    logger.debug("baseapp.views.home")
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
        breed_result = Breed.objects.filter(name__in=breeds_predicted)
        breed_result_ids = [breed_result_id.pk for breed_result_id in breed_result]
        adoptable_result = Dog.objects.filter(breed_one_id__in = breed_result_ids).order_by('-adoption_speed')
        return render(request, 'recommend.html', {
            'breedpredicted': breeds_predicted,
            'dogs': adoptable_result
        })

    return render(request, 'home.html', {
        # Global variables
        #'global': getGlobalVariables(),

    })


