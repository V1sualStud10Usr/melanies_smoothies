######## Rememebr all this code is in a version of PYTHON #########
# Import python packages
import streamlit as st
import datetime
###from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions  import col

###session = get_active_session()
### add the new connection string to be used in the active session instead
cnx = st.connection("snowflake")
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


ColumToParse="FRUIT_NAME"
MaxIngredients = 5
NamedYourDrink = st.text_input("The Name on your Smoothie for reference: ",'')

###session = get_active_session()
###session=cnx.session()
df = session.table("smoothies.public.fruit_options").select(col(ColumToParse))
###st.dataframe(data=df, use_container_width=True)
container = st.container()
allFruits = st.checkbox("Select all")
if (allFruits):
    selected_options = container.multiselect("Select all:",df,df,key="iMultiSelect",max_selections=5)
else:
    selected_options = container.multiselect("choose up to 5 ingredients:", df, key="iMultiSelect", max_selections=5)

## check if the selected options array is empty
if  len(selected_options) > MaxIngredients: 
    st.write(f"You selected more then 5 items :red[{len(selected_options)}]") 
    allFruits = False


if (selected_options):
    ingredients_list =''
    for fruit_selected in selected_options:
        ingredients_list+= fruit_selected + ' '
    
    if ingredients_list:
        st.write(f"List :blue[{ingredients_list}] ")
        SQlCmd= """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_list + """','""" + NamedYourDrink + """')"""
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
