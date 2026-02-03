from .config import awe_data, awe_adv_data, pemwe_data, pemwe_adv_data, equipment_cost_data, awe_opex_data, pemwe_opex_data, plant_data, commodity_data, awe_spec_data, pemwe_spec_data
import numpy as np

from .general_calculation import capex_calculation, crf_calculation

###############################
## Green hydrogen production ##
###############################

# capex (stack, electronics, purification, heat management, compression, contingency)

def electrolysis_capex(data, production_scale): # production_scale: [MW]
    pr = production_scale
    prm_stack = data.Stack_capex
    prm_elec = data.Electronics
    prm_puri = data.Purification
    prm_heat = data.Heat_management
    prm_comp = data.Compression
    prm_cont = data.Contingency

    prms = [prm_stack, prm_elec, prm_puri, prm_heat, prm_comp, prm_cont]
    capex_list = [capex_calculation(prm, pr) * 1e-6 for prm in prms] # [million USD]
    return capex_list # [million USD] # [stack, electronics, heat management, compression, contingency]

def awe_capex(production_scale): # production_scale: [MW]
    data = awe_data
    capex_list = electrolysis_capex(data, production_scale) # [million USD]
    return capex_list # [million USD] # [stack, electronics, heat management, compression, contingency]

def pemwe_capex(production_scale): # production_scale: [MW]
    data = pemwe_data
    capex_list = electrolysis_capex(data, production_scale) # [million USD]
    return capex_list # [million USD] # [stack, electronics, heat management, compression, contingency]

def awe_adv_capex(production_scale): # production_scale: [MW]
    data = awe_adv_data
    capex_list = electrolysis_capex(data, production_scale) # [million USD]
    return capex_list # [million USD] # [stack, electronics, heat management, compression, contingency]

def pemwe_adv_capex(production_scale): # production_scale: [MW]
    data = pemwe_adv_data
    capex_list = electrolysis_capex(data, production_scale) # [million USD]
    return capex_list # [million USD] # [stack, electronics, heat management, compression, contingency]

def electrolizer_opex(production_scale, opex_data, spec_data): # [MW]
    pr = production_scale * 1e3 / spec_data.Energy_consumption.Value * plant_data.Plant_operation_time.Value # [kg-H2 / yr]
    electricity_cost = pr * spec_data.Energy_consumption.Value * commodity_data.Electricity.Value * 1e-6 # [milion USD / yr]
    steam_cost = pr * opex_data.Steam.Value * commodity_data.Steam.Value * 1e-6 # [million USD / yr]
    cooling_cost = pr * opex_data.Cooling_water.Value * commodity_data.Cooling_water.Value * 1e-6 # [million USD / yr]
    refg_cost = pr * opex_data.Refrigerant.Value * commodity_data.Refregerant.Value * 1e-6 # million USD / yr]
    pump_cost = pr * opex_data.Pump.Value * commodity_data.Electricity.Value * 1e-6 # [million USD / yr]
    compressor_cost = pr * opex_data.Compression.Value * commodity_data.Electricity.Value * 1e-6 # [million USD / yr]
    raw_water_cost = pr * opex_data.Water.Value * 1e-3 * commodity_data.Water.Value * 1e-6 # [million USD]
    opex_list = [electricity_cost, steam_cost, cooling_cost, refg_cost, pump_cost, compressor_cost, raw_water_cost] # [million USD / yr]
    return opex_list # [million USD / yr] # [electricity, steam, cooling_water, refgerant, pump, compression, raw material water]

def awe_opex(production_scale): #[MW]
    spec_data = awe_spec_data
    opex_data = awe_opex_data
    opex_list = electrolizer_opex(production_scale, opex_data, spec_data)
    return opex_list # [million USD / yr] # [electricity, steam, cooling_water, refgerant, pump, compression, raw material water]

def pemwe_opex(production_scale): # [MW]
    spec_data = pemwe_spec_data
    opex_data = pemwe_opex_data
    opex_list = electrolizer_opex(production_scale, opex_data, spec_data)
    return opex_list # [million USD / yr] # [electricity, steam, cooling_water, refgerant, pump, compression, raw material water]

