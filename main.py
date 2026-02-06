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

def electrolysis_check():
    # pr = np.array([1, 5, 10, 100])
    pr = np.array([5, 10, 100])
    awe_cap = [awe_capex(p) for p in pr]
    awe_op = [awe_opex(p) for p in pr]
    awe_annual_cost = awe_cost(pr)
    lcoh_awe = LCOH_awe(pr)
    cap_kw_awe = CAPEX_per_kW_awe(pr)

    pem_cap = [pemwe_capex(p) for p in pr]
    pem_op = [pemwe_opex(p) for p in pr]
    pemwe_annual_cost = pemwe_cost(pr)
    lcoh_pem = LCOH_pemwe(pr)
    cap_kw_pem = CAPEX_per_kW_pemwe(pr)

    # x_list = ["AWE\n1 MW", "AWE\n5 MW", "AWE\n10 MW", "AWE\n100 MW", "PEM\n1 MW", "PEM\n5 MW", "PEM\n10 MW", "PEM\n100 MW"]
    x_list = ["AWE\n5 MW", "AWE\n10 MW", "AWE\n100 MW", "PEM\n5 MW", "PEM\n10 MW", "PEM\n100 MW"]

    y_list = awe_cap + pem_cap
    y_label = "CAPEX [million USD]"
    title = "Electrolysis CAPEX comparison"
    layer_label_list_capex = ["stack", "electronics", "purification", "heat management", "compression", "contingency"]
    plot_stack_bar(y_list, layer_label_list=layer_label_list_capex, x_list=x_list, y_label=y_label, title=title)

    y_list = list(cap_kw_awe) + list(cap_kw_pem)
    y_label = "CAPEX [USD / kW]"
    title = "Electrolysis CAPEX (per kW) comparison"
    plot_bar(y_list, x_list=x_list, y_label=y_label, title=title)

    y_list = awe_op + pem_op
    y_label = "OPEX [million USD / yr]"
    title = "Electrolysis OPEX comparison"
    layer_label_list_opex = ["electricity", "steam", "cooling_water", "refgerant", "pump", "compression", "raw material water"]
    plot_stack_bar(y_list, layer_label_list=layer_label_list_opex, x_list=x_list, y_label=y_label, title=title)

    y_list = list(awe_annual_cost) + list(pemwe_annual_cost)
    y_label = "Annual cost [million USD / yr]"
    title = "Electrolysis annual cost comparison"
    plot_bar(y_list, x_list=x_list, y_label=y_label, title=title)

    y_list = list(lcoh_awe) + list(lcoh_pem)
    y_label = "LCOH [USD / kg-H2]"
    title = "Electrolysis LCOH comparison"
    plot_bar(y_list, x_list=x_list, y_label=y_label, title=title)

def tech_comparison():
    nh3_pr = 0.7 # [Mt-NH3 / yr]
    co2_emission = nh3_pr * 2.0 # [Mt-CO2 / y], 2.0 t-CO2 / t-NH3 を仮定
    hydrogen_requirement = nh3_pr * 1e6 / 17 * (3 / 2) * 2  / 8000 * 50 # [MW], 量論比
    hydrogen_root = awe_cost(hydrogen_requirement) # [million USD / yr]
    ccs_root = ccs_total_cost(co2_emission, L=1.5) # [million USD / yr]
    print(f"Hydrogen: {hydrogen_root} mm$/yr ({hydrogen_requirement} MW)")
    print(f"CCS: {ccs_root} mm$/yr ({co2_emission} Mt-CO2 / yr)")

    nh3_pr = np.linspace(0.1, 1, 50) # [Mt-NH3 / yr]
    co2_emission = nh3_pr * 2.0 # [Mt-CO2 / y], 2.0 t-CO2 / t-NH3 を仮定
    hydrogen_requirement = nh3_pr * 1e6 / 17 * (3 / 2) * 2  / 8000 * 50 # [MW], 量論比
    hydrogen_root = awe_adv_cost(hydrogen_requirement) # [million USD / yr]
    ccs_root = ccs_total_cost(co2_emission, L=1.5) # [million USD / yr]
    
    x = nh3_pr
    y_list = [hydrogen_root, ccs_root]
    x_label = "Ammonia production [Mtpa]"
    y_label = "Additional annual cost [million USD / yr]"
    title = "Technology comparison (Hydrogen (AWE, adv.feas.) vs CCS (1.5 km pipeline))"
    legend_label = ["Hydrogen", "CCS"]

    plot_line(x, y_list=y_list, x_label=x_label, y_label=y_label, title=title, legend_label=legend_label)

