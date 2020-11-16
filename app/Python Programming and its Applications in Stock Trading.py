#For pip installing required packages
import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
#pip install all the required packages
#install("matplotlib")
#install("pandas")
#install("mpl_finance")
#install("mplfinance")
#install("tkcalendar")
#For plotting of graph
import matplotlib
matplotlib.use("TkAgg")
#import canvas to draw our graph on, and navigation toolbar (save, zoom etc)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
#To allow for live update of matplotlb graph
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
#Likes css for tkinter, for styling
from tkinter import ttk
#For loading csv files
import pandas as pd
# #For loading candlesticks
import mplfinance as mpf
#For allowing users to choose a date
import datetime
from tkcalendar import Calendar, DateEntry
#Defines the font type and size for title
LARGE_FONT= ("TkDefaultFont", 12)
#Font size for description
SMALL_FONT= ("TkDefaultFont", 9)
#Adds a background to the graph
style.use("ggplot")

def animate(i):
    #This function allows for live update of the stock data on the plot. Currently not in use yet
    #retrieves all the data to draw on the plot
    pullData = open("sampleData.txt", "r").read()
    #Split the data to different rows on a new line
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        #Ignore empty lines
        if len(eachLine) > 1:
            #Gets columns for each line
            x, y =eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    #Needs to clear the graph to avoids redrawing several times, which will cause lag
    a.clear()
    #Plots the data
    a.plot(xList, yList)
    
