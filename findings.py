import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns # for visualizing crosstab
pd.set_option('future.no_silent_downcasting', True) # for .replace()

df = pd.read_csv("./data.csv")
# drop the first one (missing responses)
df = df.drop(index=0)
# change heads
df.columns = [chr(65 + i) for i in range(len(df.columns))]

# convert Timestamp to what time of the day user submitted
df["A"] = pd.to_datetime(df["A"])
df["timeofday"] = df["A"].dt.hour + (df["A"].dt.minute / 60 )

# link time of day with church attendance
df["A"] = pd.to_datetime(df["A"])
df["timeofday"] = df["A"].dt.hour + (df["A"].dt.minute / 60 )

df.plot.scatter("timeofday", "F",
    color='purple',        # point color
    s=60,                 # marker size
    alpha=0.7,             # transparency
    edgecolor='black',     # outline color
    figsize=(7, 5)         # figure size
)

plt.title("Church Attendance vs. Time of Day", fontsize=14, fontweight='bold')
plt.xlabel('Time of day', fontsize=12)
plt.ylabel('Attendance frequency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()

# stuff for type change and filtering (for the next 2)
answersmap = {"Strongly a jerk": 2, "Mildly a jerk": 1, "Not a jerk": 0}
opgendermap = {"K": "Male", "L": "Male", "M": "Male", "N": "Male", "O": "unk", "P": "unk", "Q": "unk", "R": "Female", "S": "Male", "T": "unk", "U": "unk", "V": "unk", "W": "Male", "X": "unk"}
malecols = [col for col, gender in opgendermap.items() if gender == "Male"]
allcols = [col for col, _ in opgendermap.items()]
intdf = df.copy()
intdf.iloc[:, 10:-1] = df.iloc[:, 10:-1].replace(answersmap).astype("int64") # converting responses to numeric

# link how men vs women respond to male op
avgofmaleops = intdf.groupby("J")[malecols].mean().T.astype("float")
boxprops = dict(facecolor='lightblue', color='black', alpha=.5)
medianprops = dict(color='black', linewidth=1.5)
flierprops = dict(marker='o', color='gray', markersize=6, alpha=0.5)
avgofmaleops.plot(kind='box', patch_artist=True,
        boxprops=boxprops, medianprops=medianprops,
        flierprops=flierprops, figsize=(6,5))
# put points on top of graph
for i, col in enumerate(avgofmaleops.columns, start=1):
    plt.scatter([i]*len(avgofmaleops), avgofmaleops[col], color='black', s=30, alpha=0.7)
plt.title('Average Response to male posters by Gender')
plt.ylabel('Average')
plt.xlabel("Gender")
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()

t, p = stats.ttest_ind(avgofmaleops["Male"], avgofmaleops["Female"], equal_var=False)
print(f"Male and Female to male ttest\nt = {t:.3f}, p = {p:.4f}")

# link how men respond to male op vs any op
avgofallops = intdf.groupby("J")[allcols].mean().T.astype("float")
avgofallops["Both"] = intdf[allcols].mean().T.astype("float")
avgofallops.plot(kind='box', patch_artist=True,
        boxprops=boxprops, medianprops=medianprops,
        flierprops=flierprops, figsize=(6,5))
# put points on top of graph
for i, col in enumerate(avgofallops.columns, start=1):
    plt.scatter([i]*len(avgofallops), avgofallops[col], color='black', s=30, alpha=0.7)
plt.title('Average Response to all posters by Gender')
plt.ylabel('Average')
plt.xlabel("Gender")
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()

t, p = stats.ttest_ind (avgofallops["Male"], avgofallops["Female"])
print(f"men to men vs any\nt = {t:.3f}, p = {p:.4f}")

# mapping for the next 2 questoins
df["F"] = df["F"].apply(lambda x: "churchgoer" if x == "Frequently" or x == "Often" else "nongoer")
df["G"] = df["G"].apply(lambda x: "churchgoer" if x == "Frequently" or x == "Often" else "nongoer")

# linking parents going to church with respondents going to church
df["Self"] = df["F"]
df["Parents"] = df["G"]
ct = pd.crosstab(df["Self"], df["Parents"])
order = ["churchgoer", "nongoer"]
rev = ["nongoer", "churchgoer"]
ct = ct.reindex(index=order, columns=rev)
plt.figure(figsize=(6,5))
sns.heatmap(ct, annot=True, fmt='d', cmap='Blues')
plt.title('User vs Parent Churchgoing')
plt.xlabel('Parent Churchgoing')
plt.ylabel('User Churchgoing')
plt.show()

_, p, _, _ = stats.chi2_contingency(ct)
print(f"parent vs self churchgoing\np = {p}")

# linking parent sportwatching with respondent sport watching
df["Self"] = df["H"]
df["Parents"] = df["I"]
ct = pd.crosstab(df["Self"], df["Parents"])
order = ["Never", "Often", "Frequently"]
rev = ["Frequently", "Often", "Never"]
ct = ct.reindex(index=order, columns=rev)
plt.figure(figsize=(6,5))
sns.heatmap(ct, annot=True, fmt='d', cmap='Blues')
plt.title('User vs Parent Sportswatching')
plt.xlabel('Parent Sportswatching')
plt.ylabel('User Sportswatching')
plt.show()

_, p, _, _ = stats.chi2_contingency(ct)
print(f"parent vs self sportwatching\np = {p}")

# linking parent politcs with respondent politics
politicsmap = {"Strongly conservative": "Cons++", "Mildly conservative": "Cons+", "Mildly liberal": "Lib+", "Strongly liberal": "Lib++"}
polidf = df[(df["E"] != "Don't know / It's complicated") & (df["D"] != "Don't know / It's complicated")].replace(politicsmap)
rev = ["Lib++", "Lib+", "Neutral", "Cons+", "Cons++"]
order = ["Cons++", "Cons+", "Neutral", "Lib+", "Lib++"]
polidf["Self"] = polidf["E"]
polidf["Parents"] = polidf["D"]
ct = pd.crosstab(polidf["Self"], polidf["Parents"])
ct = ct.reindex(index=order, columns=rev)
plt.figure(figsize=(6,5))
sns.heatmap(ct, annot=True, fmt='d', cmap='Blues')
plt.title('User vs Parent Politics')
plt.xlabel('Parent Politics')
plt.ylabel('User Politics')
plt.show()

_, p, _, _ = stats.chi2_contingency(ct)
print(f"parent vs self politics\np = {p}")

# most polarizing
avgofallops["polarity"] = avgofallops["Male"] - avgofallops["Female"]
avgofallops["polarity"] =  avgofallops["polarity"].apply(lambda x: abs(x))
print(avgofallops[avgofallops["polarity"] == avgofallops["polarity"].max()])
avgofallops.index = range(1, len(avgofallops) + 1)
avgofallops["polarity"].plot(kind="bar", color="sandybrown", edgecolor="black", alpha=.9)
plt.title("Difference in Average Rating per Question (by gender)")
plt.xlabel("Question #")
plt.ylabel("Rating Difference")
plt.tight_layout()
plt.show()
