


#parameters:
k = 1
b = 1
n1 = 3
n2 = 5
n = n1/n2
J1 = 1
J2 = 1

#initial conditions
x1_0 = 0
x2_0 = 0
t0 = 0

#simulation:
h = 0.2 #step size

def Tm():
    return 1

def f(x1, x2, t):
    a = (k/n - k) / (J2 + 1)
    b = (b/n - b) / (J2 + 1)
    c = n / (J2+1) 

    return  a * x1 + b * x2  + c * Tm(t)

def g(x1, x2, Tm):
    return x2

def RK4():
    k1 = h * f(x1_0, x2_0, t0)
    l1 = h * g(x1_0, x2_0, t0)
    
    k2 = h * f(x1_0 + h/2, x2_0 + k1/2, t0 + l1/2)
    l2 = h * g(x1_0 + h/2, x2_0 + k1/2, t0 + l1/2)

    k3 = h * f(x1_0 + h/2, x2_0 + k2/2, t0 + l2/2)
    l3 = h * g(x1_0 + h/2, x2_0 + k2/2, t0 + l2/2)

    k4 = h * f(x1_0 + h, x2_0 + k3, t0 + l3)
    l4 = h * g(x1_0 + h, x2_0 + k3, t0 + l3)

    return x2_0 + 1/6 * (k1 + 2*k2 + 2*k3 + k4)