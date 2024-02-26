"""A Series of functions allowing the retrieval of data from the CTC CMS API"""

# from dotenv import load_dotenv
import json
import math
from datetime import date, datetime, timedelta
from time import perf_counter, sleep

import requests

from Logging.ctc_logging import CTCLog
from utils.read_file import read_file

# load_dotenv()

## Current list of constants before settings file is implemented
API_SETTINGS = read_file("APICore_Connection\\Settings.json")

ROWS_PER_PAGE = API_SETTINGS["apiConnection"]["rowsPerPage"]
API_ENV = API_SETTINGS["apiConnection"]["apiEnv"]["Prod"]
API_KEY = API_SETTINGS["apiConnection"]["reportKey"]
DAY_OFFSET = API_SETTINGS["apiConnection"]["dayOffset"]
LOG_TITLE = API_SETTINGS["logTitle"]


## Switch Builder used to assemble the Connection URL
def add_switches(scope: str, collection: str) -> str:
    """Adds relevant switches sourced from API_SETTINGS
    REQUIRES: valid api scope and valid collection from scope
    RETURNS: list of switches"""
    switches = ""
    try:
        switches_list = API_SETTINGS["scopes"][scope][collection.lower()][
            "optionalSwitches"
        ]
        for dictionary in switches_list:
            key = list(dictionary.keys())
            switch = key[0]
            value = dictionary[switch]
            switches += f"&{switch}={value}"
    except Exception as err:
        switches = ""
        return err
    finally:
        return switches


## Define the URL generator
def gen_url(
    scope: str,
    collection: str,
    item_id: str = None,
    page_number: int = None,
    int_rows_per_page: int = None,
    start_date: str = None,
    end_date: str = None,
    switches: str = None,
<<<<<<< Updated upstream
) -> str:
    """generates the full URL needed for any requested route"""
=======
):
    """generates the URL needed for navigation"""
    CTCLog(LOG_TITLE).info(f"Building URL for {scope} {collection} {item_id}")
>>>>>>> Stashed changes
    url_pre = f"https://{API_ENV}.ctcsoftware.com/{scope}/reports/v1/reports/{collection}?reportsKey={API_KEY}"

    ##Collection handling
    if collection == "app-sessions":
        col = "product"
    elif collection == "doc-session":
        col = "session"
    else:
        col = collection

    ##Id handling
    if item_id is not None:
        url_id = f"&{col}Id={item_id}"
    else:
        url_id = ""

    ##Page handling
    if int_rows_per_page is not None:
        rpp = str(int_rows_per_page)
    else:
        rpp = str(ROWS_PER_PAGE)

    if page_number is not None:
        if collection != "app_sessions":
            url_page = f"&page={str(page_number)}&pageSize={rpp}"
        else:
            url_page = ""
    else:
        url_page = ""

    ##Date handling
    col = collection.lower()
    if (
        col == "searches"
        or col == "app-sessions"
        or col == "doc-sessions"
        or col == "sessions"
    ) and start_date is None:
        current_date = date.today() - timedelta(DAY_OFFSET)
        date_str = current_date.strftime("%Y-%m-%d")
        start_date = date_str

    if (
        col == "app-sessions" or col == "doc-sessions" or col == "sessions"
    ) and end_date is None:
        current_date = date.today() + timedelta(1)
        date_str = current_date.strftime("%Y-%m-%d")
        end_date = date_str

    if col == "searches":
        url_date = f"&searchedAt={start_date}"
    elif col == "app-sessions" or col == "doc-sessions" or col == "sessions":
        if start_date is not None and end_date is not None:
            url_date = f"&startDate={start_date}&endDate={end_date}"
        elif start_date is not None and end_date is None:
            url_date = f"&startDate={start_date}"
        elif start_date is None and end_date is not None:
            url_date = f"&endDate={end_date}"
        else:
            url_date = ""
    else:
        url_date = ""

    ##Switches handling
    if switches is not None:
        url_switches = f"&{switches}"
    else:
        url_switches = ""

    url = f"{url_pre}{url_id}{url_date}{url_page}{url_switches}"
    CTCLog(LOG_TITLE).info(f"Successfully built {url}")
    return url


