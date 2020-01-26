import requests
import bs4


def get_list_of_hotels(city_name):
    hotel_list_query = 'https://www.tripexpert.com/'+ city_name +'/hotels/'
    result = requests.get(hotel_list_query)
    soup = bs4.BeautifulSoup(result.text, 'lxml')

    hotels = soup.findAll('div', class_="hotel_img fleft clearfix")
    list_of_hotels = list()
    for hotel in hotels:
        list_of_hotels.append(hotel.find('a')['href'].split('/')[-1])

    return list_of_hotels

def get_details(city_name, hotel_name):
    main_dict = dict()
    hotel_list_query = 'https://www.tripexpert.com/'+ city_name +'/hotels/'+ hotel_name
    result = requests.get(hotel_list_query)
    soup = bs4.BeautifulSoup(result.text, 'lxml')

    match = soup.find('div', class_='score_badge')
    score = match.div.b.text
    main_dict['hotel_score'] = score

    recommendations = soup.findAll('h1', class_='venue-mention-title')
    recommendations_score = soup.findAll('span', class_= 'venue-mention-badge')

    name = soup.find('div', class_='hotel_head')
    main_dict['hotel_name'] = name.h1.text

    reviews = soup.findAll('div', class_='fleft review_content')
    review_dict = dict()
    for review in reviews:
        review_title = review.h3.text.replace('\n','')
        review_content = review.p.span.text
        review_dict[review_title] = review_content
        #print(review_title,": ",review_content)
    main_dict['reviews'] = review_dict

    recommendation_dict = dict()
    for recommendation, score in zip(recommendations, recommendations_score):
        recommended_hotel=recommendation.text
        score = score.text
        recommendation_dict[recommended_hotel] = score

    main_dict['recommendations'] = recommendation_dict
    return main_dict

def get_list_of_cities():
    city_list = []
    city_list_query = 'https://www.tripexpert.com/destinations'
    result = requests.get(city_list_query)
    soup = bs4.BeautifulSoup(result.text, 'lxml')

    cities = soup.findAll('div', class_='destinations_title')
    for city in cities:
        city_list.append(city.find('h4').text)
    return city_list