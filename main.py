from myconfig import *
import numpy as np

def test():
    print(f"K1: {equipment_costs.Compressor.K1}")
    print(f"MEA_C0: {ccs_data_merged.MEA.Base_cost}")
    print(f"Electcity cost: {ccs_data_merged.Electricity.Value}")
    print(f"CC capex: {co2_capture_capex(1.2)}")
    print(f"steel BAU capex: {steel_capex_bau(100)}")
    print(f"bio gather cost: {bio_gather_cost(50000)}")

def ccs_check():
    cr = np.linspace(0, 1.5, 50) # [Mt-CO2 captured / y]
    capex = co2_capture_capex(cr)
    opex_list = co2_capture_opex(cr)
    opex = [(opex_list[0][i] + opex_list[1][i] + opex_list[2][i] + opex_list[3][i]) for i in range(len(opex_list[0]))]
    annual_cost = co2_capture_cost(cr)
    cocc = ccs_cost_check(cr)
    # print(f"CO2 capturing plant with capacity {cr} [Mt-CO2 captured / y]")
    # print(f"CAPEX: {capex} [million USD]")
    # print(f"OPEX: {opex_list} [million USD / y]: [electricity, water, MEA_regeneration, MEA_makeup]")
    # print(f"cost of CO2 capture: {cocc:.2f} [USD / t-CO2]")
    y_list = [capex, opex, annual_cost,cocc]
    label_list = ["CAPEX [million USD]", "OPEX [million USD / y]", "Annual cost [million USD /y]", "Cost of CO2 capture[USD / t-CO2]"]
    title = "Cost of CO2 capture (small)"
    x_label = "Capacity [Mt-CO2 captured / y]"
    y_label = "Cost"
    plot_line(cr, y_list, legend_label=label_list, x_label=x_label, y_label=y_label, title=title)

def ccs_total():
    capturing_rate = np.linspace(0, 1.5, 50) # [Mt-CO2 captured / y]
    L = 1.5 # [km] #苫小牧の実証プラントを参照
    capex, opex, total_cost = ccs_total_cost(capturing_rate, L)
    cost_of_CO2 = total_cost * 1e6 / (capturing_rate * 1e6)
    y_list = [capex, opex, total_cost]
    legend_label = ["CAPEX", "OPEX", "Total annual cost"]
    x_label, y_label, title = "capturing rate [Mt-CO2/y]", "Cost [million USD (/y)", "Carbon capture and transport cost"
    plot_line(capturing_rate, y_list, legend_label=legend_label, x_label=x_label, y_label=y_label, title=title)
    plot_line(capturing_rate, [cost_of_CO2], x_label=x_label, y_label="cost of CO2 [USD / t-CO2]", title="Cost of CO2")

def biomass_infra_check():
    Mw = 58823.5 # [t / y]
    infra_list = bio_trans_infra(Mw) # L, D, S, E, Ews, F, N
    gathering_cost = bio_gather_cost(Mw) # [million USD / y]
    trans_cost = bio_trans_cost(Mw) # [million USD / y]
    cost_after_agri = (gathering_cost + trans_cost) * 1e6 / (Mw * 1e3) # [USD / kg]
    print(f"Biomass amount: {Mw:.3f} [t / y]")
    print(f"gathering cost: {gathering_cost:.3f} [million USD / y]")
    print(f"trans_cost    : {trans_cost:.3f} [million USD / y]")
    print(f"cost after agriculture : {cost_after_agri:.3f} [USD / kg]")

    Mw = np.linspace(0, 200000, 100)
    gathering_cost = bio_gather_cost(Mw) # [million USD / y]
    trans_cost = bio_trans_cost(Mw) # [million USD / y]
    total_cost = gathering_cost + trans_cost # [million USD / y]
    cost_after_agri = (gathering_cost + trans_cost) * 1e6 / (Mw * 1e3) # [USD / kg]
    # plot_line(Mw, [gathering_cost, trans_cost, total_cost], legend_label=["Gathering", "Transport", "Total"], x_label="Biomass amount [t/y]", y_label="Cost [million USD / y]", title="Biomass infra cost")
    plot_line(Mw, [cost_after_agri], x_label="biomass amount [t/y]", y_label="Cost after agriculture [USD / kg]", title="Cost after agriculture")

""" def plot_test_ccs():
    x = np.linspace(0, 400, 100)
    y1 = 0.21 * (x / 266.6) ** 0.6 + 0.72 * (x / 225) ** 0.80
    y2 = 16.9 * (x / (0.23 * 1000000/8000)) ** 0.67
    y3 = 0.65 * 23.80 * (x / (2064.4 * 3600 * 44 / 1000000)) ** 0.67
    y4 = 116.0 * (x / (1 * 1e6 / 8000)) ** 0.67
    y_list = [y1, y2, y3, y4]
    label_list = ["y1: Cormos et al. (2013)", "y2: Yang et al.(2021), MDEA", "y3", "y4: Yang et al.(2021), MEA"]
    title = "CCS cost estimation comparison"
    x_label = "Capacity [tCO2/h]"
    y_label = "CAPEX [million USD]"
    plot_line(x, y_list, legend_label=label_list, x_label=x_label, y_label=y_label, title=title) 

def plot_test_ccs_with_point():
    x = np.linspace(0, 400, 100)
    y1 = 0.21 * (x / 266.6) ** 0.6 + 0.72 * (x / 225) ** 0.80
    y2 = 14.3 * (x / (0.23 * 1000000/8000)) ** 0.67
    y3 = 0.65 * 23.80 * (x / (2064.4 * 3600 * 44 / 1000000)) ** 0.67
    y4 = 116.0 * (x / (1 * 1e6 / 8000)) ** 0.67
    y_list = [y1, y2, y3, y4]
    label_list = ["y1: Cormos et al. (2013)", "y2: Yang et al.(2021), MDEA", "y3", "y4: Yang et al.(2021), MEA"]
    title = "CCS cost estimation comparison with actual plant"
    x_label = "Capacity [tCO2/h]"
    y_label = "CAPEX [million USD]"

    x_scat = [3420/24]
    y_scat = [176]
    plot_line_and_scatter(x, y_list, x_scat, y_scat, legend_label=label_list, x_label=x_label, y_label=y_label, title=title) """

def plot_test_ccs_trans():
    x = np.linspace(0, 100, 100)
    co2_tonne = x * 3600 * 8000 * 1e-3 * 40
    y1 = trans_pipe_capex(x) / co2_tonne
    y2 = dist_pipe_capex(x) / co2_tonne
    y_list = [y1, y2]
    label_list = ["Pipe_trans", "Pipe_dist"]
    x_label = "CO2 flowrate [kg-CO2/s]"
    y_label = "CAPEX [USD / km / t-CO2]"
    title = "Pipeline cost per tonne"
    plot_line(x, y_list, label_list, x_label=x_label, y_label=y_label, title=title)

def steel_ccs(production_rate=100):
    pr = production_rate
    capex = steel_capex_ccs(pr)
    opex = steel_opex_ccs(pr)
    annual_cost = steel_annual_ccs(pr)
    print(f"\nCarbon capture plant for {pr} Mt/y")
    print(f"capex: {capex:.2f} [million USD]\nOPEX: {opex:.2f} [million USD / y]\nannual cost: {annual_cost:.2f} [million USD / y]")

biomass_infra_check()