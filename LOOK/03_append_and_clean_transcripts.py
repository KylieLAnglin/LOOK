# %%
import pandas as pd
import numpy as np
import os

from library import start

# %% Append all empty uncoded transcript files
meta_data = pd.read_csv(start.DATA_DIR + "clean/meta_data.csv")


transcript_files = []
for filename in os.listdir(start.DATA_DIR + "clean/transcripts_to_excel/"):
    if filename.endswith(".xlsx"):
        print(filename)
        transcript_files.append(filename)
# %%
COLUMNS = [
    "Speaker",
    "Text",
]
transcript_df = pd.DataFrame(columns=COLUMNS)

for filename in transcript_files:
    df = pd.read_excel(
        start.DATA_DIR + "clean/transcripts_to_excel/" + filename,
    )
    df = df[COLUMNS]
    df["Transcript"] = filename
    transcript_df = transcript_df.append(df)

# %%
transcript_df = transcript_df.rename(
    columns={"Speaker": "speaker", "Text": "text", "Transcript": "transcript"}
)


# %%
transcript_df["speaker"] = np.where(
    transcript_df.speaker.str.contains("Teacher"), "teacher", transcript_df.speaker
)

transcript_df["speaker"] = np.where(
    transcript_df.speaker.str.contains("Coach"), "coach", transcript_df.speaker
)
# %%

transcript_df["speaker"] = np.where(
    transcript_df.speaker.isin(["coach", "teacher"]), transcript_df.speaker, ""
)

# %%

transcript_df["text"] = transcript_df["text"].str.split(":", n=1).str[1]


transcript_df.to_csv(start.DATA_DIR + "clean/long_transcript.csv")
# %%
