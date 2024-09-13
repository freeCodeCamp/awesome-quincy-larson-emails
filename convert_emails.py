#!/bin/python3

import json
import xml.etree.ElementTree as ET

JSON_PATH = "emails.json"
RSS_PATH = "emails.rss"


def rss_item(title: str | None = None,
             description: str | None = None,
             link: str | None = None,
             pubDate: str | None = None) -> ET.Element:

    item = ET.Element("item")

    # RSS 2.0 items require description or title
    # https://www.rssboard.org/rss-specification#hrelementsOfLtitemgt
    if title is None and description is None:
        title = "Untitled"

    if title is not None:
        item.append(ET.Element("title"))
        item[-1].text = title

    if description is not None:
        item.append(ET.Element("description"))
        item[-1].text = description

    if link is not None:
        item.append(ET.Element("link"))
        item[-1].text = link

    if pubDate is not None:
        item.append(ET.Element("pubDate"))
        item[-1].text = pubDate

    return item


with open(JSON_PATH, 'rb') as emails_json:
    json_data: dict = json.load(emails_json)


tree = ET.ElementTree(ET.Element("rss", {"version": "2.0"}))

root = tree.getroot()

root.append(ET.Element("channel"))
channel = root[0]

channel.extend([
    ET.Element("title"),
    ET.Element("link"),
    ET.Element("description"),
])

channel[0].text = "Quincy Larson's 5 Links Worth Your Time Emails"
channel[1].text = "https://github.com/freeCodeCamp/awesome-quincy-larson-emails"
channel[2].text = "RSS feed generated from a historical archive of Quincy's weekly newsletter."

# TODO: replace pop with get / remove extra pops
email: dict = {}
for email in json_data["emails"]:

    date = email.pop("date")
    json_links = email.get("links")
    bonus = email.get("bonus")
    quote = email.get("quote")

    if bonus is not None:
        channel.append(
            rss_item(title="Bonus", description=bonus, pubDate=date))

    if quote is not None:
        quote_author = email.get("quote_author")

        if quote_author is not None:
            quote += " - " + quote_author

        channel.append(
            rss_item(title="Quote", description=quote, pubDate=date))

    for json_link in json_links:

        channel.append(rss_item(
            description=json_link.get("description"),
            link=json_link.get("link"),
            pubDate=date,
        ))


with open(RSS_PATH, 'wb') as emails_rss:
    tree.write(emails_rss)

# verify RSS (XML) is parse-able
ET.ElementTree().parse(RSS_PATH)