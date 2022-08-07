import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("Dataset_to_plot.csv")

def data_plot_3d(data, labels=None):
    """Wrapper for 3D data plot
    
    Parameters:
        data: pandas dataframe
        labels: labels of the data points(if available)
        
    """
    fig = plt.figure(figsize=(15,10))
    ax = fig.add_subplot( projection='3d')

    g = ax.scatter(data["P_Genre"], data["S_Genre"], data["T_Genre"],c = data['Cluster_ID'])
    print(data["Cluster_ID"])
    plt.tight_layout()
    plt.show()

data_plot_3d(df)
