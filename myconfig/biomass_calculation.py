from .config import bio_infra_assump_data, bio_gather_cost_data, bio_capex_data, bio_hydrogen_requirement_data, truck_data, wood_property_data, maize_property_data, common_process_cost_data
import numpy as np
from .general_calculation import annual_cost_calculation, capex_calculation
from .infra_calculation import truck_capex, truck_opex

#############################
## Biomass gathering infra ##
#############################

# biomass gathering

def bio_gather_capex(biomass_amount): # biomass収穫量 [t / y] # 農具はscalingしないとする
    S = biomass_amount  # [t / y]
    attachment = bio_gather_cost_data.Attachment_depreciation.Value # [USD / t]
    annual_capex = attachment * S * 1e-6 # [million USD / y]
    return annual_capex # [million USD / y]

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

def bio_trans_capex(biomass_amount): # [t / yr]
    infra_list = bio_trans_infra(biomass_amount) # L, D, S, E, Ews, F, N
    N = infra_list[6]
    capex = truck_capex(N) # [million USD]
    return capex

def bio_trans_opex(biomass_amount): # [t / yr]
    infra_list = bio_trans_infra(biomass_amount) # L, D, S, E, Ews, F, N
    S = infra_list[2]
    driving_velocity = bio_infra_assump_data.VT.Value
    opex = truck_opex(S, driving_velocity) # [million USD / y]
    return opex # [million USD / yr]

def bio_trans_cost(biomass_amount, r=bio_infra_assump_data.r.Value): # L, D, S, E, Ews, F, N
    data_list = bio_trans_infra(biomass_amount, r)
    capex = bio_trans_capex(biomass_amount)
    opex = bio_trans_opex(biomass_amount)
    discount_rate=truck_data.Discount_rate.Value
    lifetime=truck_data.Lifetime.Value
    annual_cost = annual_cost_calculation(capex, opex, discount_rate=discount_rate, lifetime=lifetime) # [million USD / y]
    return annual_cost # [million USD / y]

# processing
"""
preprocessing: 最適化論文からとっているが、数値に関して論文内ではオーダー程度でしか精度を保証しないため、もっといい論文が見つかったら返る
"""
def bio_preprocess_capex(biomass_processing_capacity): # Bowling 2011 # [t-biomass / yr] # 参考値に過ぎない
    x = biomass_processing_capacity
    # ベクトル化された条件分岐
    conditions = [
        (x >= 0) & (x < 40000),
        (x >= 40000) & (x < 200000),
        (x >= 200000) & (x < 240000),
        (x >= 240000) & (x < 400000),
        (x >= 400000) & (x < 440000), 
        (x >= 440000) & (x < 600000), 
        (x >= 600000) & (x < 640000), 
        (x >= 640000)
    ]
    choices = [
        (20 * x + 200000) * 1e-6,
        (5 * x + 800000) * 1e-6,
        (20 * x - 2200000) * 1e-6,
        (5 * x + 1400000) * 1e-6,
        (20 * x - 4600000) * 1e-6,
        (5 * x + 2000000) * 1e-6,
        (20 * x - 7000000) * 1e-6,
        (5 * x + 2600000) * 1e-6
    ]

    capex = np.select(conditions, choices) # CAPEX of preprocessing unit # [million USD]
    # スカラー入力の場合はPythonのfloatを返す
    if np.isscalar(x):
        capex = float(capex)
    return capex

def bio_preprocess_opex(biomass_processing_capacity): # Bowling 2011 # [t-biomass / yr] # 参考値に過ぎない
    opex = (111 + 93) / 2 * biomass_processing_capacity * 1e-6 # [million USD / yr]
    return opex # [million USD / yr]

def bio_preprocess_cost(biomass_processing_capacity): # Bowling 2011 # [t-biomass / yr]
    bpc = biomass_processing_capacity
    capex = bio_preprocess_capex(bpc) # [million USD]
    opex = bio_preprocess_opex(bpc) # [million USD / yr]
    annual_cost = annual_cost_calculation(capex, opex)
    return annual_cost # [million USD / yr]

# biomass gasification to hydrogen

def bio_hydrogen_requirement(hydrogen_production_rate, type): # hydrogen production rate: [kt-H2 / y], biomass type: (wood / maize / ...)
    req_data = bio_hydrogen_requirement_data
    if type == "wood":
        req = req_data.Wood.Value * hydrogen_production_rate * 1e3 # [t-(wet wood chips) / y]
    elif type == "maize":
        req = req_data.Maize_silage.Value * hydrogen_production_rate * 1e3 # [t-(wet maize silage) / y]
    else:
        raise ValueError("Biomass type does not exist. Type \"wood\" is used instead.")
    return req # [t-biomass / yr]

