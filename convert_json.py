#!/bin/python3

import calendar
from datetime import datetime
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom


JSON_PATH = "emails.json"
RSS_PATH = "emails.xml"

RSS_CHANNEL_TITLE = "Quincy Larson's Links Worth Your Time"
RSS_CHANNEL_LINK = "https://github.com/freeCodeCamp/awesome-quincy-larson-emails"
RSS_CHANNEL_DESCRIPTION = "RSS feed generated from a historical archive of Quincy's weekly newsletter."


def rss_item(email_data: dict) -> ET.Element:
    """
    Create a single RSS item from an email's worth of data.
    """
    date = email_data.get("date")
    item = ET.Element("item")

    # Title
    title = ET.SubElement(item, "title")
    title.text = f"Quincy Larson's Links - {date}"

    # Determine date formats (pubDate and fallback for GUID)
    fmt_date = datetime(1970, 1, 1)
    if date:
        first_word = date.split(' ')[0]
        if first_word in calendar.month_name:
            fmt_date = datetime.strptime(date, "%B %d, %Y")
        elif first_word in calendar.month_abbr:
            fmt_date = datetime.strptime(date, "%b %d, %Y")

    # pubDate
    if date:
        pub_date_elem = ET.SubELement(item, "pubDate")
        pub_date_elem.text = fmt_date.strftime("%a, %d %b %Y 09:00:00 EST")

    # GUID
    guid_date_str = fmt_date.strftime("%Y-%m-%d") if date else "1970-01-01"
    guid = ET.SubElement(item, "guid", {"isPermaLink": "false"})
    guid.text = f"quincy-email-{guid_date_str}"

    # Build HTML Description
    description_parts = []

    links = email_data.get("links", [])
    if links:
        description_parts.append("<p>Here are Quincy Larson's links for this week:</p>")
        description_parts.append("<ol>")
        for link in links:
            desc = link.get("description", "")
            url = link.get("link", "")
            duration = f" ({link.get('time_duration')} {link.get('time_type')})" if link.get('time_duration') else ""

            # Try to extract a title if possible, or just use the description
            item_text = f"<li>{desc}{duration}"
            if url:
                item_text += f' <a href="{url}">[link]</a>'
            item_text += "</li>"
            description_parts.append(item_text)
        description_parts.append("</ol>")

    quote = email_data.get("quote")
    if quote:
        description_parts.append("<hr>")
        author = email_data.get("quote_author", "Unknown")
        description_parts.append(f"<p><strong>Quote of the Week:</strong></p>")
        description_parts.append(f"<blockquote>{quote} — {author}</blockquote>")

    bonus = email_data.get("bonus")
    if bonus:
        description_parts.append("<hr>")
        description_parts.append(f"<p><em>{bonus}</em></p>")

    description = ET.SubElement(item, "description")
    description.text = "\n".join(description_parts)

    if email_data.get("links"):
        link_elem = ET.SubElement(item, "link")
        link_elem.text = email_data["links"][0].get("link")

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
        "ref": "self",
        "type": "application/rss+xml"
    }),
])
channel[0].text = RSS_CHANNEL_TITLE
channel[1].text = RSS_CHANNEL_LINK
channel[2].text = RSS_CHANNEL_DESCRIPTION

for email in json_data["emails"]:
    channel.append(rss_item(email))

rss = minidom.parseString(
    ET.tostring(tree.getroot(), 'utf-8')) \
    .toprettyxml(indent="  ")

with open(RSS_PATH, 'w') as emails_rss_file:
    emails_rss_file.write(rss)

# Verify RSS (XML) is parse-able
ET.ElementTree().parse(RSS_PATH)