def electrolysis_cost(capex_list, opex_list, spec_data, discount_rate=plant_data.Discount_rate.Value):
    stack_capex = sum(capex_list[0])
    stack_lifetime = spec_data.Stack_lifetime.Value # [yr]
    stack_crf = crf_calculation(discount_rate, stack_lifetime)

    bop_capex = sum(capex_list[1:])
    bop_lifetime = spec_data.System_lifetime.Value # [yr]
    bop_crf = crf_calculation(discount_rate, bop_lifetime)

    annual_cost = stack_capex * stack_crf + bop_capex * bop_crf + sum(opex_list)
    return annual_cost # [million USD / yr]

def awe_cost(production_scale, discount_rate=plant_data.Discount_rate.Value): # [MW]
    capex_list = awe_capex(production_scale)
    opex_list = awe_opex(production_scale)
    spec_data = awe_spec_data
    annual_cost = electrolysis_cost(capex_list, opex_list, spec_data, discount_rate)
    return annual_cost # [million USD / yr]

def pemwe_cost(production_scale, discount_rate=plant_data.Discount_rate.Value): # [MW]
    capex_list = pemwe_capex(production_scale)
    opex_list = pemwe_opex(production_scale)
    spec_data = pemwe_spec_data
    annual_cost = electrolysis_cost(capex_list, opex_list, spec_data, discount_rate)
    return annual_cost # [million USD / yr]

# LCOH

def LCOH_awe(production_scale): # production scale: [MW], annual cost : [million USD / yr]
    production_rate = production_scale * 1e3 / awe_spec_data.Energy_consumption.Value * plant_data.Plant_operation_time.Value # [kg-H2 / yr]
    cost = awe_cost(production_scale) * 1e6 # [USD / yr]
    lcoh = cost / production_rate # [USD / kg-H2]
    return lcoh

def LCOH_pemwe(production_scale): # production scale: [MW], annual cost : [million USD / yr]
    production_rate = production_scale * 1e3 / pemwe_spec_data.Energy_consumption.Value * plant_data.Plant_operation_time.Value # [kg-H2 / yr]
    cost = pemwe_cost(production_scale) * 1e6 # [USD / yr]
    lcoh = cost / production_rate # [USD / kg-H2]
    return lcoh

def CAPEX_per_kW_awe(production_scale): # [MW]
    capex = sum(awe_capex(production_scale)) * 1e6 # [USD]
    pr = production_scale * 1e3 # [kW]
    return capex / pr # [USD / kW]

def CAPEX_per_kW_pemwe(production_scale): # [MW]
    capex = sum(pemwe_capex(production_scale)) * 1e6 # [USD]
    pr = production_scale * 1e3 # [kW]
    return capex / pr # [USD / kW]

def OPEX_per_kW_pemwe(production_scale): # [MW]
    capex = sum(pemwe_opex(production_scale)) * 1e6 # [USD]
    pr = production_scale * 1e3 # [kW]
    return capex / pr # [USD / kW]


# infra cost

def water_pump_requirement(production_scale, electricity_use=50, eta=0.99): # hydrogen production scale [MW], electricity_use: 50 [kWh / kg-H2], eta: Faraday efficiency: 0.99 [-]
    ps = production_scale # [MW]
    eu = electricity_use # [kWh / kg-H2]
    hydrogen_production = ps / (eu / eta) # [kg-H2 / h]
    water_requirement = hydrogen_production * (18 / 2) # [kg-water / h]
    return water_requirement # [kg-water / h]

def water_pump_capex(production_scale, electricity_use=50, eta=0.99): # hydrogen production scale [MW], electricity_use: 50 [kWh / kg-H2], eta: Faraday efficiency: 0.99 [-]
    water_requirement = water_pump_requirement(production_scale, electricity_use, eta)
    
    prm = equipment_cost_data.Pump
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