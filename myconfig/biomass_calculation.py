from .config import bio_infra_assump_data, bio_gather_cost_data, truck_data
import numpy as np
from .general_calculation import annual_cost_calculation
from .infra_calculation import truck_capex, truck_opex

#############################
## Biomass gathering infra ##
#############################

# biomass gathering

def bio_gather_opex(biomass_amount):  # biomass収穫量 [t / y]
    S = biomass_amount  # [t / y]

    data = bio_gather_cost_data
    labor = data.Labor.Value # [USD / t]
    fuel = data.Fuel.Value # [USD / t]
    equipment = data.Equipment.Value  # [USD / t]
    maintenance = data.Maintenance.Value  # [USD / t]

    gathering_opex_list = [labor * S, fuel * S, equipment * S, maintenance * S]  # [USD / y]
    gathering_opex_list = [opex * 1e-6 for opex in gathering_opex_list] # [million USD / y]
    return gathering_opex_list # [million USD / y]

def bio_gather_capex(biomass_amount): # biomass収穫量 [t / y] # 農具はscalingしないとする
    S = biomass_amount  # [t / y]
    attachment = bio_gather_cost_data.Attachment_depreciation.Value # [USD / t]
    annual_capex = attachment * S * 1e-6 # [million USD / y]
    return annual_capex # [million USD / y]

def bio_gather_cost(biomass_amount): # biomass収穫量 [t / y]
    S = biomass_amount  # [t / y]
    annual_cost = bio_gather_capex(S) + sum(bio_gather_opex(S))
    return annual_cost # [million USD / y]

# biomass trans infra

def bio_trans_infra(biomass_amount, r=bio_infra_assump_data.r.Value): # biomass収集量 [t/y]
    data = bio_infra_assump_data

    Mw = biomass_amount
    Yw = data.Yw.Value # [t / km^2 / y]
    r = r   # [-]
    MT = data.MT.Value # [t (/ truck)]
    Cf = data.Cf.Value # [L-fuel / km]
    VT = data.VT.Value # [km / h]
    Hb = data.Hb.Value # [h]
    Hd = data.Hd.Value # [h / d]
    P = data.P.Value # [d / y]

    L = np.sqrt(Mw / (np.pi * r * Yw)) # 収集圏の半径 [km]
    D = 2 * L / 3   # 平均輸送距離 [km]
    S = 2 * D * Mw / MT # 総輸送距離 [km]
    E = Cf * S  # 輸送の総燃料消費 [L-fuel]
    Ews = Cf * S / Mw   #1t輸送当たりの燃料消費 [L / t-biomass]
    F = Hd / (2 * D / VT + Hb)  # １日の平均輸送回数 [/d]
    N = Mw / (F * MT * P) # トラック台数

    bio_trans_infra_list = [L, D, S, E, Ews, F, N] 

    return bio_trans_infra_list # L, D, S, E, Ews, F, N

def bio_trans_capex(bio_trans_infra_list): # L, D, S, E, Ews, F, N
    N = bio_trans_infra_list[6]
    capex = truck_capex(N) # [million USD]
    return capex

def bio_trans_opex(bio_trans_infra_list): # L, D, S, E, Ews, F, N
    L = bio_trans_infra_list[0]
    driving_velocity = bio_infra_assump_data.VT.Value
    opex = truck_opex(L, driving_velocity) # [million USD / y]
    return opex

def bio_trans_cost(biomass_amount, r=bio_infra_assump_data.r.Value): # L, D, S, E, Ews, F, N
    data_list = bio_trans_infra(biomass_amount, r)
    capex = bio_trans_capex(data_list)
    opex = bio_trans_opex(data_list)
    discount_rate=truck_data.Discount_rate.Value
    lifetime=truck_data.Lifetime.Value
    annual_cost = annual_cost_calculation(capex, opex, discount_rate=discount_rate, lifetime=lifetime) # [million USD / y]
    return annual_cost # [million USD / y]

# processing

def bio_process_capex(biomass_processing_rate): 
    return True

def bio_process_opex(biomass_processing_rate):
    return True

def bio_process_cost(biomass_processing_rate):
    return True

