
import pandas as pd
import numpy as np
import copy
import math
from pandas import DataFrame


def Jaccard_distance(set1, set2):
    # TODO: Distance =  1- (A.intersection(B))/ (A.union(B))
    distance = 1 - len(set1.intersection(set2)) / len(set1.union(set2))
    return distance


def read_csv(instances):
    tweet_data = pd.read_csv(
        "https://raw.githubusercontent.com/daniel-le18/dataset/master/bbchealth.csv",
        sep="|",
        header=None,
        usecols=[2],
    ).head(instances)
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
    for i in range(k):
        new_centroid = tweet_data.iloc[new_centroids_index_list[i]]
        new_centroids.append(new_centroid)
    return new_centroids


def calculate_sse(new_centroid_index, centroids, centroids_sse, k):
    sse = 0.0
    for i in range(k):
        set1 = set(centroids[i].str.split(expand=True).iloc[0, :])
        set2 = set(centroids_sse[i].str.split(expand=True).iloc[0, :])
        distance = Jaccard_distance(set1, set2) ** 2
        sse += distance
    # print(new_centroid_index)
    # print(centroids)
    return sse


def K_mean(k, iteration, centroids, cluster_sizes):
    sse = 0
    for z in range(iteration):
        print("\nIteration: ", z + 1)
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
            cluster = [x for x in list[i] if x != 0 and x != 1]
            if(z == iteration-1):
                cluster_sizes.append(len(cluster))
            print("Cluster size for", "centroid", i, ":", len(cluster))
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
        centroids_sse = centroids
        #print("Previous centroids: ", centroids)
        centroids = copy.deepcopy(new_centroids)

        sse += calculate_sse(new_centroid_index, centroids, centroids_sse, k)
        #print("\nNew centroids: ", new_centroids)
        print("SSE", sse)
    return sse


if __name__ == "__main__":
    instances = int(input("How many tweets do you want to loop through: "))

    # Read in and process data
    tweet_data = read_csv(instances)
    tweet_data = preprocess(tweet_data)

    # print(tweet_data)

    # Parameter for K mean
    k = int(input("Please input number of cluster you want: "))

    iteration = 5

    # Choosing the first 5 tweets
    centroids = []
    for i in range(k):
        centroids.append(tweet_data.iloc[i, :])

    # K-mean
    sse = 0.0
    cluster_sizes = []
    sse = K_mean(k, iteration, centroids, cluster_sizes)
    print("| Value of K | SSE | Size of each cluster |")
    print("|", k, " "*(9-len(str(k))), "|", round(sse), " "*(3-len(str(sse))), "|", end =" ")
    print(1, ":", cluster_sizes[0], "tweets", " "*(9-len(str(cluster_sizes[0]))-len(str(1))), "|")
    for i in range(1, k):
        print("|", " "*(10), "|", " "*(3), "|", i+1, ":", cluster_sizes[i], "tweets", " "*(9-len(str(cluster_sizes[i]))-len(str(i+1))), "|")
    # print("\n", centroids)