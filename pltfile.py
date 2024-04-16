import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import requests
import seaborn as sns
import json
from datetime import datetime, date
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from collections import defaultdict

class Pltcl:
    def __init__(self, window):
        sns.set_theme()
        self.window = window
        self._ini()
        self._load_data()


    def get_list_prib(self, prd_idx):
        prd = ['Hydra-L', 'РОСА К-2', 'Тест воздуха', 'Тест Студии']
        for prb_idx in [prd_idx]:
            dicts = []
            for date_now in self.data.keys():
                jsn = self.data[date_now]
                for k in jsn.keys():
                    if jsn[k]['uName'] == prd[prb_idx]:
                        for data_keys in jsn[k]['data'].keys():
                            try:
                                f = float(jsn[k]['data'][data_keys])
                            except:
                                continue
                            if data_keys not in dicts:
                                dicts.append(data_keys)
                        else:
                            continue
                    else:
                        continue


        return dicts

    def _load_data(self):
        d_dct = defaultdict(dict)
        for i in range(1, 15):
            # if i == 3 or i == 11:
            #     continue
            with open(f'./data/log{i}F.txt', 'r') as f:
                jsn = json.load(f)
                s = 1
                d_two = None
                for j in jsn.keys():
                    if s:
                        d_one = datetime.fromisoformat(jsn[j]['Date'])
                        s = 0

                    if datetime.fromisoformat(jsn[j]['Date']).date() == d_one.date():
                        d_dct[d_one.date()][j] = jsn[j]

                    else:
                        if not d_two:
                            d_two = datetime.fromisoformat(jsn[j]['Date'])
                        d_dct[d_two.date()][j] = jsn[j]
        self.data = d_dct


    def _ini(self):
        self.fig = Figure(figsize=(7, 5), dpi = 100)
        self.plot1 = self.fig.add_subplot(111)

    def get_date(self):
        ans = []
        for i in self.data.keys():
            ans.append(i.isoformat())

        return ans
    def get_plot(self, sr_i, prb_idx_l=[0], date_from=date(2021, 9, 20), date_to=date(2021, 10, 18), plot_name='Линейный',prd_v = ['BME280_temp','weather_temp', 'BME280_temp', 'BME280_temp']):

        if not sr_i:
            sr_i = 'Без усреднения'

        prd = ['Hydra-L', 'РОСА К-2', 'Тест воздуха', 'Тест Студии']

        print(prb_idx_l)
        for prb_idx in prb_idx_l:

            arr_x = []
            arr_y = []

            for date_now in self.data.keys():
                if date_from <= date_now <= date_to:
                    jsn = self.data[date_now]
                    for k in jsn.keys():
                        if jsn[k]['uName'] == prd[prb_idx]:
                            if jsn[k]['data'].get(prd_v[prb_idx]):
                                arr_x.append(jsn[k]['data'].get(prd_v[prb_idx]))
                                arr_y.append(datetime.fromisoformat(jsn[k]['Date']))
                            else:
                                continue
                        else:
                            continue
                else:
                    continue

            sr = {
                'Без усреднения' : lambda x: x.isoformat(" ","minutes"),
                'По часу' : lambda x: x.isoformat(" ","hours"),
                'По дню' : lambda x: x.date().isoformat(),
                'По 3 часа' : lambda x: x.isoformat(" ","hours"),
                'Макс-мин' : lambda x: x.date().isoformat(),
            }


            arr_y = list(map(sr[sr_i], arr_y))

            if sr_i == 'По 3 часа':
                for i in range(len(arr_y)):
                    t = arr_y[i]
                    t_e = int(t[-2:]) // 3
                    if t_e <= 9:
                        t_e = '0' + str(t_e)
                    else:
                        t_e = str(t_e)
                    t = t[:-2] + t_e
                    arr_y[i] = t

            data = pd.DataFrame({'temp':arr_x, 'date': arr_y})
            data['temp'] = data['temp'].astype(float)

            if sr_i != 'Макс-мин':
                data = data.groupby('date').agg('mean')
                data.index = data.index.astype('datetime64[ns]')
            else:
                data_max = data.groupby('date').agg('max')
                data_min = data.groupby('date').agg('min')

            if plot_name == 'Линейный':
                if sr_i != 'Макс-мин':
                    self.plot1.plot(data.index, data.temp)
                else:
                    self.plot1.plot(data_max.index, data_max.temp)
                    self.plot1.plot(data_min.index, data_min.temp)

            if plot_name == 'Столбчатый':
                if sr_i != 'Макс-мин':
                    self.plot1.bar(data.index, data.temp)
                else:
                    self.plot1.bar(data_max.index, data_max.temp)
                    self.plot1.bar(data_min.index, data_min.temp)

            if plot_name == 'Гистограмма':
                if sr_i != 'Макс-мин':
                    self.plot1.hist(data.temp,density=True, bins=50)
                else:
                    self.plot1.hist(data_max.temp,density=True,bins=30)
                    self.plot1.hist(data_min.temp,density=True,bins=30)

        if sr_i != 'Макс-мин':
            self.plot1.legend([prd[i] for i in prb_idx_l])
        else:
            self.plot1.legend(np.array([[str(prd[i]) + ' max', str(prd[i]) + ' min'] for i in prb_idx_l]).ravel())

        for tick in self.plot1.get_xticklabels():
            # float or {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
            tick.set_fontsize('xx-small')
            tick.set_rotation(35)

        canvas = FigureCanvasTkAgg(self.fig, master = self.window)
        canvas.draw()
        return canvas.get_tk_widget()

    def clear_plot(self):
        self.plot1.clear()
        self.fig.clear()
        self._ini()
