# %%
import pandas as pd
import numpy as np

# %%
df = pd.read_csv(
    "/Users/kylieanglin/Box Sync/Measuring Coaching Fidelity and Quality/-LOOK/data/temp/LIWC-22 Results - long_transcript - LIWC Analysis.csv"
)

# %% Turns of talk
df["coach"] = np.where(df.speaker == "coach", 1, 0)
df["teacher"] = np.where(df.speaker == "teacher", 1, 0)

turns = df[["transcript", "coach", "teacher"]].groupby(["transcript"]).sum()
# %%
df[df.coach == 1].WC.mean()

df[df.teacher == 1].WC.mean()

# %%
teachers = df[df.teacher == 1]

coaches = df[df.coach == 1]

# %%
teachers.i.mean()
teachers.you.mean()
# %%
coaches.i.mean()
coaches.you.mean()
# %%
coaches.emo_pos.mean()
teachers.emo_pos.mean()
# %%
coaches.emo_neg.mean()
teachers.emo_neg.mean()
# %%
