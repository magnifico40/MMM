import wx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure


import numpy as np
import scipy
import matplotlib.pyplot as plt
from main2 import Simulation

class ChartPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)

        self.SetSizer(sizer)


class ChartFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Simulation", size=(1440, 1000))

        self.chartData = Simulation()

        self.splitter = wx.SplitterWindow(self)

        self.control_panel = wx.Panel(self.splitter)
        control_sizer = wx.BoxSizer(wx.VERTICAL)

        # radio box
        chart_box = wx.StaticBox(self.control_panel, label="Input Signal Type")
        chart_sizer = wx.StaticBoxSizer(chart_box, wx.VERTICAL)
        self.signal_type = ["Square", "Triangle", "Sinus"]
        self.chart_radio = wx.RadioBox(
            self.control_panel,
            choices=self.signal_type,
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS
        )
        self.chart_radio.Bind(wx.EVT_RADIOBOX, self.on_input_signal_change)  # event
        chart_sizer.Add(self.chart_radio, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(chart_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # slider
        iter_box = wx.StaticBox(self.control_panel, label="Number of Iterations")
        iter_sizer = wx.StaticBoxSizer(iter_box, wx.VERTICAL)

        self.iter_slider = wx.Slider(
            self.control_panel,
            value=1000,
            minValue=100,
            maxValue=8000,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.iter_slider.Bind(wx.EVT_SLIDER, self.on_iter_change)  # slider event
        iter_sizer.Add(self.iter_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(iter_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Button
        self.random_btn = wx.Button(self.control_panel, label="Random settings")
        self.random_btn.Bind(wx.EVT_BUTTON, self.on_random_settings)  # random btn event
        control_sizer.Add(self.random_btn, 0, wx.EXPAND | wx.ALL, 10)

        self.control_panel.SetSizer(control_sizer)

        self.v_splitter = wx.SplitterWindow(self.splitter)
        # Matplot panel
        self.plot1_panel = ChartPanel(self.v_splitter)
        self.plot2_panel = ChartPanel(self.v_splitter)

        self.splitter.SplitVertically(self.control_panel, self.v_splitter)
        self.splitter.SetMinimumPaneSize(200)
        self.splitter.SetSashPosition(350)

        self.v_splitter.SplitHorizontally(self.plot1_panel, self.plot2_panel)
        self.v_splitter.SetMinimumPaneSize(100)
        self.v_splitter.SetSashPosition(self.GetSize().GetHeight() // 2)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(frame_sizer)

        self.update_chart()

        self.Centre()

    def OnSize(self, event):
        # When the window is resized, keep the panels equal
        size = self.GetSize()
        self.v_splitter.SetSashPosition(size.GetHeight() // 2)
        event.Skip()

    def update_chart(self):
        self.plot1_panel.figure.clear()
        self.plot2_panel.figure.clear()

        dataX1, dataX2, dataT = self.chartData.getRK4ChartData()
        ax = self.plot1_panel.figure.add_subplot(111)
        ax.plot(dataT, dataX1, color='blue')
        ax.plot(dataT, dataX2, color='orange')

        ax.grid(True)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_title('RK4 Chart')

        EdataX1, EdataX2, EdataT = self.chartData.getEulerChartData()
        ax = self.plot2_panel.figure.add_subplot(111)
        ax.plot(EdataT, EdataX1, color='red')
        ax.plot(EdataT, EdataX2, color='green')

        ax.grid(True)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_title('Euler Chart')

        self.plot1_panel.canvas.draw()
        self.plot2_panel.canvas.draw()

    def on_input_signal_change(self):
        pass

    def on_iter_change(self, event):
        self.chartData.setIterationsNumber(self.iter_slider.GetValue())
        self.update_chart()

    def on_random_settings(self):
        pass


if __name__ == '__main__':
    app = wx.App()
    frame = ChartFrame()
    frame.Show()
    app.MainLoop()
