import re

def case_insensitive(flags):
    return "i" in flags


def regex(flags):
    return "r" in flags


def partial(flags):
    return "p" in flags


def extract_query(text):
    flags = ""
    if "|" in search_string:
        query, flags, *_ = search_string.split("|")
    else:
        query = search_string
    return query, flags


def search_json(json_data, search_string):
    """
    Search for users based on the provided query.

    Supports:
    1. Exact Search: Matches the user exactly (e.g., "User 149").
    2. Case Insensitive Search: Use " | i" (e.g., "user 149 | i").
    3. Regex Search: Use " | r" (e.g., "User 1[0-9]9 | r").
    4. Partial Regex Search: Use " | p" (e.g., "User 14 | p").

    Args:
        json_data (list): List of user strings to search.
        search_string (str): The search query with optional flags.

    Returns:
        list: Matching users.
    """
    
    results = []
    query, flags = extract_query(search_json)
    query = query.strip()
    for user in json_data:
        user_id = user.get("User")

        if regex(flags):
            pattern = re.compile(query)
            if bool(pattern.search(user_id)):
                results.append(user)
            else:
                continue

        if case_insensitive(flags):
            user_id = user_id.lower()
            query = query.lower()
        
        if partial(flags):
            if query in user_id:
                results.append(user)
        elif user_id == query:
            results.append(user)

    return results

# Tests
# User 149
# user 149
# user 149 | i
# User 1[0-9]9 | r
# User 14 | p