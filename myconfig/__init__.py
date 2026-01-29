"""
init.py
"""

# general
from .general_calculation import installation_cost, annual_cost_calculation
general_list = ["installation_cost", "annual_cost_calculation"]

# infra cost
from .infra_calculation import dist_pipe_capex, trans_pipe_capex, truck_capex, truck_opex
infra_list = ["dist_pipe_capex", "trans_pipe_capex", "truck_capex", "truck_opex"]

# process cost
# from .cost_calculation import steel_capex_bau, steel_capex_dri_eaf, steel_capex_ccs, steel_opex_ccs, steel_annual_ccs
from .process_steel import steel_capex_bau, steel_capex_dri_eaf, steel_capex_ccs, steel_opex_ccs, steel_annual_ccs
process_list = ["steel_capex_bau", "steel_capex_dri_eaf", "steel_capex_ccs", "steel_opex_ccs", "steel_annual_ccs"]

# hydrogen
from .hydrogen_calculation import awe_capex, water_pump_capex
hydrogen_list = ["awe_capex", "water_pump_capex"]

# ccs
from .ccs_calculation import co2_capture_capex, co2_capture_opex, co2_capture_cost, ccs_cost_check, ccs_total_cost
ccs_list = ["co2_capture_capex", "co2_capture_opex", "co2_capture_cost", "ccs_cost_check", "ccs_total_cost"]

# biomass
from .biomass_calculation import bio_trans_infra, bio_gather_cost, bio_trans_cost, bio_hydrogen_capex
biomass_list = ["bio_trans_infra", "bio_gather_cost", "bio_trans_cost", "bio_hydrogen_capex"]

# data set
from .config import ccs_data_merged
data_list = ["ccs_data_merged"]

# tool
from .plotter import plot_line, plot_bar, plot_scatter, plot_line_and_scatter
tool_list = ["plot_line", "plot_bar", "plot_scatter", "plot_line_and_scatter"]

cost_calculation_list = general_list + process_list + hydrogen_list + ccs_list + infra_list + biomass_list

__all__ = data_list + cost_calculation_list + tool_list