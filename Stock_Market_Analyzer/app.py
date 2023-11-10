import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import *
from ttkbootstrap import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

def clear_plot():
    # Clear the plot if it exists
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().destroy()


def fetch_stock_data():

    try:
        stock_symbol = entry_stck.get()
        stock_data = yf.download(stock_symbol, start = '2022-01-01', end = '2023-11-09')
        return stock_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch stock data: {e}")
        return None

def analyze_stock():

    clear_plot()
    stock_data = fetch_stock_data()
    if stock_data is not None:
        # Assuming 'Close' price for analysis
        df = pd.DataFrame(stock_data['Close'])
        df['Prediction'] = df['Close'].shift(-1)
        
        X = np.array(df.drop(columns=['Prediction', 'Prediction']))
        X = X[:-1]
        
        y = np.array(df['Prediction'])
        y = y[:-1]
        
        model = LinearRegression()
        model.fit(X, y)
        
        # For simplicity, predict the next day's price
        prediction = model.predict(np.array([df.iloc[-1][:-1]]).reshape(1, -1))
        
        label_predict.config(text=f"Predicted Price: {prediction[0]:.2f}")

       # Plotting
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(df.index, df['Close'], label='Historical Prices')
        ax.axvline(x=df.index[-1], color='r', linestyle='--', label='Prediction Point')
        ax.scatter(df.index[-1], prediction, color='r', marker='o', s=100, label='Predicted Price')
        ax.set_title('Stock Price Analysis')
        ax.set_xlabel('Date')
        ax.set_ylabel('Stock Price')
        ax.legend()

        # Embedding plot in Tkinter
        root.canvas = FigureCanvasTkAgg(fig, master=root)
        root.canvas.draw()
        root.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Optionally, add a toolbar for navigation in the plot
        toolbar = NavigationToolbar2Tk(root.canvas, root)
        toolbar.update()
        root.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Setup the app
root = tk.Tk()
root.title('Stock Market Analyzer')
root.geometry('1500x900')

label_stk = ttk.Label(root, text = 'Enter Stock Symbol')
label_stk.pack(padx = 10, pady = 10)

entry_stck = ttk.Entry(root)
entry_stck.pack(padx = 10, pady = 10)

button_analyze = ttk.Button(root, text = 'Analyze Stock', command = analyze_stock)
button_analyze.pack(padx = 10, pady = 10)

label_predict = tk.Label(root)
label_predict.pack(padx = 10, pady = 10)

root.mainloop()