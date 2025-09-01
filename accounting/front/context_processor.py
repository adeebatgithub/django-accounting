from datetime import datetime


def global_data(request):
    return {
        "TODAY": datetime.now().date(),
    }