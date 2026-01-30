from .config import cepci_dict, plant_data
import numpy as np

###############################
## general capex calculation ##
###############################

def capex_calculation(prm, scale):
    C0 = prm.Base_cost # process plant cost (PPC)
    base_scale = prm.Base_scale
    sf = prm.Scaling_factor
    capex = C0 * (scale / base_scale) ** sf
    ref_year_cepci = cepci_dict[2019]
    plant_year_cepci = cepci_dict[prm.Year]

    capex_2019 = capex * ref_year_cepci / plant_year_cepci
    return capex_2019

def installation_cost(equipment_cost):
    PPC = equipment_cost # process plant cost
    TPC = plant_data.Total_plant_cost
    TCR = plant_data.Total_capital_requirement
    installation_cost = PPC * (TPC.Value / 100) * (TCR.Value / 100)
    return installation_cost

def total_capex(installation_cost): # global CCS 2025
    bec = installation_cost # Bare erected cost (process iquipment, installation, supporting facilities, direct and indirect labor cost)
    epc = 0.15 * bec # engineering procurement and ocnstruction
    process_contigency = 0.159 * (bec + epc)
    project_ocntigency = 0.207 * (bec + epc + process_contigency)
    tpc = bec + epc + process_contigency + project_ocntigency # total plant cost
    start_up_cost = sum([]) # OPEX後につくる
    inventory_capital = sum([]) # OPEX後につくる
    financing_capital = 0.027 * tpc
    other_owner_cost = 0.15 * tpc
    owners_cost = start_up_cost + inventory_capital + financing_capital + other_owner_cost
    toc = tpc + owners_cost # total overnight cost
    return toc # capexの最終的な総和

def crf_calculation(discount_rate, lifetime):
    r = discount_rate # [-]
    n = lifetime # [y]
    crf = (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return crf

def annual_cost_calculation(capex, opex, discount_rate=plant_data.Discount_rate.Value, lifetime=plant_data.Plant_lifetime.Value):
    crf = crf_calculation(discount_rate, lifetime)
    annual_cost = capex * crf + opex # [(million) USD / y]
    return annual_cost # [(million) USD / y]

def other_operation_cost(TPC): # total plant cost [million USD]
    maintenance_cost = TPC * plant_data.Maintenance.Value # [million USD]
    insurance_cost = TPC * plant_data.Insurance.Value # [million USD]
    taxes = TPC * plant_data.Taxes.Value # [million USD]
    return [maintenance_cost, insurance_cost, taxes] # [maintenance_cost, insurance_cost, taxes]