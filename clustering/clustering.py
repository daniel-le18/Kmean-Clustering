import pandas as pd
import numpy as np
import copy


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


def update_new_centroids(new_centroids_index_list, centroids, k):
    new_centroids = []
    new_centroid = tweet_data.iloc[new_centroids_index_list]
    new_centroids.append(new_centroid)
    return new_centroids


def K_mean(k, coverge, iteration, centroids):
    for z in range(iteration):
        print(type(centroids))
        # # Create 5 cluster list
        # for i in range(k):
        #     cluster[i] = []

        # TODO:✔️💯  Get the distance between each elements of centroids list with the remaining
        list = []
        for i in range(k):
            set1 = set(centroids[i].str.split(expand=True).iloc[0, :])
            for j in range(tweet_data.shape[0]):
                set2 = set(tweet_data.iloc[j, :].str.split(expand=True).iloc[0, :])
                # print(i, set1)
                # print(j, set2)
                distance = Jaccard_distance(set1, set2)
                list.append(distance)
                # print(distance, "\n")

        list = np.array(list).reshape(k, int(len(list) / k))
        # print(list)

        new_centroids_index_list = []
        for i in range(k):
            shortest_distance = [x for x in list[i] if x != 0]

            # New centroids
            new_centroid_distance = min(shortest_distance)

            # New centroids index
            new_centroid_index = shortest_distance.index(min(shortest_distance))
            new_centroids_index_list.append(new_centroid_index)

            # print(
            #     "Shortest distance between the old centroid index",
            #     i,
            #     "and the new centroid index",
            #     new_centroid_index,
            #     "centroids",
            #     ":",
            #     new_centroid_distance,
            # )

        # TODO : Update the new centroids into the centroids[]
        new_centroids = update_new_centroids(new_centroids_index_list, centroids, k)
        centroids = copy.deepcopy(new_centroids)
        print("\nNew centroids: ", new_centroids)
        print(type(centroids))


if __name__ == "__main__":
    # Read in and process data
    tweet_data = read_csv()
    tweet_data = preprocess(tweet_data)

    # print(tweet_data)

    # Parameter for K mean
    k = 5
    converge = 0.0001
    iteration = 4

    # Choosing the first 5 tweets
    centroids = []
    for i in range(k):
        centroids.append(tweet_data.iloc[i, :])

    print(centroids)
    # K-mean
    K_mean(k, converge, iteration, centroids)
    # print("\n", centroids)