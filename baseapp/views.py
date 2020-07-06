from django.shortcuts import render
import logging
from baseapp.management.predictbreed import predict_breed
logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    logger.debug("rowdata.views.home")

    return render(request, 'home.html', {
        # Global variables
        #'global': getGlobalVariables(),

    })


def recommend(request):
    logger.debug("rowdata.views.recommend")

    return render(request, 'recommend.html', {
        # Global variables
        # 'global': getGlobalVariables(),

    })