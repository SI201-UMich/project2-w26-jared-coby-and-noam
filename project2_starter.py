# SI 201 HW4 (Library Checkout System)
# Your name: Jared Weingarten, Noam Altman, Elliot Bolour
# Your student id: 71252257
# Your email: jfwein@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): Claude
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    with open(html_path, 'r', encoding="utf-8-sig") as f:
        file_content = f.read()

        soup = BeautifulSoup(file_content, 'html.parser')

        listings = soup.find_all('div', class_='c1l1h97y')

        results = []
        for listing in listings:
            title = listing.find('div', class_='t1jojoys').text
            link = listing.find('a')['href']
            listing_id = link.split('?')[0].split('/')[-1]
            results.append((title, listing_id))

        return results
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    file_path = "html_files/listing_" + listing_id + ".html"

    with open(file_path, 'r', encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
        policy_number = ""
        lis = soup.find_all('li', class_="f19phm7j")
        for li in lis:
            if "Policy" in li.get_text():
                span = li.find('span', class_='ll4r2nl')
                policy_number = span.text.strip()
            if "pending" in policy_number.lower():
                policy_number = "Pending"
            elif "exempt" in policy_number.lower():
                policy_number = "Exempt"

        host_type = "regular"
        spans = soup.find_all('span', class_='l1dfad8f')
        for span in spans:
            if "Superhost" in span.text:
                host_type = "Superhost"
                break

        host_name = ""
        h2_tags = soup.find_all('h2')
        for h2 in h2_tags:
            if "Hosted by" in h2.get_text():
                host_name = h2.get_text().replace("Hosted by", "").strip()
                break

        subtitle = ""
        h2s = soup.find_all('h2', class_='_14i3z6h')
        for h2 in h2s:
            if "hosted by" in h2.get_text().lower():
                subtitle = h2.get_text()
                break
        if not subtitle:
            fallback_div = soup.find('div', class_='_kh3xmo')
            if fallback_div:
                subtitle = fallback_div.get_text()
        if "Private" in subtitle:
            room_type = "Private Room"
        elif "Shared" in subtitle:
            room_type = "Shared Room"
        else:
            room_type = "Entire Room"

        location_rating = 0.0
        location_div = soup.find('div', class_='_y1ba89', string='Location')
        if location_div:
            rating_div = location_div.find_next_sibling('div', class_='_bgq2leu')
            if rating_div:
                location_rating = float(rating_div.text.strip())

        return {
            listing_id: {
                "policy_number": policy_number,
                "host_type": host_type,
                "host_name": host_name,
                "room_type": room_type,
                "location_rating": location_rating
            }
        }

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listing_results = load_listing_results(html_path)
    database = []

    for listing_title, listing_id in listing_results:
        details = get_listing_details(listing_id)
        info = details[listing_id]

        listing_tuple = (
            listing_title,
            listing_id,
            info["policy_number"],
            info["host_type"],
            info["host_name"],
            info["room_type"],
            info["location_rating"]
        )

        database.append(listing_tuple)

    return database

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Listing Title",
            "Listing ID",
            "Policy Number",
            "Host Type",
            "Host Name",
            "Room Type",
            "Location Rating"
        ])

        for row in sorted_data:
            writer.writerow(row)    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    ratings_by_room = {}
    counts_by_room = {}

    for listing in data:
        room_type = listing[5]
        location_rating = listing[6]

        if location_rating == 0.0:
            continue

        if room_type not in ratings_by_room:
            ratings_by_room[room_type] = location_rating
            counts_by_room[room_type] = 1
        else:
            ratings_by_room[room_type] += location_rating
            counts_by_room[room_type] += 1

    averages = {}
    for room_type in ratings_by_room:
        averages[room_type] = round(ratings_by_room[room_type] / counts_by_room[room_type], 1)

    return averages
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid_listings = []
    pattern1 = r"^20\d\d-00\d\d\d\dSTR$"
    pattern2 = r"^STR-000\d\d\d\d$"
    
    for listing in data:
        policy_number = listing[2]
        listing_id = listing[1]

        if policy_number == "Pending" or policy_number == "Exempt":
            continue

        if not re.match(pattern1, policy_number) and not re.match(pattern2, policy_number):
            invalid_listings.append(listing_id)

    return invalid_listings
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = "https://scholar.google.com/scholar?q=" + query
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    titles = []
    results = soup.find_all('h3', class_='gs_rt')
    for result in results:
        titles.append(result.get_text())

    return titles
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================
print(google_scholar_searcher("airbnb"))

class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        results = load_listing_results("html_files/search_results.html")
        self.assertEqual(len(results), 18)
        self.assertEqual(results[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        result_1550913 = get_listing_details("1550913")
        result_4614763 = get_listing_details("4614763")
        result_6092596 = get_listing_details("6092596")
        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        result_467507 = get_listing_details("467507")
        self.assertEqual(result_467507["467507"]["policy_number"], "STR-0005349")
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        result_1944564 = get_listing_details("1944564")
        self.assertEqual(result_1944564["1944564"]["host_type"], "Superhost")
        self.assertEqual(result_1944564["1944564"]["room_type"], "Entire Room")
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(result_1944564["1944564"]["location_rating"], 4.9)
        pass

    def test_create_listing_database(self):
        for item in self.detailed_data:
            self.assertEqual(len(item), 7)

        self.assertEqual(
            self.detailed_data[-1],
            ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
        )

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")
        rows = []
        with open(out_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                rows.append(row)

        self.assertEqual(rows[1], ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"])
            # TODO: Call output_csv() to write the detailed_data to a CSV file.
            # TODO: Read the CSV back in and store rows in a list.
            # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
            pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
            pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)