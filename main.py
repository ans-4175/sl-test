import numpy as np
import pandas as pd
import streamlit as st

st.title('Test Streamlit')
st.write("### Hi there!")
st.text("This is an app!")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# SIDEBAR
hour_to_filter = st.sidebar.slider('Hour of Pickups', 0, 23, 17)
# ---END SIDEBAR

# STATE HANDLER
if "df_option" not in st.session_state:
    st.session_state.df_option = df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })
if "df_table" not in st.session_state:
    st.session_state.df_table = pd.DataFrame(
        np.random.randn(10, 20),
        columns=('col %d' % i for i in range(20))
    )
if "df_map" not in st.session_state:
    st.session_state.df_map = map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon']
    )

# --END STATE HANDLER

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

left_column, right_column = st.columns(2)
with left_column:
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f'Map of all pickups at {hour_to_filter}:00')
    st.map(filtered_data)

with right_column:
    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0,24)
    )[0]
    st.bar_chart(hist_values)
    
    # option = st.selectbox(
    #     'Which number do you like best?',
    #     st.session_state.df_option['first column'])
    # st.write('You selected: ', option)
    # st.table(st.session_state.df_table)

if st.checkbox('Show All Data'):
    st.subheader('Raw data')
    st.write(data)

    st.subheader('Map of all pickups')
    st.map(data)