def tech_comparison_capex():
    nh3_pr = np.linspace(0.1, 1, 50) # [Mt-NH3 / yr]
    co2_emission = nh3_pr * 2.0 # [Mt-CO2 / y], 2.0 t-CO2 / t-NH3 を仮定
    hydrogen_requirement = nh3_pr * 1e6 / 17 * (3 / 2) * 2  / 8000 * 50 # [MW], 量論比
    hydrogen_production_rate = nh3_pr / 17 * (3 / 2) * 2 * 1e3 # [kt-H2 / yr]

    hydrogen_root = [sum(awe_capex(hr)) for hr in hydrogen_requirement] # [million USD]
    hydrogen_adv_root = [sum(awe_adv_capex(hr)) for hr in hydrogen_requirement] # [million USD]

    ccs_root_1p5 = [sum(ccs_total_cost(ce, L = 1.5)[0]) for ce in co2_emission] # [million USD]
    ccs_root_5 = [sum(ccs_total_cost(ce, L = 5)[0]) for ce in co2_emission] # [million USD]
    ccs_root_10 = [sum(ccs_total_cost(ce, L = 10)[0]) for ce in co2_emission] # [million USD]
    ccs_root_30 = [sum(ccs_total_cost(ce, L = 30)[0]) for ce in co2_emission] # [million USD]
    ccs_root_50 = [sum(ccs_total_cost(ce, L = 50)[0]) for ce in co2_emission] # [million USD]

    biomass_root = [sum(bio_hydrogen_total_cost(hpr)[0]) for hpr in hydrogen_production_rate] # [million USD]
    
    x = nh3_pr
    y_list = [hydrogen_root, hydrogen_adv_root, ccs_root_1p5, ccs_root_5, ccs_root_10, ccs_root_30, ccs_root_50, biomass_root]
    x_label = "NH3 production rate [Mtpa]"
    y_label = "Additional CAPEX [million USD]"
    title = f"Technology comparison in CAPEX (Hydrogen vs CCS vs Biomass)"
    legend_label = ["Hydrogen", "Hydrogen adv.feas.", "CCS\n(1.5 km pipeline)", "CCS\n(5 km pipeline)", "CCS\n(10 km pipeline)", "CCS\n(30 km pipeline)", "CCS\n(50 km pipeline)", "Biomass"]

    plot_line(x=x, y_list=y_list, legend_label=legend_label, x_label=x_label, y_label=y_label, title=title)

