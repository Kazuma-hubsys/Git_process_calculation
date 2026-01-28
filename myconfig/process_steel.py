from .config import *
import numpy as np

from .general_calculation import capex_calculation, annual_cost_calculation, installation_cost
from .ccs_calculation import co2_capture_capex, co2_capture_opex, co2_capture_cost, ccs_cost_check

def steel_requirement(production_rate):
    pr = production_rate # [million t/y]
    refined_steel = pr       # [million t/y]
    crude_steel = refined_steel * 0.99 # [million t/y]
    hot_metal = crude_steel * 0.90 # [million t/y]
    iron_ore = crude_steel * 0.005 # [million t/y]
    lime = crude_steel * 0.064 # [million t/y]
    dolomite = crude_steel * 0.011 # [million t/y]
    coke = hot_metal * 0.377 #[million t/y]
    iron_ore_46p_Fe = hot_metal * 0.134 #[million t/y]
    iron_ore_63p_Fe = hot_metal * 0.366 #[million t/y]
    limestone = hot_metal * 0.013 #[million t/y]
    sinter = hot_metal * 1.14 #[million t/y]
    return [sinter, coke, hot_metal, crude_steel, refined_steel]

def steel_capex_bau(production_rate): # [million t/y]
    s, c, hm, cs, rs = steel_requirement(production_rate)

    capex_coking = capex_calculation(steel_data.Coking, c)
    capex_sintering = capex_calculation(steel_data.Sintering, s)
    capex_bf = capex_calculation(steel_data.BF, hm)
    capex_dri = capex_calculation(steel_data.DRI, hm) # 本当はsponge_ironだけど、いったんhot_metalとして計算している
    capex_bof = capex_calculation(steel_data.BOF, cs)    
    capex_eaf = capex_calculation(steel_data.EAF, cs)
    capex_list_bau = [capex_coking, capex_sintering, capex_bf, capex_bof]

    return capex_list_bau

def steel_capex_dri_eaf(production_rate): # [million t/y]
    s, c, hm, cs, rs = steel_requirement(production_rate)

    capex_coking = capex_calculation(steel_data.Coking, c)
    capex_sintering = capex_calculation(steel_data.Sintering, s)
    capex_bf = capex_calculation(steel_data.BF, hm)
    capex_dri = capex_calculation(steel_data.DRI, hm) # 本当はsponge_ironだけど、いったんhot_metalとして計算している
    capex_bof = capex_calculation(steel_data.BOF, cs)    
    capex_eaf = capex_calculation(steel_data.EAF, cs)
    capex_list_dri_eaf = [capex_dri, capex_eaf]

    return capex_list_dri_eaf

###############################
## Steel production with CCS ##
###############################

def steel_capex_ccs(production_rate):
    cr = production_rate * 0.1 * 0.9 # [Mt-CO2-captured / y] # 0.1 kg-CO2-emission / kg-steel, 90% capture を仮置き。この数値は後で必ず修正しなければならない
    capex = co2_capture_capex(cr)
    return capex # [million EURO]

def steel_opex_ccs(production_rate): # [million t/y]
    cr = production_rate * 0.1 * 0.9 # [Mt-CO2-captured / y] # 0.1 kg-CO2-emission / kg-steel, 90% capture を仮置き。この数値は後で必ず修正しなければならない
    opex_list = co2_capture_opex(cr)
    opex = sum(opex_list)
    return opex # [million USD / y] 

def steel_annual_ccs(production_rate): # [million t/y]
    pr = production_rate
    capex = steel_capex_ccs(pr)
    capex = installation_cost(capex)
    opex = steel_opex_ccs(pr)
    annual_cost = annual_cost_calculation(capex, opex)
    return annual_cost # [million USD / y]