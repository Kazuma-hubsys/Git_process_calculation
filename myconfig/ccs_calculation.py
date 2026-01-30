from .config import plant_data, cc_data, cc_opex_data, commodity_data, ppi_us_dict, cc_comp_data
import numpy as np
from .general_calculation import capex_calculation, annual_cost_calculation, installation_cost, other_operation_cost
from .infra_calculation import dist_pipe_capex, dist_pipe_opex, dist_pipe_cost

#########
## CCS ##
#########

# capture
def co2_capture_capex(capturing_rate, tec="MEA"): # capturing rate: [Mt-CO2-captured / y, tec: MEA, MDEA etc.
    if tec == "MEA":
        prm = cc_data.MEA # [million USD] 
    elif tec == "MDEA":
        prm = cc_data.MDEA
    capex_cc = capex_calculation(prm, capturing_rate)
    return capex_cc # [million USD]

def co2_capture_opex(capturing_rate): # capturing rate: [Mt-CO2-captured / y]
    cr = capturing_rate * 1e9 # [kg-CO2 captured / y]
    electricity_cost = cc_opex_data.Electricity.Value * cr * commodity_data.Electricity.Value # [USD / y]
    water_cost = cc_opex_data.Water.Value * cr * (commodity_data.Water.Value * 1e-3) # [USD/y]
    mea_regene_cost = cc_opex_data.MEA_regeneration.Value * cr * commodity_data.Heat.Value # [USD / y]
    mea_makeup_consumed = cc_opex_data.MEA_makeup_consumption.Value * (cr * 1e-3) # [kg-MEA / y]
    mea_makeup_cost = mea_makeup_consumed * cc_opex_data.MEA_makeup_cost.Value # [USD / y]

    opex_cc = [electricity_cost, water_cost, mea_regene_cost, mea_makeup_cost] # [USD / y]
    opex_cc_list = [cost * 1e-6 for cost in opex_cc] # [million USD / y]
    return opex_cc_list # [million USD / y]

def co2_capture_cost(capturing_rate): # capturing rate: [Mt-CO2-captured / y]
    cr = capturing_rate # capturing rate: [Mt-CO2-captured / y]
    capex = co2_capture_capex(cr)  # [million USD]
    opex = sum(co2_capture_opex(cr))  # [million USD / y]
    annual_cost = annual_cost_calculation(capex, opex) # [million USD / y]
    return annual_cost # [million USD / y]

def ccs_cost_check(capturing_rate): # capturing rate: [Mt-CO2-captured / y]
    cr = capturing_rate # capturing rate: [Mt-CO2-captured / y]
    annual_cost = co2_capture_cost(cr)  # [million USD / y]
    cost_of_co2_captured = (annual_cost * 1e6) / (cr * 1e6) # [USD / t-captured]
    return cost_of_co2_captured # [USD / t-captured]

# CO2 transport (compression & piping) # by global CCS, Advancements in CCS Technologies and Costs, 2025

def co2_compression_capex(capturing_rate, N_train=1): # [Mt-CO2-captured / y]
    Mt = capturing_rate * 1e9 / (plant_data.Plant_operation_time.Value * 3600) # CO2 flow rate [kg /s]
    P_cut_off = 73.8 # compressor outlet pressure [bar]
    P_initial = 1.0 # compressor inlet pressure [bar]
    PPI_US_2005 = ppi_us_dict[2005]
    PPI_US_2023 = ppi_us_dict[2023]
    capex = Mt * N_train * (0.13 * 1e6 * (Mt ** (-0.71)) + 1.40 * 1e6 * (Mt ** (-0.60)) * np.log(P_cut_off / P_initial)) * (PPI_US_2023 / PPI_US_2005) * 1e-6 # [million USD]
    return capex # [million USD]

def co2_compression_power(capturing_rate, i): # capturing_rate: [Mt-CO2-captured / y] i: number of stage
    m = capturing_rate * 1e6 / (plant_data.Plant_operation_time.Value / 24) # [t/d]
    R = 8.314 # universal gas constant [kJ / kmol / K]
    T_in = 308.15 # temperature of CO2 at stage inlet [K] (35℃)
    M = 44.01 # molecular weight of CO2 [kg / kmol]
    eta = 0.75 # isentropic efficiency of each stage [-]
    CR = (73.8 / 1) ** (1 / 8) # compression ratio

    if i == 1:
        prm = cc_comp_data.S1
    elif i == 2:
        prm = cc_comp_data.S2
    elif i == 3:
        prm = cc_comp_data.S3
    elif i == 4:
        prm = cc_comp_data.S4
    elif i == 5:
        prm = cc_comp_data.S5
    elif i == 6:
        prm = cc_comp_data.S6
    elif i == 7:
        prm = cc_comp_data.S7
    elif i == 8:
        prm = cc_comp_data.S8
    else:
        raise ValueError("Number of stage is fixed (from 1 to 8). Please check the range of number of stages.")
    
    zs = prm.Zs
    ks = prm.Ks
    p_in = prm.P_inlet
    p_out = prm.P_outlet

    Ws = (1000 / (24 * 3600)) * (m * zs * R * T_in / (M * eta)) * (ks / (ks - 1)) * (CR ** ((ks - 1) / ks) - 1) # shaft work (energy) for stage i [kW]
    return Ws # [kW]

