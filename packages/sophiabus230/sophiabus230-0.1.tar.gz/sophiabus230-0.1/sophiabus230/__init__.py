#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import gettz
from datetime import timedelta
from bs4 import BeautifulSoup


def _get_html_from_cg06(stop_id):
    """
    Requests the timetable from the cg06 website

    :param stop_id: the stop to fetch the timetable for
    :return: The result of the request as a html content
    :rtype: str
    """
    cg06_url = "http://cg06.tsi.cityway.fr/qrcode/?id={0}"
    req = urllib.urlopen(cg06_url.format(stop_id))
    content = req.read()
    return content


def _sanitize_entry(entry):
    """
    Sanitize the entry by removing the extra spaces and empty lines

    :param entry: the entry to sanitize
    :return: the entry without unnecessary spaces
    :rtype: str
    """
    sane_line = re.sub(r"^\s+$", '\n', entry)
    sane_line = re.sub(r"\s+$", '', sane_line)
    sane_line.replace(u"é", "e")
    if len(sane_line) > 1:
        return sane_line
    else:
        return None


def _parse_entry(entry):
    """
    Convert a entry into a dict containing the following attributes:

    - bus_time
    - dest
    - is_real_time

    :param entry: the string representation of one bus passage
    :return: a dict representing the relevant information of the string
    :rtype: dict
    """
    split_entry = entry.split(' ')
    idx_end_direction = len(split_entry)
    is_real_time = True
    tz_paris = gettz('Europe/Paris')
    if split_entry[-1] == '*':
        is_real_time = False
        idx_end_direction = len(split_entry) - 1
    if split_entry[0] == 'dans':
        # case for immediate upcoming bus
        date_now = datetime.now(tz=tz_paris)
        delta_minutes = int(split_entry[1])
        bus_time = date_now + timedelta(minutes=delta_minutes)
        idx_start_direction = 4
    else:
        # case for later upcoming bus
        tzinfos = {'FR': tz_paris}
        bus_time = parse(split_entry[1], tzinfos=tzinfos)
        idx_start_direction = 3
    dest = ' '.join(split_entry[idx_start_direction:idx_end_direction])
    dest = dest.encode('utf-8')
    return {'bus_time': bus_time, 'dest': dest, 'is_real_time': is_real_time}


def get_next_buses(debug=False):
    """
    Fetches the list of upcoming buses at the INRIA bus stop for the bus 230 towards Nice

    :return: upcoming buses
    :rtype: list
    """
    tt = []
    content = _get_html_from_cg06(1939)
    soup = BeautifulSoup(content, "html.parser")
    for br in soup.find_all("br"):
        br.replace_with('\n')
    data = [e for e in soup.find_all("div", attrs={"class": "data"}) if '230' in e.get_text()]
    if len(data) != 0:
        assert len(data) <= 1
        data_230 = data[0]
        for e in data_230.div.get_text().split('\n'):
            sane_entry = _sanitize_entry(e)
            if sane_entry is not None:
                if debug:
                    print '[DEBUG]: {0}'.format(sane_entry.encode('utf-8'))
                tt.append(_parse_entry(sane_entry))
    return tt
