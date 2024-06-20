import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings

@login_required
@api_view(['GET'])
def news(request):
    # query = request.data

    # url = "https://api.newscatcherapi.com/v2/search"

    # querystring = {"q":query,"lang":"en","sort_by":"relevancy","page":"1",}

    # headers = {
    #     "x-api-key": 
    #     }

    # response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response)  # Parse the JSON response

    # response_data= []
    # if response.status_code == 200:
    #     response_data = response.json()
    #     return Response(response_data)

    #     articles = response_data.get('articles')
    
    # paginator = Paginator(articles,10)
    # content = list(paginator.get_page(1))
    # return Response(content)
    return Response()


@login_required
@api_view(['GET'])
def weather(request):
    location='kochi'

    url = "https://api.tomorrow.io/v4/weather/forecast" 
    querystring = {
        "location": location,
        "timesteps": ["1h", "1d"],
        "apikey": settings.WEATHER_APIKEY
    }
    headers = {"accept": "application/json"}

    response = requests.get(url,params=querystring, headers=headers)
    content = response.json()

    return Response(content)