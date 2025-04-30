from discord_utils import process_campsite_results
import datetime
from dotenv import load_dotenv

test_options = [
{'campsite': '010 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 7, 7, 0, 0), 'check_out': datetime.datetime(2025, 7, 14, 0, 0), 'nights': 7, 'check_in_str': 'July 07, 2025', 'check_out_str': 'July 14, 2025'},
{'campsite': '012 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 7, 2, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 1, 'check_in_str': 'July 02, 2025', 'check_out_str': 'July 03, 2025'},

{'campsite': '014 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 6, 10, 0, 0), 'check_out': datetime.datetime(2025, 6, 15, 0, 0), 'nights': 5, 'check_in_str': 'June 10, 2025', 'check_out_str': 'June 15, 2025'},

{'campsite': '015 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 7, 9, 0, 0), 'check_out': datetime.datetime(2025, 7, 15, 0, 0), 'nights': 6, 'check_in_str': 'July 09, 2025', 'check_out_str': 'July 15, 2025'},
{'campsite': '016 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 9, 15, 0, 0), 'check_out': datetime.datetime(2025, 9, 18, 0, 0), 'nights': 3, 'check_in_str': 'September 15, 2025', 'check_out_str': 'September 18, 2025'},
{'campsite': '019 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 2, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 1, 'check_in_str': 'July 02, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '020 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '021 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 2, 0, 0), 'nights': 1, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 02, 2025'},
{'campsite': '022 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '023 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 6, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 4, 'check_in_str': 'July 06, 2025', 'check_out_str': 'July 10, 2025'},
{'campsite': '024 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '025 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '027 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 2, 0, 0), 'nights': 1, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 02, 2025'},
{'campsite': '028 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '030 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 8, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 2, 'check_in_str': 'July 08, 2025', 'check_out_str': 'July 10, 2025'},
{'campsite': '033 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 2, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 1, 'check_in_str': 'July 02, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '034 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 9, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 1, 'check_in_str': 'July 09, 2025', 'check_out_str': 'July 10, 2025'},
{'campsite': '035 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 2, 0, 0), 'nights': 1, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 02, 2025'},
{'campsite': '038 Pinecone Strip', 'check_in': datetime.datetime(2025, 7, 2, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 1, 'check_in_str': 'July 02, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '066 Sierra Spur', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '067 Sierra Spur', 'check_in': datetime.datetime(2025, 7, 9, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 1, 'check_in_str': 'July 09, 2025', 'check_out_str': 'July 10, 2025'},
{'campsite': '068 Sierra Spur', 'check_in': datetime.datetime(2025, 7, 21, 0, 0), 'check_out': datetime.datetime(2025, 7, 22, 0, 0), 'nights': 1, 'check_in_str': 'July 21, 2025', 'check_out_str': 'July 22, 2025'},
{'campsite': '069 Sierra', 'check_in': datetime.datetime(2025, 10, 1, 0, 0), 'check_out': datetime.datetime(2025, 10, 2, 0, 0), 'nights': 1, 'check_in_str': 'October 01, 2025', 'check_out_str': 'October 02, 2025'},
{'campsite': '070 Sierra', 'check_in': datetime.datetime(2025, 8, 6, 0, 0), 'check_out': datetime.datetime(2025, 8, 7, 0, 0), 'nights': 1, 'check_in_str': 'August 06, 2025', 'check_out_str': 'August 07, 2025'},
{'campsite': '070 C Sierra', 'check_in': datetime.datetime(2025, 7, 9, 0, 0), 'check_out': datetime.datetime(2025, 7, 10, 0, 0), 'nights': 1, 'check_in_str': 'July 09, 2025', 'check_out_str': 'July 10, 2025'},
{'campsite': '138 Chimney', 'check_in': datetime.datetime(2025, 7, 16, 0, 0), 'check_out': datetime.datetime(2025, 7, 17, 0, 0), 'nights': 1, 'check_in_str': 'July 16, 2025', 'check_out_str': 'July 17, 2025'},
{'campsite': '139 Chimney', 'check_in': datetime.datetime(2025, 7, 1, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 2, 'check_in_str': 'July 01, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '140 Chimney', 'check_in': datetime.datetime(2025, 7, 16, 0, 0), 'check_out': datetime.datetime(2025, 7, 17, 0, 0), 'nights': 1, 'check_in_str': 'July 16, 2025', 'check_out_str': 'July 17, 2025'}
]
load_dotenv()
process_campsite_results(test_options)