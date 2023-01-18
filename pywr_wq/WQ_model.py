import pandas as pd

def baseflow_separation(alpha, beta, flow_current, flow_before, sep_flow_before):
    """!
    Separate baseflow from total flow using a statistical baseflow separation method with two parameters.
    Refer to Hughes et al. (2003)  Continuous baseflow separation from time series of
    daily and monthly streamflow data. Water SA, 29 (1).
    @param alpha - first parameter for baseflow separation
    @param beta - second parameter for baseflow separation
    @param flow_current - total flow of the current timestep
    @param flow_before - total flow of the previous timestep
    @param sep_flow_before - baseflow of the previous timestep
    @return baseflow of the current timestep 
    """
    return (alpha * sep_flow_before) + beta * (1 + alpha) * (flow_current - flow_before)
        

class WQ_Model:
    """!
    Stipulates water quality modelling functionality
     
    """
    def __init__(self):
        self.network = []
    
    
    def step(self, node_flows, timestep):
        """!
        Required for integration with the Pywr model. Water quality simulation within each timestep of the model
        @param node_flows - dictionary of flows/storage volume for a particular timestep
        @param timestep - current timestep
     
        """
       
        for flow_node in node_flows:
            for wq_node in self.network:
                if wq_node.get_node_name() == flow_node:
                    wq_node.set_flow(node_flows[flow_node])
        
        for node in self.node_order:
            current_WQ_node = self.network[self.node_order[node]]
            j = len(current_WQ_node.flow_timeseries) - 1
            if len(current_WQ_node.upstream_nodes) == 1 and current_WQ_node.upstream_nodes[0].get_node_type() == "storage" and current_WQ_node.upstream_nodes[0].flow_timeseries[j]> 0:
                current_WQ_node.daily_TDS_load[j] = current_WQ_node.flow_timeseries[j]/current_WQ_node.upstream_nodes[0].flow_timeseries[j] * current_WQ_node.upstream_nodes[0].daily_TDS_load[j]
                current_WQ_node.daily_NO3_load[j] = current_WQ_node.flow_timeseries[j]/current_WQ_node.upstream_nodes[0].flow_timeseries[j] * current_WQ_node.upstream_nodes[0].daily_NO3_load[j]
                current_WQ_node.daily_NH4_load[j] = current_WQ_node.flow_timeseries[j]/current_WQ_node.upstream_nodes[0].flow_timeseries[j] * current_WQ_node.upstream_nodes[0].daily_NH4_load[j]
            
                current_WQ_node.daily_TDS_load[j] += upstream_node.daily_TDS_load[j]
                current_WQ_node.daily_NO3_load[j] += upstream_node.daily_NO3_load[j]
                current_WQ_node.daily_NH4_load[j] += upstream_node.daily_NH4_load[j]


                if current_WQ_node.daily_TDS_load[j] < 0: current_WQ_node.daily_TDS_load[j] = 0
                if current_WQ_node.daily_NO3_load[j] < 0: current_WQ_node.daily_NO3_load[j] = 0
                if current_WQ_node.daily_NH4_load[j] < 0: current_WQ_node.daily_NH4_load[j] = 0

            else:
                for upstream_node in current_WQ_node.upstream_nodes:
                    if upstream_node.flow_timeseries[j] > 0:
                        if upstream_node.get_node_type() == "catchment" and "catchment" in upstream_node.get_node_name():
                            upstream_node.daily_TDS_load[j] = upstream_node.TDS_concentration_GW * upstream_node.GW_flow[j] * 1000
                            upstream_node.daily_TDS_load[j] += upstream_node.TDS_concentration_IF * upstream_node.interflow[j] * 1000

                            upstream_node.daily_NO3_load[j] = upstream_node.NO3_concentration_GW * upstream_node.GW_flow[j] * 1000
                            upstream_node.daily_NO3_load[j] += upstream_node.NO3_concentration_IF * upstream_node.interflow[j] * 1000

        
                            upstream_node.daily_NH4_load[j] = upstream_node.NH4_concentration_GW * upstream_node.GW_flow[j] * 1000
                            upstream_node.daily_NH4_load[j] += upstream_node.NH4_concentration_IF * upstream_node.interflow[j] * 1000

                            sflow = upstream_node.surface_flow[j]
                            if sflow > 0:
                                 upstream_node.daily_TDS_load[j] += upstream_node.TDS_concentration_SF * sflow * 1000
                                 upstream_node.daily_NO3_load[j] += upstream_node.NO3_concentration_SF * sflow * 1000
                                 upstream_node.daily_NH4_load[j] += upstream_node.NH4_concentration_SF * sflow * 1000
                            upstream_node.daily_TDS_concentration[j] =(upstream_node.daily_TDS_load[j]/ (upstream_node.flow_timeseries[j] * 1000))[0]
                            upstream_node.daily_NO3_concentration[j] =(upstream_node.daily_NO3_load[j]/ (upstream_node.flow_timeseries[j] * 1000))[0]
                            upstream_node.daily_NH4_concentration[j] =(upstream_node.daily_NH4_load[j]/ (upstream_node.flow_timeseries[j] * 1000))[0]
                            
                        elif upstream_node.get_node_type() == "catchment" :
                            upstream_node.daily_TDS_load[j] = upstream_node.TDS_concentration * upstream_node.flow_timeseries[j] * 1000
                            upstream_node.daily_TDS_concentration[j] =(upstream_node.daily_TDS_load[j]/ (upstream_node.flow_timeseries[j] * 1000))[0]
                            
                            upstream_node.daily_NO3_load[j] = upstream_node.NO3_concentration * upstream_node.flow_timeseries[j] * 1000
                            upstream_node.daily_NO3_concentration[j] =(upstream_node.daily_NO3_load[j]/ (upstream_node.flow_timeseries[j] * 1000))[0]
                            
                            upstream_node.daily_NH4_load[j] = upstream_node.NH4_concentration * upstream_node.flow_timeseries[j] * 1000
                            upstream_node.daily_NH4_concentration[j] =(upstream_node.daily_NH4_load[j]/ (upstream_node.flow_timeseries[j] * 1000))[0]
                        
                        upstream_node.daily_water_temperature[j] = upstream_node.temp_profile[timestep.month - 1]    
                         # account for nitrification
                        #update coefficient for water temperature
                        coeff = upstream_node.nitrification_coefficient * pow(1.024,upstream_node.daily_water_temperature[j] - 20)  
                        nitrific_change = coeff *  upstream_node.daily_NH4_concentration[j]
                        #nitrific_change = upstream_node.nitrification_coefficient *  upstream_node.daily_NH4_concentration[j]
                        upstream_node.daily_NH4_concentration[j] -= nitrific_change
                        upstream_node.daily_NH4_load[j] -= nitrific_change * upstream_node.flow_timeseries[j] * 1000
                        upstream_node.daily_NO3_concentration[j] += nitrific_change
                        upstream_node.daily_NO3_load[j] += nitrific_change * upstream_node.flow_timeseries[j] * 1000
                        #update for photoplankton assimilation of NO3
                        coeff = upstream_node.phyto_coefficient * pow(1.066,upstream_node.daily_water_temperature[j] - 20)  
                        phyto_change = coeff *  upstream_node.daily_NO3_concentration[j]
                        upstream_node.daily_NO3_concentration[j] -= phyto_change
                        upstream_node.daily_NO3_load[j] -= phyto_change * upstream_node.flow_timeseries[j] * 1000
                       
                        current_WQ_node.daily_TDS_load[j] += upstream_node.daily_TDS_load[j]
                        current_WQ_node.daily_NO3_load[j] += upstream_node.daily_NO3_load[j]
                        current_WQ_node.daily_NH4_load[j] += upstream_node.daily_NH4_load[j]

            if current_WQ_node.flow_timeseries[j]> 0:
                current_WQ_node.daily_TDS_concentration[j] = (current_WQ_node.daily_TDS_load[j]/ (current_WQ_node.flow_timeseries[j]* 1000))[0]
                current_WQ_node.daily_NO3_concentration[j] = (current_WQ_node.daily_NO3_load[j]/ (current_WQ_node.flow_timeseries[j]* 1000))[0] 
                current_WQ_node.daily_NH4_concentration[j] = (current_WQ_node.daily_NH4_load[j]/ (current_WQ_node.flow_timeseries[j]* 1000))[0] 
                # account for nitrification
                current_WQ_node.daily_water_temperature[j] = current_WQ_node.temp_profile[timestep.month - 1]  
                #update coefficient for water temperature
                coeff = current_WQ_node.nitrification_coefficient * pow(1.024, current_WQ_node.daily_water_temperature[j] - 20)  
                nitrific_change = coeff *  current_WQ_node.daily_NH4_concentration[j]
                #nitrific_change = current_WQ_node.nitrification_coefficient *  current_WQ_node.daily_NH4_concentration[j]
                current_WQ_node.daily_NH4_concentration[j] -= nitrific_change
                current_WQ_node.daily_NH4_load[j] -= nitrific_change * current_WQ_node.flow_timeseries[j] * 1000
                current_WQ_node.daily_NO3_concentration[j] += nitrific_change
                current_WQ_node.daily_NO3_load[j] += nitrific_change * current_WQ_node.flow_timeseries[j] * 1000
                #update for photoplankton assimilation of NO3
                coeff = current_WQ_node.phyto_coefficient * pow(1.066,current_WQ_node.daily_water_temperature[j] - 20)  
                phyto_change = coeff *  current_WQ_node.daily_NO3_concentration[j]
                current_WQ_node.daily_NO3_concentration[j] -= phyto_change
                current_WQ_node.daily_NO3_load[j] -= phyto_change * current_WQ_node.flow_timeseries[j] * 1000  
                        
                load_lost_TDS = 0
                load_lost_NO3 = 0
                load_lost_NH4 = 0


                for downstream_node in current_WQ_node.downstream_nodes:
                    if "evaporation" in downstream_node.get_node_name():
                        downstream_node.daily_TDS_load[j] = 0 
                        downstream_node.daily_TDS_concentration[j] = 0
                        downstream_node.daily_NO3_load[j] = 0 
                        downstream_node.daily_NO3_concentration[j] = 0
                        downstream_node.daily_NH4_load[j] = 0 
                        downstream_node.daily_NH4_concentration[j] = 0
                        continue
                    if downstream_node.get_node_type() == "output":
                        if downstream_node.flow_timeseries[j] > 0:
                            downstream_node.daily_TDS_load[j] = downstream_node.flow_timeseries[j]/current_WQ_node.flow_timeseries[j] * current_WQ_node.daily_TDS_load[j] 
                            downstream_node.daily_TDS_concentration[j] = (downstream_node.daily_TDS_load[j]/ (downstream_node.flow_timeseries[j] * 1000))[0]
                            
                            downstream_node.daily_NO3_load[j] = downstream_node.flow_timeseries[j]/current_WQ_node.flow_timeseries[j] * current_WQ_node.daily_NO3_load[j] 
                            downstream_node.daily_NO3_concentration[j] = (downstream_node.daily_NO3_load[j]/ (downstream_node.flow_timeseries[j] * 1000))[0]
                                               
                            downstream_node.daily_NH4_load[j] = downstream_node.flow_timeseries[j]/current_WQ_node.flow_timeseries[j] * current_WQ_node.daily_NH4_load[j] 
                            downstream_node.daily_NH4_concentration[j] = (downstream_node.daily_NH4_load[j]/ (downstream_node.flow_timeseries[j] * 1000))[0]
                            
                            downstream_node.daily_water_temperature[j] = downstream_node.temp_profile[timestep.month - 1]
                            # account for nitrification
                            #update coefficient for water temperature
                            coeff = downstream_node.nitrification_coefficient * pow(1.024,downstream_node.daily_water_temperature[j] - 20)  
                            nitrific_change = coeff *  downstream_node.daily_NH4_concentration[j]
                            #print(nitrific_change)
                            #nitrific_change = downstream_node.nitrification_coefficient *  downstream_node.daily_NH4_concentration[j]
                            downstream_node.daily_NH4_concentration[j] -= nitrific_change
                            downstream_node.daily_NH4_load[j] -= nitrific_change * downstream_node.flow_timeseries[j] * 1000
                            downstream_node.daily_NO3_concentration[j] += nitrific_change
                            downstream_node.daily_NO3_load[j] += nitrific_change * downstream_node.flow_timeseries[j] * 1000

                            #update for photoplankton assimilation of NO3
                            coeff = downstream_node.phyto_coefficient * pow(1.066,downstream_node.daily_water_temperature[j] - 20)  
                            phyto_change = coeff *  downstream_node.daily_NO3_concentration[j]
                            downstream_node.daily_NO3_concentration[j] -= phyto_change
                            downstream_node.daily_NO3_load[j] -= phyto_change * downstream_node.flow_timeseries[j] * 1000
                            
                        else:
                            downstream_node.daily_TDS_load[j] = 0 
                            downstream_node.daily_TDS_concentration[j] = 0

                            downstream_node.daily_NO3_load[j] = 0 
                            downstream_node.daily_NO3_concentration[j] = 0
                              
                            downstream_node.daily_NH4_load[j] = 0 
                            downstream_node.daily_NH4_concentration[j] = 0
                        load_lost_TDS += downstream_node.daily_TDS_load[j]
                        load_lost_NO3 += downstream_node.daily_NO3_load[j]
                        load_lost_NH4 += downstream_node.daily_NH4_load[j]
                        
                current_WQ_node.daily_TDS_load[j] -= load_lost_TDS 
                current_WQ_node.daily_NO3_load[j] -= load_lost_NO3 
                current_WQ_node.daily_NH4_load[j] -= load_lost_NH4 

                if current_WQ_node.daily_TDS_load[j] < 0:
                    current_WQ_node.daily_TDS_load[j] = 0
                if current_WQ_node.daily_NO3_load[j] < 0:
                    current_WQ_node.daily_NO3_load[j] = 0
                if current_WQ_node.daily_NH4_load[j] < 0:
                    current_WQ_node.daily_NH4_load[j] = 0


                if current_WQ_node.get_node_type() == "storage":
                    load_released_TDS = 0
                    load_released_NO3 = 0
                    load_released_NH4 = 0

                    for downstream_node in current_WQ_node.downstream_nodes:
                        if downstream_node.get_node_type() == "link":
                            if downstream_node.flow_timeseries[j] > 0:
                                load_released_TDS += downstream_node.flow_timeseries[j]/current_WQ_node.flow_timeseries[j] * current_WQ_node.daily_TDS_load[j]
                                load_released_NO3 += downstream_node.flow_timeseries[j]/current_WQ_node.flow_timeseries[j] * current_WQ_node.daily_NO3_load[j] 
                                load_released_NH4 += downstream_node.flow_timeseries[j]/current_WQ_node.flow_timeseries[j] * current_WQ_node.daily_NH4_load[j] 

                    current_WQ_node.daily_TDS_load[j + 1] = current_WQ_node.daily_TDS_load[j] - load_released_TDS
                    current_WQ_node.daily_NO3_load[j + 1] = current_WQ_node.daily_NO3_load[j] - load_released_NO3
                    current_WQ_node.daily_NH4_load[j + 1] = current_WQ_node.daily_NH4_load[j] - load_released_NH4

                    if current_WQ_node.daily_TDS_load[j + 1] < 0:
                        current_WQ_node.daily_TDS_load[j + 1] = 0
                    if current_WQ_node.daily_NO3_load[j + 1] < 0:
                        current_WQ_node.daily_NO3_load[j + 1] = 0
                    if current_WQ_node.daily_NH4_load[j + 1] < 0:
                        current_WQ_node.daily_NH4_load[j + 1] = 0

            else:
                current_WQ_node.daily_TDS_load[j] = 0
                current_WQ_node.daily_TDS_concentration[j] = 0
                current_WQ_node.daily_NO3_load[j] = 0
                current_WQ_node.daily_NO3_concentration[j] = 0
                current_WQ_node.daily_NH4_load[j] = 0
                current_WQ_node.daily_NH4_concentration[j] = 0
              
    def setup(self, data):
        """!
        Sets up the water quality parameters for the model
        @param data - json model in memory
        """
        universal_temp_profile = [20, 21, 19, 16, 12, 10, 8, 12, 16, 18, 19, 20]
        for edge in data['edges']:
            downstream_node_name = edge[1]
            upstream_node_name = edge[0]
            downstream_type = None
            upstream_type = None
            upstream_initial_storage = 0
            downstream_initial_storage = 0
            for node in data['nodes']:
                if node['name'] == downstream_node_name:
                    downstream_type = node["type"] 
                    downstream_TDS_concentration_GW = node["TDS_concentration_GW"]
                    downstream_TDS_concentration_IF = node["TDS_concentration_IF"]
                    downstream_TDS_concentration_SF = node["TDS_concentration_SF"]
                    downstream_TDS_concentration = node["TDS_concentration"]

                    downstream_NO3_concentration_GW = node["NO3_concentration_GW"]
                    downstream_NO3_concentration_IF = node["NO3_concentration_IF"]
                    downstream_NO3_concentration_SF = node["NO3_concentration_SF"]
                    downstream_NO3_concentration = node["NO3_concentration"]

                    downstream_NH4_concentration_GW = node["NH4_concentration_GW"]
                    downstream_NH4_concentration_IF = node["NH4_concentration_IF"]
                    downstream_NH4_concentration_SF = node["NH4_concentration_SF"]
                    downstream_NH4_concentration = node["NH4_concentration"]
                    if downstream_type == "storage":
                        downstream_initial_storage = node["initial_volume"]
                if node['name'] == upstream_node_name:
                    upstream_type = node["type"]
                    upstream_TDS_concentration_GW = node["TDS_concentration_GW"]
                    upstream_TDS_concentration_IF = node["TDS_concentration_IF"]
                    upstream_TDS_concentration_SF = node["TDS_concentration_SF"]
                    upstream_TDS_concentration = node["TDS_concentration"]

                    upstream_NO3_concentration_GW = node["NO3_concentration_GW"]
                    upstream_NO3_concentration_IF = node["NO3_concentration_IF"]
                    upstream_NO3_concentration_SF = node["NO3_concentration_SF"]
                    upstream_NO3_concentration = node["NO3_concentration"]

                    upstream_NH4_concentration_GW = node["NH4_concentration_GW"]
                    upstream_NH4_concentration_IF = node["NH4_concentration_IF"]
                    upstream_NH4_concentration_SF = node["NH4_concentration_SF"]
                    upstream_NH4_concentration = node["NH4_concentration"]
                    if upstream_type == "storage":
                        upstream_initial_storage = node["initial_volume"]
            downstream_node = None
            upstream_node = None
            for i in range(0, len(self.network)):
                current_node = self.network[i]
                if current_node.get_node_name() == downstream_node_name:
                    downstream_node = current_node
                if current_node.get_node_name() == upstream_node_name:
                    upstream_node = current_node
            if downstream_node == None:
                downstream_node = WQ_Node(downstream_node_name, downstream_type, downstream_TDS_concentration_GW, downstream_TDS_concentration_IF, downstream_TDS_concentration_SF, downstream_TDS_concentration,
                                            downstream_NO3_concentration_GW, downstream_NO3_concentration_IF, downstream_NO3_concentration_SF, downstream_NO3_concentration, 
                                            downstream_NH4_concentration_GW, downstream_NH4_concentration_IF, downstream_NH4_concentration_SF, downstream_NH4_concentration, 0.04, 0.01, universal_temp_profile)
                if downstream_type == "storage":
                    downstream_node.daily_TDS_load[0] = 200 * downstream_initial_storage * 1000 
                    downstream_node.daily_NO3_load[0] = 0.5 * downstream_initial_storage * 1000 
                    downstream_node.daily_NH4_load[0] = 0.5 * downstream_initial_storage * 1000 

                #self.network[downstream_node_name] = downstream_node
                self.network.append(downstream_node)
            if upstream_node == None:
                upstream_node = WQ_Node(upstream_node_name, upstream_type, upstream_TDS_concentration_GW, upstream_TDS_concentration_IF, upstream_TDS_concentration_SF, 
                                        upstream_TDS_concentration, upstream_NO3_concentration_GW, upstream_NO3_concentration_IF, upstream_NO3_concentration_SF, upstream_NO3_concentration, 
                                        upstream_NH4_concentration_GW, upstream_NH4_concentration_IF, upstream_NH4_concentration_SF, upstream_NH4_concentration, 0.04, 0.01, universal_temp_profile)
                if upstream_type == "storage":
                    upstream_node.daily_TDS_load[0] = 200 * upstream_initial_storage * 1000 
                    upstream_node.daily_NO3_load[0] = 0.5 * upstream_initial_storage * 1000 
                    upstream_node.daily_NH4_load[0] = 0.5 * upstream_initial_storage * 1000 
                #self.network[upstream_node_name] = upstream_node
                self.network.append(upstream_node)
            upstream_node.set_downstream_node(downstream_node)
            downstream_node.set_upstream_node(upstream_node)
    
    def get_concentration(self, node_name, determinand):
        for i in range(0, len(self.network)):
            current_WQ_node = self.network[i]
            if current_WQ_node.get_node_name() == node_name:
                if determinand == "TDS":
                    return current_WQ_node.daily_TDS_concentration[len(current_WQ_node.flow_timeseries) - 1]
                elif determinand == "NO3":
                    return current_WQ_node.daily_NO3_concentration[len(current_WQ_node.flow_timeseries) - 1]
                elif determinand == "NH4":
                    return current_WQ_node.daily_NH4_concentration[len(current_WQ_node.flow_timeseries) - 1]
                elif determinand == "WT":
                    return current_WQ_node.daily_Water_Temperature[len(current_WQ_node.flow_timeseries) - 1]

    def set_node_order(self, node_order):
        self.node_order = node_order
        for node in self.node_order:
            for i in range(0, len(self.network)):
                current_WQ_node = self.network[i]
                if current_WQ_node.get_node_name() == node:
                    #print("got here!!!!")
                    self.node_order[node] = i
                     
    def finish(self):
        """!
        Saves water quality simulations at the completion of the model run
        """
        WQ_results = {}
        flow_separation_total_flow = {}
        flow_separation_interflow = {}
        flow_separation_GW = {}
        flow_separation_SW = {}    
        for i in range(0, len(self.network)):
            current_WQ_node = self.network[i]
            #print(current_WQ_node.daily_TDS_concentration)
            WQ_results[current_WQ_node.get_node_name() + ":TDS"] = current_WQ_node.daily_TDS_concentration
            WQ_results[current_WQ_node.get_node_name() + ":NO3"] = current_WQ_node.daily_NO3_concentration
            WQ_results[current_WQ_node.get_node_name() + ":NH4"] = current_WQ_node.daily_NH4_concentration
            WQ_results[current_WQ_node.get_node_name() + ":WT"] = current_WQ_node.daily_water_temperature
            if current_WQ_node.get_node_type() == "catchment" and "catchment" in current_WQ_node.get_node_name():
                flow_separation_total_flow[current_WQ_node.get_node_name()] = current_WQ_node.flow_timeseries
                flow_separation_interflow[current_WQ_node.get_node_name()] = current_WQ_node.interflow
                flow_separation_GW[current_WQ_node.get_node_name()] = current_WQ_node.GW_flow
                flow_separation_SW[current_WQ_node.get_node_name()] = current_WQ_node.surface_flow 
        WQ_results = pd.DataFrame(WQ_results)
        WQ_results.to_csv("results/WQ_results.csv")  
        flow_separation_total_flow = pd.DataFrame(flow_separation_total_flow)
        flow_separation_total_flow.to_csv("results/catchment_inflow.csv")  
        flow_separation_interflow = pd.DataFrame(flow_separation_interflow)
        flow_separation_interflow.to_csv("results/catchment_interflow.csv")  
        flow_separation_GW = pd.DataFrame(flow_separation_GW)
        flow_separation_GW.to_csv("results/catchment_GW.csv")  
        flow_separation_SW = pd.DataFrame(flow_separation_SW)
        flow_separation_SW.to_csv("results/catchment_SW.csv") 

