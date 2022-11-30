import streamlit as st
import pandas as pd
import plotly.express as px


#####################################
#            FUNCTIONS              #
#####################################
def additional_bedroom_opportunity(x):
  try:
    # 2bd >= 1300 can usually fit an additional bd
    # 3bd >= 1950 can usually fit an additional bd
    # 4bd >= 2600 can usually fit an additional bd
    if (x['ratio_sqft_bd'] >= 650) and (x['ratio_sqft_bd'] is not None) and (x['BEDS'] > 1) and (x['PROPERTY TYPE'] == 'Single Family Residential'):
      return True
    else:
      return False
  
  except:
    return False


def adu_potential(x):
  try:
    if (x['ratio_lot_sqft'] >= 5) and (x['ratio_lot_sqft'] is not None) and (x['HOA/MONTH'] is not None) and (x['PROPERTY TYPE'] == 'Single Family Residential'):
      return True
    else:
      return False
  except:
    return False


def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


#####################################
#            HOME PAGE              #
#####################################
st.title('Property Data Redfin 🏠')
st.markdown('The purpose of this app is to provide summary stats 📊 based on your Redfin data search.')
st.markdown("#### {0} :point_down:".format('Upload a CSV file'))
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # read csv file
    df = pd.read_csv(uploaded_file)


    #####################################
    #              METRICS              #
    #####################################
    st.markdown("## Property Metrics 🏙️")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total',  len(df), help='Number of properties in search')
    col2.metric('Avg Price', "${:,}".format(df['PRICE'].mean()).split(',')[0] + 'K', help='Average sale price of properties in search')
    col3.metric('Avg DOM', int(df['DAYS ON MARKET'].mean()), help='Average days on market of properties in search')
    col4.metric('Avg PPSQFT', "${:,}".format(int(df['$/SQUARE FEET'].mean())), help='Average price per square foot of properties in search')


    #####################################
    #             CHARTS                #
    #####################################
    with st.expander('Charts', expanded=True):
      st.markdown("## Charts 📈")
      fig = px.histogram(df, x="DAYS ON MARKET", title="Days on Market Histogram Chart")
      st.plotly_chart(fig, use_container_width=True)

      fig = px.box(df, x="PRICE", title="Price Box Plot Chart")
      st.plotly_chart(fig, use_container_width=True)

      fig = px.histogram(df, x="$/SQUARE FEET", title="Price per SQFT Histogram Chart")
      st.plotly_chart(fig, use_container_width=True)


    #####################################
    #             FEATURES              #
    #####################################
    df_features = df.copy()
    df_features['ratio_sqft_bd'] = df_features['SQUARE FEET'] / df_features['BEDS']
    df_features['additional_bd_opp'] = df_features.apply(lambda x: 
      additional_bedroom_opportunity(x), axis=1)
    df_features['ratio_lot_sqft'] =  df_features['LOT SIZE'] / df_features['SQUARE FEET']
    df_features['adu_potential'] = df_features.apply(lambda x: 
      adu_potential(x), axis=1)


    #####################################
    #              TABLES               #
    #####################################
    with st.expander('Opportunities', expanded=True):
        st.markdown("## Opportunities 💡")
        df_add_bd = df_features.loc[df_features['additional_bd_opp'] == True]
        df_adu = df_features.loc[df_features['adu_potential'] == True]

        col1, col2 = st.columns(2)
        col1.metric('Total Add Bd', len(df_add_bd), help='Number of properties with additonal bedroom opportunity')
        col2.metric('Total ADU', len(df_adu), help='Number of properties with ADU potential')

        st.markdown("#### Featurized Dataset")
        st.write(df_features)

        # convert featurized dataset to csv
        csv = convert_df(df_features)

        st.download_button(
            "Download 🔽",
            csv,
            "property_dataset.csv",
            "text/csv",
            key='download-csv'
        )