#Create a class that inherits from tk.Tk
#This class sets the base to add more pages
class BaseClass(tk.Tk):
    #This init function will always be called when the class initialises
    #self is optional but recommended
    #*args allows you to pass in any number of positional arguments
    #**kwargs allows you to pass in any number of keyword arguments
    def __init__(self, *args, ** kwargs):
        #Initialise the tkinter application
        tk.Tk.__init__(self,*args,**kwargs)
        #Change the icon on the top left of the window
        #tk.Tk.iconbitmap(self, default="clienticon.ico")        
        #Creates a container that contains everything in the Tkinter app
        #frame is the window itself
        #Sets a width and height, need to call grid_propagate to keep this setting
        container = tk.Frame(self, width=1400, height=820)
        container.grid_propagate(False)
        #Positions the window on the top and fill it on both sides
        container.pack(side="top", fill="both", expand = True)
        #0 is the minimum size, weight is to indicate priority
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #Allows the application to load different types of windows (pages)
        self.frames = {}
        #Need to add each of the page class to the frame
        #Remember to add the page class here each time a new page is added
        for F in (StartPage, TutorialPage, AboutPage, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            #nsew is north south east west, eg putting n will stretch everything towards the north
            frame.grid(row = 0, column= 0, stick="nsew")
        #Disploay the StartPage when the app initialises
        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        #Displays the frame (page)
        frame.tkraise()
#Adds a new page to the tkinter app
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        #parent class refers to BaseClass()
        tk.Frame.__init__(self, parent)
        #Add text to the tkinter window
        #Label is a class, this initialises a new object label from this class
        label = tk.Label(self, text="Python Programming and its Applications in Stock Trading", font=LARGE_FONT)
        #Pack positions the label, alternative is to use grid. Do NOT use both pack and grid in the same page!
        #Add padding size of 10 on x and y axis
        label.pack(pady=10,padx=10)
        #Add a button to go to another page
        #Create a button 1 object and defines the text on that button
        #command defines the function that will be called when the button is pressed, shows TutorialPage class (frame) on keypress
        ##Need to use lambda: to prevent the button from immediately executing at initialisation    
        button1 = ttk.Button(self, text="Tutorial", command=lambda: controller.show_frame(TutorialPage))
        button1.pack(pady=10,padx=10)
        button2 = ttk.Button(self, text="About", command=lambda: controller.show_frame(AboutPage))
        button2.pack(pady=10,padx=10)
        button3 = ttk.Button(self, text="Graph", command=lambda: controller.show_frame(GraphPage))
        button3.pack(pady=10,padx=10)

#Adds a new page
class TutorialPage(tk.Frame):
    #This part is very similar to the start page above
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Tutorial", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        #Need to give a new variable to each button to uniquely identify each buttons
        #show_frame to show the home page on button press
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()


#Adds a new page
class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="About", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        about = tk.Label(self, text="Made by Damian Er Zhong Ying, Loo Hui Ming, Elias Lim Khong Mun, Lok Shu Fen, Camellia, Sim Sheng Qin, Angelico De Los Reyes Garcia", font=SMALL_FONT)
        about.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()



class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Sets the title display
        title_label = tk.Label(self, text="Graph", font=LARGE_FONT)         
        #Creates a label for the input text box
        csv_file_label = tk.Label(self, text="Enter CSV file: ", font=SMALL_FONT) 
        # Creates an input text box for the user to type in the csv file path    
        csv_file_input = ttk.Entry(self,width=45) 
        #Add a default value in the input box
        csv_file_input.insert(0,r"C:\Users\sheng\OneDrive - Singapore Management University\QF205-Computing Technology For Finance\project\SPY_20110701_20120630_Bollinger.csv")
        # Positions the cursor on the input text box at the start 
        csv_file_input.focus()  
        #Adds a checkbox to allows user to turn on/off the display of moving average
        display_moving_average_value = tk.IntVar()
        display_moving_average_value.set('1')
        display_moving_average = ttk.Checkbutton(self, text="Show 20-day moving average", variable=display_moving_average_value, command=lambda: self.load_graph(csv_file_input.get(), start_date.get_date(), end_date.get_date(), display_moving_average_value.get(), display_bollinger_bands_value.get(), display_support_resistance_breaks_value.get(), display_wbottom_mtop_value.get()))    
        #Adds a checkbox to allows user to turn on/off the display of bollinger bands
        #display_bollinger_bands_value stores the value of the checkbox
        display_bollinger_bands_value = tk.IntVar()
        #use var.set() to set the value of the variable and var.get() to get value of the variable
        display_bollinger_bands_value.set('1')
        #The checkbutton will automaticcally call the load_graph() function whenever it is checked/unchecked
        # Remember to put SELF.load_graph whenever calling a function of this class (GraphPage())
        display_bollinger_bands = ttk.Checkbutton(self, text="Show bolllinger bands", variable=display_bollinger_bands_value, command=lambda: self.load_graph(csv_file_input.get(), start_date.get_date(), end_date.get_date(), display_moving_average_value.get(), display_bollinger_bands_value.get(), display_support_resistance_breaks_value.get(), display_wbottom_mtop_value.get()))
        #Creates a checkbox to turn on/off the display of support & resistance breaks
        display_support_resistance_breaks_value = tk.IntVar()
        display_support_resistance_breaks_value.set('1')
        display_support_resistance_breaks = ttk.Checkbutton(self, text="Show support & resistance breaks", variable=display_support_resistance_breaks_value, command=lambda: self.load_graph(csv_file_input.get(), start_date.get_date(), end_date.get_date(), display_moving_average_value.get(), display_bollinger_bands_value.get(), display_support_resistance_breaks_value.get(), display_wbottom_mtop_value.get()))        
        #Creates a checkbox to turn on/off the display of W-Bottoms and M-Tops
        display_wbottom_mtop_value = tk.IntVar()
        display_wbottom_mtop_value.set('1')
        display_wbottom_mtop = ttk.Checkbutton(self, text="Show W-Bottoms and M-Tops", variable=display_wbottom_mtop_value, command=lambda: self.load_graph(csv_file_input.get(), start_date.get_date(), end_date.get_date(), display_moving_average_value.get(), display_bollinger_bands_value.get(), display_support_resistance_breaks_value.get(), display_wbottom_mtop_value.get()))    
        #Allows user to change start and end date display
        start_date_label=tk.Label(self,text="Select start date")
        start_date = DateEntry(self, width=12, background='darkblue',
                    foreground='white', borderwidth=2)  
        #Sets a default value for the start date
        start_date.set_date(datetime.date(2011,7,1))
        end_date_label=tk.Label(self,text="Select end date")   
        end_date = DateEntry(self, width=12, background='darkblue',
                    foreground='white', borderwidth=2)   
        end_date.set_date(datetime.date(2012, 3, 1))
        #Get the values in the input text using .get()
        #Updates the values such as start date and end date on key press
        update_values = ttk.Button(self, text="Update values", command=lambda: self.load_graph(csv_file_input.get(), start_date.get_date(), end_date.get_date(), display_moving_average_value.get(), display_bollinger_bands_value.get(), display_support_resistance_breaks_value.get(), display_wbottom_mtop_value.get()))
        
        #Adds a button to go back to the homer page
        back_to_home = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))   
        #Loads the graph on start
        self.load_graph(csv_file_input.get(), start_date.get_date(), end_date.get_date(), display_moving_average_value.get(), display_bollinger_bands_value.get(), display_support_resistance_breaks_value.get(), display_wbottom_mtop_value.get())
        #Positions everything in a grid
        #columnspan means that it occupies multiple columns
        #sticky="W" (west) means that it is aligned to the left, WE(West, East) means to align it in the center
        #padx is the right padding of this input box, pady is the padding bottom of this input box 
        #Refer to https://www.geeksforgeeks.org/python-grid-method-in-tkinter/ for examples
        title_label.grid(row=0, column=1, columnspan=3, sticky = "WE", pady = 4)
        csv_file_label.grid(row=1,column=1, sticky = "E", pady = 4)  
        csv_file_input.grid(row=1,column=2, columnspan=3, sticky = "W", padx = 10, pady = 4)   
        display_moving_average.grid(row=2, column=0, sticky = "WE", padx = 10, pady = 4)
        display_bollinger_bands.grid(row=2, column=1, sticky = "WE", padx = 10, pady = 4)
        display_support_resistance_breaks.grid(row=2, column=2, sticky = "WE", pady = 4)
        display_wbottom_mtop.grid(row=2, column=3, sticky = "WE", pady = 4)
        start_date_label.grid(row=3, column=0, sticky = "W", padx = 10, pady = 4)
        start_date.grid(row=3,column=1, sticky = "W", pady = 4) 
        end_date_label.grid(row=3, column=2, sticky = "W", pady = 4)
        end_date.grid(row=3,column=3, sticky = "W", pady = 4)
        update_values.grid(row=4,column=2, sticky = "WE", padx = 10, pady = 4)
        back_to_home.grid(row=5,column=2, sticky = "WE", padx = 10, pady = 4)  
        
        
        
    def load_graph(self, csv_filepath, start_date, end_date, display_moving_average_value, display_bollinger_bands, display_support_resistance_breaks, display_wbottom_mtop):
        #Read the csv file
        idf = pd.read_csv(csv_filepath,index_col=0,parse_dates=True)
        #Grabs a specified date range from the input data frame
        df = idf.loc[start_date : end_date]
        #Shows the 20-day moving average. Allows user to turn on/off the display of 20-day moving average
        #mav = (20) means to show the 20 days moving average
        mav = ()
        if display_moving_average_value == 1:
            mav = (20)
        ap0 = []
        #Shows the bollinger bands. Allows user to turn on/off the display of bollinger bands
        if display_bollinger_bands == 1:
            ap0 = [ mpf.make_addplot(df['UpperB'],color='g'),  # uses panel 0 by default
            mpf.make_addplot(df['LowerB'],color='b'),  # uses panel 0 by default
                ]
        #Shows the support/resistance breaks. Allows user to turn off the display of support/resistance breaks
        seq_of_seq_of_points=[]
        colors = []
        linewidths = []
        if display_support_resistance_breaks == 1:  
            #The 1st value is the x axis, the 2nd value is the y axis
            # Yaxis value is the middle of the rectangle        
            seq_of_seq_of_points += [
            [('2011-07-29',129.29),('2011-08-10',112.81)],
            [('2011-09-22',113.85),('2011-10-04',110.24)],
            [('2011-11-21',120.29),('2011-11-25',116.65)],
            [('2011-07-01',132.40),('2011-07-07',135.29)]
                            ]
            #corresponds to the seq_of_seq_of_points on top. This means the first 3 values will be highlighted red, 4th value will be highlighted green
            colors += ['r','r','r','g']
            #Sets how thick the line is
            linewidths += [20,20,20,20]
        #Shows the w-bottoms/m-tops as vertical lines. Allows user to turn on/off the display of w-bottoms/m-tops
        seq_of_points = []
        if display_wbottom_mtop == 1:          
            #the first value is the start of wbottom and second value is the end of wbottom
            seq_of_points += ['2011-11-15','2012-02-03']
        #Refer to https://github.com/matplotlib/mplfinance/blob/master/examples/panels.ipynb and https://github.com/matplotlib/mplfinance/blob/master/examples/using_lines.ipynb for examples
        #returnfig = True to return f (figure) for tkinter to draw it
        f, ax = mpf.plot(df,
                        figsize=(14,6),
                        type='candle',
                        mav = mav,
                        volume=True,
                        addplot=ap0,                     
                        alines=dict(alines=seq_of_seq_of_points,                        
                        colors=colors,
                        linewidths=linewidths,
                        alpha=0.35),
                        vlines = dict(vlines=seq_of_points,
                        linestyle='-.',
                        alpha=1), 
                        returnfig = True)         
        #Normally its use plt.show(), but we want to show it on tkinter window directly
        #Use canvas to draw on the tkinter window directly
        canvas = FigureCanvasTkAgg(f, self) 
        canvas.draw()
        #These 2 lines of code seems to be the same, so use either one
        canvas.get_tk_widget().grid(row=6, column=0, columnspan=8)
        #canvas._tkcanvas.grid(row=6, column=0, columnspan=8)
        #Adds a navigation toolbar for the graph (zoom, pan around etc)
        toolbarFrame = tk.Frame(self)
        #As the navigation toolbar will show a text value whenever the user hovers over the graph, it will resize column = 0, causing the input boxes on top to move right
        #To fix this, we allow it to occupy more columns and align it to the left using sticky = "W"
        toolbarFrame.grid(row=7,column=0, sticky = "W", columnspan=8)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)        
        toolbar.update()
#This is same as app = tk.Tk()
app = BaseClass()
#Updates the data every 1 second
#ani = animation.FuncAnimation(f, animate,interval=1000) 
#Sets title of the app
app.title("Python Programming and its Applications in Stock Trading")
#mainloop is inherited from tk.Tk class
app.mainloop()