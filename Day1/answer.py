import pandas as pd
from math import floor

def fuel_required(x):
    return floor(x/3)-2

def fuel_mass(mass):
    total_fuel = 0
    fuel = fuel_required(mass)
    while fuel > 0:
        total_fuel += fuel
        fuel = fuel_required(fuel)
    return total_fuel


if __name__=='__main__':
    df = pd.read_csv("input.csv")
    print(fuel_mass(100756))

    print(df['mass'].apply(lambda x: fuel_mass(x)).sum())
