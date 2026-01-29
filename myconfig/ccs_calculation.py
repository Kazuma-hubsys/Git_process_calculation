from .config import plant_data, cc_data, cc_opex_data, commodity_data, ppi_us_dict
import numpy as np
from .general_calculation import capex_calculation, annual_cost_calculation, installation_cost
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

# CO2 transport (compression & piping) # from global CCS, Advancements in CCS Technologies and Costs, 2025

def co2_compression_capex(capturing_rate, N_train=1): # [Mt-CO2-captured / y]
    Mt = capturing_rate * 1e9 / (plant_data.Plant_operation_time.Value * 3600) # CO2 flow rate [kg /s]
    P_cut_off = 73.8 # compressor outlet pressure [bar]
    P_initial = 1.0 # compressor inlet pressure [bar]
    PPI_US_2005 = ppi_us_dict[2005]
    PPI_US_2023 = ppi_us_dict[2023]
    capex = Mt * N_train * (0.13 * 1e6 * (Mt ** (-0.71)) + 1.40 * 1e6 * (Mt ** (-0.60)) * np.log(P_cut_off / P_initial)) * (PPI_US_2023 / PPI_US_2005) * 1e-6 # [million USD]
    return capex # [million USD]

def co2_pump_capex(capturing_rate): # [Mt-CO2-captured / y]
    Wp = capturing_rate * 1e6 / (plant_data.Plant_operation_time.Value * 24) # [t/d]
    capex = 1.11 * 1e6 * (Wp / 1000) * 7e4 * (ppi_us_dict[2023] / ppi_us_dict[2005]) * 1e-6 # [million USD]
    return capex # [million USD]

def co2_compression_opex(capturing_rate): # [Mt-CO2-captured / y]

def ccs_transport_capex(capturing_rate):


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
    Q = capturing_rate *1e9 / (plant_data.Plant_operation_time.Value * 3600) # [kg-CO2 / s]
    pipe_capex = dist_pipe_capex(Q, L) # [million USD]
    pipe_opex = dist_pipe_opex(Q, L) # [million USD / y]
    pipe_cost = dist_pipe_cost(Q, L)  # [million USD / y]

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
