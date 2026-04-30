import base64
import streamlit as st
import time


st.set_page_config(page_title="Maya's Cafe", page_icon="☕", layout="wide")

def show_logo(url, width=120, justify="center"):
    st.markdown(f"""
    <div style="display: flex; justify-content: {justify}; margin-top: 10px;">
        <img src="{url}" width="{width}">
    </div>
    """, unsafe_allow_html=True)

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
    
def menu_item(name, price, desc="",cu="₹"):
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <div style="display: flex; align-items: center;">
            <span style="font-weight: 600;">{name.upper()}</span>
            <div style="flex: 1; border-bottom: 1px dotted #999; margin: 0 10px;"></div>
            <span style="font-weight: 500;">{cu}{price}</span>
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



def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("logo.png")

# st.title("Ashu's Makeover",text_alignment="center")
#====================================================================================
# Display the logo at the top of the page, centered, with a height of 200px
#====================================================================================#
st.markdown(f"""
    <div style="display:flex; justify-content:center; ">
        <img src="data:image/png;base64,{img}" height="150px" alt="Logo">
    </div>
    
""", unsafe_allow_html=True)

# st.title("Maya's Cafe",text_alignment="center")
# st.markdown("Welcome to Maya's Cafe!",text_alignment="center")
st.markdown("""
<div style="display: flex; align-items: center; text-align: center;">
  <hr style="flex: 1; border: none; border-top: 2px solid #999;">
  <span style="padding: 0 10px; font-weight: 800; font-size: 20px">MENU</span>
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

tabs = st.tabs(["Food","Beverages"])

tab1=tabs[0]
with tab1:
    food_tabs= st.tabs(['Momos', 'Pizza', 'Sandwich', 'Pasta', 'Nachos', 'French fries', 'Finger bites', 'Meal bowls', 'Sizzlers', 'Choice of dessert'])
    
    momos_tab = food_tabs[0]
    with momos_tab:
        momos = get_doc_data(db,"menu","momos")
        
        for name,price in dict(zip(momos["name"],momos["price"])).items():
            menu_item(name,price) 
        
    pizza_tab = food_tabs[1]
    with pizza_tab:
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
