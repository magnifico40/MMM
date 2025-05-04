import numpy as np
import scipy
import matplotlib.pyplot as plt

def squareSignal(frequency, readTime, amplitude, dutyCycle = 0.5):
    value = amplitude * scipy.signal.square(2 * np.pi * frequency * readTime, duty = dutyCycle)
    return value

def sawToothSignal(frequency, readTime, amplitude):
    value = amplitude* scipy.signal.sawtooth(2 * np.pi * frequency * readTime)
    return value

def sinSignal(frequency, readTime, amplitude):
    value = amplitude * np.sin(2 * np.pi * frequency * readTime)
    return value

def f(x1, x2, t, function):
    global k, b, J1, J2, n, frequency, amplitude
    a = (k/n - k) / (J2 + J1)
    b = (b/n - b) / (J2 + J1)
    c = n / (J2 + J1) 
    
    if function == 'square': Tm = squareSignal(frequency, t, amplitude)
    elif function == 'sawTooth': Tm = sawToothSignal(frequency, t, amplitude)
    elif function == 'sin': Tm = sinSignal(frequency, t, amplitude)

    return  a * x1 + b * x2  + c * Tm

def g(x1, x2, t):
    return x2

def RK4(x1_0, x2_0, t0, h, function, iterations):
    x1Values = []
    x2Values = []
    tValues = []

    for i in range(iterations):
        t0+=h
        x1Values.append(x1_0)
        x2Values.append(x2_0)
        tValues.append(t0)

        k1 = h * f(x1_0, x2_0, t0, function)
        l1 = h * g(x1_0, x2_0, t0)
        
        k2 = h * f(x1_0 + h/2, x2_0 + k1/2, t0 + l1/2, function)
        l2 = h * g(x1_0 + h/2, x2_0 + k1/2, t0 + l1/2)

        k3 = h * f(x1_0 + h/2, x2_0 + k2/2, t0 + l2/2, function)
        l3 = h * g(x1_0 + h/2, x2_0 + k2/2, t0 + l2/2)

        k4 = h * f(x1_0 + h, x2_0 + k3, t0 + l3, function)
        l4 = h * g(x1_0 + h, x2_0 + k3, t0 + l3)

        x1_0 = x1_0 + 1/6 * (l1 + 2*l2 + 2*l3 + l4)
        x2_0 = x2_0 + 1/6 * (k1 + 2*k2 + 2*k3 + k4)

    return x1Values, x2Values, tValues





#parameters:
k = 1
b = 1
n1 = 3
n2 = 5
n = n1/n2
J1 = 1
J2 = 1

#initial conditions:
x1_0 = 0
x2_0 = 0
t0 = 0
x1Values = []
x2Values = []
tValues = []

#simulation:
h = 0.2 #step size
N = 100 #RK4 iterations

#signal auxiliary
amplitude = 1
frequency = 2
amplitude = 1

function = 'sin'
iterations = 100
x1Values, x2Values, tValues = RK4(x1_0, x2_0, t0, h, function, iterations)

plt.figure(figsize=(10, 5))
plt.plot(tValues, x1Values, label="x1 (Pozycja wału 2)")
plt.plot(tValues, x2Values, label="x2 (Prędkość wału 2)")
plt.xlabel("Czas [s]")
plt.ylabel("Wartości")
plt.title("Trajektoria")
plt.legend()
plt.grid()
plt.show()