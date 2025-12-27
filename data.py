import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

pd.set_option('future.no_silent_downcasting', True)
# Load CSV
df = pd.read_csv("./data.csv")
# drop the first one (missing responses)
df = df.drop(index=0)
# change heads
df.columns = [chr(65 + i) for i in range(len(df.columns))]

# politics_map = {"Strongly conservative": 5, "Mildly conservative": 4, "Neutral": 3, "Mildly liberal": 2, "Strongly liberal": 1, "Don't know / It's complicated": 0}
# df["me"] = df["D"].map(politics_map)
# df["mine"] = df["E"].map(politics_map)
# df.plot.scatter("me", "mine", title="Simple Scatter Plot")

# df2 = pd.concat([df["D"].value_counts(), df["E"].value_counts()], axis=1)
# df2.columns = ["Parents", "Personal"]
# print(df2.head(6))

df["A"] = pd.to_datetime(df["A"])
df["timeofday"] = df["A"].dt.hour + (df["A"].dt.minute / 60 )
# print(df["timeofday"].head())
# df.plot.scatter("timeofday", "F")
# plt.show()

answersmap = {"Strongly a jerk": 2, "Mildly a jerk": 1, "Not a jerk": 0}
opgendermap = {"K": "Male", "L": "Male", "M": "Male", "N": "Male", "O": "unk", "P": "unk", "Q": "unk", "R": "Female", "S": "Male", "T": "unk", "U": "unk", "V": "unk", "W": "Male", "X": "unk"}


# # turn the map into a array of cols
# maleposts = ["J"] + [col for col, gender in opgendermap.items() if gender == "Male"]
# intdf = df.replace(answersmap).apply(pd.to_numeric, errors="ignore")
# intdf = intdf.drop(df.columns[[0, -1]], axis=1)

# maleopmeans = intdf[maleposts].groupby("J").mean(numeric_only=True)
# print(maleopmeans.T)
# maleopmeans.T.boxplot()
# plt.show()

# print(maleanswers[malecols].mean().mean())
# print(femaleanswes[malecols].mean().mean())
#print(df.columns.map(gendermap))



# V is the LGBTQ question
# how the church goers voted on the lgbt folk
df["F"] = df["F"].apply(lambda x: "yes" if x == "Frequently" or x == "Often" else "no")
ct = pd.crosstab(df["F"], df["V"])
print(ct)
chi2, p, _, expected = stats.chi2_contingency(ct)
print(f"Chi2 results: {chi2:.3f}, p = {p:.4f}")
print(df["V"].map(answersmap))

# df.plot.scatter("timeofday", "L")
# numericaldf = df.replace(answersmap)
# numericaldf = numericaldf.drop(index=0, columns="timeofday")
# sumstat = numericaldf.iloc[:, 10:].var()
# print(sumstat)
# print(sumstat.max())

# print(maleanswers["O"].mean())
# maleanswers.plot.scatter("timeofday", "O")
# plt.show()
# print(femaleanswers["O"].mean())

# frequencymap = {"Frequently": "yes", "Often": "no", "Never": "no"}
# freqdf = df.replace(frequencymap)
# ct = pd.crosstab(freqdf["H"], freqdf["J"])
# print(ct)
# chi2, p, _, expected = stats.chi2_contingency(ct)
# print(f"Chi2 results: {chi2:.3f}, p = {p:.4f}") # passes :)

# ct = pd.crosstab(df["J"], df["K"])
# chi2, p, _, _ = stats.chi2_contingency(ct)
# print(f"Chi2 results: {chi2:.3f}, p = {p:.4f}")
