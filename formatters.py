"""
Defines subtitle formatters used by autosub.
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import sys
import pysrt
import six

text_type = unicode


def force_unicode(s, encoding="utf-8"):
    if isinstance(s, text_type):
        return s
    return s.decode(encoding)


def srt_formatter(subtitles, show_before=0, show_after=0):
    f = pysrt.SubRipFile()
    for i, (rng, text) in enumerate(subtitles, 1):
        item = pysrt.SubRipItem()
        item.index = i
        item.text = force_unicode(text)
        start, end, num = rng
        item.start.seconds = max(0, start - show_before)
        item.end.seconds = end + show_after
        f.append(item)
    return '\n'.join(six.text_type(item) for item in f)
    #return '\n'.join(map(str, f))


def vtt_formatter(subtitles, padding_before=0, padding_after=0):
    """
    Serialize a list of subtitles according to the VTT format, with optional time padding.
    """
    text = srt_formatter(subtitles, padding_before, padding_after)
    text = 'WEBVTT\n\n' + text.replace(',', '.')
    return text


def json_formatter(subtitles):
    """
    Serialize a list of subtitles as a JSON blob.
    """
    subtitle_dicts = [
        {
            'start': start,
            'end': end,
            'content': text,
        }
        for ((start, end), text)
        in subtitles
    ]
    return json.dumps(subtitle_dicts)


def raw_formatter(subtitles):
    """
    Serialize a list of subtitles as a newline-delimited string.
    """
    return ' '.join(text for (_rng, text) in subtitles)


FORMATTERS = {
    'srt': srt_formatter,
    'vtt': vtt_formatter,
    'json': json_formatter,
    'raw': raw_formatter,
}
