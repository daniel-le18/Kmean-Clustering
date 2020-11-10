import pandas as pd
import numpy as np


def Jaccard_distance(set1, set2):
    # TODO: Distance =  1- (A.intersection(B))/ (A.union(B))
    distance = 1 - len(set1.intersection(set2)) / len(set1.union(set2))
    return distance


def read_csv():
    tweet_data = pd.read_csv(
        "https://raw.githubusercontent.com/daniel-le18/dataset/master/bbchealth.csv",
        sep="|",
        header=None,
        usecols=[2],
    ).head(50)
    return tweet_data


def preprocess(tweet_data):
    # Remove link
    tweet_data = tweet_data.replace(
        regex=True,
        to_replace=[r"(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b"],
        value=[""],
    )

    # Remove @
    tweet_data = tweet_data.replace(
        regex=True,
        to_replace=[r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"],
        value=[""],
    )

    # Remove #tag
    tweet_data = tweet_data.replace(
        regex=True,
        to_replace=[r"(#[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"],
        value=[""],
    )

    # Convert tweets to lowercase
    tweet_data = tweet_data.apply(lambda x: x.astype(str).str.lower())

    return tweet_data


def K_mean():
    pass


if __name__ == "__main__":
    # Read in and process data
    tweet_data = read_csv()
    tweet_data = preprocess(tweet_data)

    # Getting the distances between points
    list = []
    for i in range(tweet_data.shape[0]):
        set1 = set(tweet_data.iloc[i, :].str.split(expand=True).iloc[0, :])
        for j in range(tweet_data.shape[0]):
            set2 = set(tweet_data.iloc[j, :].str.split(expand=True).iloc[0, :])
            distance = Jaccard_distance(set1, set2)
            list.append(distance)

    list = np.array(list).reshape(tweet_data.shape[0], tweet_data.shape[0])
    print("\nDistance between each tweets: ")
    print(list)
