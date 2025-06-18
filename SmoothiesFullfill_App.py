######## Rememebr all this code is in a version of PYTHON #########
## check the refresh mechanism from cache object.
# Import python packages
import streamlit as st
import datetime
import pandas as pd

from snowflake.snowpark.context   import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched


cnx = st.connection("smothieConnStr","snowflake")
session = cnx.session()

### Write directly to the app
timestamp = datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")
st.title(f":cup_with_straw: Pending Smoothie Orders Today:cup_with_straw: {st.__version__}")
st.write(f""" Orders that need to be filled: {timestamp} """ )

###session = get_active_session()
df = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
##obj=st.dataframe(data=df, use_container_width=True, key='DefaultOrders')

if (len(df) <= 0) :
    st.success('There are NO pending order right now', icon='👍')   
else :        
    edf = st.data_editor(df,num_rows='dynamic')
    submitted=st.button('Submit')
    if  submitted:
        timestamp = datetime.datetime.now()
        try:
            OrdrDs = session.table("smoothies.public.orders")
            EordrDs = session.create_dataframe(edf)
            OrdrDs.merge(EordrDs
                             , (OrdrDs['ORDER_UID'] == EordrDs['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': EordrDs['ORDER_FILLED']})]
                            )
            Msg=(f"Your Order has been Updated!!  {timestamp}")
            st.success(Msg, icon='👍')     
        except:    
            Msg=(f"Something went Wrong with your smoothie!! {timestamp}")
            st.write(Msg)
   
   
    ### this is the command to stop further execution when troubleshooting
    ###st.stop()
   

