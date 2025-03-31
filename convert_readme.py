#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Processes quotes from
#   https://github.com/sourabh-joshi/awesome-quincy-larson-emails
# Use https://regex101.com to help create regular expressions
# Usage:
# $ python3 convert_readme.py

import json
import re

IN_FILE = 'README.md'
OUT_FILE = 'emails.json'

with open(IN_FILE, 'r') as fh:
    texts = fh.readlines()
    texts = texts[5:]  # Skip first lines with repository info
    texts = [x.strip() for x in texts]
    texts = [x for x in texts if x != '']  # Remove new lines

with open(OUT_FILE, 'w') as fh:
    # Holds all data to be saved as JSON
    data = {}
    data['emails'] = []
    first_pass = True

    for line in texts:
        # Replace some fancier quotes with normal ones
        line = re.sub('“|”', '"', line)
        line = re.sub('’', "'", line)

        # Look for dates which start with ###
        if re.match('^###', line):
            # First case when int_data doesn't exist
            if first_pass:
                first_pass = False
                int_data = {}
            else:
                # Add and rest data
                data['emails'].append(int_data)
                int_data = {}

            # Extract date information
            int_data['links'] = []
            date_text = re.search('### (.*)', line).group(1)
            int_data['date'] = date_text

        # Links start with numbers
        elif re.search('^[0-9]', line):
            line = re.sub('–', '--', line)  # Replace em-dash
            link_data = {}

            try:
                re_link = r'([0-9])\. (.*)\s+(https?://.*)?'
                result = re.search(re_link, line)

                link_data['order'] = result.group(1)
                link_data['link'] = result.group(3)

                description = result.group(2).strip(':')

                # Newer descriptions with descriptions ending with period
                # before parens with time to explore the link.
                # Edge case of description ending with '?"
                if description[-1] == ')' and ('. (' in description or '? (' in description):
                    info = re.search(r'(.*[\.|\?])\s?\(', description)
                    link_data['description'] = info.group(1)

                # Edge case with some links only taking 1 minute.
                elif 'takes 1 minute' in description:
                    info = re.search(r'(.*) \(takes 1 minute\)', description)
                    link_data['description'] = info.group(1).strip() + '.'

                # Older links or variation of the link where there is no period
                # after the description and before the time to explore the
                # link.
                elif description[-1] == ')':
                    info = re.search(r'(.*)\s?\((\d+|browsable)', description)
                    link_data['description'] = info.group(1).strip() + '.'

                else:
                    # Make a full sentence with period at the end to be
                    # consistent with newer entries.
                    link_data['description'] = description + '.'

                re_time = re.compile(r'(\d\.?\d*)\s+'
                                     r'(minute|hour)\s+'
                                     r'(read|YouTube|watch|course|video)')
                time_text = re_time.search(description)
                link_data['time_duration'] = time_text.group(1)
                link_data['time_type'] = time_text.group(2) + 's'  # Plural

                # Edge case of one minute
                if 'takes 1 minute' in description:
                    link_data['time_duration'] = '1'
                    link_data['time_type'] = 'minutes'  # Plural consistency

            except Exception:
                pass

            int_data['links'].append(link_data)

        elif re.search('^(Quote|This week)', line):
            line = re.sub('–', '-', line)  # Replace en-dash
            line = re.sub('―', '-', line)  # Replace em-dash
            line = re.sub('—', '-', line)  # Replace other dash type
            line = re.sub(' ', '', line)  # Replace odd space
            try:
                quote_info = re.search(r'\*\"(.*)\"\*\s*', line)
                int_data['quote'] = quote_info.group(1).strip()

                auth_info = re.search(r'\"\*\s*-\s*(.*)$', line)
                int_data['quote_author'] = auth_info.group(1).strip()
            except Exception:
                pass

        else:
            line = re.sub(u' — ', ' - ', line)
            if 'int_data' not in locals():
              int_data = {}
            int_data['bonus'] = line

    data['emails'].append(int_data)  # Last case
    json.dump(data, fh, indent=2, sort_keys=True)
