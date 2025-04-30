import datetime
from scraper_utils import send_discord_message  # Ensure this import is correct
best_options = [
{'campsite': '010 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 9, 7, 0, 0), 'check_out': datetime.datetime(2025, 9, 11, 0, 0), 'nights': 4, 'check_in_str': 'September 07, 2025', 'check_out_str': 'September 11, 2025'},
{'campsite': '012 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 7, 2, 0, 0), 'check_out': datetime.datetime(2025, 7, 3, 0, 0), 'nights': 1, 'check_in_str': 'July 02, 2025', 'check_out_str': 'July 03, 2025'},
{'campsite': '014 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 9, 9, 0, 0), 'check_out': datetime.datetime(2025, 9, 11, 0, 0), 'nights': 2, 'check_in_str': 'September 09, 2025', 'check_out_str': 'September 11, 2025'},
{'campsite': '015 Pinecone Peninsula', 'check_in': datetime.datetime(2025, 9, 9, 0, 0), 'check_out': datetime.datetime(2025, 9, 11, 0, 0), 'nights': 2, 'check_in_str': 'September 09, 2025', 'check_out_str': 'September 11, 2025'},
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


# Create the "Best Campsite Options Found" message
message = "**🏕️Best Campsite Options Found:**\n"
for i, c in enumerate(best_options[:10], 1):
    # Check if the campsite is one of the specified ones
    star = "⭐" if any(num in c['campsite'] for num in ["014", "015", "016"]) else ""
    message += f"**{i}. {c['campsite']} {star}**\n"
    message += f"📅 {c['check_in_str']} to {c['check_out_str']} ({c['nights']} nights)\n\n"

# Truncate if message exceeds 2000 characters
if len(message) > 2000:
    message = message[:1970] + '...'

# Create the more concise "Other Options Found" message

more_message = "\n"
for i, c in enumerate(best_options[10:28], 11):
    more_message += f"**{i}. {c['campsite']}**{star} ({c['nights']} nights)\n"


# Truncate if more_message exceeds 2000 characters
if len(more_message) > 2000:
    more_message = more_message[:1970] + '...'

# Send the messages
send_discord_message(message)
send_discord_message(more_message)


