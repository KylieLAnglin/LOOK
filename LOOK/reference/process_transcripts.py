# %%
import os
import re
import fnmatch
import collections

import pandas as pd
import docx
from openpyxl import load_workbook

import random
from moves.library import start
from moves.library import process_transcripts


def extract_paragraphs(doc_file: str):
    """Extracts paragraphs (new lines) from .docx file

    Args:
        doc_file (str): path to docx file

    Returns:
        [list]: list of text in paragraphs
    """
    doc = docx.Document(doc_file)

    paragraphs = [para.text for para in doc.paragraphs if len(para.text) > 0]

    return paragraphs


def extract_data_from_go_transcript(turns_of_talk: list):
    """Extract speaker, time, and text from turns of talk (word doc paragraphs)
     in go transcript formatting.

    Args:
        turns_of_talk (list): list of paragraphs in go transcript word doc

    Returns:
        named tuple: time_stamps, speaker_tags, text
    """
    time_stamp_regex = re.compile(r"\[[0-9:]*\]")
    time_stamps = [time_stamp_regex.findall(text) for text in turns_of_talk]
    time_stamps = [tag[0] if tag else "" for tag in time_stamps]

    turns_of_talk = [re.sub(time_stamp_regex, "", text) for text in turns_of_talk]

    speaker_tag_regex = re.compile(r"(\S[a-zA-Z1-3]+)\:")
    speaker_tags = [speaker_tag_regex.findall(text) for text in turns_of_talk]

    turns_of_talk = [re.sub(speaker_tag_regex, "", text) for text in turns_of_talk]

    if speaker_tags[2] == []:
        speaker_tag_regex = re.compile(r"([A-z]+\s[A-z]+[\s1-9]+)\:")
        speaker_tags = [speaker_tag_regex.findall(text) for text in turns_of_talk]
        turns_of_talk = [re.sub(speaker_tag_regex, "", text) for text in turns_of_talk]

    if speaker_tags[2] == []:
        speaker_tag_regex = re.compile(r"([A-z]+[\s1-9]+)\:")
        speaker_tags = [speaker_tag_regex.findall(text) for text in turns_of_talk]
        turns_of_talk = [re.sub(speaker_tag_regex, "", text) for text in turns_of_talk]

    Transcript = collections.namedtuple(
        "Transcript", ["time_stamps", "speaker_tags", "text"]
    )

    speaker_tags = [tag[0].strip() if tag else "" for tag in speaker_tags]

    transcript = Transcript(
        time_stamps=time_stamps, speaker_tags=speaker_tags, text=turns_of_talk
    )

    return transcript


def extract_data_from_otter_transcript(turns_of_talk: list):
    """Extract speaker, time, and text from turns of talk (word doc paragraphs)
     in otter transcript formatting.

    Args:
        turns_of_talk (list): list of paragraphs in otter transcript word doc

    Returns:
        named tuple: time_stamps, speaker_tags, text
    """
    speaker_tags = []
    time_stamps = []
    texts = []
    turn = 6
    while turn < len(turns_of_talk):
        speaker_tags.append(turns_of_talk[turn][:-5].strip())
        time_stamps.append(turns_of_talk[turn][-5:])
        turn = turn + 1

        texts.append(turns_of_talk[turn])
        turn = turn + 1

    Transcript = collections.namedtuple(
        "Transcript", ["time_stamps", "speaker_tags", "text"]
    )

    transcript = Transcript(
        time_stamps=time_stamps, speaker_tags=speaker_tags, text=texts
    )
    return transcript


def word_to_transcript(doc_file=str):
    """Extracts paragraphs from word doc and directs
    to appropriate processing function

    Args:
        doc_file ([str], optional): String path to file

    Returns:
        named tuple: time_stamps, speaker_tags, text
    """
    paragraphs = extract_paragraphs(doc_file=doc_file)
    if "[0" in paragraphs[0]:
        return extract_data_from_go_transcript(turns_of_talk=paragraphs)
    if paragraphs[2] == "SUMMARY KEYWORDS":
        return extract_data_from_otter_transcript(turns_of_talk=paragraphs)

    else:
        print("error with " + doc_file)


def transcript_to_cleaned_df(transcript):
    """Turns transcript named tuple to dataframe

    Args:
        transcript ([named tuple]): transcript named tuple

    Returns:
        [df]: dataframe with three columns: time, speaker, text
    """
    new_speaker_tags = []
    current_speaker = ""
    for speaker in transcript.speaker_tags:
        if speaker:
            current_speaker = speaker
            new_speaker_tags.append(speaker)
        else:
            new_speaker_tags.append(current_speaker)

    new_time_tags = []
    current_time = ""
    for time in transcript.time_stamps:
        if time:
            current_time = time
            new_time_tags.append(current_time)
        else:
            new_time_tags.append(current_time)

    df = pd.DataFrame(
        {
            "time": new_time_tags,
            "speaker": new_speaker_tags,
            "text": transcript.text,
        }
    )

    df["full_text"] = df.groupby(["speaker", "time"])["text"].transform(
        lambda x: " ".join(x)
    )
    df = df.drop_duplicates(subset=["speaker", "time", "full_text"], keep="first")
    df = df[["speaker", "time", "full_text"]].rename(columns={"full_text": "text"})
    return df
