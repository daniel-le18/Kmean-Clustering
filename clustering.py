import pandas as pd


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
    )
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
    return tweet_data


if __name__ == "__main__":
    tweet_data = read_csv()
    tweet_data = preprocess(tweet_data)

    print(tweet_data)

    # Distance testing
    set1 = {"1", "2", "3"}
    set2 = {"3", "4", "5"}
    distance = Jaccard_distance(set1, set2)
    print(distance)

    # for i in range(tweet_data.shape[0]):
    #     print(tweet_data.iloc[[i]])

    # TODO: Spliting each row into a set then pass to distance
