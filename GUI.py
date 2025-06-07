import wx
import wx.lib.scrolledpanel as scrolled
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from main2 import Simulation


class ChartPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.figure = Figure(figsize=(1, 1), dpi=100)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)

        self.SetSizer(sizer)


class ChartFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Simulation", size=(1440, 1000))

        self.chartData = Simulation()

        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left side: Scrolled Control Panel
        control_panel = scrolled.ScrolledPanel(main_panel, -1, size=(350, -1))
        control_panel.SetupScrolling(scroll_x=False, scroll_y=True)
        control_sizer = wx.BoxSizer(wx.VERTICAL)

        # Input Signals parameters group

        signal_box = wx.StaticBox(control_panel, label="Input Signal Parameters")
        signal_sizer = wx.StaticBoxSizer(signal_box, wx.VERTICAL)
        control_sizer.Add(signal_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # radio box
        chart_box = wx.StaticBox(signal_box, label="Input Signal Type")
        chart_sizer = wx.StaticBoxSizer(chart_box, wx.VERTICAL)
        self.signal_type = ["square", "sawtooth", "sin"]
        self.chart_radio = wx.RadioBox(
            chart_box,
            choices=self.signal_type,
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS
        )
        self.chart_radio.Bind(wx.EVT_RADIOBOX, self.on_input_signal_change)  # event
        chart_sizer.Add(self.chart_radio, 0, wx.EXPAND | wx.ALL, 5)
        signal_sizer.Add(chart_sizer, 0, wx.EXPAND | wx.ALL, 10)

        #  Duty Cycle Slider
        self.dutyCycle_box = wx.StaticBox(signal_box, label="Input Signal Duty Cycle")
        dutyCycle_sizer = wx.StaticBoxSizer(self.dutyCycle_box, wx.VERTICAL)
        self.dutyCycle_slider = wx.Slider(
            self.dutyCycle_box,
            value=50,
            minValue=1,
            maxValue=100,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.dutyCycle_slider.Bind(wx.EVT_SLIDER, self.on_duty_cycle_change)  # slider event
        dutyCycle_sizer.Add(self.dutyCycle_slider, 0, wx.EXPAND | wx.ALL, 5)
        signal_sizer.Add(dutyCycle_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # simulation time slider
        iter_box = wx.StaticBox(control_panel, label="Simulation Time")
        iter_sizer = wx.StaticBoxSizer(iter_box, wx.VERTICAL)
        self.iter_slider = wx.Slider(
            iter_box,
            value=10,
            minValue=1,
            maxValue=200,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.iter_slider.Bind(wx.EVT_SLIDER, self.on_iter_change)  # slider event
        iter_sizer.Add(self.iter_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(iter_sizer, 0, wx.EXPAND | wx.ALL, 10)

        #  Amplitude Slider
        ampl_box = wx.StaticBox(signal_box, label="Signal Amplitude")
        ampl_sizer = wx.StaticBoxSizer(ampl_box, wx.VERTICAL)
        self.ampl_slider = wx.Slider(
            ampl_box,
            value=1,
            minValue=1,
            maxValue=100,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.ampl_slider.Bind(wx.EVT_SLIDER, self.on_signal_amplitude_change)  # slider event
        ampl_sizer.Add(self.ampl_slider, 0, wx.EXPAND | wx.ALL, 5)
        signal_sizer.Add(ampl_sizer, 0, wx.EXPAND | wx.ALL, 10)

        #  Frequency Slider
        freq_box = wx.StaticBox(signal_box, label="Signal Frequency")
        freq_sizer = wx.StaticBoxSizer(freq_box, wx.VERTICAL)
        self.freq_slider = wx.Slider(
            freq_box,
            value=1,
            minValue=1,
            maxValue=50,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.freq_slider.Bind(wx.EVT_SLIDER, self.on_signal_frequency_change)  # slider event
        freq_sizer.Add(self.freq_slider, 0, wx.EXPAND | wx.ALL, 5)
        signal_sizer.Add(freq_sizer, 0, wx.EXPAND | wx.ALL, 10)

        #  Signal Time Slider
        self.sigTime_box = wx.StaticBox(signal_box, label="Input Signal Time")
        sigTime_sizer = wx.StaticBoxSizer(self.sigTime_box, wx.VERTICAL)
        self.sigTime_slider = wx.Slider(
            self.sigTime_box,
            value=2,
            minValue=1,
            maxValue=20,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.sigTime_slider.Bind(wx.EVT_SLIDER, self.on_signal_time_change)  # slider event
        sigTime_sizer.Add(self.sigTime_slider, 0, wx.EXPAND | wx.ALL, 5)
        signal_sizer.Add(sigTime_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # step_size slider
        step_size_box = wx.StaticBox(control_panel, label="Step size x0.001")
        step_size_sizer = wx.StaticBoxSizer(step_size_box, wx.VERTICAL)
        self.step_size_slider = wx.Slider(
            step_size_box,
            value=10,
            minValue=1,
            maxValue=100,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.step_size_slider.Bind(wx.EVT_SLIDER, self.on_step_size_change)  # slider event
        step_size_sizer.Add(self.step_size_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(step_size_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # k slider
        k_box = wx.StaticBox(control_panel, label="k value")
        k_sizer = wx.StaticBoxSizer(k_box, wx.VERTICAL)
        self.k_slider = wx.Slider(
            k_box,
            value=1,
            minValue=1,
            maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.k_slider.Bind(wx.EVT_SLIDER, self.on_k_change)  # slider event
        k_sizer.Add(self.k_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(k_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # b slider
        b_box = wx.StaticBox(control_panel, label="b value")
        b_sizer = wx.StaticBoxSizer(b_box, wx.VERTICAL)
        self.b_slider = wx.Slider(
            b_box,
            value=1,
            minValue=1,
            maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.b_slider.Bind(wx.EVT_SLIDER, self.on_b_change)  # slider event
        b_sizer.Add(self.b_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(b_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # n1 slider
        n1_box = wx.StaticBox(control_panel, label="n1 value")
        n1_sizer = wx.StaticBoxSizer(n1_box, wx.VERTICAL)
        self.n1_slider = wx.Slider(
            n1_box,
            value=5,
            minValue=1,
            maxValue=50,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.n1_slider.Bind(wx.EVT_SLIDER, self.on_n1_change)  # slider event
        n1_sizer.Add(self.n1_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(n1_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # n2 slider
        n2_box = wx.StaticBox(control_panel, label="n2 value")
        n2_sizer = wx.StaticBoxSizer(n2_box, wx.VERTICAL)
        self.n2_slider = wx.Slider(
            n2_box,
            value=3,
            minValue=1,
            maxValue=50,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.n2_slider.Bind(wx.EVT_SLIDER, self.on_n2_change)  # slider event
        n2_sizer.Add(self.n2_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(n2_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # x1 initial condition
        x1_0_box = wx.StaticBox(control_panel, label="x1_0 initial value")
        x1_0_sizer = wx.StaticBoxSizer(x1_0_box, wx.VERTICAL)
        self.x1_0_slider = wx.Slider(
            x1_0_box,
            value=0,
            minValue=-10,
            maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.x1_0_slider.Bind(wx.EVT_SLIDER, self.on_x1_0_change)  # slider event
        x1_0_sizer.Add(self.x1_0_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(x1_0_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # x2 initial condition
        x2_0_box = wx.StaticBox(control_panel, label="x2_0 initial value")
        x2_0_sizer = wx.StaticBoxSizer(x2_0_box, wx.VERTICAL)
        self.x2_0_slider = wx.Slider(
            x2_0_box,
            value=0,
            minValue=-10,
            maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.x2_0_slider.Bind(wx.EVT_SLIDER, self.on_x2_0_change)  # slider event
        x2_0_sizer.Add(self.x2_0_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(x2_0_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # J1
        j1_box = wx.StaticBox(control_panel, label="J1 value")
        j1_sizer = wx.StaticBoxSizer(j1_box, wx.VERTICAL)
        self.j1_slider = wx.Slider(
            j1_box,
            value=0,
            minValue=0,
            maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.j1_slider.Bind(wx.EVT_SLIDER, self.on_j1_change)  # slider event
        j1_sizer.Add(self.j1_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(j1_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # J2
        j2_box = wx.StaticBox(control_panel, label="J2 value")
        j2_sizer = wx.StaticBoxSizer(j2_box, wx.VERTICAL)
        self.j2_slider = wx.Slider(
            j2_box,
            value=0,
            minValue=0,
            maxValue=10,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        self.j2_slider.Bind(wx.EVT_SLIDER, self.on_j2_change)  # slider event
        j2_sizer.Add(self.j2_slider, 0, wx.EXPAND | wx.ALL, 5)
        control_sizer.Add(j2_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Button
        self.update_btn = wx.Button(control_panel, label="Update chart")
        self.update_btn.Bind(wx.EVT_BUTTON, self.generate_chart)  # random btn event
        control_sizer.Add(self.update_btn, 0, wx.EXPAND | wx.ALL, 10)

        control_panel.SetSizer(control_sizer)

        self.v_splitter = wx.SplitterWindow(main_panel)
        # Matplot panel
        self.plot1_panel = ChartPanel(self.v_splitter)
        self.plot2_panel = ChartPanel(self.v_splitter)

        self.v_splitter.SplitHorizontally(self.plot1_panel, self.plot2_panel)
        self.v_splitter.SetMinimumPaneSize(100)
        self.v_splitter.SetSashPosition(self.GetSize().GetHeight() // 2)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        main_sizer.Add(control_panel, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.v_splitter, 1, wx.EXPAND | wx.ALL, 10)

        main_panel.SetSizer(main_sizer)

        self.update_chart()

        self.Centre()
        self.Maximize(True)

    def OnSize(self, event):
        # When the window is resized, keep the panels equal
        size = self.GetSize()
        self.v_splitter.SetSashPosition(size.GetHeight() // 2)
        event.Skip()

    def update_chart(self):
        self.plot1_panel.figure.clear()
        self.plot2_panel.figure.clear()

        dataX1, dataX2, dataT = self.chartData.getRK4ChartData()
        EdataX1, EdataX2, EdataT = self.chartData.getEulerChartData()

        ax = self.plot1_panel.figure.add_subplot(111)
        ax.plot(dataT, dataX1, color='blue', label='Position  RK4')
        ax.plot(dataT, EdataX1, color='orange', label='Position Euler')

        ax.grid(True)
        ax.set_xlabel('Time axis [s]')
        ax.set_ylabel('Value')
        ax.set_title('Position Chart')
        ax.legend()

        ax = self.plot2_panel.figure.add_subplot(111)
        ax.plot(EdataT, dataX2, color='red', label='Speed  RK4')
        ax.plot(EdataT, EdataX2, color='green', label='Speed Euler')

        ax.grid(True)
        ax.set_xlabel('Time axis')
        ax.set_ylabel('Value')
        ax.set_title('Speed Chart')
        ax.legend()

        self.plot1_panel.canvas.draw()
        self.plot2_panel.canvas.draw()

    def generate_chart(self, event):
        self.update_chart()

    def on_input_signal_change(self, event):
        signalType = self.chart_radio.GetItemLabel(self.chart_radio.GetSelection())
        self.chartData.setInputFunctionType(signalType)
        if signalType == 'square':
            self.dutyCycle_box.Show()
            self.sigTime_box.Show()
        else:
            self.dutyCycle_box.Hide()
            self.sigTime_box.Hide()

    def on_signal_amplitude_change(self, event):
        self.chartData.setInputSignalAmplitude(self.ampl_slider.GetValue())

    def on_signal_frequency_change(self, event):
        self.chartData.setInputSignalFrequency(self.freq_slider.GetValue())

    def on_duty_cycle_change(self, event):
        self.chartData.setSignalDutyCycle(self.dutyCycle_slider.GetValue())

    def on_signal_time_change(self, event):
        self.chartData.setSignalTime(self.sigTime_slider.GetValue())

    def on_iter_change(self, event):
        self.chartData.setSimulationTime(self.iter_slider.GetValue())

    def on_step_size_change(self, event):
        self.chartData.setStepSizeNumber(self.step_size_slider.GetValue())

    def on_k_change(self, event):
        self.chartData.setKValue(self.k_slider.GetValue())

    def on_b_change(self, event):
        self.chartData.setBValue(self.b_slider.GetValue())

    def on_n1_change(self, event):
        self.chartData.setN1Value(self.n1_slider.GetValue())

    def on_n2_change(self, event):
        self.chartData.setN2Value(self.n2_slider.GetValue())

    def on_x1_0_change(self, event):
        self.chartData.setX1_0Value(self.x1_0_slider.GetValue())

    def on_x2_0_change(self, event):
        self.chartData.setX2_0Value(self.x2_0_slider.GetValue())

    def on_j1_change(self, event):
        self.chartData.setJ1Value(self.j1_slider.GetValue())

    def on_j2_change(self, event):
        self.chartData.setJ2Value(self.j2_slider.GetValue())


if __name__ == '__main__':
    app = wx.App()
    frame = ChartFrame()
    frame.Show()
    app.MainLoop()
