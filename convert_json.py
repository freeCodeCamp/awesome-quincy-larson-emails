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
    """
    Create an RSS-formatted element

    Takes input as strings and processes the strings into a form that is RSS compliant.
    """

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
        # 09:00:00 EST is set as default for simplicity
        if pubDate.split(' ')[0] in calendar.month_name:
            fmt_date = datetime.strptime(pubDate, "%B %d, %Y")
        elif pubDate.split(' ')[0] in calendar.month_abbr:
            fmt_date = datetime.strptime(pubDate, "%b %d, %Y")
        else:
            fmt_date = datetime(1970, 1, 1) # Just default to UNIX start '01 January 1970'

        item[-1].text = fmt_date.strftime("%a, %d %b %Y 09:00:00 EST")

    # Make GUID link a mix of the date and description
    # https://validator.w3.org/feed/docs/warning/MissingGuid.html
    # https://validator.w3.org/feed/docs/error/InvalidHttpGUID.html
    item.append(ET.Element("guid", {"isPermaLink": "false"}))
    if pubDate is not None and description is not None:
        item[-1].text = f"{pubDate} {' '.join(description.split(' ')[:5])}"
    elif pubDate is not None and description is None:
        item[-1].text = f"{pubDate} Quincy Larson weekly email shared information."
    else:
        item[-1].text = "Quincy Larson weekly email shared information."
      
    return item


with open(JSON_PATH, 'rb') as emails_json_file:
    json_data: dict = json.load(emails_json_file)

tree = ET.ElementTree(ET.Element(
    "rss",
    {"version": "2.0", "xmlns:atom": "http://www.w3.org/2005/Atom"}
))

root = tree.getroot()

root.append(ET.Element("channel"))
channel = root[0]

# Setup RSS metadata specifications
# atom:link https://validator.w3.org/feed/docs/warning/MissingAtomSelfLink.html
channel.extend([
    ET.Element("title"),
    ET.Element("link"),
    ET.Element("description"),
    ET.Element("atom:link", {
        "href": RSS_CHANNEL_LINK,
        "ref": "rel",
        "type": "application/rss+xml"
    }),
])
channel[0].text = RSS_CHANNEL_TITLE
channel[1].text = RSS_CHANNEL_LINK
channel[2].text = RSS_CHANNEL_DESCRIPTION

for email in json_data["emails"]:

    date = email.get("date")
    bonus = email.get("bonus")
    quote = email.get("quote")

    if bonus is not None:
        channel.append(rss_item(
            title="Bonus",
            description=bonus,
            pubDate=date
        ))

    if quote is not None:
        quote_author = email.get("quote_author")

        if quote_author is not None:
            quote += " - " + quote_author

        channel.append(rss_item(
            title="Quote",
            description=quote,
            pubDate=date
        ))

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

# Verify RSS (XML) is parse-able
ET.ElementTree().parse(RSS_PATH)
