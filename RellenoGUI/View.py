import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Style().configure("TButton", padding=6, relief="flat",)

        # create widgets
        
        # set the controller
        self.controller = None
        
        
        # labe frame parametros
        self.label_frame = ttk.LabelFrame(self, text='Parametros')
        self.label_frame.grid(column=0, row=0, padx=0, pady=5, columnspan=2, sticky='nsew')
        
        # labe frame coordenadas
        self.lb_coordenadas = ttk.LabelFrame(self.label_frame, text='Coordeandas')
        self.lb_coordenadas.grid(column=0, row=1, padx=0, pady=5, columnspan=2, sticky='nsew')

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=2, column=1, sticky=tk.W)

        # label tamaño area
        self.label_tam_area = ttk.Label(self.label_frame, text='Region: ')
        self.label_tam_area.grid(row=0, column=0)

        # tamaño area entry
        self.tam_area_var = tk.StringVar()
        self.tam_area_entry = ttk.Entry(self.label_frame, textvariable=self.tam_area_var, width=10, )
        self.tam_area_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=3, sticky='nsew')
        
        
        # label x (Este)
        self.label_tam_area = ttk.Label(self.lb_coordenadas, text='Este: ')
        self.label_tam_area.grid(row=0, column=0)
        
        # entry x
        self.x_var = tk.StringVar()
        self.x_entry = ttk.Entry(self.lb_coordenadas, textvariable=self.x_var, width=5)
        self.x_entry.grid(row=0, column=1, padx=2, pady=5)
        
        # label y (Norte)
        self.label_tam_area = ttk.Label(self.lb_coordenadas, text='Norte: ')
        self.label_tam_area.grid(row=0, column=2 )
        
        # entry y
        self.y_var = tk.StringVar()
        self.y_entry = ttk.Entry(self.lb_coordenadas, textvariable=self.y_var, width=5)
        self.y_entry.grid(row=0, column=3, padx=2, pady=5)
        
        self.s = ttk.Style(self.lb_coordenadas)
        #self.s.theme_use('default')
        self.s.configure('flat.TButton', borderwidth=0)
        
        # add item button
        self.img_add = tk.PhotoImage(file='plus.png')
        self.add_item_button = ttk.Button(self.lb_coordenadas, image=self.img_add, command=self.add_item_button_clicked,
                                          style='flat.TButton')
        self.add_item_button.config(width=0)
        self.add_item_button.grid(row=0, column=4, padx=0, pady=0)
        # treeview -------------------------------------------------------------
        # define columns
        self.columns = ('1', '2', '3')

        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')
        
        # colums whidth
        self.tree.column('1', width=50, anchor=tk.CENTER)
        self.tree.column('2', width=50, anchor=tk.CENTER)
        self.tree.column('3', width=50, anchor=tk.CENTER)
        
        # define headings
        self.tree.heading('1', text='Ciudad')
        self.tree.heading('2', text='Este')
        self.tree.heading('3', text='Norte')
        
        self.tree.grid(row=1, column=0, padx=0, pady=5, sticky='nsew')

        # add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, pady=5, sticky='nsew')
        # ----------------------------------------------------------------------
        # data buttons ---------------------------------------------------------
        # labe frame data controllers buttons
        self.lb_data_controllers = ttk.LabelFrame(self, text='Controles')
        self.lb_data_controllers.grid(column=0, row=2, padx=0, pady=10 , columnspan=2, sticky='nsew')
        
        # import button
        self.save_button = ttk.Button(self.lb_data_controllers, text='Importar', command=self.save_button_clicked)
        self.save_button.grid(row=0, column=1, padx=10)
        
        # run model button
        self.save_button = ttk.Button(self.lb_data_controllers, text='Ejecutar', command=self.save_button_clicked)
        self.save_button.grid(row=0, column=2, padx=10)
        
        # figure matplotlib ----------------------------------------------------
        #self.graficar(10)
        self.graficar(10, [], [])
        # ----------------------------------------------------------------------

    def set_controller(self, controller):
        self.controller = controller

    def get_tam_area(self):
        return print("cpsa = ", self.controller.get_tam_area())

    def save_button_clicked(self):
        if self.controller:
            self.controller.save()
            
        
    def add_item_button_clicked(self):
        if self.controller:
            self.controller.add_item(['0',self.x_var.get(), self.y_var.get()], self.tam_area_var.get())
            tam_area = int(self.controller.get_tam_area())
            #print(type(num), " ", num)
            x,y = self.controller.get_data_tree()
            #print("x = ", x)
            self.controller.generate_dzm_content(x,y, tam_area)
            self.graficar(tam_area, x, y)

    def graficar(self, n, x , y):
        # figure matplotlib ----------------------------------------------------
        # size and color:
        sizes = np.random.uniform(15, 80, len(x))
        colors = np.random.uniform(15, 255, len(x))

        # plot
        
        fig, ax = plt.subplots()
        fig.suptitle('Graficas Ubicaciones')
        fig.set_facecolor('#F0F0F0')
        
        # fig plt style sean-whitegrid
        plt.style.use('seaborn-whitegrid')
        
        
        
        ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=50)

        ax.set(xlim=(0, n), xticks=np.arange(1, n, step=n/10),
            ylim=(0, n), yticks=np.arange(1, n, step=n/10))
        
        canvas = FigureCanvasTkAgg(fig, master = self)  # Crea el area de dibujo en Tkinter
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=3, rowspan=3, sticky='nsew')
        # ---------------------------------------------------------------------
        
    
                