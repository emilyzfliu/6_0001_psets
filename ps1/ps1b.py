#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:59:05 2020

@author: Foofoo
"""

annual_salary = int(input("Annual Salary: "))
portion_saved = float(input("Portion Saved: "))
total_cost = int(input("Total Cost: "))
semi_annual_raise = float(input("Semi-annual raise: "))

monthly_salary = annual_salary/12
current_savings = 0
r = 0.04
portion_down_payment = 0.25

threshold = portion_down_payment*total_cost

n_months=0

while (current_savings<threshold):
    current_savings=(current_savings+portion_saved*monthly_salary+
                             current_savings*r/12)
    n_months = n_months+1
    if (n_months%6==0):
        monthly_salary = monthly_salary+monthly_salary*semi_annual_raise

print("Number of months: "+str(n_months))