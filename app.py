import streamlit as st
import time
import razorpay

st.set_page_config(page_title="Maya's Cafe", page_icon="☕", layout="wide")

import streamlit as st

def set_bg(image_url):
    st.markdown(f"""
    <style>
    .stApp {{
        background: url("{image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Optional: dark overlay for readability */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.3);
        z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)


def menu_title(name="Name of Dish", price="Price", desc=""):
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <div style="display: flex; align-items: center;">
            <span style="font-weight: 600;">{name.capitalize()}</span>
            <div style="flex: 1; border-bottom: 1px  #999; margin: 0 10px;"></div>
            <span style="font-weight: 500;">{price}</span>
        </div>
        <div style="font-size: 12px; color: #666;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
    
def menu_item(name, price, desc=""):
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <div style="display: flex; align-items: center;">
            <span style="font-weight: 600;">{name.upper()}</span>
            <div style="flex: 1; border-bottom: 1px dotted #999; margin: 0 10px;"></div>
            <span style="font-weight: 500;">₹{price}</span>
        </div>
        <div style="font-size: 12px; color: #666;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
# Initialize Database connection
placeholder = st.empty()
def start_app(path):
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    
    path = dict(path)
    
    # Fix newline issue
    path['private_key'] = path['private_key'].replace('\\n', '\n')
    
    # Initialize only once
    if not firebase_admin._apps:
        placeholder.info("Connecting to database...")
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        time.sleep(0.5)
        placeholder.success("Connected to database successfully! 🚀")
        time.sleep(1)
        placeholder.empty()
    return firestore.client()






st.title("☕ Maya's Cafe",text_alignment="center")
# st.markdown("Welcome to Maya's Cafe!",text_alignment="center")
st.markdown("""
<div style="display: flex; align-items: center; text-align: center;">
  <hr style="flex: 1; border: none; border-top: 2px solid #999;">
  <span style="padding: 0 10px; font-weight: 600;">MENU</span>
  <hr style="flex: 1; border: none; border-top: 2px solid #999;">
</div>
""", unsafe_allow_html=True)

upper_placeholder = st.empty()
mid_placeholder = st.container()
lower_placeholder = st.empty()

# Correct way to access secrets
db = start_app(st.secrets["firebase"])

def get_doc_data(_db,collection_name:str,doc_name:str):
    doc_d =_db.collection(collection_name).document(doc_name).get().to_dict()
    return doc_d

# make Clean table for representation

def represent_df(db,order:list,set_index:str):
    import pandas as pd

    actual=list(db.keys())
    if all(key in actual for key in order):
        if type(db[actual[0]])==list:
            df=pd.DataFrame(db,columns=order)
            df[set_index]=df[set_index].str.capitalize()
            df.columns=df.columns.str.capitalize().str.replace("_"," ")
            df=df.set_index(set_index.capitalize())
        
        else:
            df=pd.DataFrame(db,index=[0],columns=order)
            df[set_index]=df[set_index].str.capitalize()
            df.columns=df.columns.str.capitalize().str.replace("_"," ")
            df=df.set_index(set_index.capitalize())

        return df
    else:
        st.error("incorrect order")

#====================================================================================
# Set the background of the entire app to a gradient from #1e3c72 to #2a5298 to skyblue, with a diagonal direction (315 degrees)
#====================================================================================
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(315deg, #E2CEB1, #FDFBD4,beige);
            background-attachment: flex;
            background-size: cover;
            
        }
    </style>
""", unsafe_allow_html=True)

tabs = st.tabs(["Snacks","Food","Beverages"])

tab1=tabs[1]
snacks_tab = tabs[0]

with snacks_tab:
    # set_bg("https://images.unsplash.com/photo-1509042239860-f550ce710b93?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2FmZXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60")
    # menu_title()
    menu_item("Espresso Tradicional", 70, "")
    menu_item("Espresso Duplo", 100, "Double shot strong coffee")
    menu_item("Cappuccino Italiano", 120, "Milk + foam + espresso")
with tab1:
    food_tabs= st.tabs(['Momos', 'Pizza', 'Sandwich', 'Pasta', 'Nachos', 'French fries', 'Finger bites', 'Meal bowls', 'Sizzlers', 'Choice of dessert'])
    
    momos_tab = food_tabs[0]
    with momos_tab:
        momos = get_doc_data(db,"menu","momos")
        
        for name,price in dict(zip(momos["name"],momos["price"])).items():
            menu_item(name,price) 
        
    pizza_tab = food_tabs[1]
    with pizza_tab:
        # set_bg("https://images.unsplash.com/photo-1548365328-9c0bfbf1e7c3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGl6emF8ZW58MHx8MHx8&auto=format&fit=crop&w=800&q=60")
        pizza = get_doc_data(db,"menu","pizza")
        
        for name,price in dict(zip(pizza["name"],pizza["price"])).items():
            menu_item(name,price) 
        
    sandwich_tab = food_tabs[2]
    with sandwich_tab:
        sandwich = get_doc_data(db,"menu","sandwiches")
        
        for name,price in dict(zip(sandwich["name"],sandwich["price"])).items():
            menu_item(name,price) 
            
    
    
    
    nachos_tab = food_tabs[4]
    with nachos_tab:
        nachos = get_doc_data(db,"menu","nachos")
        
        for name,price in dict(zip(nachos["name"],nachos["price"])).items():
            menu_item(name,price) 
    
    
    french_fries_tab = food_tabs[5]
    with french_fries_tab:
        french_fries = get_doc_data(db,"menu","french fries")
        for name,price in dict(zip(french_fries["name"],french_fries["price"])).items():
            menu_item(name,price)

    finger_bites_tab = food_tabs[6]
    with finger_bites_tab:
        finger_bites = get_doc_data(db,"menu","finger bites")
        
        for name,price in dict(zip(finger_bites["name"],finger_bites["price"])).items():
            menu_item(name,price) 
        
    meal_bowls_tab = food_tabs[7]
    with meal_bowls_tab:
        meal_bowls = get_doc_data(db,"menu","meal bowl")
        
        for name,price in dict(zip(meal_bowls["name"],meal_bowls["price"])).items():
            menu_item(name,price) 



    sizzler_tab = food_tabs[8]
    with sizzler_tab:
        sizzlers = get_doc_data(db,"menu","sizzlers")
        
        for name,price in dict(zip(sizzlers["name"],sizzlers["price"])).items():
            menu_item(name,price) 
        
       
            
            
    dessert_tab = food_tabs[9]
    with dessert_tab:
        desserts = get_doc_data(db,"menu","dessert")
        
        for name,price in dict(zip(desserts["name"],desserts["price"])).items():
            menu_item(name,price) 