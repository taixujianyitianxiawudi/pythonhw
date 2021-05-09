def get_businesses(query, api_key, min_rating= 0.0, max_results = 30):
    import requests
    url=  "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s" % (query, api_key)
    print(url)
    #fetching informations
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                response_data = response.json()
            except:
                print("Response not in valid JSON format")
        else:
            print("HTTP error",response.status_code)
    except:
        print("Something went wrong with requests.get")
    results = response_data['results']
    results_list = []
    condition = True
    count = 0
    #adding results to list
    while condition:
        for result in results:
            rating = result.get('rating')
            if rating >= min_rating and condition:
                name = result['name']
                address = result['formatted_address']
                opening_hours =  result.get('opening_hours')
                price = result.get('price_level')
                rating = result.get('rating')
                results_list.append((name,address,opening_hours,price,rating))
                count = count + 1
                if count == max_results:
                    condition = False
                    print("received %s objects" % count)
            else:
                continue
        next_page_token = response_data.get('next_page_token')
        if next_page_token:
            new_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=%s&pagetoken=%s" % (api_key, next_page_token)
            #fetching new pages
            response = requests.get(new_url)
            while response.json().get('status') != 'OK':
                from time import sleep
                from random import random
                sleep(random())
                response = requests.get(new_url)
            response_data = response.json()
            results = response_data['results']
        else:
            condition = False
            print("received %s objects" % count)
    return results_list

api_key = 'AIzaSyC8CyCGw_hWlLAeL8qjn6SBQD_Drk2kgIA'
query = "restaurants near Columbia University"
result123 = get_businesses(query, api_key, min_rating= 0.0, max_results = 30)
print(result123)