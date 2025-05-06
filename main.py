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


def f(x1, x2, t, function): #speed
    global k, b, J1, J2, n, frequency, amplitude, funTime
    a = -b / (J2 + n**2 * J1) #(k/n - k) / (J2 + J1)
    bb = -k / (J2 + n**2 * J1) #(b/n - b) / (J2 + J1)
    c = (1/n) / (J2 + n**2 *J1) #n / (J2 + J1) 
    if t <= funTime:
        if function == 'square': Tm = squareSignal(frequency, t, amplitude)
        elif function == 'sawTooth': Tm = sawToothSignal(frequency, t, amplitude)
        elif function == 'sin': Tm = sinSignal(frequency, t, amplitude)
        else: Tm = 0
    else: Tm = 0

    return  a * x1 + bb * x2  + c * Tm


def g(x1, x2, t, function): #position
    return x2


def RK4(x1_0, x2_0, t0, h, function, iterations):
    x1Values = []
    x2Values = []
    tValues = []

    for i in range(iterations):
        tValues.append(t0)
        x1Values.append(x1_0)
        x2Values.append(x2_0)

        k1 = h * g(x1_0, x2_0, t0, function)
        l1 = h * f(x1_0, x2_0, t0, function)
        
        k2 = h * g(x1_0 + k1/2, x2_0 + l1/2, t0 + h/2, function)
        l2 = h * f(x1_0 + k1/2, x2_0 + l1/2, t0 + h/2, function)

        k3 = h * g(x1_0 + k2/2, x2_0 + l2/2, t0 + h/2, function)
        l3 = h * f(x1_0 + k2/2, x2_0 + l2/2, t0 + h/2, function)

        k4 = h * g(x1_0 + k3, x2_0 + l3, t0 + h, function)
        l4 = h * f(x1_0 + k3, x2_0 + l3, t0 + h, function)

        x1_0 = x1_0 + (k1 + 2*k2 + 2*k3 + k4) / 6
        x2_0 = x2_0 + (l1 + 2*l2 + 2*l3 + l4) / 6
        t0 += h

    return x1Values, x2Values, tValues


def Euler(x1_0, x2_0, h, fun, iter):
    x1Values = [x1_0]
    x2Values = [x2_0]
    t0 = 0
    tValues = [t0]

    for i in range(iter):
        t0 += h
        lastX1_0 = x1_0
        x1_0 = x1_0 + h * g(x1_0, x2_0, t0, fun)  
        x2_0 = x2_0 + h * f(x1_0, x2_0, t0, fun)  # Poprawiona, wcześniej było: x2_0 = abs(lastX1_0-x1_0)/h, w dodatku x1 powinno byc raczej powiazane z g, x2 z f (chyba?)
        #x2_0=abs(lastX1_0-x1_0)/h 
        x1Values.append(x1_0)
        x2Values.append(x2_0)
        tValues.append(t0)

        
        """
        Wcześniej:
        t0 += h
        lastX1_0 = x1_0
        x1_0 = x1_0 + h * f(x1_0, x2_0, t0, fun)
        x2_0=abs(lastX1_0-x1_0)/h                   
        x1Values.append(x1_0)
        x2Values.append(x2_0)
        tValues.append(t0)
        Ale nwm, wyniki chyba nie powinny iść w nieskończoność
        """

    return x1Values, x2Values, tValues



# parameters:
k = 5
b = 5
n1 = 5
n2 = 3
n = n1/n2
J1 = 1
J2 = 1
#by był stabilny

# initial conditions:
x1_0 = 0
x2_0 = 0
t0 = 0
x1Values = []
x2Values = []
tValues = []

# simulation:
h = 0.01 # step size
N = 10000 # RK4 iterations

# signal auxiliary
amplitude = 1
frequency = 0.5
funTime = 2

function = 'square'
iterations = N
RKx1Values, RKx2Values, RKtValues = RK4(x1_0, x2_0, t0, h, function, iterations)
Ex1Values, Ex2Values, EtValues = Euler(x1_0, x2_0, h, function, iterations)

plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(RKtValues, RKx1Values, label="RK4 (Pozycja wału 2)")
plt.plot(EtValues, Ex1Values, label="E (Pozycja wału 2)")
plt.xlabel("Czas [s]")
plt.ylabel("Angle [rad]")
plt.title("Trajektoria (RK4)")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(RKtValues, RKx2Values, label="RK4 (Prędkość wału 2)")
plt.plot(EtValues, Ex2Values, label="E (Prędkość wału 2)")
plt.xlabel("Czas [s]")
plt.ylabel("Speed [rad/s]")
plt.title("Trajektoria (Euler)")
plt.legend()
plt.grid()
plt.show()