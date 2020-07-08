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
        friendliness = int(postValues['friendlinessSelect'])
        exercise_needs = int(postValues['exerciseNeedsSelect'])
        trainability = int(postValues['trainabilitySelect'])
        apartment_living= int(postValues['apartmentLivingSelect'])
        affectionate_with_family = int(postValues['affectationFamilySelect'])
        groom = int(postValues['groomingSelect'])
        energy = int(postValues['energySelect'])
        intelligence = int(postValues['intelligenceSelect'])
        sensitivity_lvl = int(postValues['sensitivitySelect'])
        size = int(postValues['sizeSelect'])
        bark_howl_tendency = int(postValues['barkingSelect'])
        being_alone = int(postValues['aloneSelect'])
        breeds_predicted = predict_breed(friendliness, exercise_needs, trainability,apartment_living, affectionate_with_family,
                                         groom, energy, intelligence, sensitivity_lvl, size, bark_howl_tendency, being_alone)
        breed_result = Breed.objects.filter(csv_id__in=breeds_predicted)
        breed_result_ids = [breed_result_id.pk for breed_result_id in breed_result]
        adoptable_result = Dog.objects.filter(breed_one_id__in = breed_result_ids).order_by('-adoption_speed')
        return render(request, 'recommend.html', {
            'breed': breed_result,
            'dogs': adoptable_result
        })

    return render(request, 'home.html', {
        # Global variables
        #'global': getGlobalVariables(),

    })


