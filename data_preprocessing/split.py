import pandas as pd
import random

# Read the clustering results
clusters = pd.read_csv("cluster_result.tsv", sep="\t", header=None)
clusters.columns = ["SequenceID", "ClusterID"]

# Group by ClusterID
cluster_groups = clusters.groupby("ClusterID").groups

# Set the data set partitioning ratio
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Random partition clustering
cluster_ids = list(cluster_groups.keys())
random.shuffle(cluster_ids)
train_cutoff = int(len(cluster_ids) * train_ratio)
val_cutoff = train_cutoff + int(len(cluster_ids) * val_ratio)

train_clusters = cluster_ids[:train_cutoff]
val_clusters = cluster_ids[train_cutoff:val_cutoff]
test_clusters = cluster_ids[val_cutoff:]

# Assign a data set label to each sequence
clusters["Dataset"] = clusters["ClusterID"].apply(
    lambda x: "train" if x in train_clusters else
              "val" if x in val_clusters else
              "test"
)

# Save partition result
clusters.to_csv("split_dataset.tsv", sep="\t", index=False)

print("Dataset split complete. Saved to split_dataset.tsv")

# Merge the partition result with the original sequence data

sequences = pd.read_csv("all_sequences.csv")
dataset_split = pd.read_csv("split_dataset.tsv", sep="\t")

# print("Sequences columns: ", sequences.columns)
# print("Dataset split columns: ", dataset_split.columns)
data_with_split = sequences.merge(dataset_split, left_on="ID", right_on="SequenceID")

print(data_with_split.head())
data_with_split.to_csv("merged_dataset.csv", index=False)