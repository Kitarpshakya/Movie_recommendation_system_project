import pre_processing
from sklearn.cluster import KMeans


def Clustered_final_df(df):
    df['Cluster_ID'] = None

    #modify the n_clusters value to get the more detailed clustering
    kmeans = KMeans(n_clusters= 500)
    features = df[['P_Genre','S_Genre','T_Genre']]
    kmeans.fit(features)
    df['Cluster_ID'] = kmeans.predict(features)
    return df


def cluster_everything(input_movies):
    df = pre_processing.pre_process_all()
    # print(df)
    df = Clustered_final_df(df)
    # print(df)
    df.to_csv('Dataset_to_plot.csv',index = False)
    #check if the movie is present or not

    input_movies = input_movies.lower()
    try:
        movie_not_found = df.loc[~df['Movies'].str.contains(input_movies)]
        if len(movie_not_found) == 0:
            print('Movie not found!!')
            return 0
        get_cluster = df['Cluster_ID'].loc[df['Movies'].str.contains(input_movies)].values[0]
        similar_movies_list = df['Movies'].loc[df['Cluster_ID']==get_cluster].values
        return similar_movies_list
    except:
        print('Movie not found!!!')
        return 0


# test = cluster_everything('Blonde')




