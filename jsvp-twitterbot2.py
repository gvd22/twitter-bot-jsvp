from urllib.request import urlopen
import ssl
import re
from requests.structures import CaseInsensitiveDict
import datetime
import json
from requests_oauthlib import OAuth1Session

## Here we are defining the variables for the Twitter API Authentication ##
consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

access_token ="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

## Counting the days since JSVP has released their press release ##
today = datetime.date.today()
someday = datetime.date(2022, 7, 27)
diff = today - someday
##print(diff.days)

daycounter = diff.days + 1

context = ssl._create_unverified_context()

url = "https://jsvp.ch/spenden/"

page = urlopen(url,context=context)

## Here we are searching for the Text on the Website ##
gesuchterText = "Bank: UBS Switzerland AG, CH-8098 Zürich"

html_bytes = page.read()
html = html_bytes.decode("utf-8")

webinhalt = re.findall(gesuchterText, html);

## Here we are checking if the text is in the website or not ##
if webinhalt == ['Bank: UBS Switzerland AG, CH-8098 Zürich']:
    finaltweet = ( str(daycounter) + " Tage seit heuchlerischem @jungesvp-Aufruf zu @UBSschweiz Boykott, trotzdem haben sie ihr Spendenkonto nach wie vor bei der UBS.")
    payload = {"text": "" + finaltweet + ""}

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

else:
    print("Die UBS ist nicht mehr die Bank der Wahl für die @jungesvp.")


