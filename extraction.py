import requests
import pandas as pd

state_mapping = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

url = "https://lamadeleine.com/wp-json/wp/v2/restaurant-locations"

querystring = {"per_page": "150"}

payload = ""
headers = {
    "authority": "lamadeleine.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "__cf_bm=s3_oxmV3gyCAqjI6FLuCAnS1Y19s5pRjl2jE3UrOOG8-1712680353-1.0.1.1-k1A1qqG0vVG7qXdnKDlCOPd2W2dUfCHyKSDOokcFWGE8TD8plCZRbMCWwIZJrKjnv.atwysyXJ.Bhz5Ibh2GEQ; _gcl_au=1.1.1476892625.1712680354; _gid=GA1.2.452426304.1712680354; _ga_2JLMKBSDRP=GS1.2.1712680466.1.0.1712680466.0.0.0; _ga_EEE7E5V467=GS1.2.1712680466.1.0.1712680466.60.0.0; arp_scroll_position=0; _ga=GA1.2.578401085.1712680354; _ga_3CV9XCRYRX=GS1.2.1712680353.1.1.1712680632.56.0.0; _ga_192BG8G1PN=GS1.2.1712680353.1.1.1712680632.0.0.0; _ga_G3C3KCQEMF=GS1.1.1712680353.1.1.1712680727.0.0.0",
    "referer": "https://lamadeleine.com/locations",
    "^sec-ch-ua": "^Chromium^;v=^122^, ^Not",
    "sec-ch-ua-mobile": "?0",
    "^sec-ch-ua-platform": "^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

locations_list = []

if response.status_code == 200:
    data = response.json()

    # Iterate over each location in the response
    for location in data:
        store_id = location.get("id")
        title = location.get("title", {}).get("rendered")
        acf_data = location.get("acf", {})
        
        if store_id is not None and title is not None and acf_data:
            # print("Store ID:", store_id)
            # print("Title:", title)
            
            # Accessing data within "acf"
            store_name = acf_data.get("locationHero", {}).get("storeName")
            address_line1 = acf_data.get("locationHero", {}).get("addressLine1")
            address_line2 = acf_data.get("locationHero", {}).get("addressLine2")
            city = acf_data.get("locationHero", {}).get("city")
            state = acf_data.get("locationHero", {}).get("state")
            zipcode = acf_data.get("locationHero", {}).get("zip")
            lat = acf_data.get("locationHero", {}).get("lat")
            lng = acf_data.get("locationHero", {}).get("lng")
            phone = acf_data.get("locationHero", {}).get("phone")

            # Convert full state name to abbreviation using dict above
            if state and len(state) > 2:
                state = state_mapping.get(state.title(), state)

            # Combine and encode street address to ensure correct special characters
            street_address = f'{address_line1}, {address_line2}'.encode('utf-8').decode('utf-8')

            location_item = {
                "locationName": store_name,
                "streetAddress": street_address,
                "city": city,
                "state": state,
                "postalCode": zipcode,
                "phoneNumber": phone,
                "storeID": store_id
            }

            locations_list.append(location_item)

    print(f"Returned {len(locations_list)} items")
else:
    print("Failed to retrieve data. Status code:", response.status_code)

# Save new locations data to csv
locations_df = pd.DataFrame(locations_list)
locations_df.to_csv("locations.csv", index=False, encoding='utf-8')