from userresource.models import *


def index(request):
    return


def get_user_resources(request, userID, getType, getTitle, count, getTime):
    getData = getResource()
    getData.userID = userID
    getData.getType = getType
    getData.getTitle = getTitle
    getData.count = count
    getData.time = getTime
    getData.save()


def expend_user_resource(request, userID, expendType, count):
    expendData = expendResource()
    expendData.userID = userID
    expendData.expendType = expendType
    expendData.count = count
    expendData.save()
