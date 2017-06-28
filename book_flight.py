#!/usr/bin/python3

# Homework for kiwi.com weekend application
# Author: Ladislav Dobrovsky  (ladislav.dobrovsky@gmail.com)

import argparse
import flights_api
from datetime import datetime, timedelta
import sys

argparse.Namespace

args_parser = argparse.ArgumentParser(description='Flight search program')
args_parser.add_argument('--from')
args_parser.add_argument('--date')
args_parser.add_argument('--to')
groupA = args_parser.add_mutually_exclusive_group()
groupA.add_argument('--one-way', action="store_true")
groupA.add_argument('--return', type=int)
groupB = args_parser.add_mutually_exclusive_group()
groupB.add_argument('--cheapest', action="store_true")
groupB.add_argument('--shortest', action="store_true")

args = args_parser.parse_args()

# cheapest is default
if not getattr(args, 'shortest') and not getattr(args, 'cheapest'):
    setattr(args, 'cheapest', True)

sort_type = flights_api.SortType.Cheapest if getattr(args, 'cheapest') else flights_api.SortType.Shortest

from_str = getattr(args, 'from')
to_str = getattr(args, 'to')
# one-way is default
return_nights = -1 if getattr(args, 'one_way') or getattr(args, 'return') is None else getattr(args, 'return')
date = datetime.strptime(getattr(args, 'date'), '%Y-%m-%d')

# call the API after all arguments are evaluated and checked

flight = flights_api.find_flight(from_str, to_str, date, return_nights, sort_type)
if flight:
    booking = flights_api.book_flight(from_str, to_str, date, flight['booking_token'], return_nights)
    if 'pnr' in booking:
        print(booking['pnr'])
        if 'status' not in booking or booking['status'] != 'confirmed':
            print('WARNING: PNR received, however status is not confirmed!', file=sys.stderr)
    else:
        print('ERROR: Cannot book flight', file=sys.stderr)
        print('   booking:', repr(booking), file=sys.stderr)
else:
    print('ERROR: No suitable flight found', file=sys.stderr)
