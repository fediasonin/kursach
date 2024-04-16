from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import Combobox
from pltfile import Pltcl
from datetime import datetime, date

class Window():
    def __init__(self, tittle, resizabl, geometry):
        self.root = Tk()
        self.root.title(tittle)
        self.root.geometry(geometry)
        self.root.configure(background='#a8d8ff')
        if not resizabl:
            self.root.resizable(False, False)

        self.c = Checkbutton(self.root)
        self.c.invoke()

        self.var_0 = IntVar()
        self.var_1 = IntVar()
        self.var_2 = IntVar()
        self.var_3 = IntVar()

        self.fig = Pltcl(self.root)
        self.plot = self.fig.get_plot(None)

        self.cmb1 = Combobox(self.root, values=self.fig.get_date())
        self.cmb2 = Combobox(self.root, values=self.fig.get_date())
        self.cmb3 = Combobox(self.root, values=['Линейный','Столбчатый','Гистограмма'])
        self.cmb4 = Combobox(self.root, values=['Без усреднения', 'По часу', 'По 3 часа', 'По дню','Макс-мин'])


        self.cmb11 = Combobox(self.root, values=self.fig.get_list_prib(0))
        self.cmb12 = Combobox(self.root, values=self.fig.get_list_prib(1))
        self.cmb13 = Combobox(self.root, values=self.fig.get_list_prib(2))
        self.cmb14 = Combobox(self.root, values=self.fig.get_list_prib(3))

        self.cmb11.current(self.fig.get_list_prib(0).index('BME280_temp'))
        self.cmb12.current(self.fig.get_list_prib(1).index('weather_temp'))
        self.cmb13.current(self.fig.get_list_prib(2).index('BME280_temp'))
        self.cmb14.current(self.fig.get_list_prib(3).index('BME280_temp'))

        self.cmb1.current(0)
        ind = len(self.fig.get_date())-1
        self.cmb2.current(ind)

        self.cmb3.current(0)
        self.cmb4.current(0)

    def run(self):
            self.draw_botton()
            self.root.mainloop()

    def draw_botton(self):
        Label(self.root, text='Прибор', bg='#a8d8ff',font=('Consolas', 14, 'bold')).place(x=720,y=100, width=140, height=30)

        Checkbutton(self.root, text='Hydra-L', variable=self.var_0,bg='#cccccc').place(x=720,y=180, width=140, height=30)
        self.cmb11.place(x=860,y=180, width=120, height=30)
        Checkbutton(self.root, text='РОСА К-2', variable=self.var_1,bg='#cccccc').place(x=720,y=140, width=140, height=30)
        self.cmb12.place(x=860,y=140, width=120, height=30)
        Checkbutton(self.root, text='Тест воздуха', variable=self.var_2,bg='#cccccc').place(x=720,y=260, width=140, height=30)
        self.cmb13.place(x=860,y=260, width=120, height=30)
        Checkbutton(self.root, text='Тест Студии', variable=self.var_3,bg='#cccccc').place(x=720,y=220, width=140, height=30)
        self.cmb14.place(x=860,y=220, width=120, height=30)

        Label(self.root, text='Усреднение', bg='#a8d8ff').place(x=30,y=510, width=120, height=30)
        self.cmb4.place(x=30,y=550, width=130, height=30)
        Label(self.root, text='Начало', bg='#a8d8ff').place(x=260,y=510, width=120, height=30)
        self.cmb1.place(x=260,y=550, width=120, height=30)
        Label(self.root, text='Конец', bg='#a8d8ff').place(x=480,y=510, width=120, height=30)
        self.cmb2.place(x=480,y=550, width=120, height=30)
        Label(self.root, text='Тип графика', bg='#a8d8ff').place(x=700,y=510, width=120, height=30)
        self.cmb3.place(x=700,y=550, width=120, height=30)

        self.plot.place(x=10, y = 10, width=680, height=480)

        Button(self.root, text='Построить', command=self.go, font=('Consolas', 10, 'bold'), ).place(x=745,y=310, width=80, height=30)

    def go(self):
        us = self.cmb4.get()
        dt1 = date.fromisoformat(self.cmb1.get())
        dt2 = date.fromisoformat(self.cmb2.get())
        plot_name = self.cmb3.get()
        if dt1 > dt2:
            mb.showerror('Не корректная дата','Введите правильный промежуток времени')
            return

        self.plot.place_forget()
        graph = []
        prd_v = []

        if self.var_0.get():
            graph.append(0)
            prd_v.append(self.cmb11.get())
        else:
            prd_v.append('BME280_temp')

        if self.var_1.get():
            graph.append(1)
            prd_v.append(self.cmb12.get())
        else:
            prd_v.append('weather_temp')

        if self.var_2.get():
            graph.append(2)
            prd_v.append(self.cmb13.get())
        else:
            prd_v.append('BME280_temp')

        if self.var_3.get():
            graph.append(3)
            prd_v.append(self.cmb14.get())
        else:
            prd_v.append('BME280_temp')

        self.fig.clear_plot()
        self.plot = self.fig.get_plot(us, graph, dt1, dt2, plot_name, prd_v)
        self.plot.place(x=10, y = 10, width=680, height=480)

app = Window('Погода', True, '1000x600')
app.run()