#!/bin/python3

import calendar
from datetime import datetime
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

JSON_PATH = "emails.json"
RSS_PATH = "emails.rss"

RSS_CHANNEL_TITLE = "Quincy Larson's Links Worth Your Time"
RSS_CHANNEL_LINK = "https://github.com/freeCodeCamp/awesome-quincy-larson-emails"
RSS_CHANNEL_DESCRIPTION = "RSS feed generated from a historical archive of Quincy's weekly newsletter."


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

    # Format dates in RFC-822 date-time
    # https://validator.w3.org/feed/docs/error/InvalidRFC2822Date.html
    if pubDate is not None:
        item.append(ET.Element("pubDate"))

        # Make sure months are processed correctly when there's some inconsistency
        # https://docs.python.org/3/library/datetime.html#format-codes
        if pubDate in calendar.month_name:
            fmt_date = datetime.strptime(pubDate, "%B %d, %Y").strftime("%d %b %Y")
        elif pubDate in calendar.month_abbr:
            fmt_date = datetime.strptime(pubDate, "%b %d, %Y").strftime("%d %b %Y")
        else:
            fmt_date = '01 January 1970'  # Just default to UNIX start
        item[-1].text = fmt_date

    return item


with open(JSON_PATH, 'rb') as emails_json_file:
    json_data: dict = json.load(emails_json_file)


tree = ET.ElementTree(ET.Element("rss", {"version": "2.0"}))

root = tree.getroot()

root.append(ET.Element("channel"))
channel = root[0]

channel.extend([
    ET.Element("title"),
    ET.Element("link"),
    ET.Element("description"),
])

channel[0].text = RSS_CHANNEL_TITLE
channel[1].text = RSS_CHANNEL_LINK
channel[2].text = RSS_CHANNEL_DESCRIPTION

for email in json_data["emails"]:

    date = email.get("date")
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

    json_links = email.get("links")

    for json_link in json_links:

        channel.append(rss_item(
            description=json_link.get("description"),
            link=json_link.get("link"),
            pubDate=date,
        ))

rss = minidom.parseString(
    ET.tostring(tree.getroot(), 'utf-8')) \
    .toprettyxml(indent="  ")

with open(RSS_PATH, 'w') as emails_rss_file:
    emails_rss_file.write(rss)

# verify RSS (XML) is parse-able
ET.ElementTree().parse(RSS_PATH)
