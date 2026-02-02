from myconfig import *
import numpy as np

def test():
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
    plot_line(Mw, [gathering_cost, trans_cost, total_cost], legend_label=["Gathering", "Transport", "Total"], x_label="Biomass amount [t/y]", y_label="Cost [million USD / y]", title="Biomass infra cost")
    plot_line(Mw, [cost_after_agri], x_label="biomass amount [t/y]", y_label="Cost after agriculture [USD / kg]", title="Cost after agriculture")

def plot_test_ccs():
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
    plot_line_and_scatter(x, y_list, x_scat, y_scat, legend_label=label_list, x_label=x_label, y_label=y_label, title=title)

def steel_ccs(production_rate=100):
    pr = production_rate
    capex = steel_capex_ccs(pr)
    opex = steel_opex_ccs(pr)
    annual_cost = steel_annual_ccs(pr)
    print(f"\nCarbon capture plant for {pr} Mt/y")
    print(f"capex: {capex:.2f} [million USD]\nOPEX: {opex:.2f} [million USD / y]\nannual cost: {annual_cost:.2f} [million USD / y]")

def biomass_hydrogen_capex_check():
    pr = 90 * 1e-6 * 8000 # [kt-H2 / y], 90 kg-H2/h
    capex = bio_hydrogen_capex(pr)
    print(f"Production rate: {pr} kt-H2 / y\nCAPEX for hydrogen production from wood chip: {capex} million USD")

    pr = np.linspace(0, 5, 100)
    capex = bio_hydrogen_capex(pr)
    x_list = pr
    y_list = [capex]
    x_scat = [90 * 1e-6 * 8000]
    y_scat = [11]
    x_label = "Hydrogen production scale [kt-H2/y]"
    y_label = "CAPEX [million USD]"
    title = "CAPEX for hydrogen production from wood chips"
    plot_line_and_scatter(x_list, y_list, x_scat=x_scat, y_scat=y_scat, x_label=x_label, y_label=y_label, title=title)

def co2_compression_pump_check():
    co2_flowrate = np.array([1000, 2500, 5000, 10000, 15000, 20000, 25000]) # [t / d]
    N = np.array([1, 1, 1, 1, 2, 2, 3])
    cr = co2_flowrate * (8000 / 24) * 1e-6 # [Mt / y]
    comp_capex = co2_compression_capex(cr, N)
    # comp_power = co2_compression_power(cr)
    comp_opex = co2_compression_opex(cr, N)
    pump_capex = co2_pump_capex(cr)
    pump_power = co2_pump_power(cr)
    pump_opex = co2_pump_opex(cr)

    print(f"compression capex: {comp_capex}")
    # print(f"compression opex: {comp_opex}")
    # print(f"compression power: {comp_power}")
    print(f"pump capex: {pump_capex}")
    # print(f"pump_opex: {pump_opex}")
    print(f"pump power: {pump_power}")

def ccs_total():
    capturing_rate = 1.0 # [Mt-CO2 captured / y]
    L = 1.5 # [km] #苫小牧の実証プラントを参照
    capex, opex, total_cost, layer_label_list = ccs_total_cost(capturing_rate, L)
    print(capex)
    y_list = [capex, opex, total_cost]
    x_list = ["CAPEX\n[M$]", "OPEX\n[M$/year]", "Total annual cost\n[M$/year]"]
    y_label = "Cost [million USD (/y)]"
    title = "CCS Cost of 1.0 Mtpa capturing (without storage)"
    plot_stack_bar(y_list=y_list, x_list=x_list, layer_label_list=layer_label_list, y_label=y_label, title=title)

def ccs_total_comparison():
    capturing_rate = [0.5, 1.0, 5.0]
    L = [1.5, 3.0, 10.0]
    for cr in capturing_rate:
        for l in L:
            capex, opex, total_cost, layer_label_list = ccs_total_cost(cr, l)
            y_list = [capex, opex, total_cost]
            x_list = ["CAPEX\n[M$]", "OPEX\n[M$/year]", "Total annual cost\n[M$/year]"]
            y_label = "Cost [million USD (/y)]"
            title = f"CCS Cost of {cr} Mtpa with {l} km pipeline (without storage)"
            plot_stack_bar(y_list=y_list, x_list=x_list, layer_label_list=layer_label_list, y_label=y_label, title=title)

def ccs_total_check():
    cr = np.linspace(0, 6.0, 50) # [Mt-CO2 captured / y]
    capex = co2_capture_capex(cr)
    opex_list = co2_capture_opex(cr)
    opex = [(opex_list[0][i] + opex_list[1][i] + opex_list[2][i] + opex_list[3][i]) for i in range(len(opex_list[0]))]
    annual_cost = co2_capture_cost(cr)
    cocc = ccs_cost_check(cr)
    y_list = [capex, opex, annual_cost,cocc]
    label_list = ["CAPEX [million USD]", "OPEX [million USD / y]", "Annual cost [million USD /y]", "Cost of CO2 capture and transport\n[USD / t-CO2]"]
    # y_list = [annual_cost,cocc]
    # label_list = ["Annual cost [million USD /y]", "Cost of CO2 capture and transport\n[USD / t-CO2]"]
 
    title = "Cost of CO2 capture and transport"
    x_label = "Capacity [Mt-CO2 captured / y]"
    y_label = "Cost"
    plot_line(cr, y_list, legend_label=label_list, x_label=x_label, y_label=y_label, title=title)

def biomass_gasifier():
    pr = np.linspace(1, 100, 50) # [kt-H2 / y]
    capex = bio_hydrogen_capex(pr)
    plot_line(pr, [capex], x_label="Hydrogen production rate [kt-H2 / yr]", y_label="CAPEX [millin USD]", title="Biomass gasification cost")

biomass_gasifier()