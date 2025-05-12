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
        self.h = 0.001  # step size
        self.simTime = 10
        self.iter = int(self.simTime // self.h)  # iterations

        # signal auxiliary
        self.amplitude = 1
        self.frequency = 1
        self.function = 'square'
        self.duty_cycle = 0.5
        self.signal_time = 2

    def __squareSignal(self, readTime):
        value = self.amplitude * scipy.signal.square(2 * np.pi * self.frequency * readTime, duty=self.duty_cycle)
        return value

    def __sawToothSignal(self, readTime):
        value = self.amplitude * scipy.signal.sawtooth(2 * np.pi * self.frequency * readTime)
        return value

    def __sinSignal(self, readTime):
        value = self.amplitude * np.sin(2 * np.pi * self.frequency * readTime)
        return value

    def __f(self, x1, x2, t):
        a = (-self.b) / (self.J2 + self.n ** 2 * self.J1)
        b = (-self.k) / (self.J2 + self.n ** 2 * self.J1)
        c = (1/self.n) / (self.J2 + self.n ** 2 * self.J1)

        if self.function == 'square':
            Tm = self.__squareSignal(t)
        elif self.function == 'sawtooth':
            Tm = self.__sawToothSignal(t)
        elif self.function == 'sin':
            Tm = self.__sinSignal(t)
        else: Tm = 0

        return a * x1 + b * x2 + c * Tm

    def __g(self, x1, x2, t):
        return x2

    def __RK4(self):
        self.RKx1Values.clear()
        self.RKx2Values.clear()
        self.tValues.clear()
        x1_0 = self.x1_0
        x2_0 = self.x2_0
        t0 = self.t0
        for i in range(self.iter):
            self.RKx1Values.append(x1_0)
            self.RKx2Values.append(x2_0)
            self.tValues.append(t0)

            k1 = self.h * self.__g(x1_0, x2_0, t0)
            l1 = self.h * self.__f(x1_0, x2_0, t0)

            k2 = self.h * self.__g(x1_0 + self.h / 2, x2_0 + k1 / 2, t0 + l1 / 2)
            l2 = self.h * self.__f(x1_0 + self.h / 2, x2_0 + k1 / 2, t0 + l1 / 2)

            k3 = self.h * self.__g(x1_0 + self.h / 2, x2_0 + k2 / 2, t0 + l2 / 2)
            l3 = self.h * self.__f(x1_0 + self.h / 2, x2_0 + k2 / 2, t0 + l2 / 2)

            k4 = self.h * self.__g(x1_0 + self.h, x2_0 + k3, t0 + l3)
            l4 = self.h * self.__f(x1_0 + self.h, x2_0 + k3, t0 + l3)

            x1_0 = x1_0 + (k1 + 2*k2 + 2*k3 + k4) / 6
            x2_0 = x2_0 + (l1 + 2*l2 + 2*l3 + l4) / 6
            t0 += self.h

    def __Euler(self):
        self.Ex1Values.clear()
        self.Ex2Values.clear()
        self.tValues.clear()
        x1_0 = self.x1_0
        x2_0 = self.x2_0
        t0 = self.t0
        for i in range(self.iter):
            t0 += self.h
            self.Ex1Values.append(x1_0)
            self.Ex2Values.append(x2_0)
            self.tValues.append(t0)

            x1_0 = x1_0 + self.h * self.__g(x1_0, x2_0, t0)
            x2_0 = x2_0 + self.h * self.__f(x1_0, x2_0, t0)

    def getRK4ChartData(self):
        self.__RK4()
        return self.RKx1Values, self.RKx2Values, self.tValues

    def getEulerChartData(self):
        self.__Euler()
        return self.Ex1Values, self.Ex2Values, self.tValues

    def setSimulationTime(self, num):
        self.simTime = num
        self.iter = int(self.simTime // self.h)

    def setStepSizeNumber(self, num):
        self.h = num*0.001
        self.iter = int(self.simTime // self.h)

    def setInputFunctionType(self, type):
        self.function = type

    def setInputSignalAmplitude(self, ampl):
        self.amplitude = ampl

    def setInputSignalFrequency(self, freq):
        self.frequency = freq

    def setSignalDutyCycle(self, duty_cycle):
        self.duty_cycle = duty_cycle * 0.01

    def setSignalTime(self, sig_time):
        self.signal_time = sig_time

    def setKValue(self, k_val):
        self.k = k_val

    def setBValue(self, b_val):
        self.b = b_val

    def setN1Value(self, n1_val):
        self.n1 = n1_val
        self.n = self.n1/self.n2

    def setN2Value(self, n2_val):
        self.n2 = n2_val
        self.n = self.n1/self.n2

'''
a = Simulation()
a.RK4()
a.Euler()
x1Data, x2Data, x1tData = a.getRK4ChartData()
y1Data, y2Data, y1tData = a.getEulerChartData()

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
'''