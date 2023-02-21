# %%
import pandas as pd
import numpy as np
import os

# from moves.library import start

# moves = [
#     "1 TellBack Positive Evaluation",
#     "2 Tellback Observation",
#     "3 Tellforward Suggestion",
#     "4 Tellforward Instruction",
#     "5 Tellforward Demonstration",
#     "6 Askforward Anticipation",
#     "7 Practice",
#     "8 Rapport Encouragement",
# ]

# %% Append all Coder 1 Week 1 Files
DIR = "/Users/kylieanglin/Box Sync/Measuring Coaching Fidelity and Quality/-LOOK/"
DIR_DATA = DIR + "annotations/completed/"

transcript_files = []
for filename in os.listdir(DIR_DATA):
    if os.path.isfile(os.path.join(DIR_DATA, filename)):
        print(filename)
        transcript_files.append(filename)
# %%
COLUMNS = [
    "Speaker",
    "Text",
    "Move 1",
    "Move 2",
    "Move 3",
    "Move 4",
    "Move 5",
    "Move 6",
    "Move 7",
    "Move 8",
    "Move 9",
    "Move 10",
]
transcript_df = pd.DataFrame(columns=COLUMNS)

for filename in transcript_files:
    df = pd.read_excel(
        DIR_DATA + filename,
    )
    df = df[COLUMNS]
    df["Transcript"] = filename
    transcript_df = transcript_df.append(df)

# %%
transcript_df = transcript_df[~transcript_df["Move 1"].isnull()]


# %%
move_columns = [col for col in transcript_df.columns if col.startswith("Move")]
moves = []
for column in move_columns:
    moves += df[column].unique().tolist()
moves = set(moves)

# %%
moves = []
for column in move_columns:
    values = transcript_df[column].value_counts().index.to_list()
    for value in values:
        if value not in moves:
            moves.append(value)
moves.sort()
# %%
moves_df = transcript_df[["Transcript"]]
for move in moves:
    moves_df[move] = 0
moves_df

# %%
for move in moves:
    for col in move_columns:
        moves_df[move] = np.where(transcript_df[col] == move, 1, moves_df[move])


# %%
moves_df["Transcript"] = moves_df.Transcript.str.replace(".xlsx", "")
grouped_df = moves_df.groupby(["Transcript"]).sum()

# %%
meta_data = pd.read_csv(DIR + "data/clean/meta_data.csv")

final_df = grouped_df.merge(meta_data, left_index=True, right_on="file", how="left")

# %%
final_df.to_excel(DIR + "data/clean/move_counts_by_transcript.xlsx")

# %%

cols = ["coach"]
for move in moves:
    cols.append(move)

coach_df = final_df[cols].groupby("coach").sum()

coach_df.to_excel(DIR + "data/clean/move_counts_by_coach.xlsx")

# %%
cols = ["data_conversation"]
for move in moves:
    cols.append(move)

conversation_df = final_df[cols].groupby("data_conversation").sum()

coach_df.to_excel(DIR + "data/clean/move_counts_by_data_conversation.xlsx")

# %%
