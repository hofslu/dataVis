from sklearn.decomposition import PCA
from sklearn import preprocessing

import pandas as pd

def build_PCA(df, attribute):
    """builds PCA scatter-data-frame for each country, based on attribute-selection

    Args:
        df (Pandas.DataFrame): the actual data frame
        attribute (string): the attribute selection string

    Returns:
        Pandas.DataFrame: head{adCountryCode, PCA1, PCA2}
    """


def PrComAnalysis(df, string):
    df_2020 = df[df["year"] == 2020].copy()

    tmp = list(df_2020.columns)
    tmp.remove(string)
    tmp.remove('Country Name')
    tmp.remove('Country Code')
    tmp.remove('year') 

    # distributing the dataset into two components X and y
    # We decided to do the regression on Agricultural land (% of land area)
    X = df_2020[tmp].values 
    y =  df_2020.loc[:,[string]].values

    # fitting the Standard scale
    X_scaled = preprocessing.scale(X)

    # Create a PCA object and fit it to the data
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(X_scaled)

    df_PCA = pd.DataFrame(data = principalComponents
                          , columns = ['PC1', 'PC2'])
    df_PCA = pd.concat([df_PCA, pd.Series(df_2020['Country Code'].values)], axis = 1)
    df_PCA.columns = ['PC1', 'PC2', 'Country Code']

    return df_PCA