from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.orm import sessionmaker
import torch
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk

# Create SQLite database engine
engine = create_engine('sqlite:///shopping_list.db', echo=True)
Base = declarative_base()

# Define Item and Store classes as before...

# Create tables
Base.metadata.create_all(engine)

# Function to create a PyTorch Tensor from item prices
def create_price_tensor(session):
    prices = session.query(Store.price).all()
    price_list = [price[0] for price in prices]
    price_tensor = torch.tensor(price_list, dtype=torch.float32)
    return price_tensor

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add items and stores (as before)

# Query data for visualization
all_stores = session.query(Store).options(joinedload(Store.item)).all()

# Visualize data using Seaborn
store_data = {'Store Name': [], 'Item Name': [], 'Price': []}
for store in all_stores:
    store_data['Store Name'].append(store.store_name)
    store_data['Item Name'].append(store.item.name)
    store_data['Price'].append(store.price)

store_df = pd.DataFrame(store_data)
sns.barplot(x='Store Name', y='Price', hue='Item Name', data=store_df)
plt.title('Price Distribution in Different Stores')
plt.show()

# Create a Tensor from item prices
price_tensor = create_price_tensor(session)
print("PyTorch Tensor of Item Prices:")
print(price_tensor)

# GUI: Display item names in a Tkinter Window
def show_item_names():
    top = Tk()
    top.title("Item Names")

    item_names = session.query(Item.name).all()
    for name in item_names:
        Label(top, text=name[0]).pack()

    top.mainloop()

# Run the Tkinter GUI
show_item_names()
