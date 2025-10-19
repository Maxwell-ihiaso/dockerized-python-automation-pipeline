from typing import Iterable, List, Dict, Any

def filter_https(entries: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Return a list of dictionaries that have an "HTTPS" field.

    This function will iterate through an iterable of dictionaries and return a list of dictionaries that have an "HTTPS" field.

    Args:
        entries (Iterable[Dict[str, Any]]): An iterable of dictionaries.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries with an "HTTPS" field.
    """
    return [e for e in entries if bool(e.get("HTTPS"))]

def select_fields(entries: Iterable[Dict[str, Any]], fields: List[str]) -> List[Dict[str, Any]]:
    """
    Return a list of dictionaries that have been filtered to only include the specified fields.

    This function will iterate through an iterable of dictionaries and return a list of dictionaries that only include the specified fields.

    Args:
        entries (Iterable[Dict[str, Any]]): An iterable of dictionaries.

        fields (List[str]): A list of strings that are field names to be included in the filtered dictionaries.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries that have been filtered to only include the specified fields.
    """
    out = []
    for e in entries:
        out.append({k: e.get(k) for k in fields})
    return out
