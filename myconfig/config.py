from pathlib import Path
from .loader import load_csv, load_csv_as_dict, merge_dotdicts

# --------------------------------------------------------
# モジュール読み込み時に自動でロードしておく
# --------------------------------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "DATA"

# general
cepci_dict = load_csv_as_dict(DATA_DIR / "general" / "CEPCI.csv")
plant_data = load_csv(DATA_DIR / "general" / "plant_parameter.csv")
commodity_data = load_csv(DATA_DIR / "general" / "commodity_price.csv")
equipment_cost_data = load_csv(DATA_DIR / "general" / "equipment_cost.csv")
common_process_cost_data = load_csv(DATA_DIR / "general" / "common_process_cost.csv")

general_data = ["cepci_dict", "plant_data", "commodity_data", "equipment_cost_data", "common_process_cost_data"]

# infra
pipe_data = load_csv(DATA_DIR / "infra" / "pipeline_parameter.csv")
truck_data = load_csv(DATA_DIR / "infra" / "truck_parameter.csv")

infra_data = ["pipe_data", "truck_data"]

# each process
steel_data = load_csv(DATA_DIR / "steel_production.csv")

process_data = ["steel_data"]

# CCS
cc_data = load_csv(DATA_DIR / "ccs" / "carbon_capture.csv")
cc_opex_data = load_csv(DATA_DIR / "ccs" / "carbon_capture_opex.csv")

ccs_data_list = [cc_data, cc_opex_data]
ccs_data_merged = merge_dotdicts(ccs_data_list)

ccs_data = ["cc_data", "cc_opex_data", "ccs_data_merged"]

# Water electrolysis
awe_data = load_csv(DATA_DIR / "electrolysis" / "AWE_parameter.csv")
pemwe_data = load_csv(DATA_DIR / "electrolysis" / "PEMWE_parameter.csv")
awe_adv_data = load_csv(DATA_DIR / "electrolysis" / "AWE_adv_parameter.csv")
pemwe_adv_data = load_csv(DATA_DIR / "electrolysis" / "PEMWE_adv_parameter.csv")

we_data = ["awe_data", "pemwe_data", "awe_adv_data", "pemwe_adv_data"]

# Biomass
bio_infra_assump_data = load_csv(DATA_DIR / "biomass" / "biomass_infra_assumption.csv")
bio_gather_cost_data = load_csv(DATA_DIR / "biomass" / "biomass_gathering_cost.csv")
bio_capex_data = load_csv(DATA_DIR / "biomass" / "biomass_cost.csv")
bio_hydrogen_requirement_data = load_csv(DATA_DIR / "biomass" / "biomass_requirement_hydrogen.csv")
wood_property_data = load_csv(DATA_DIR / "biomass" / "wood_physical_property.csv")
maize_property_data = load_csv(DATA_DIR / "biomass" / "maize_physical_property.csv")

biomass_data = ["bio_infra_assump_data", "bio_gather_cost_data", "bio_capex_data", "bio_hydrogen_requirement_data", "wood_property_data", "maize_property_data"]


#########
## all ##
#########

__all__ = general_data + infra_data + process_data + ccs_data + we_data + biomass_data