def bio_kj_conversion(biomass_throughput, type): # [t-biomass / yr]
    bt = biomass_throughput
    if type == "wood":
        req_kj = bt * 1e-3 * wood_property_data.LHV.Value * 1e6 * 1e-9 # [PJ-(wet wood chips) / y]
    elif type == "maize":
        req_kj = bt * 1e-3 * maize_property_data.LHV.Value * 1e6 * 1e-9 # [PJ-(wet maize silage) / y]
    else:
        raise ValueError("Biomass type does not exist. Type \"wood\" is used instead.")
    return req_kj # [PJ-biomass / yr]

def bio_gasif_capex(hydrogen_production_rate, biomass_type="wood"): # [kt-H2 / y]
    pr = hydrogen_production_rate # [kt-H2 / y]
    req_kj = bio_kj_conversion(bio_hydrogen_requirement(pr, biomass_type), biomass_type)
    capex_gasif = capex_calculation(bio_capex_data.Gasifier, req_kj)
    capex_wgs = capex_calculation(common_process_cost_data.WGS, pr)
    capex_psa = capex_calculation(common_process_cost_data.PSA, pr)
    capex = sum([capex_gasif, capex_wgs, capex_psa]) # [million USD]
    return capex # [million USD]

def bio_gasif_opex(hydrogen_production_rate): # [kt-H2 / yr]
    return 0

def bio_gasif_cost(hydrogen_production_rate): # [kt-H2 / yr]
    return 0

def bio_hydrogen_total_cost(hydrogen_production_rate, biomass_type="wood"): # [kt-H2 / yr]
    hpr = hydrogen_production_rate * 1e3 # [t-H2 / yr]
    biomass_req = bio_hydrogen_requirement(hpr*1e-3, biomass_type) # [t-biomass / yr]

    gather_capex = bio_gather_capex(biomass_req) * 10 # [million USD] # depreciationを10年で設定
    gather_opex = sum(bio_gather_opex(biomass_req)) # [million USD / yr]
    gather_cost = bio_gather_cost(biomass_req) # [million USD / yr]

    trans_capex = bio_trans_capex(biomass_req) # [million USD]
    trans_opex = bio_trans_opex(biomass_req) # [million USD / yr]
    trans_cost = bio_trans_cost(biomass_req) # [million USD / yr]

    preprocess_capex = bio_preprocess_capex(biomass_req) # [million USD]
    preprocess_opex = bio_preprocess_opex(biomass_req) # [million USD / yr]
    preprocess_cost = bio_preprocess_cost(biomass_req) # [million USD / yr]

    gasif_capex = bio_gasif_capex(hydrogen_production_rate, biomass_type) # [million USD]
    gasif_opex = bio_gasif_opex(hydrogen_production_rate) # [million USD / yr]
    gasif_cost = bio_gasif_cost(hydrogen_production_rate) # [million USD / yr]

    capex_list = [gather_capex, trans_capex, preprocess_capex, gasif_capex]
    opex_list = [gather_opex, trans_opex, preprocess_opex, gasif_opex]
    total_list = [gather_cost, trans_cost, preprocess_cost, gasif_cost]
    label_list = ["gaterinng", "transport", "preprocessing", "gasification"]
    return [capex_list, opex_list, total_list, label_list]

def bio_price_check(biomass_amount, raw_biomass_price=0): # biomass amount: [t-biomass / yr], raw biomass price: [USD / kg]
    ba = biomass_amount # [t / yr]
    gather_cost = bio_gather_cost(ba) # [million USD / yr]
    trans_cost = bio_trans_cost(ba) # [million USD / yr]
    preprocess_cost = bio_preprocess_cost(ba) # [million USD / yr]

    total_cost = gather_cost + trans_cost + preprocess_cost # [million USD / yr]
    cost_after_agriculture = total_cost * 1e6 / (ba * 1e3) # [USD / kg-biomass]
    biomass_price = raw_biomass_price + cost_after_agriculture # [USD / kg]
    biomass_price_list = [raw_biomass_price] + [cost * 1e6 / (ba * 1e3) for cost in [gather_cost, trans_cost, preprocess_cost]]
    label_list = ["raw biomass price", "gathering", "transport", "preprocessing"]
    return [biomass_price_list, label_list]