class WQ_Node:
    """!
    Node class for the water quality modelling network. Sets water quality parameters for each node
     
    """
    def __init__(self, name, nodetype, TDS_concentration_GW, TDS_concentration_IF, TDS_concentration_SF, TDS_concentration,
                NO3_concentration_GW, NO3_concentration_IF, NO3_concentration_SF, NO3_concentration,
                NH4_concentration_GW, NH4_concentration_IF, NH4_concentration_SF, NH4_concentration, nitrification_coefficient, phyto_coefficient, temp_profile):
        self.node_name = name
        self.temp_profile = temp_profile
        self.node_type = nodetype
        self.downstream_nodes = []
        self.upstream_nodes = []
        #TDS
        self.TDS_concentration_GW = TDS_concentration_GW
        self.TDS_concentration_IF = TDS_concentration_IF
        self.TDS_concentration_SF = TDS_concentration_SF
        self.TDS_concentration = TDS_concentration
        #NO3 + NO2
        self.NO3_concentration_GW = NO3_concentration_GW
        self.NO3_concentration_IF = NO3_concentration_IF
        self.NO3_concentration_SF = NO3_concentration_SF
        self.NO3_concentration = NO3_concentration
        #NH4
        self.NH4_concentration_GW = NH4_concentration_GW
        self.NH4_concentration_IF = NH4_concentration_IF
        self.NH4_concentration_SF = NH4_concentration_SF
        self.NH4_concentration = NH4_concentration
        self.nitrification_coefficient = nitrification_coefficient
        self.phyto_coefficient = phyto_coefficient
        self.daily_water_temperature = [0] * 32872
        self.daily_TDS_load = [0] * 32872
        self.daily_TDS_concentration = [0] * 32872
        self.flow_timeseries = []
        self.daily_NO3_load = [0] * 32872
        self.daily_NO3_concentration = [0] * 32872
        self.daily_NO2_load = [0] * 32872
        self.daily_NO2_concentration = [0] * 32872
        self.daily_NH4_load = [0] * 32872
        self.daily_NH4_concentration = [0] * 32872
        self.surface_flow = []
        self.GW_flow = []
        self.interflow = []

   
    def set_flow(self, current_flow):
        self.flow_timeseries.append(current_flow) 
        i = len(self.flow_timeseries) - 1
        #find a way of doing the proper flow separation
        if self.node_type == "catchment" and "catchment" in self.node_name:
            #self.interflow.append(current_flow * 0.2)
            #self.GW_flow.append(current_flow * 0.1)
            if self.flow_timeseries[i] > 0:
                s_flow = baseflow_separation(0.95, 0.5, self.flow_timeseries[i], self.flow_timeseries[i-1], self.surface_flow[i-1])
                if s_flow < 0:
                    s_flow = 0
                self.surface_flow.append(s_flow)
                subsurface_flow = current_flow - s_flow
                interflow = baseflow_separation(0.95, 0.5, subsurface_flow, self.interflow[i-1] + self.GW_flow[i-1], self.interflow[i-1])
                if interflow < 0:
                    interflow = 0
                self.interflow.append(interflow)
                self.GW_flow.append(subsurface_flow - interflow)                
            else:
                self.surface_flow.append(0)
                self.GW_flow.append(0)
                self.interflow.append(0)
    
    def set_downstream_node(self, node):
        self.downstream_nodes.append(node)
        
    def set_upstream_node(self, node):
        self.upstream_nodes.append(node)
    
    def get_node_name(self):
        return self.node_name
    
    def get_node_type(self):
        return self.node_type

    def get_downstream_nodes(self):
        return self.downstream_nodes
    
    def get_upstream_nodes(self):
        return self.upstream_nodes