## Calls CTC Reporting API to get items by ID
def get_x_by_id(
        scope: str,
        collection: str,
        item_id: set,
        added_data: str = None
) -> dict:
    """retrieves an item record based on the item's id value"""
    CTCLog(LOG_TITLE).info(f"Fetching {scope} {collection} item {item_id}")
    try:
        switches = add_switches(scope, collection)
        url = gen_url(
            scope=scope, collection=collection, item_id=item_id, switches=switches
        )
        response_start = perf_counter()
        response = requests.get(url).text
        data = json.loads(response)
        response_end = perf_counter()
        # sleep(response_end - response_start)
        CTCLog(LOG_TITLE).info(f"Successfully fetched {url}")
    except Exception as err:
        data = {}
        CTCLog(LOG_TITLE).error(f"Failed to fetch {url}")
    finally:
        return data


## Calls CTC Reporting API to get total items for a given collection
def get_total_items(scope: str, collection: str) -> int:
    """Retrieves total count of items by category"""
    CTCLog(LOG_TITLE).info(f"Fetching total item count for {scope} {collection}")
    switches = add_switches(scope, collection.lower())
    url = gen_url(
        scope=scope,
        collection=collection,
        page_number=1,
        int_rows_per_page=1,
        switches=switches,
    )
    try:
        response_start = perf_counter()
        response = requests.get(url).text
        base_data = json.loads(response)
        total_items = int(base_data["totalItems"])
        response_end = perf_counter()
        # sleep(response_end - response_start)
        CTCLog(LOG_TITLE).info(
            f"Successfully fetched {total_items} as item count from {url}"
        )
    except Exception as err:
        total_items = None
        CTCLog(LOG_TITLE).error(f"Failed to fetch total item count from {url}")
    finally:
        return total_items


## Calls CTC Reporting API to get next X items
def get_next_x(scope: str, collection: str, page_number: int):
    """Retrieves next X items"""
    CTCLog(LOG_TITLE).info(
        f"Fetching next {ROWS_PER_PAGE} items from page: {page_number} for {scope} {collection}"
    )
    switches = add_switches(scope=scope, collection=collection)
    url = gen_url(
        scope=scope, collection=collection, page_number=page_number, switches=switches
    )
    try:
        response_start = perf_counter()
        response = requests.get(url).text
        next_json = json.loads(response)
        response_end = perf_counter()
        # sleep(response_end - response_start)
        CTCLog(LOG_TITLE).info(f"Successfully fetched items from {url}")
    except Exception as err:
        next_json = None
        CTCLog(LOG_TITLE).error(f"Failed to fetch items from {url}")
    return next_json


def get_keys(scope: str, collection: str) -> list[str]:
    """Used to get the data structure of the json stream"""
    CTCLog(LOG_TITLE).info(f"Fetching keys from {scope} {collection}")
    try:
        stream = get_next_x(scope=scope, collection=collection, page_number=1)
        keys = stream["items"][0].keys()
        CTCLog(LOG_TITLE).info(f"Successfully fetched keys from {scope} {collection}")
        return list(keys)
    except Exception as err:
<<<<<<< Updated upstream
        raise err
=======
        CTCLog(LOG_TITLE).error(f"Failed to fetch keys from {scope} {collection}")
        return err
>>>>>>> Stashed changes


# test_keys = get_keys('CMS','Contents')


## Calls the CTC Reporting API to get all items in a collection
## Uses the get_next_x function to recursively call the API to get all items
def get_all_x(
    scope: str,
    collection: str,
    total_rows: int = None,
    page_number: int = None,
    previous_items: list[dict] = None,
) -> list[dict]:
    """Use to recursively call API to get all <collection> items"""
    CTCLog(LOG_TITLE).info("Fetching all items from {scope} {collection}")
    if total_rows is None:
        total_rows = int(ROWS_PER_PAGE)
    page_count = math.ceil(int(total_rows) / int(ROWS_PER_PAGE))
    # Establish current page number
    if page_number is None:
        page_number = 1
    else:
        page_number += 1
    # Combine results into single result set
    if previous_items is None:
        total_items = get_next_x(
            scope=scope, collection=collection, page_number=page_number
        )
    else:
        next_json = get_next_x(
            scope=scope, collection=collection, page_number=page_number
        )
        for item in next_json["items"]:
            previous_items["items"].append(item)
        total_items = previous_items
    # Continue to fetch next page of results
    # Or return final result set
    if page_number < page_count:
        get_all_x(
            scope=scope,
            collection=collection,
            total_rows=total_rows,
            page_number=page_number,
            previous_items=total_items,
        )
    CTCLog(LOG_TITLE).info(
        f"Successfully fetched {total_items.count} items from {scope} {collection}"
    )
    return total_items
