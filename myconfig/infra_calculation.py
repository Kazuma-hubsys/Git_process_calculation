from .config import commodity_data, pipe_data, truck_data
import numpy as np
from .general_calculation import annual_cost_calculation


###################
## Pipeline cost ##
###################

def pipe_diameter(capacity, rho=1.977, vel=15): # capacity [kg/s], rho [kg/m^3] = density of CO2 in standard state, vel [m/s]
    diameter_square = capacity / rho / vel / np.pi * 4
    diameter = np.sqrt(diameter_square) # [m]
    return diameter

# pipeline for distribution (without recompression)

def dist_pipe_capex(capacity, L): # capacity [kg/s], L: pipeline length [km]
    d = pipe_diameter(capacity) # [m]
    capex_dist_pipe = 1.5e6 * d ** 2 + 860500 * d + 247500 # [€_2010 / km]
    EURO_TO_USD_2010 = 1.33 #[USD / Euro in 2010]
    INTEREST_RATE_2010_2020 = 1.187 #[%] 
    capex_dist_pipe_2020_USD = capex_dist_pipe * EURO_TO_USD_2010 * ((100 + INTEREST_RATE_2010_2020) / 100)
    capex = capex_dist_pipe_2020_USD * L * 1e-6 # [million USD]
    return capex # [million USD]

def dist_pipe_opex(capacity, L): # [USD_2020 / km] # capacity [kg/s], L: pipeline length [km]
    pipe_unit_opex = pipe_data.OPEX.Value # [USD / km / y]
    opex = pipe_unit_opex * L * 1e-6 # [million USD / y]
    return opex

def dist_pipe_cost(capacity, L):
    capex = dist_pipe_capex(capacity, L)
    opex = dist_pipe_opex(capacity, L)
    lifetime = pipe_data.Lifetime.Value # [y]
    discount_rate = pipe_data.Discount_rate.Value # [-]
    annual_cost = annual_cost_calculation(capex, opex, lifetime=lifetime, discount_rate=discount_rate)
    return annual_cost

# pipeline cost for transmission (with recompression)

def trans_pipe_capex(capacity, L): # capacity [kg/s] # L: pipeline length [km]
    d = pipe_diameter(capacity) # [m]
    capex_trans_pipe = 2.2e6 * d ** 2 + 860500 * d + 247500 # [€_2010 / km]
    EURO_TO_USD_2010 = 1.33 #[USD / Euro in 2010]
    INTEREST_RATE_2010_2020 = 1.187 #[%] 
    capex_trans_pipe_2020_USD = capex_trans_pipe * EURO_TO_USD_2010 * ((100 + INTEREST_RATE_2010_2020) / 100)
    capex = capex_trans_pipe_2020_USD * L * 1e-6 # [million USD]
    return capex # [million USD]

def trans_pipe_opex(capacity, L): # [USD_2020 / km] # capacity [kg/s], L: pipeline length [km]
    pipe_unit_opex = pipe_data.OPEX.Value # [USD / km / y]
    opex = pipe_unit_opex * L * 1e-6 # [million USD / y]
    return opex

def trans_pipe_cost(capacity, L):
    capex = trans_pipe_capex(capacity, L)
    opex = trans_pipe_opex(capacity, L)
    lifetime = pipe_data.Lifetime.Value # [y]
    discount_rate = pipe_data.Discount_rate.Value # [-]
    annual_cost = annual_cost_calculation(capex, opex, lifetime=lifetime, discount_rate=discount_rate)
    return annual_cost

################
## Truck cost ##
################

def truck_capex(N): # number of truck [-]
    capex = truck_data.CAPEX.Value * N * 1e-6 # [million USD]
    return capex

def truck_opex(L, driving_velocity=truck_data.Average_speed.Value): # L: total driving distance [km / y], driving_velocity: [km / h]
    driving_time = L / driving_velocity   # [h / y]
    labor = commodity_data.Labor.Value * driving_time * 1e-6   # [million USD / y]
    fuel = L * truck_data.Cf.Value * commodity_data.Fuel.Value * 1e-6   # [million USD / y]
    opex = labor + fuel # [million USD / y]
    return opex # [million USD / y]

