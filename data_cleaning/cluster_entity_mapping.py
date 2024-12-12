from utils.cluster_mapping import clusters


def map_cluster_with_entity(df):
    """
    Maps each entity in the dataframe to its corresponding cluster name based on the clusters mapping.
    Args:
        df (pandas.DataFrame): The input dataframe containing an 'ENTITY' column.
    Returns:
        pandas.DataFrame: The input dataframe with a new column 'ENTITY_CLUSTER_NAME'
                           indicating the cluster name for each entity.
    """

    # Create a dictionary to map entities to their respective cluster names
    entity_to_cluster = {}

    # Loop through each cluster and its corresponding entities, assigning them to the dictionary
    for cluster_name, entities in clusters.items():
        for entity in entities:
            entity_to_cluster[entity] = cluster_name

    # Map the 'ENTITY' column to 'ENTITY_CLUSTER_NAME' based on the entity_to_cluster mapping
    df["ENTITY_CLUSTER_NAME"] = df["ENTITY"].map(entity_to_cluster)

    return df
