#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:06:13 2020

@author: Foofoo
"""


semi_annual_raise = 0.07
r = 0.04
portion_down_payment = 0.25
total_cost = 1000000
annual_salary = int(input("Starting salary: "))

n_months = 36

def amt_saved(savings_rate):
    portion_saved = savings_rate/10000.
    current_savings = 0
    monthly_salary = annual_salary/12;
    for i in range(0,36):
        current_savings=(current_savings+current_savings*r/12
                         +portion_saved*monthly_salary)
        if (i%6==5):
            monthly_salary = monthly_salary+monthly_salary*semi_annual_raise
    return (round(current_savings, 2))

lbound = 0
rbound = 10000
saving_r = 0
n_steps = 0
threshold = portion_down_payment*total_cost
#print("variables defined")

max_amt = amt_saved(rbound)
#print(max_amt)
#print(threshold)
#print("max amt defined")
if (max_amt<threshold and abs(threshold-max_amt)>100):
    print("It is not possible to pay the down payment in three years")
else:
    #print("starting search")
    while (lbound<=rbound):
        mid = (lbound+rbound)//2
        #print("low: "+str(lbound)+" mid: "+str(mid)+" hi: "+str(rbound))
        money = amt_saved(mid)
        #print(money)
        n_steps = n_steps+1
        if (abs(threshold-money)<100):
            #print("it's a match!")
            saving_r = mid
            break
        elif (money<threshold):
            #print("raising low")
            lbound = mid
        elif (money>threshold):
            #print("lowering high")
            rbound = mid

    saving_r = round(saving_r/10000., 4)
    print("Best savings rate: "+str(saving_r))
    print("Steps in bisection search: "+str(n_steps))



