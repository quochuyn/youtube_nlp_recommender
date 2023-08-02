# transcripts.py

import numpy as np
import pandas as pd

from youtube_transcript_api import YouTubeTranscriptApi

import re
import unicodedata
from typing import Union
        


def get_video_transcript(video_id : str) -> str:
    r"""
    Get the video transcript, if available, from the Youtube video ID.
    Returns np.NaN if not available.
    """

    try:
        raw_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = _convert_raw_transcript_to_string(raw_transcript)
        clean_transcript = _clean_transcript(transcript)
        return clean_transcript
    except Exception as e:
        # pass silently
        return np.NaN



def _convert_raw_transcript_to_string(raw_transcript : list[dict]) -> str:
    r"""
    Convert the raw transcript returned by the Youtube Transcript API
    (a list of dictionaries) into a single string. Each dictionary has 3 keys:
    `text`, `start`, and `duration`.
    """

    return ' '.join([annotation_dict['text'] for annotation_dict in raw_transcript])



def _clean_transcript(transcript : str) -> str:
    r"""
    Clean the transcript in preparation for any NLP techniques or downstream analysis.
    """

    # remove unicode characters; idea stems from the following StackOverflow post:
    # https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
    transcript = unicodedata.normalize('NFKD', transcript)

    # remove any unwanted characters, such as annotations and special symbols
    transcript = re.sub(pattern=r'\[\w+\]', repl='', string=transcript)

    # remove extra whitespaces
    transcript = re.sub(r'\s+', ' ', transcript)
    transcript = transcript.strip()

    return transcript


