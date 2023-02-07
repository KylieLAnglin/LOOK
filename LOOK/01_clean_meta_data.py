# %%
import os
import pandas as pd
import numpy as np
from library import start

# %%
meta_data = pd.read_excel(start.DATA_DIR + "raw/LOOK Transcripts - ALL.xlsx")

# %%
files = [
    f.name
    for f in os.scandir(start.DATA_DIR + "raw/transcripts/")
    if f.name.endswith(".txt")
]

filenames = [file.replace(".txt", "") for file in files]

meta_data["file"] = meta_data["File Name"].str.replace(".docx", "")
meta_data["file"] = meta_data["file"].str.replace("_otter_ai", "")
meta_data["file"] = meta_data["file"].str.replace(".mov", "")

meta_data["transcript_in_box"] = np.where(meta_data["file"].isin(filenames), 1, 0)
meta_data = meta_data[meta_data.transcript_in_box == 1]
# %%
meta_data["coach"] = meta_data.Coach
original_column = "Does the coach appear to spend time sharing/explaining student assessment data with the teacher?"
meta_data["data_conversation"] = np.where(
    meta_data[original_column].isin(["Yes", "yes"]), 1, 0
)
meta_data["strata_type"] = (
    meta_data["coach"].astype(str) + "_" + meta_data["data_conversation"].astype(str)
)

# %%
df_1 = meta_data[meta_data.strata_type == "16_0"]
df_1["random_order"] = np.random.permutation(len(df_1))
df_2 = meta_data[meta_data.strata_type == "11_0"]
df_2["random_order"] = np.random.permutation(len(df_2))

df_3 = meta_data[meta_data.strata_type == "16_1"]
df_3["random_order"] = np.random.permutation(len(df_3))

df_4 = meta_data[meta_data.strata_type == "11_1"]
df_4["random_order"] = np.random.permutation(len(df_4))

df = pd.concat([df_1, df_2, df_3, df_4])
df = df.sort_values(by=["random_order", "strata_type"])

df = df[["file", "coach", "data_conversation", "random_order"]]

df.to_csv(start.DATA_DIR + "clean/meta_data.csv", index=False)


# %%
for file in filenames:
    if file not in list(meta_data.file):
        print(file)
# %%
