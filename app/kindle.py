#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import uuid
from datetime import datetime

from .config import Config, UserConfig


class Kindle:

    clip_boundary = "=========="
    clip_note = "Note"
    clip_bookmark = "Bookmark"
    clip_highlight = "Highlight"

    def __init__(self, file):

        self.file = file

    def _build_clippings(self):

        with open(self.file) as file:

            clippings = []
            data = []

            for line in file:

                if line.startswith(self.clip_boundary):

                    # TODO: Need a better way to do this...
                    if self.clip_highlight in data[1]:

                        clip = Clip(data)
                        clippings.append(clip)

                    data = []

                else:

                    data.append(line.strip())

        return clippings

    @property
    def clippings(self) -> list:

        return [clip.to_dict() for clip in self._build_clippings()]


class Clip:
    """
    Basic My Clippings Syntax.

            ==========
    data[0] Title (Lastname, Firstname)
    data[1] - Your Highlight on page 0000 | Location 0000-0000 | Added on Date
    data[2]
    data[3] Full highlighted passage.

            ==========
    data[0] Title (Lastname, Firstname)
    data[1] - Your Highlight on Location 0000-0000 | Added on Date
    data[2]
    data[3] Full highlighted passage.

    Date format: Monday, January 1, 2099 0:00:00 AM
    """

    # TODO: Need to document this crazy mess better...
    re_source = re.compile(r"(?P<source_name>.*?)[ ]{1}\((?P<source_author>[^()]+)\)(?=[^()]*$)")
    re_date = re.compile(r"Added on (?P<date>.*$)")

    def __init__(self, data):

        self.process_passage(data)
        self.process_source(data)
        self.process_date(data)

    def process_passage(self, data):
        """
        TODO: Needs to be tested when there are passages that are longer than
        one paragraph. Not sure how the Kindle deals with the linebreaks. This
        should handle all passage text, but need to keep an eye on it.
        """

        self._passage = "\n".join(data[3:])

    def process_source(self, data):
        """
        TODO: This needs a bit of further testing to make sure its performing
        well with different books.
        """

        match_source = re.search(self.re_source, data[0])

        self._source_name = match_source.group("source_name")
        self._source_author = match_source.group("source_author")

        comma = ", "

        if comma in self._source_author:

            last, first = self._source_author.split(comma, 1)

            self._source_author = f"{first} {last}"

    def process_date(self, data):
        """
        via. http://strftime.org

        NOTE: Did not use %-m or %-I for 0-padding. It kept causing errors
        although it seems like that's how Kindle formats the date.
        """

        strftime_format = "%A, %B %d, %Y %I:%M:%S %p"

        match_date = re.search(self.re_date, data[1])

        date_as_string = match_date.group("date")
        date_as_datetime = datetime.strptime(date_as_string, strftime_format)
        date_as_iso8601 = date_as_datetime.isoformat()

        self._date = date_as_iso8601

    @property
    def id(self):
        """
        Generate a UUID from source_name, source_author and date.
        """

        data = self.source_name + self.source_author + self.date

        self._id = uuid.uuid5(uuid.NAMESPACE_DNS, data)

        return str(self._id).upper()

    @property
    def passage(self):
        return self._passage

    @property
    def notes(self):
        return ""

    @property
    def source_name(self):
        return self._source_name

    @property
    def source_author(self):
        return self._source_author

    @property
    def tags(self):
        return []

    @property
    def collections(self):
        """
         TODO: Might be good to tack on a `collection` with the import date.
        """
        return [f"imported-{Config.date}", ]

    @property
    def date(self):
        return self._date

    def to_dict(self):

        data = {
            "id": self.id,
            "passage": self.passage,
            "notes": self.notes,
            "source": {
                "name": self.source_name,
                "author": self.source_author,
            },
            "tags": self.tags,
            "collections": self.collections,
            "metadata": {
                "created": self.date,
                "modified": self.date,
                "origin": UserConfig.origin,
                "is_protected": True,
                "in_trash": False,
            }
        }

        return data
