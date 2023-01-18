import pandas as pd
import os
import json
   
   

    
def update_json(data):
    """!
    Updates a JSON file with input data and any additional parameters. 
    Typically, the model topology can be created on the online Pywr at www.waterstrategy.org. The 
    model can be exported as a Pywr JSON. This function can then be called from cli.py to update the JSON with 
    forcing data and any additional parameters needed
    @param data - json model read into memory
    @return data - json model in memory with additional forcing data and parameters
    """
 
    try:
        tables = data["tables"]
    except KeyError:
        tables = {}
    
    #inflows
    data["parameters"]["__catchment_1__:flow"] = {
                        "type": "dataframe",
                        "table": "__catchment_1__:flow", 
                        "index_col": 0,
                        "scenario": "scenario A",
                        "parse_dates": True}
    
    tables["__catchment_1__:flow"] = {
                    "url": "data/flows/NODE_34.xlsx",
                    "index_col": "index",
                    "header": 0,
                    "parse_dates": True}

    data["parameters"]["__catchment_2__:flow"] = {
                          "type": "dataframe",
                          "table": "Node_373_inflows",
                          "index_col": 0,
                          "scenario": "scenario A",
                          "parse_dates": True}
    tables["Node_373_inflows"] = {
                          "url": "data/flows/NODE_373.xlsx",
                          "index_col": 0,
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__catchment_3__:flow"] = {
                          "type": "dataframe",
                          "table": "DD1_inflows",
                          "index_col": 0,
                          "scenario": "scenario A",
                          "parse_dates": True}
    tables["DD1_inflows"] = {
                          "url": "data/flows/DD1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__catchment_4__:flow"] = {
                          "type": "dataframe",
                          "table": "Node_392_inflows",
                          "index_col": 0,
                          "scenario": "scenario A",
                          "parse_dates": True}
    tables["Node_392_inflows"] = {
                          "url": "data/flows/NODE_392.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__catchment_5__:flow"] = {
                          "type": "dataframe",
                          "table": "DD2_inflows",
                          "index_col": 0,
                          "scenario": "scenario A",
                          "parse_dates": True}
    tables["DD2_inflows"] = {
                          "url": "data/flows/DD2.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__catchment_6__:flow"] = {
                          "type": "dataframe",
                          "table": "Groot_inflows",
                          "index_col": 0,
                          "scenario": "scenario A",
                          "parse_dates": True}
    tables["Groot_inflows"] = {
                          "url": "data/flows/Groot.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
                        
    for node in data['nodes']:
        if node['name'] == 'catchment_1':
            node['flow'] = "__catchment_1__:flow"
            #node['flow'] = 10
        if node['name'] == 'catchment_2':
            node['flow'] = "__catchment_2__:flow"
            #node['flow'] = 10
        if node['name'] == 'catchment3':
            node['flow'] = "__catchment_3__:flow"
            #node['flow'] = 10
        if node['name'] == 'catchment4':
            node['flow'] = 0#"__catchment_4__:flow"
            #node['flow'] = 10
        if node['name'] == 'catchment5':
            node['flow'] = "__catchment_5__:flow"
            #node['flow'] = 10
        if node['name'] == 'catchment6':
            node['flow'] = "__catchment_6__:flow"
            #node['flow'] = 10
    #abstractions
    data["parameters"]["__output_1__:max_flow"] = {
                    "type": "dataframe",
                    "table": "output_1_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["output_1_max_flow"] = {
                          "url": "data/demands/output_1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__output_2__:max_flow"] = {
                    "type": "dataframe",
                    "table": "output_2_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["output_2_max_flow"] = {
                          "url": "data/demands/output_2.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__output_3__:max_flow"] = {
                    "type": "dataframe",
                    "table": "output_3_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["output_3_max_flow"] = {
                          "url": "data/demands/output_3.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__output_4__:max_flow"] = {
                    "type": "dataframe",
                    "table": "output_4_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["output_4_max_flow"] = {
                          "url": "data/demands/output_4.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__output_5__:max_flow"] = {
                    "type": "dataframe",
                    "table": "output_5_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["output_5_max_flow"] = {
                          "url": "data/demands/output_5.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__output_6__:max_flow"] = {
                    "type": "dataframe",
                    "table": "output_6_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["output_6_max_flow"] = {
                          "url": "data/demands/output_6.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__output_7__:max_flow"] = {
                    "type": "dataframe",
                    "table": "output_7_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["output_7_max_flow"] = {
                          "url": "data/demands/output_7.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__output_8__:max_flow"] = {
                    "type": "dataframe",
                    "table": "output_8_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["output_8_max_flow"] = {
                          "url": "data/demands/output_8.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    
        
    for node in data['nodes']:
        if node['name'] == 'output_1':
            node['max_flow'] = "__output_1__:max_flow"
            node['cost'] = -10000
        if node['name'] == 'output_2':
            node['max_flow'] = "__output_2__:max_flow"
            node['cost'] = -10000
        if node['name'] == 'output_3':
            node['max_flow'] = "__output_3__:max_flow"
            node['cost'] = -10000
        if node['name'] == 'output_4':
            node['max_flow'] = "__output_4__:max_flow"#
            node['cost'] = -10000
        if node['name'] == 'output_5':
            node['max_flow'] = "__output_5__:max_flow"
            node['cost'] = -10000
        if node['name'] == 'output_6':
            node['max_flow'] = "__output_6__:max_flow"
            node['cost'] = -10000
        if node['name'] == 'output_7':
            node['max_flow'] = "__output_7__:max_flow"
            node['cost'] = -10000
        if node['name'] == 'output_8':
            node['max_flow'] = "__output_8__:max_flow"
            node['cost'] = -10000
        
    #return flows
    data["parameters"]["__return_flow1__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_372_1_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_372_1_return_flow"] = {
                          "url": "data/return_flows/NODE_372_1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow2__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_372_2_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_372_2_return_flow"] = {
                          "url": "data/return_flows/NODE_372_2.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow3__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_372_3_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_372_3_return_flow"] = {
                          "url": "data/return_flows/NODE_372_3.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow4__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_374_1_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_374_1_return_flow"] = {
                          "url": "data/return_flows/NODE_374_1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow5__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_374_2_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_374_2_return_flow"] = {
                          "url": "data/return_flows/NODE_374_2.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow6__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_100_1_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_100_1_return_flow"] = {
                          "url": "data/return_flows/NODE_100_1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow7__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_7005_1_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_7005_1_return_flow"] = {
                          "url": "data/return_flows/NODE_7005_1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow8__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_7005_2_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_7005_2_return_flow"] = {
                          "url": "data/return_flows/NODE_7005_2.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow9__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_402_1_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_402_1_return_flow"] = {
                          "url": "data/return_flows/NODE_402_1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow10__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_402_2_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_402_2_return_flow"] = {
                          "url": "data/return_flows/NODE_402_2.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow11__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_402_3_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_402_3_return_flow"] = {
                          "url": "data/return_flows/NODE_402_3.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__return_flow12__:flow"] = {
                    "type": "dataframe",
                    "table": "Groot_1_return_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["Groot_1_return_flow"] = {
                          "url": "data/return_flows/Groot_1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    
    for node in data['nodes']:
        if node['name'] == 'return_flow1':
            node['flow'] = "__return_flow1__:flow"
        if node['name'] == 'return_flow2':
            node['flow'] = "__return_flow2__:flow"
        if node['name'] == 'return_flow3':
            node['flow'] = "__return_flow3__:flow"
        if node['name'] == 'return_flow4':
            node['flow'] = "__return_flow4__:flow"
        if node['name'] == 'return_flow5':
            node['flow'] = "__return_flow5__:flow"
        if node['name'] == 'return_flow6':
            node['flow'] = "__return_flow6__:flow"
        if node['name'] == 'return_flow7':
            node['flow'] = "__return_flow7__:flow"
        if node['name'] == 'return_flow8':
            node['flow'] = "__return_flow8__:flow"
        if node['name'] == 'return_flow9':
            node['flow'] = "__return_flow9__:flow"
        if node['name'] == 'return_flow10':
            node['flow'] = "__return_flow10__:flow"
        if node['name'] == 'return_flow11':
            node['flow'] = "__return_flow11__:flow"
        if node['name'] == 'return_flow12':
            node['flow'] = "__return_flow12__:flow"
    
    #transfers_in
    data["parameters"]["__transfer_in1__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_7004_transfers_in",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_7004_transfers_in"] = {
                          "url": "data/transfers_in/NODE_7004.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__transfer_in2__:flow"] = {
                    "type": "dataframe",
                    "table": "NODE_287_transfers_in",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["NODE_287_transfers_in"] = {
                          "url": "data/transfers_in/NODE_287.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    for node in data['nodes']:
        if node['name'] == 'transfer_in1':
            node['flow'] = "__transfer_in1__:flow"
            #node['flow'] = 10
        if node['name'] == 'transfer_in2':
            node['flow'] = "__transfer_in2__:flow"
            #node['flow'] = 10
   
    #transfers_out
    data["parameters"]["__transfer_out1__:max_flow"] = {
                    "type": "dataframe",
                    "table": "Groot_transfers_out",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["Groot_transfers_out"] = {
                          "url": "data/transfers_out/Groot.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    for node in data['nodes']:
        if node['name'] == 'transfer_out1':
            node['max_flow'] = "__transfer_out1__:max_flow"
            node['cost'] = -10000

    #reservoir rainfall
    data["parameters"]["__DD1_rainfall__:flow"] = {
                    "type": "dataframe",
                    "table": "DD1_rainfall_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["DD1_rainfall_flow"] = {
                          "url": "data/rainfall/DD1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__DD2_rainfall__:flow"] = {
                    "type": "dataframe",
                    "table": "DD2_rainfall_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["DD2_rainfall_flow"] = {
                          "url": "data/rainfall/DD2.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__Groot_rainfall__:flow"] = {
                    "type": "dataframe",
                    "table": "Groot_rainfall_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["Groot_rainfall_flow"] = {
                          "url": "data/rainfall/Groot.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    for node in data['nodes']:
        if node['name'] == 'DD1_rainfall':
            node['flow'] = "__DD1_rainfall__:flow"
        if node['name'] == 'DD2_rainfall':
            node['flow'] = "__DD2_rainfall__:flow"
        if node['name'] == 'Groot_rainfall':
            node['flow'] = "__Groot_rainfall__:flow"

    #reservoir evaporation
    data["parameters"]["__DD1_evaporation__:max_flow"] = {
                    "type": "dataframe",
                    "table": "DD1_evaporation_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["DD1_evaporation_max_flow"] = {
                          "url": "data/evaporation/Groot.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__DD2_evaporation__:max_flow"] = {
                    "type": "dataframe",
                    "table": "DD2_evaporation_max_flow",
                    "index_col": 0,
                    "scenario": "scenario A",
                    "parse_dates": True}
    tables["DD2_evaporation_max_flow"] = {
                          "url": "data/evaporation/DD2.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__Groot_evaporation__:max_flow"] = {
                    "type": "dataframe",
                    "table": "Groot_evaporation_max_flow",
                    "index_col": 0,
                    "parse_dates": True}
    tables["Groot_evaporation_max_flow"] = {
                          "url": "data/evaporation/Groot.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    for node in data['nodes']:
        if node['name'] == 'DD1_evaporation':
            node['max_flow'] = "__DD1_evaporation__:max_flow"
            node['cost'] = -1000
        if node['name'] == 'DD2_evaporation':
            node['max_flow'] = "__DD2_evaporation__:max_flow"
            node['cost'] = -1000
        if node['name'] == 'Groot_evaporation':
            node['max_flow'] = "__Groot_evaporation__:max_flow"
            node['cost'] = -1000
    
    #reservoir releases
    data["parameters"]["__Groot_releases__:max_flow"] = {
                    "type": "dataframe",
                    "table": "Groot_releases_max_flow",
                    "index_col": 0,
                    "parse_dates": True}
    tables["Groot_releases_max_flow"] = {
                          "url": "data/reservoir_releases/Groot.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__DD1_releases__:max_flow"] = {
                    "type": "dataframe",
                    "table": "DD1_releases_max_flow",
                    "index_col": 0,
                    "parse_dates": True}
    tables["DD1_releases_max_flow"] = {
                          "url": "data/reservoir_releases/DD1.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    data["parameters"]["__DD2_releases__:max_flow"] = {
                    "type": "dataframe",
                    "table": "DD2_releases_max_flow",
                    "index_col": 0,
                    "parse_dates": True}
    tables["DD2_releases_max_flow"] = {
                          "url": "data/reservoir_releases/DD2.xlsx",
                          "index_col": "index",
                          "header": 0,
                          "parse_dates": True}
    for node in data['nodes']:
        if node['name'] == 'Groot_release':
            node["cost"] = -1000
            node["max_flow"] = 0#"__Groot_releases__:max_flow"
        if node['name'] == 'DD1_release':
            node["cost"] = -1000
            node["max_flow"] = 0#"__DD1_releases__:max_flow"
        if node['name'] == 'DD2_release':
            node["cost"] = -1000
            node["max_flow"] = 0#"__DD2_releases__:max_flow"

    
    data["tables"] = tables
    data["parameters"]["control_curve"] =  {
                                            "type": "monthlyprofile",
                                            "values": [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
                                            }
    data["parameters"]["Groot_transfer_controller"] = {
                                            "type": "controlcurve",
                                            "storage_node": "Grootdraai_Dam",
                                            "control_curve": "control_curve",
                                            "values": [0.0, 10.0]}
    #other changes
    for node in data['nodes']:
        if node['name'] == 'Grootdraai_Dam':
            node["cost"] = -500
            node["initial_volume"] = 347.46
            #node["max_volume"] = 500
        if node['name'] == 'DD1':
            node["cost"] = -500
        if node['name'] == 'DD2':
            node["cost"] = -500
        if node['name'] == 'Groot_spill':
            node["cost"] = 100000
        if node['name'] == 'DD1_spill':
            node["cost"] = 100000
        if node['name'] == 'DD2_spill':
            node["cost"] = 100000
    return data



def update_recorders(data):
    """!
    Updates a JSON file with any additional recorders needed. 
    @param data - json model read into memory
    @return data - json model in memory with additional recorders
    """
    recorders = {}

    for node in data['nodes']:
        node_name = node['name']
        if node['type'] == 'storage':
            recorders["__" + node_name + "__:sv_recorder"] = {"type": "NumpyArrayStorageRecorder", "node": node_name}
        else:
            recorders["__" + node_name + "__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": node_name}
        
    #recorders["__Grootdraai_Dam__:sv_recorder"] = {"type": "NumpyArrayStorageRecorder", "node": "Grootdraai_Dam"} 
    #recorders["__DD1__:sv_recorder"] = {"type": "NumpyArrayStorageRecorder", "node": "DD1"} 
    #recorders["__DD2__:sv_recorder"] = {"type": "NumpyArrayStorageRecorder", "node": "DD2"} 
    
    #recorders["__Node_402__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Node_402"}
    #recorders["__Node_372__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Node_372"}
    #recorders["__Node_373__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Node_373"}
    #recorders["__Node_34__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Node_34"}
    #recorders["__Node_374__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Node_374"}
    #recorders["__Node_392__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Node_392"}
    #recorders["__Node_402__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Node_402"}
    #recorders["__Node_100__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Node_100"}
    #recorders["__Groot_spill__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Groot_spill"}
    #recorders["__Groot_release__:flow_recorder"] = {"type": "NumpyArrayNodeRecorder", "node": "Groot_release"}
    
    data["recorders"] = recorders
    return data


