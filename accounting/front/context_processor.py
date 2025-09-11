from datetime import datetime

from accounting import models

def global_data(request):
    return {
        "TODAY": datetime.now().date(),
    }