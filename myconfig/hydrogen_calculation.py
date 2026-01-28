from .config import awe_data, awe_adv_data, pemwe_data, pemwe_adv_data, equipment_data
import numpy as np

from .general_calculation import capex_calculation, annual_cost_calculation

###############################
## Green hydrogen production ##
###############################

# capex (stack, electronics, purification, heat management, compression, contingency)

def electrolysis_cost(data, production_scale): # production_scale: [MW]
    pr = production_scale
    prm_stack = data.Stack_capex
    prm_elec = data.Electronics
    prm_puri = data.Purification
    prm_heat = data.Heat_management
    prm_comp = data.Compression
    prm_cont = data.Contingency

    prms = [prm_stack, prm_elec, prm_puri, prm_heat, prm_comp, prm_cont]
    capex_list = [capex_calculation(prm, pr) for prm in prms]
    capex_total = sum(capex_list)
    return capex_total

def awe_capex(production_scale): # production_scale: [MW]
    data = awe_data
    capex = electrolysis_cost(data, production_scale) * 1e-6 # [million USD]
    return capex # [million USD]

def pemwe_capex(production_scale): # production_scale: [MW]
    data = pemwe_data
    capex = electrolysis_cost(data, production_scale) * 1e-6 # [million USD]
    return capex # [million USD]

def awe_adv_capex(production_scale): # production_scale: [MW]
    data = awe_adv_data
    capex = electrolysis_cost(data, production_scale) * 1e-6 # [million USD]
    return capex # [million USD]

def pemwe_adv_capex(production_scale): # production_scale: [MW]
    data = pemwe_adv_data
    capex = electrolysis_cost(data, production_scale) * 1e-6 # [million USD]
    return capex # [million USD]

# infra cost

def water_pump_requirement(production_scale, electricity_use=50, eta=0.99): # hydrogen production scale [MW], electricity_use: 50 [kWh / kg-H2], eta: Faraday efficiency: 0.99 [-]
    ps = production_scale # [MW]
    eu = electricity_use # [kWh / kg-H2]
    hydrogen_production = ps / (eu / eta) # [kg-H2 / h]
    water_requirement = hydrogen_production * (18 / 2) # [kg-water / h]
    return water_requirement # [kg-water / h]

def water_pump_capex(production_scale, electricity_use=50, eta=0.99): # hydrogen production scale [MW], electricity_use: 50 [kWh / kg-H2], eta: Faraday efficiency: 0.99 [-]
    water_requirement = water_pump_requirement(production_scale, electricity_use, eta)
    
    prm = equipment_data.Pump
    capex = capex_calculation(prm, production_scale) * 1e-6 # [million USD]
    return capex # [million USD]

def grid_requirement():
    return True

def grid_capex():
    return True

def grid_opex():
    return True

def grid_annual_cost():
    return True