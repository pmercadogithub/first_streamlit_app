import streamlit 
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents new Healthy Diner')

streamlit.header('Breakfast Menu')

										
streamlit.text('🥣 Omega 3 & Blueberry Oatmel')
streamlit.text('🥗 Kale, Spinach & Rocket Smoohie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Importing CSV from external source
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Change the index so we can use a more human readable index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)

###############################################################################################
#New Section to dispaly fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized
###############################################################################################

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        fruityvice_data = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruityvice_data)

except URLError as e:
    streamlit.error(e)

streamlit.header("The fruit load list contains:")
###############################################################################################
#Snowflake functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
###############################################################################################
#Add button to load the fruit
if streamlit.button('Get Fruit Load List2'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows= get_fruit_load_list()
	my_cnx.close()
	streamlit.dataframe(my_data_rows)
	
###############################################################################################
#Allow user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('%s')" %new_fruit)
        return 'Thanks for adding ' + new_fruit
###############################################################################################

#add_my_fruit = streamlit.text_input('What fruit would you like information about to add3?')
#if streamlit.button('Add a Fruit to the List'):
#	back_from_funtion = insert_row_snowflake(add_my_fruit)
#	streamlit.text(back_from_funtion)




add_my_fruit = streamlit.text_input('What fruit would you like information about to add3?')
if streamlit.button('Add Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    res= insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(res)

