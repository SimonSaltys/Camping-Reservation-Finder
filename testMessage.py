from copy import deepcopy

# best_options_new = [
# {'campsite': '010 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 9, 7, 0, 0), 'check_out': datetime.datetime(2025, 9, 11, 0, 0), 'nights': 4, 'check_in_str': 'September 07, 2025', 'check_out_str': 'September 11, 2025'},
# {'campsite': '012 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 7, 2, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 1, 'check_in_str': 'July 02, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '014 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 9, 9, 0, 0), 'check_out': datetime.datetime(2025, 9, 11, 0, 0), 'nights': 2, 'check_in_str': 'September 09, 2025', 'check_out_str': 'September 11, 2025'},
# {'campsite': '015 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 9, 9, 0, 0), 'check_out': datetime.datetime(2025, 9, 11, 0, 0), 'nights': 2, 'check_in_str': 'September 09, 2025', 'check_out_str': 'September 11, 2025'},
# {'campsite': '016 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 9, 15, 0, 0), 'check_out': datetime.datetime(2025, 9, 18, 0, 0), 'nights': 3, 'check_in_str': 'September 15, 2025', 'check_out_str': 'September 18, 2025'},
# {'campsite': '019 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 2, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 1, 'check_in_str': 'July 02, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '020 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '021 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 2, 0, 0), 'nights': 1, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 02, 2025'},
# {'campsite': '022 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '023 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 6, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 4, 'check_in_str': 'July 06, 2025', 'check_out_str': 'July 10, 2025'},
# {'campsite': '024 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '025 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '027 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 2, 0, 0), 'nights': 1, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 02, 2025'},
# {'campsite': '028 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '030 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 8, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 2, 'check_in_str': 'July 08, 2025', 'check_out_str': 'July 10, 2025'},
# {'campsite': '033 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 2, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 1, 'check_in_str': 'July 02, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '034 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 9, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 1, 'check_in_str': 'July 09, 2025', 'check_out_str': 'July 10, 2025'},
# {'campsite': '035 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 2, 0, 0), 'nights': 1, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 02, 2025'},
# {'campsite': '038 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 2, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 1, 'check_in_str': 'July 02, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '066 Sierra Spur', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '067 Sierra Spur', 'check_in': datetime.datetime(2025, 7, 9, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 1, 'check_in_str': 'July 09, 2025', 'check_out_str': 'July 10, 2025'},
# {'campsite': '068 Sierra Spur', 'check_in': datetime.datetime(2025, 7, 21, 0, 0), 'check_out': datetime.datetime(2025, 7, 22, 0, 0), 'nights': 1, 'check_in_str': 'July 21, 2025', 'check_out_str': 'July 22, 2025'},
# {'campsite': '069 Sierra', 'check_in': datetime.datetime(2025, 10, 1, 0, 0), 'check_out': datetime.datetime(2025, 10, 2, 0, 0), 'nights': 1, 'check_in_str': 'October 01, 2025', 'check_out_str': 'October 02, 2025'},
# {'campsite': '070 Sierra', 'check_in': datetime.datetime(2025, 8, 6, 0, 0), 'check_out': datetime.datetime(2025, 8, 7, 0, 0), 'nights': 1, 'check_in_str': 'August 06, 2025', 'check_out_str': 'August 07, 2025'},
# {'campsite': '070 C Sierra', 'check_in': datetime.datetime(2025, 7, 9, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 1, 'check_in_str': 'July 09, 2025', 'check_out_str': 'July 10, 2025'},
# {'campsite': '138 Chimney', 'check_in': datetime.datetime(2025, 7, 16, 0, 0), 'check_out': datetime.datetime(2025, 7, 17, 0, 0), 'nights': 1, 'check_in_str': 'July 16, 2025', 'check_out_str': 'July 17, 2025'},
# {'campsite': '139 Chimney', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
# {'campsite': '140 Chimney', 'check_in': datetime.datetime(2025, 7, 16, 0, 0), 'check_out': datetime.datetime(2025, 7, 17, 0, 0), 'nights': 1, 'check_in_str': 'July 16, 2025', 'check_out_str': 'July 17, 2025'}
# ]




def sort_campsites(options):
    """
    Sort campsites with the following priority:
    1. Campsites 014, 015, 016 Pinecone Peninsula first (in that order)
    2. Check-in dates in July
    3. Highest number of nights
    """

    priority_campsites = {
        "014 Pinecone Peninsula": 1,
        "015 Pinecone Peninsula": 2,
        "016 Pinecone Peninsula": 3
    }

    def get_sort_key(option):
        # First priority: 014, 015, 016 campsites
        campsite_priority = priority_campsites.get(option['campsite'], 999)
        
        # Second priority: check-in dates in July (month = 7)
        is_july = 0 if option['check_in'].month == 7 else 1
        
        # Third priority: higher number of nights (negative for descending order)
        nights_priority = -option['nights']
        
        return (campsite_priority, is_july, nights_priority, option['campsite'])
    
    return sorted(options, key=get_sort_key)
