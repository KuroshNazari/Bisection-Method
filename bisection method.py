'''
Solutions of Equations in One Variable,  The Bisection Method
October 6, 2024 by Kurosh Nazari
'''


from sympy import symbols, plot, sympify, lambdify
from prettytable import PrettyTable as pt
import matplotlib.pyplot as plt
import numpy as np


class BisectionMethod:
    def __init__(self, max_iteration, epsilon, stopping_procedures):
        self.equation = None
        self.initial_point = None
        self.terminal_point = None
        self.breaked = None
        self.stopping_procedures = int(stopping_procedures)
        self.max_iteration = max_iteration
        self.epsilon = epsilon

    def is_accurate(self, mid_point, last_mid_point):

        """
        This function checks, if we've got the desired accuracy
        """

        # returns true if |midpoint_N − midpoint_N−1| < ε,
        if self.stopping_procedures == 1:
            if last_mid_point:
                return True if abs(mid_point-last_mid_point) < self.epsilon else False
        
        # returns true if |f(midpoint_N)| < ε,
        elif self.stopping_procedures == 2:
            x = symbols('x')
            return True if abs(self.equation.subs(x, mid_point)) < self.epsilon else False
        
        # returns true if |midpoint_N − midpoint_N−1|/|midpoint_N| < ε and midpoint != 0,
        elif self.stopping_procedures == 3:
            if last_mid_point:
                f = (abs(mid_point - last_mid_point)/abs(mid_point))
                return True if f < self.epsilon and mid_point != 0 else False


    def get_problem(self):

        """
        This function takes a function and plots it to user 
        then takes an interval to search for root inside, again plots it to check 
        if there is a root inside the interval.
        """

        x = symbols('x')
        satisfied = False

        # taking function
        equation = input('input an equation: ')
        self.equation = sympify(equation)

        # ploting the function to estimate the (a,b) interval
        p = plot(self.equation, (x, -10, 10), show=True)

        # getting (a,b) interval
        while not satisfied:
            interval = input('input an interval in form of (x,y): ')
            interval = interval.strip('()')
            interval = interval.split(',')
            self.initial_point = float(interval[0])
            self.terminal_point = float(interval[1])

            # ploting function and interval to check if the root is in interval
            function = lambdify(x, self.equation)
            x_values = np.linspace(self.initial_point, self.terminal_point, 100)
            y_values = function(x_values)

            plt.axvline(x=self.initial_point, color='blue', label='a')
            plt.axvline(x=self.terminal_point, color='red', label='b')
            plt.plot(x_values, y_values, color='green', label=self.equation)
            plt.axhline(y=0, color="black", linestyle="--", label='y axis')
            plt.grid(color='grey')
            plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, ncol=4)
            plt.title(self.equation)
            plt.show()
            
            satisfied = input('are you satisfied? (y/N) ') == 'y'


    def solve(self):

        """
        This function uses bisection method to approximate the root of the function
        """

        self.get_problem()

        # using pretty table to print output beautifully
        my_table = pt(['n', 'a', 'b', 'mid point','f(mid point)', 'sign(f(mid point)*f(a))'])

        x = symbols('x')
        initial_point = self.initial_point
        terminal_point = self.terminal_point
        last_mid_point = None

        for i in range(1, self.max_iteration):
            sign = '0'
            mid_point = (initial_point + terminal_point)/2
            f_initial_point = self.equation.subs(x, initial_point)
            f_mid_point = self.equation.subs(x, mid_point)

            if f_mid_point * f_initial_point > 0:
                initial_point = mid_point
                sign = "+"
            
            elif f_mid_point * f_initial_point < 0:
                terminal_point = mid_point
                sign = "-"

            # using pretty table to print output beautifully
            my_table.add_row([i, f"{initial_point:.5f}", f"{terminal_point:.5f}", f"{mid_point:.5f}", f"{f_mid_point:.5f}", sign])
            

            if f_mid_point == float(0):
                print()
                print(f'The approximated root for {self.equation} is: {mid_point:.5f}')
                print(my_table)
                print()
                self.breaked = True
                break

            if self.is_accurate(mid_point=mid_point, last_mid_point=last_mid_point):
                print()
                print(f'The approximated root for "{self.equation}" is: {mid_point:.5f} | Telorance: {self.epsilon}')
                print(my_table)
                print()
                self.breaked = True
                break

            last_mid_point = mid_point
        

"""
procedur_1: checks if |midpoint_N - midpoint_N-1| < ε
procedur_2: checks if |f(midpoint_N)| < ε
procedur_3: checks if |midpoint_N - midpoint_N-1|/|midpoint_N| < ε and midpoint != 0
 
"""            

b = BisectionMethod(max_iteration=100, epsilon=0.00001, stopping_procedures=3)
b.solve()

if not b.breaked:
    print('Bisection failed to approximate the root.')


