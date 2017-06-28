#!/usr/bin/python3

# Homework for kiwi.com weekend application
# Author: Ladislav Dobrovsky  (ladislav.dobrovsky@gmail.com)


import requests
from datetime import datetime, timedelta
import enum


class SortType(enum.Enum):
    Cheapest = 0
    Shortest = 1

__endpoint_flights = 'https://api.skypicker.com/flights'
__endpoint_book = 'http://37.139.6.125:8080/booking'
__search_date_format = '%d/%m/%Y'


def find_flight(from_str, to_str, date, return_nights=-1, sort_type=SortType.Cheapest):
    params = {'flyFrom': from_str,
              'to': to_str,
              'dateFrom': date.strftime(__search_date_format),
              'dateTo': date.strftime(__search_date_format),
              'currency': 'CZK',
              'booking_token': 'hashed%20data',
              'passengers': 1,
              'adults': 1
              }

    if return_nights >= 0:
        return_date_str = (date + timedelta(days=return_nights)).strftime(__search_date_format)
        params['returnFrom'] = return_date_str
        params['returnTo'] = return_date_str

    if sort_type == SortType.Cheapest:
        params['asc'] = 1
    elif sort_type == SortType.Shortest:
        params['asc'] = 0
    else:
        raise RuntimeError('sorting shinanigens not allowed')

    r = requests.get(__endpoint_flights, params=params)

    flights = r.json()['data']

    try:
        if sort_type == SortType.Cheapest:
            return flights[0]  # should be sorted by 'asc'
        elif sort_type == SortType.Shortest:
            return sorted(flights, key=lambda item: item['distance'])[0]
    except IndexError:
        return None


def book_flight(from_str, to_src, date, booking_token='hashed%20data', return_nights=-1):

    payload = {'flyFrom': from_str,
               'to': to_src,
               'dateFrom': date.strftime('%d/%m/%Y'),
               'dateTo': date.strftime('%d/%m/%Y'),
               'currency': 'CZK',
               'booking_token': booking_token,
               'passengers': [{'title': 'Mr',
                               'firstName': 'John',
                               'lastName': 'Doe',
                               'documentID': '123456',
                               'birthday': '1985-05-05',
                               'email': 'john.doe@mailnull.com'}],
               }

    if return_nights >= 0:
        return_date_str = (date + timedelta(days=return_nights)).strftime(__search_date_format)
        payload['returnFrom'] = return_date_str
        payload['returnTo'] = return_date_str

    r = requests.post(__endpoint_book, json=payload)
    # print(r.json())
    return r.json()


if __name__ == '__main__':
    from datetime import datetime, timedelta
    #flight = find_flight('BCN', 'DUB', datetime.now()+timedelta(days=1), sort_type=SortType.Shortest)
    #flight = find_flight('BCN', 'DUB', datetime.now()+timedelta(days=1), sort_type=SortType.Cheapest)
    #flight = find_flight('LHR', 'DXB', datetime.now()+timedelta(days=1), sort_type=SortType.Cheapest)
    flight = find_flight('LHR', 'DXB', datetime.now() + timedelta(days=1), sort_type=SortType.Cheapest, return_nights=4)
    print(flight)
    print(flight['booking_token'])
    print(flight['distance'])
    #book_flight('BCN', 'DUB', datetime.now()+timedelta(days=1))
    book_flight('LHR', 'DXB', datetime.now() + timedelta(days=1), booking_token=flight['booking_token'], return_nights=4)

