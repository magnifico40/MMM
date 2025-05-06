import numpy as np
import scipy
import matplotlib.pyplot as plt

class Simulation:
    def __init__(self):
        # parameters:
        self.k = 5
        self.b = 5
        self.n1 = 5
        self.n2 = 3
        self.n = self.n1 / self.n2
        self.J1 = 1
        self.J2 = 1

        # initial conditions:
        self.x1_0 = 0
        self.x2_0 = 0
        self.t0 = 0
        self.RKx1Values = []
        self.RKx2Values = []
        self.Ex1Values = []
        self.Ex2Values = []
        self.tValues = []

        # simulation:
        self.h = 0.01  # step size
        self.N = 1000  # RK4 iterations

        # signal auxiliary
        self.amplitude = 1
        self.frequency = 0.5
        self.function = 'sin'
        self.duty_cycle = 0.5

    def squareSignal(self, readTime):
        value = self.amplitude * scipy.signal.square(2 * np.pi * self.frequency * readTime, duty=self.dutyCycle)
        return value

    def sawToothSignal(self, readTime):
        value = self.amplitude * scipy.signal.sawtooth(2 * np.pi * self.frequency * readTime)
        return value

    def sinSignal(self, readTime):
        value = self.amplitude * np.sin(2 * np.pi * self.frequency * readTime)
        return value

    def f(self, x1, x2, t):
        a = (-self.b) / (self.J2 + self.n ** 2 * self.J1)
        b = (-self.k) / (self.J2 + self.n ** 2 * self.J1)
        c = (1/self.n) / (self.J2 + self.n ** 2 * self.J1)

        if self.function == 'square':
            Tm = self.squareSignal(t)
        elif self.function == 'sawTooth':
            Tm = self.sawToothSignal(t)
        elif self.function == 'sin':
            Tm = self.sinSignal(t)
        else: Tm = 0

        return a * x1 + b * x2 + c * Tm

    def g(self, x1, x2, t):
        return x2

    def RK4(self):
        self.RKx1Values.clear()
        self.RKx2Values.clear()
        self.tValues.clear()
        x1_0 = self.x1_0
        x2_0 = self.x2_0
        t0 = self.t0
        for i in range(self.N):
            self.RKx1Values.append(x1_0)
            self.RKx2Values.append(x2_0)
            self.tValues.append(t0)

            k1 = self.h * self.g(x1_0, x2_0, t0)
            l1 = self.h * self.f(x1_0, x2_0, t0)

            k2 = self.h * self.g(x1_0 + self.h / 2, x2_0 + k1 / 2, t0 + l1 / 2)
            l2 = self.h * self.f(x1_0 + self.h / 2, x2_0 + k1 / 2, t0 + l1 / 2)

            k3 = self.h * self.g(x1_0 + self.h / 2, x2_0 + k2 / 2, t0 + l2 / 2)
            l3 = self.h * self.f(x1_0 + self.h / 2, x2_0 + k2 / 2, t0 + l2 / 2)

            k4 = self.h * self.g(x1_0 + self.h, x2_0 + k3, t0 + l3)
            l4 = self.h * self.f(x1_0 + self.h, x2_0 + k3, t0 + l3)

            x1_0 = x1_0 + (k1 + 2*k2 + 2*k3 + k4) / 6
            x2_0 = x2_0 + (l1 + 2*l2 + 2*l3 + l4) / 6
            t0 += self.h

    def Euler(self):
        self.Ex1Values.clear()
        self.Ex2Values.clear()
        self.tValues.clear()
        x1_0 = self.x1_0
        x2_0 = self.x2_0
        t0 = self.t0
        for i in range(self.N):
            t0 += self.h
            self.Ex1Values.append(x1_0)
            self.Ex2Values.append(x2_0)
            self.tValues.append(t0)

            x1_0 = x1_0 + self.h * self.g(x1_0, x2_0, t0)
            x2_0 = x2_0 + self.h * self.f(x1_0, x2_0, t0)

    def getRK4ChartData(self):
        return self.RKx1Values, self.RKx2Values, self.tValues

    def getEulerChartData(self):
        return self.Ex1Values, self.Ex2Values, self.tValues


a = Simulation()
a.RK4()
a.Euler()
x1Data, x2Data, x1tData = a.getRK4ChartData()
y1Data, y2Data, y1tData = a.getEulerChartData()

"""

"""
plt.figure(figsize=(10, 8))
plt.plot(x1tData, x1Data, label="Położenie  RK4 ")
plt.plot(x1tData, x2Data, label="Prędkość RK4")
plt.plot(y1tData, x2Data, label="Położenie Euler")
plt.plot(y1tData, x2Data, label="Prędkość Euler")
plt.xlabel("Czas [s]")
plt.ylabel("Wartości")
plt.title("Trajektoria (RK4)")
plt.legend()
plt.grid()

plt.show()

"""
#Alternative View for testing

plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(x1tData, x1Data, label="RK4 (Pozycja wału 2)")
plt.plot(y1tData, y1Data, label="E (Pozycja wału 2)")
plt.xlabel("Czas [s]")
plt.ylabel("Angle [rad]")
plt.title("Trajektoria (RK4)")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(x1tData, x2Data, label="RK4 (Prędkość wału 2)")
plt.plot(y1tData, y2Data, label="E (Prędkość wału 2)")
plt.xlabel("Czas [s]")
plt.ylabel("Speed [rad/s]")
plt.title("Trajektoria (Euler)")
plt.legend()
plt.grid()
plt.show()
"""