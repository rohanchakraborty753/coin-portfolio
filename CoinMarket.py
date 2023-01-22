import requests
import json
from tkinter import *
from tkinter import messagebox,Menu
import sqlite3

root = Tk()
root.title("Crypto Portfolio")
root.resizable(False, False)

con = sqlite3.connect("coin.db")
Cobj = con.cursor()

Cobj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()

def reset():
  for frame in root.winfo_children():
    frame.destroy()
  
  header()
  crypto()  
  app()

def app():
  
  def clear_all():
    Cobj.execute("DELETE FROM coin")
    con.commit()
    
    messagebox.showinfo("Notification","All Cleared- Add new Coins")
    reset()
  
  def close_app():
    root.destroy()

  menu = Menu(root)
  file_item = Menu(menu)
  file_item.add_command(label='clear', command=clear_all)
  file_item.add_command(label='close', command=close_app)
  menu.add_cascade(label="File", menu=file_item)
  root.config(menu=menu)  
  
    
def crypto():
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  parameters = {
    'start':'1',
    'limit':'50',
    'convert':'USD',
    'CMC_PRO_API_KEY' : 'fa74495d-59bd-4246-8f2a-b76af1128226' 
  }

  response = requests.get(url, params = parameters)
  content = response.content
  api_data = json.loads(content)

  Cobj.execute("SELECT * FROM coin")
  my_coins = Cobj.fetchall()
  
  def color(amount):
    if amount >= 0:
      return "green"
    else:
      return "red"    
  
  def insert_coin():
    Cobj.execute("INSERT INTO coin(symbol, price, amount) VALUES(?,?,?)",(symbol_entry.get(), price_entry.get(), amount_entry.get()))
    con.commit()
    messagebox.showinfo("Notification","Coin Added Successfully")
    reset()  
  
  def update_coin():
    Cobj.execute("UPDATE coin SET price=?, amount=? WHERE id=?",(price_update.get(), amount_update.get(), ID_update.get()))
    con.commit()
    messagebox.showinfo("Notification","Coin Updated Successfully")
    reset()
  
  def delete_coin():
    Cobj.execute("DELETE FROM coin WHERE id=?",(P_ID_update.get(),))
    con.commit()
    messagebox.showinfo("Notification","Coin Deleted Successfully")
    reset()

  total_PL = 0
  coinRow = 1
  total_CurrValue = 0
  total_buying_amount = 0
  
  for i in range(0,50):
      for coin in my_coins:
          if api_data["data"][i]["symbol"] == coin[1]:
              total_buying_price = float(coin[2]) * float(coin[3])
              pl_unit =  float(api_data["data"][i]["quote"]["USD"]["price"]) - float(coin[3])
              total_PL_coins = pl_unit * float(coin[2])
              total_PL += total_PL_coins
              total_CurrValue += float(api_data["data"][i]["quote"]["USD"]["price"])
              total_buying_amount += total_buying_price
            
              portfolio_id = Label(root, text=coin[0], bg="#F3F4F6", fg="black", font="Poppins 12 bold", padx=2, pady=2, borderwidth=2, relief=GROOVE)
              portfolio_id.grid(row=coinRow, column=0, sticky=N+S+E+W)
              
              name = Label(root, text=api_data["data"][i]["symbol"], bg="#F3F4F6", fg="black", font="Poppins 12 bold", padx=2, pady=2, borderwidth=2, relief=GROOVE)
              name.grid(row=coinRow, column=1, sticky=N+S+E+W)
              
              price = Label(root, text="$" + str(coin[3]), bg="#F3F4F6", fg="black", font="Arial 15", padx=2, pady=2, borderwidth=2, relief=GROOVE)
              price.grid(row=coinRow, column=2, sticky=N+S+E+W)
              
              no_coins = Label(root, text=coin[2], bg="#F3F4F6", fg="black", font="Arial 15", padx=2, pady=2, borderwidth=2, relief=GROOVE)
              no_coins.grid(row=coinRow, column=3, sticky=N+S+E+W)
              
              buy_cost = Label(root, text="${0:.2f}".format(total_buying_price), bg="#F3F4F6", fg="black", font="Arial 15", padx=2, pady=2, borderwidth=2, relief=GROOVE)
              buy_cost.grid(row=coinRow, column=4, sticky=N+S+E+W)
              
              curr_Price = Label(root, text="${0:.2f}".format(api_data["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6", fg="black", font="Arial 15", padx=2, pady=2, borderwidth=2, relief=GROOVE)
              curr_Price.grid(row=coinRow, column=5, sticky=N+S+E+W)
              
              pl_coin = Label(root, text="${0:.2f}".format(pl_unit), bg="#F3F4F6", fg=color(float("{0:.2f}".format(pl_unit))), font="Arial 15", padx=2, pady=2, borderwidth=2, relief=GROOVE)
              pl_coin.grid(row=coinRow, column=6, sticky=N+S+E+W)
              
              total_coin_pl = Label(root, text="${0:.2f}".format(total_PL_coins), bg="#F3F4F6", fg=color(float("{0:.2f}".format(total_PL_coins))), font="Arial 15", padx=2, pady=2, borderwidth=2, relief=GROOVE)
              total_coin_pl.grid(row=coinRow, column=7, sticky=N+S+E+W)
              
              coinRow += 1
  
  symbol_entry = Entry(root, borderwidth=2, relief=GROOVE)
  symbol_entry.grid(row=coinRow + 1, column=1)

  price_entry = Entry(root, borderwidth=2, relief=GROOVE)
  price_entry.grid(row=coinRow + 1, column=2)

  amount_entry = Entry(root, borderwidth=2, relief=GROOVE)
  amount_entry.grid(row=coinRow + 1, column=3)
  
  addCoin = Button(root, text="Add Coin", bg="#1E6AE1", fg="black", command=insert_coin, font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=RAISED)
  addCoin.grid(row=coinRow +1, column=4, sticky=N+S+E+W)
  
  #update coin
  ID_update = Entry(root, borderwidth=2, relief=GROOVE)
  ID_update.grid(row=coinRow + 2, column=0)

  symbol_update = Entry(root, borderwidth=2, relief=GROOVE)
  symbol_update.grid(row=coinRow + 2, column=1)

  price_update = Entry(root, borderwidth=2, relief=GROOVE)
  price_update.grid(row=coinRow + 2, column=2)
  
  amount_update = Entry(root, borderwidth=2, relief=GROOVE)
  amount_update.grid(row=coinRow + 2, column=3)
  
  updateCoin = Button(root, text="Update Coin", bg="#1E6AE1", fg="black", command=update_coin, font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=RAISED)
  updateCoin.grid(row=coinRow +2, column=4, sticky=N+S+E+W)
  
  #delete coin
  P_ID_update = Entry(root, borderwidth=2, relief=GROOVE)
  P_ID_update.grid(row=coinRow + 3, column=0)
  
  deleteCoin = Button(root, text="Delete Coin", bg="#1E6AE1", fg="black", command=delete_coin, font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=RAISED)
  deleteCoin.grid(row=coinRow +3, column=4, sticky=N+S+E+W)
  
  total_paid = Label(root, text="${0:.2f}".format(total_buying_amount), bg="#F3F4F6", fg="black", font="Arial 15", padx=2, pady=2, borderwidth=2, relief=GROOVE)
  total_paid.grid(row=coinRow, column=4, sticky=N+S+E+W)
  
  totalcv = Label(root, text="${0:.2f}".format(total_CurrValue), bg="#F3F4F6", fg="black", font="Arial 15", padx=2, pady=2, borderwidth=2, relief=GROOVE)
  totalcv.grid(row=coinRow, column=5, sticky=N+S+E+W)
  
  totalpl = Label(root, text="${0:.2f}".format(total_PL), bg="#F3F4F6", fg=color(float("{0:.2f}".format(total_PL))), font="Arial 15", padx=2, pady=2, borderwidth=2, relief=GROOVE)
  totalpl.grid(row=coinRow, column=7, sticky=N+S+E+W)
  
  api_data = ""
  refresh = Button(root, text="Refresh", bg="#1E6AE1", fg="black", command=reset, font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=RAISED)
  refresh.grid(row=coinRow +1, column=7, sticky=N+S+E+W)
  

def header():
  portfolio_id = Label(root, text="P_ID", bg="#1E6AE1", fg="white", font="Poppins 15 bold", padx=2, pady=5, borderwidth=5, relief=GROOVE)
  portfolio_id.grid(row=0, column=0, sticky=N+S+E+W)
  
  name = Label(root, text="Coin Name", bg="#1E6AE1", fg="white", font="Poppins 15 bold", padx=2, pady=5, borderwidth=5, relief=GROOVE)
  name.grid(row=0, column=1, sticky=N+S+E+W)
  
  price = Label(root, text="Buying Price", bg="#1E6AE1", fg="white", font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=GROOVE)
  price.grid(row=0, column=2, sticky=N+S+E+W)
  
  no_coins = Label(root, text="Coin Owned", bg="#1E6AE1", fg="white", font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=GROOVE)
  no_coins.grid(row=0, column=3, sticky=N+S+E+W)
  
  buy_cost = Label(root, text="Total Buying Amount", bg="#1E6AE1", fg="white", font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=GROOVE)
  buy_cost.grid(row=0, column=4, sticky=N+S+E+W)
  
  curr_Price = Label(root, text="Current Value", bg="#1E6AE1", fg="white", font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=GROOVE)
  curr_Price.grid(row=0, column=5, sticky=N+S+E+W)
  
  pl_coin = Label(root, text="P/L per Coin", bg="#1E6AE1", fg="white", font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=GROOVE)
  pl_coin.grid(row=0, column=6, sticky=N+S+E+W)
  
  total_coin_pl = Label(root, text="Total P/L(Coin)", bg="#1E6AE1", fg="white", font="Poppins 15 bold", padx=5, pady=5, borderwidth=2, relief=GROOVE)
  total_coin_pl.grid(row=0, column=7, sticky=N+S+E+W)

app()
header() 
crypto()
root.mainloop()

Cobj.close()
con.close()             
            
            
        