######## Rememebr all this code is in a version of PYTHON #########
### this section commented out to a convert SIS to SnIS solution ####
### Import python packages 
##import streamlit as st  ## This is s streamlit package running in python engine
##import datetime
###import pandas
###from snowflake.snowpark.context import get_active_session
#from snowflake.snowpark.functions  import col

###session = get_active_session()
### add the new connection string to be used in the active session instead
###cnx = st.connection("smothiesConstr", type="snowflake")
###session = cnx.session()
#############################################################################

######## Rememebr all this code is in a version of PYTHON #########
##### Import python packages
import streamlit as st
import datetime
import requests
import pandas as pd
###from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions  import col

cnx = st.connection("smothieConnStr","snowflake")
session = cnx.session()

# create a function that sets the value in state back to an empty list
##To identify the element in the state do as in asp.net toi dentify the lement with the unique KEY 
def clear_multi():
    st.session_state['iMultiSelect']= []
    return

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write("""Choose the fruits you want in your custom smoothie!! """)

option = st.selectbox("How would you like to be contacted", ('Email','Home Phone', 'Mobile phone'), index=0)
st.write('You selected:', option)

## option = st.selectbox("What is your favorite Fruit", ('Banana','Strawberries', 'Peaches'), index=0)
## st.write('Your favorite Fruit is:', option)

NamedYourDrink = st.text_input("The Name on your Smoothie will be: ",'')

###session = get_active_session()
###session=cnx.session()
df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))
##st.dataframe(data=df, use_container_width=True)

pd_df=df.to_pandas()
###st.dataframe(pd_df)

container = st.container()
allFruits = st.checkbox("Select all")
if (allFruits):
    ingredients_list = container.multiselect("Select all:",df.select(col("FRUIT_NAME")),df.select(col("FRUIT_NAME")),key="iMultiSelect",max_selections=5)
else:
####    selected_options = container.multiselect("choose up to 5 ingredients:", df.select(col("FRUIT_NAME")), key="iMultiSelect", max_selections=5)
    ingredients_list = st.multiselect('Choose up to 5 ingredients:',df,max_selections=5)

## check if the selected options array is empty
st.divider()
if  st.toggle("Check Ingredients..."):
    ingredients_str=''
    if (ingredients_list):
        for fruit_selected in ingredients_list:
            ingredients_str += fruit_selected + ' '
            st.subheader(fruit_selected + ' Nutrition Information')
            search_on=pd_df.loc[pd_df["FRUIT_NAME"] == fruit_selected, "SEARCH_ON"].iloc[0]
            webRestResponse = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
            if (webRestResponse.status_code != 200):
                st.write('The search value for ', fruit_selected, ' is ', search_on, '.')
                ingredients_list = st.dataframe(webRestResponse.json(),use_container_width=True)
                UpdtSQlCmd= """ Update smoothies.public.fruit_options(search_on)
                                values ('""" + fruit_selected  + """')"""
                ##st.write(UpdtSQlCmd)
                ###session.sql(UpdtSQlCmd).collect()
            st.divider()
            SQlCmd= """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_str + """','""" + NamedYourDrink + """')"""
        ### Start the sql command to insert the rows
        st.write(SQlCmd)
        ### this is the command to stop further execution when troubleshooting
        ### st.stop()
        start_order=st.button('Submit order')
        if start_order:
            session.sql(SQlCmd).collect()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            sucessMsg=(f"Your smoothie {NamedYourDrink} is ordered! {timestamp}")
            st.write(sucessMsg)
            st.success(sucessMsg, icon="✅") 


        ##create your button to clear the state of the multiselect
        st.button("Clear form", on_click=clear_multi)
