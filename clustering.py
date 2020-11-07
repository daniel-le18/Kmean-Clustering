import pandas as pd

tweet_data = pd.read_csv(
    "https://raw.githubusercontent.com/daniel-le18/dataset/master/bbchealth.csv",
    sep="|",
    header=None,
    usecols=[2],
)
tweet_data = tweet_data.replace(
    regex=True, to_replace=[r"(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b"], value=[""]
)
tweet_data = tweet_data.replace(
    regex=True,
    to_replace=[r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"],
    value=[""],
)

print(tweet_data)
