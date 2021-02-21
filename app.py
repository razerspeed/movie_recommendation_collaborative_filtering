import streamlit as st
import requests
import pandas as pd
from io import BytesIO
from PIL import Image
import math
import pickle
import scipy.sparse

lookup_dataframe=pd.read_csv('final_list.csv',index_col='index_col')

max_no_of_suggestion = st.sidebar.select_slider('How many suggestion you want' ,[x for x in range(10) if x],value=9)
st.sidebar.write("Selected :",max_no_of_suggestion)

options=st.multiselect('Select Movie', lookup_dataframe.title.values)
movie_sparse = scipy.sparse.load_npz('sparse_matrix.npz')
model = pickle.load(open("model.save", 'rb'))

if options:
    for i in range(len(options)):
        st.write('You selected:', options[i])



#api configuration
CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
KEY = '27f7e04d7115ca346c575e9209a44616'

url = CONFIG_PATTERN.format(key=KEY)
r = requests.get(url)
config = r.json()

base_url = config['images']['base_url']
sizes = config['images']['poster_sizes']

def size_str_to_int(x):
    return float("inf") if x == 'original' else int(x[1:])
max_size = max(sizes, key=size_str_to_int)



def fetch_image(imdbid):
    IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
    imdbid="{:07d}".format(imdbid)
    imdbid_full='tt'+str(imdbid)
    # st.write(imdbid_full)
    r = requests.get(IMG_PATTERN.format(key=KEY, imdbid=f'{imdbid_full}'))
    api_response = r.json()
    # st.write(api_response)
    posters = api_response['posters'][0]
    url = base_url + max_size + posters['file_path']
    r = requests.get(url)
    im = Image.open(BytesIO(r.content))
    return im


if st.button('Done Selection'):
    if options:
        st.write('Please wait fetching data...')
        movies_df = pd.DataFrame(columns=["distance", 'suggestions', 'rank'])
        for i in options:
            print(i)
            # st.write('i',i)
            a = lookup_dataframe[lookup_dataframe.title == f"{i}"].index[0]
            rank = [x for x in range(0, 10)]
            distances, suggestions = model.kneighbors(movie_sparse[a, :].toarray())
            temp_df = pd.DataFrame(list(zip(distances.reshape(-1), suggestions.reshape(-1), [x for x in range(1, 11)])),
                                   columns=["distance", 'suggestions', 'rank'])

            movies_df = movies_df.append(temp_df)
        # st.write(movies_df)
        movies_df.sort_values(['rank'], inplace=True)
        movies_df = movies_df.drop_duplicates(subset=['suggestions']) #dropping duplicate suggestions


        # st.write(movies_df)

        images=[]
        title=[]
        # len(options) because it contains the user selected movies
        for i in range(len(movies_df[:max_no_of_suggestion + len(options)])):
            title_temp=lookup_dataframe[lookup_dataframe.index==movies_df.iloc[i]['suggestions']].title.values[0]
            title.append(title_temp)
            imdb_no=lookup_dataframe[lookup_dataframe.index==movies_df.iloc[i]['suggestions']].imdbId.values[0]
            # st.write(imdb_no)
            images.append(fetch_image(imdb_no))

        y=True
        if len(options)>3:
            no_of_col=3
        else:
            no_of_col=len(options)
        st.header("your choice")
        i = 0
        while y:

            for col in st.beta_columns(no_of_col):

                with col:
                    st.header(title[i])
                    st.image(images[i], use_column_width=True)
                    i+=1
                if i>=len(options):
                    y=False
                    break

        st.header("your recommendations")

        i=len(options)
        # st.write(i)
        y=True

        while y:

            for col in st.beta_columns(3):

                with col:
                    st.header(title[i])
                    st.image(images[i], use_column_width=True)
                    i+=1
                if i>=max_no_of_suggestion:
                    y=False
                    break

    else:
        st.write('Select a movie then press Done Selecting')

