import requests
import os
from copy import deepcopy
from testMessage import sort_campsites
import pickle

PREVIOUS_RESULTS_FILE = "previous_campsite_results.pkl"

def send_discord_message(message, mention_role=False):
    webhook_url = os.getenv("WEB_HOOK")
    role_id = os.getenv("ROLE_ID")
    
    if not webhook_url:
        raise ValueError("WEB_HOOK environment variable not set")
    
    content = f"<@&{role_id}> {message}" if mention_role and role_id else message

    data = {
        "content": content,
        "allowed_mentions": {
            "roles": [role_id] if mention_role and role_id else []
        }
    }

    response = requests.post(webhook_url, json=data)
    
    if response.status_code != 204:
        raise RuntimeError(f"Failed to send message: {response.status_code}, {response.text}")


def broadcast_all_sorted(options):
    """
    Broadcast sorted campsite options in two messages:
    1. Top 10 options with detailed information
    2. Additional options (11-28) in a more concise format
    """
    sorted_options = sort_campsites(deepcopy(options))
    
    # First message with top 10 options
    message = "**🏕️ Best Campsite Options Found:**\n"
    for i, c in enumerate(sorted_options[:10], 1):
        star = "⭐" if any(num in c['campsite'] for num in ["014", "015", "016"]) else ""
        message += f"**{i}. {c['campsite']} {star}**\n"
        message += f"📅 {c['check_in_str']} to {c['check_out_str']} ({c['nights']} nights)\n\n"

    # Second message with additional options
    more_message = "**Other Options Found:**\n"
    for i, c in enumerate(sorted_options[10:28], 11):
        star = "⭐" if any(num in c['campsite'] for num in ["014", "015", "016"]) else ""
        more_message += f"**{i}. {c['campsite']}** {star} ({c['nights']} nights)\n"


    # Send the messages
    send_discord_message(message)
    send_discord_message(more_message)


def campsite_to_key(campsite):
    """Convert a campsite dict to a unique string key for comparison"""
    return f"{campsite['campsite']}_{campsite['check_in_str']}_{campsite['check_out_str']}"


def compare_campsite_lists(old_list, new_list):
    """
    Compare two lists of campsites and identify additions and removals
    Returns:
        - added_campsites: list of campsites in new_list but not in old_list
        - removed_campsites: list of campsites in old_list but not in new_list
    """
    old_dict = {campsite_to_key(item): item for item in old_list}
    new_dict = {campsite_to_key(item): item for item in new_list}
    
    added_keys = set(new_dict.keys()) - set(old_dict.keys())
    removed_keys = set(old_dict.keys()) - set(new_dict.keys())
    
    added_campsites = [new_dict[key] for key in added_keys]
    removed_campsites = [old_dict[key] for key in removed_keys]
    
    return added_campsites, removed_campsites


def broadcast_changes(old_options, new_options):
    """
    Compare old and new options and broadcast significant changes
    """
    # Sort both lists for fair comparison
    sorted_old = sort_campsites(deepcopy(old_options))
    sorted_new = sort_campsites(deepcopy(new_options))
    
    # Find additions and removals
    added_campsites, removed_campsites = compare_campsite_lists(sorted_old, sorted_new)
    
    # Check for priority campsites (014, 015, 016)
    priority_added = [c for c in added_campsites if any(num in c['campsite'] for num in ["014", "015", "016"])]
    
    # Check for July campsites
    july_added = [c for c in added_campsites if c['check_in'].month == 7]
    
    # Generate messages for changes
    changes_found = False
    
    # Priority campsite additions (always notify with role mention)
    if priority_added:
        changes_found = True
        message = "🚨 **PRIORITY CAMPSITE ALERT!** 🚨\n\n"
        message += "**New Priority Campsites Available:**\n"
        for i, c in enumerate(priority_added, 1):
            message += f"**{i}. {c['campsite']} ⭐**\n"
            message += f"📅 {c['check_in_str']} to {c['check_out_str']} ({c['nights']} nights)\n\n"
        send_discord_message(message, mention_role=True)
    
    # July campsite additions (notify with role mention)
    if july_added and not priority_added:  
        changes_found = True
        message = "**NEW JULY CAMPSITES AVAILABLE!**\n\n"
        for i, c in enumerate(july_added, 1):
            star = "⭐" if any(num in c['campsite'] for num in ["014", "015", "016"]) else ""
            message += f"**{i}. {c['campsite']} {star}**\n"
            message += f"📅 {c['check_in_str']} to {c['check_out_str']} ({c['nights']} nights)\n\n"
        send_discord_message(message, mention_role=True)
    
    # Other additions
    other_added = [c for c in added_campsites if c not in priority_added and c not in july_added]
    if other_added:
        changes_found = True
        message = "**New Campsites Available:**\n"
        for i, c in enumerate(other_added, 1):
            message += f"**{i}. {c['campsite']}**\n"
            message += f"📅 {c['check_in_str']} to {c['check_out_str']} ({c['nights']} nights)\n\n"
        send_discord_message(message)
    
    # Removals (if sites were removed)
    if removed_campsites:
        changes_found = True
        message = "**No Longer Available:**\n"
        for i, c in enumerate(removed_campsites, 1):
            star = "⭐" if any(num in c['campsite'] for num in ["014", "015", "016"]) else ""
            message += f"**{i}. {c['campsite']} {star}** - {c['check_in_str']} ({c['nights']} nights)\n"
        send_discord_message(message)
    
    # No changes message (optional)
    if not changes_found:
        print("No changes detected in campsite availability")
        send_discord_message("**Campsite Check:** No changes in availability since last check.")
    
    return changes_found

def save_results(options):
    """Save the current results to a file for future comparison"""
    try:
        with open(PREVIOUS_RESULTS_FILE, 'wb') as f:
            pickle.dump(options, f)
        print(f"Saved {len(options)} campsite options to {PREVIOUS_RESULTS_FILE}")
    except Exception as e:
        print(f"Error saving results: {e}")

def load_previous_results():
    """Load the previous results from file"""
    try:
        if os.path.exists(PREVIOUS_RESULTS_FILE):
            with open(PREVIOUS_RESULTS_FILE, 'rb') as f:
                options = pickle.load(f)
            print(f"Loaded {len(options)} previous campsite options from {PREVIOUS_RESULTS_FILE}")
            return options
        else:
            print(f"No previous results file found at {PREVIOUS_RESULTS_FILE}")
            return []
    except Exception as e:
        print(f"Error loading previous results: {e}")
        return []
    
def process_campsite_results(new_options):
    """Process new results, compare with previous, and broadcast changes"""
    previous_options = load_previous_results()
    
    if previous_options:
        broadcast_changes(previous_options, new_options)
    else:
        print("First run - broadcasting all available campsites")
        broadcast_all_sorted(new_options)

    save_results(new_options)
    