def tech_comparison_capex_stack(nh3_pr=0.01): # [Mt-NH3 / yr] = [Mtpa]
    co2_emission = nh3_pr * 2.0 # [Mt-CO2 / y], 2.0 t-CO2 / t-NH3 を仮定
    hydrogen_requirement = nh3_pr * 1e6 / 17 * (3 / 2) * 2  / 8000 * 50 # [MW], 量論比
    hydrogen_production_rate = nh3_pr / 17 * (3 / 2) * 2 * 1e3 # [kt-H2 / yr]

    hr = hydrogen_requirement # [MW]
    hydrogen_root = awe_capex(hr) # [million USD]
    hydrogen_adv_root = awe_adv_capex(hr) # [million USD]

    ce = co2_emission # [Mt-CO2 / y]
    ccs_root_1p5 = ccs_total_cost(ce, L = 1.5)[0] # [million USD]
    ccs_root_5 = ccs_total_cost(ce, L = 5)[0] # [million USD]
    ccs_root_10 = ccs_total_cost(ce, L = 10)[0] # [million USD]
    ccs_root_30 = ccs_total_cost(ce, L = 30)[0] # [million USD]
    ccs_root_50 = ccs_total_cost(ce, L = 50)[0] # [million USD]

    hpr = hydrogen_production_rate # [kt-H2 / yr]
    biomass_root = bio_hydrogen_total_cost(hpr)[0] # [million USD]
    
    y_list = [hydrogen_root, hydrogen_adv_root, ccs_root_1p5, ccs_root_5, ccs_root_10, ccs_root_30, ccs_root_50, biomass_root]
    y_label = "Additional CAPEX [million USD]"
    title = f"Technology comparison in CAPEX of {nh3_pr * 1e3} Ktpa-NH3 plant"
    x_label = ["AWE", "AWE\nadv.feas.", "CCS\n1.5 km", "CCS\n5 km", "CCS\n10 km", "CCS\n30 km", "CCS\n50 km", "Biomass\n(wood)"]
    x = f"\nElectrolysis: {hr:.2f} MW-H2\nCCS: {ce * 1e3} Ktpa-CO2\nBiomass: {hpr:.2f} Ktpa-H2"

    plot_stack_bar(y_list=y_list, x_label=x, x_list=x_label, y_label=y_label, title=title)

def hub_capex_check():
    x = np.linspace(1, 799999, 300)
    y = bio_gasif_capex(x)
    plot_line(x=x, y_list=[y], x_label="Preprocessing capacity [t / yr]", y_label="CAPEX [million USD]", title="Biomass preprocessing CAPEX")

def biomass_total_cost_check(hydrogen_production_rate=50):     # [kt-H2 / yr]
    capex, opex, total, label = bio_hydrogen_total_cost(hydrogen_production_rate)
    print(capex)
    print(opex)
    print(total)
    print(label)
    y_list = [capex, opex, total]
    x_label = ["CAPEX\n[million USD]", "OPEX\nw/o gasification\n[million USD/yr]", "Annual cost\n[million USD/yr]"]
    y_label = "Cost"
    title = f"Biomass cost configuration for {hydrogen_production_rate} Ktpa-H2 production"
    plot_stack_bar(y_list=y_list, x_list=x_label, layer_label_list=label, y_label=y_label, title=title)

def biomass_price_check(raw_biomass_price=0): # raw biomass price: 0 [USD / kg]
    biomass_amount = np.linspace(100, 1000, 100) # [t-biomass / yr]

    raw_price = [bio_price_check(ba, raw_biomass_price)[0][0] for ba in biomass_amount] # [USD/ kg]
    gather_price = [bio_price_check(ba, raw_biomass_price)[0][1] for ba in biomass_amount] # [USD/ kg]
    trans_price = [bio_price_check(ba, raw_biomass_price)[0][2] for ba in biomass_amount] # [USD/ kg]
    prepro_price = [bio_price_check(ba, raw_biomass_price)[0][3] for ba in biomass_amount] # [USD/ kg]
    total_price = [raw_price[i] + gather_price[i] + trans_price[i] + prepro_price[i] for i in range(len(raw_price))] # [USD / kg]
    label_list = bio_price_check(100, raw_biomass_price)[1]

    
    
    x_list = biomass_amount
    y_list = [raw_price, gather_price, trans_price, prepro_price, total_price]
    x_label = "Biomass amount [t-biomass / yr]"
    y_label = "Biomass price [USD / kg]"
    title = f"Biomass price configuration"
    legend_label = label_list + ["total price"]
    plot_line(x=x_list, y_list=y_list, x_label=x_label, y_label=y_label, title=title, legend_label=legend_label)

biomass_price_check(0)