def co2_compression_opex(capturing_rate, N_train=1): # [Mt-CO2-captured / y]
    cr = capturing_rate # [Mt-CO2-captured / y]
    Ws_list = [co2_compression_power(cr, i) for i in range(1, 9)] # [kW]
    electricity_cost = sum([Ws * 3600 * plant_data.Plant_operation_time.Value * commodity_data.Electricity.Value * 1e-6 for Ws in Ws_list]) # [million USD / y]
    other_opex_list  = other_operation_cost(co2_compression_capex(cr, N_train)) # [maintenance_cost, insurance_cost, taxes] # [million USD / y]
    opex_list = [electricity_cost] + other_opex_list
    return opex_list # [million USD / y] # [electricity, maintenance_cost, insurance_cost, taxes]

def co2_pump_power(capturing_rate): # [Mt-CO2-captured / y]
    m = capturing_rate * 1e6 / (plant_data.Plant_operation_time.Value / 24) # [t/d]
    P_final = 150 * 0.1013 # pump outlet pressure [MPa]
    P_cut_off = 73.8 * 0.1013 # pump inlet pressure [MPa] = critical pressure of CO2
    eta = 0.75 # pump efficiency [-]
    rho = 630 # CO2 density [kg/m^3]
    Wp = (1000 * 10) / (24 * 36) * (m * (P_final - P_cut_off) / (rho * eta)) # pump power [kW]
    return Wp # [kW]

def co2_pump_capex(capturing_rate): # [Mt-CO2-captured / y]
    Wp = co2_pump_power(capturing_rate) # [kW]
    capex = (1110000 * (Wp / 1000) + 70000) * (ppi_us_dict[2023] / ppi_us_dict[2005]) * 1e-6 # [million USD]
    return capex # [million USD]

def co2_pump_opex(capturing_rate): # [Mt-CO2-captured / y]                             
    cr = capturing_rate # [Mt-CO2-captured / y]
    Wp = co2_pump_power(cr)
    electricity_cost = Wp * 3600 * plant_data.Plant_operation_time.Value * commodity_data.Electricity.Value * 1e-6 # [million USD / y]
    other_opex_list  = other_operation_cost(co2_pump_capex(cr)) # [maintenance_cost, insurance_cost, taxes] # [million USD / y]
    opex_list = [electricity_cost] + other_opex_list
    return opex_list # [million USD / y] # [electricity, maintenance_cost, insurance_cost, taxes]

def ccs_transport_capex(capturing_rate, L):
    Q = capturing_rate *1e9 / (plant_data.Plant_operation_time.Value * 3600) # [kg-CO2 / s]
    pipe_capex = dist_pipe_capex(Q, L) # [million USD]
    return pipe_capex # [million USD]

def ccs_transport_opex(capturing_rate, L):
    Q = capturing_rate *1e9 / (plant_data.Plant_operation_time.Value * 3600) # [kg-CO2 / s]
    pipe_opex = dist_pipe_opex(Q, L) # [million USD / y]
    return pipe_opex # [million USD]

def ccs_transport_cost(capturing_rate, L):
    Q = capturing_rate *1e9 / (plant_data.Plant_operation_time.Value * 3600) # [kg-CO2 / s]
    pipe_cost = dist_pipe_cost(Q, L)  # [million USD / y]
    return pipe_cost

# storage
def co2_storage_capex(capturing_rate):
    return True

def co2_storage_opex(capturing_rate):
    return True

def co2_storage_cost(capturing_rate):
    return True

def ccs_total_cost(capturing_rate, L): # capturing_rate: [Mt-CO2-captured / y], L: transportation distance [km]
    # capture
    cr = capturing_rate # [Mt-CO2-captured / y]
    capture_capex = co2_capture_capex(cr) # [million USD]
    capture_opex_list = co2_capture_opex(cr) # [million USD / y]
    capture_cost = co2_capture_cost(cr) # [million USD / y]

    #pipeline
    pipe_capex = ccs_transport_capex(capturing_rate, L) # [million USD]
    pipe_opex = ccs_transport_capex(capturing_rate, L) # [million USD / y]
    pipe_cost = ccs_transport_cost(capturing_rate, L)  # [million USD / y]

    #storage
    storage_capex = 0 
    storage_opex = 0
    storage_cost = 0

    # total
    total_capex = capture_capex + pipe_capex + storage_capex
    total_opex = sum(capture_opex_list) + pipe_opex + storage_opex
    total_cost = capture_cost + pipe_cost + storage_cost
    ccs_cost_list = [total_capex, total_opex, total_cost]
    return ccs_cost_list