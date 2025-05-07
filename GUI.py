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
        self.signal_type = ["square", "sawtooth", "sin"]
        self.chart_radio = wx.RadioBox(
            self.control_panel,
            choices=self.signal_type,
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS
        )
        self.chart_radio.Bind(wx.EVT_RADIOBOX, self.on_input_signal_change)  # event
        chart_sizer.Add(self.chart_radio, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(chart_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # simulation time slider
        iter_box = wx.StaticBox(self.control_panel, label="Simulation Time")
        iter_sizer = wx.StaticBoxSizer(iter_box, wx.VERTICAL)
        self.iter_slider = wx.Slider(
            self.control_panel,
            value=10,
            minValue=1,
            maxValue=20,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.iter_slider.Bind(wx.EVT_SLIDER, self.on_iter_change)  # slider event
        iter_sizer.Add(self.iter_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(iter_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # step_size slider
        step_size_box = wx.StaticBox(self.control_panel, label="Step size")
        step_size_sizer = wx.StaticBoxSizer(step_size_box, wx.VERTICAL)
        self.step_size_slider = wx.Slider(
            self.control_panel,
            value=10,
            minValue=1,
            maxValue=100,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.step_size_slider.Bind(wx.EVT_SLIDER, self.on_step_size_change)  # slider event
        step_size_sizer.Add(self.step_size_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(step_size_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # k slider
        k_box = wx.StaticBox(self.control_panel, label="k value")
        k_sizer = wx.StaticBoxSizer(k_box, wx.VERTICAL)
        self.k_slider = wx.Slider(
            self.control_panel,
            value=1,
            minValue=1,
            maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.k_slider.Bind(wx.EVT_SLIDER, self.on_k_change)  # slider event
        k_sizer.Add(self.k_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(k_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # b slider
        b_box = wx.StaticBox(self.control_panel, label="b value")
        b_sizer = wx.StaticBoxSizer(b_box, wx.VERTICAL)
        self.b_slider = wx.Slider(
            self.control_panel,
            value=1,
            minValue=1,
            maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.b_slider.Bind(wx.EVT_SLIDER, self.on_b_change)  # slider event
        b_sizer.Add(self.b_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(b_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # n1 slider
        n1_box = wx.StaticBox(self.control_panel, label="n1 value")
        n1_sizer = wx.StaticBoxSizer(n1_box, wx.VERTICAL)
        self.n1_slider = wx.Slider(
            self.control_panel,
            value=5,
            minValue=1,
            maxValue=50,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.n1_slider.Bind(wx.EVT_SLIDER, self.on_n1_change)  # slider event
        n1_sizer.Add(self.n1_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(n1_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # n2 slider
        n2_box = wx.StaticBox(self.control_panel, label="n2 value")
        n2_sizer = wx.StaticBoxSizer(n2_box, wx.VERTICAL)
        self.n2_slider = wx.Slider(
            self.control_panel,
            value=3,
            minValue=1,
            maxValue=50,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.n2_slider.Bind(wx.EVT_SLIDER, self.on_n2_change)  # slider event
        n2_sizer.Add(self.n2_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(n2_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Button
        self.update_btn = wx.Button(self.control_panel, label="Update chart")
        self.update_btn.Bind(wx.EVT_BUTTON, self.generate_chart)  # random btn event
        control_sizer.Add(self.update_btn, 0, wx.EXPAND | wx.ALL, 10)

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
        ax.set_xlabel('Time axis')
        ax.set_ylabel('Y axis')
        ax.set_title('RK4 Chart')

        EdataX1, EdataX2, EdataT = self.chartData.getEulerChartData()
        ax = self.plot2_panel.figure.add_subplot(111)
        ax.plot(EdataT, EdataX1, color='red')
        ax.plot(EdataT, EdataX2, color='green')

        ax.grid(True)
        ax.set_xlabel('Time axis')
        ax.set_ylabel('Y axis')
        ax.set_title('Euler Chart')

        self.plot1_panel.canvas.draw()
        self.plot2_panel.canvas.draw()

    def generate_chart(self, event):
        self.update_chart()

    def on_input_signal_change(self, event):
        self.chartData.setInputFunctionType(self.chart_radio.GetItemLabel(self.chart_radio.GetSelection()))

    def on_iter_change(self, event):
        self.chartData.setSimulationTime(self.iter_slider.GetValue())

    def on_step_size_change(self, event):
        self.chartData.setStepSizeNumber(self.step_size_slider.GetValue())

    def on_k_change(self, event):
        self.chartData.setKValue(self.k_slider.GetValue())

    def on_b_change(self, event):
        self.chartData.setKValue(self.b_slider.GetValue())

    def on_n1_change(self, event):
        self.chartData.setKValue(self.n1_slider.GetValue())

    def on_n2_change(self, event):
        self.chartData.setKValue(self.n2_slider.GetValue())


if __name__ == '__main__':
    app = wx.App()
    frame = ChartFrame()
    frame.Show()
    app.MainLoop()
