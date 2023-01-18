import click
import os
import json
from pywr.core import Model
import pandas
import logging
logger = logging.getLogger(__name__)
import numpy as np
from . import process_json
from . import WQ_model
from . import flow_WQ_integration
from . import parameters
import warnings
import tables
import timeit

@click.group()
def cli():
    pass


def start_cli():
    cli()



@cli.command('run')
@click.argument('filename', type=click.Path(dir_okay=False))
@click.option('--debug/--no-debug', default=False)


def run(filename, debug):
    """!
        Runs a Pywr model stipulated as a JSON file to generate flow. 
        The output file is a .h5 file and is output to the 'results' folder. The outputs 
        depend on recorders stipulated in the JSON file. You don't need to generate the flow
        first to run the water quality model, i.e., you don't need to run this function if you 
        are wanting to run the water quality model
        @param filename - the name of the JSON file
        @param debug - set to False by default
    """
    logger.info('Loading model from file: "{}"'.format(filename))
    #print(model_run)
    base = filename[:filename.find('.')]
    with open(filename) as fh:
        data = json.load(fh)
    m = Model.load(data, solver='glpk-edge')
   

    m.setup()

    if debug:
        m.step()
        import pdb; pdb.set_trace()
        return
    else:
        res = m.run()
    with pandas.HDFStore(os.path.join('results', f"{base}_dataframes_results.h5"), mode='w') as store:
        for rec in m.recorders:
            if hasattr(rec, 'to_dataframe'):
                df = rec.to_dataframe()
                store[rec.name] = df

    logger.info('Complete! :)')
    


@cli.command('update-json')
@click.argument('filename', type=click.Path(dir_okay=False))
@click.argument('output', type=click.Path(dir_okay=False))

def update_json(filename, output):
    """!
    Updates a JSON file with input data and any additional parameters. 
    Typically, the model topology can be created on the online Pywr at www.waterstrategy.org. The 
    model can be exported as a Pywr JSON. This function can then be called to update the JSON with 
    forcing data and any additional parameters needed
    @param filename - the name of the JSON file
    @param output - the name of the updated JSON file
    """

    with open(filename) as fh:
        data = json.load(fh)
    data = process_json.update_json(data)
    #m = Model.load(data)
    with open(output, mode='w') as fh:
        json.dump(data, fh, indent=2)


@cli.command('update-recorders')
@click.argument('filename', type=click.Path(dir_okay=False))
@click.argument('output', type=click.Path(dir_okay=False))

def update_recorders(filename, output):
    """!
    Updates a JSON file with any additional recorders . 
    This function can then be called to update the JSON with any additional recorders needed
    @param filename - the name of the JSON file
    @param output - the name of the updated JSON file
    """
    with open(filename) as fh:
        data = json.load(fh)
    data = process_json.update_recorders(data)
    #m = Model.load(data)
    with open(output, mode='w') as fh:
        json.dump(data, fh, indent=2)



 
    
@cli.command('run-WQ')
@click.argument('filename', type=click.Path(dir_okay=False))

def run_WQ(filename):
    """!
    Runs the water quality model. Requires a Pywr model stipulated as a JSON file. Also
    requires a JSON file in which water quality parameters are stipulated for nodes, given the
    same name as the Pywr JSON file with the suffix "_WQ". For example, if the filename parameter
    is "test_catchment.json", the json with water quality parameters would be "test_catchment_WQ.json"
    @param filename - the name of the pywr JSON file
    """
    start = timeit.default_timer()
    base = filename[:filename.find('.')]
    with open(filename) as fh:
        data = json.load(fh)
    with open(base + "_WQ.json") as fh:
        data_WQ = json.load(fh)
    flow_model = Model.load(data, solver='glpk-edge')
    logger = logging.getLogger("")
    wq_model = WQ_model.WQ_Model()
    #The node order is set to stipulate the order in which water quailty loads are routed down the system. Only link and reservoir nodes
    #need to be considered, i.e., no need to include abstractions and inflow nodes. This solution is not ideal as it is not a generic solution.
    node_order = {"Node_34": 0, "Node_372": 0, "Node_7004": 0, "Node_373": 0, "DD1": 0, "DD1_release": 0, 
                  "DD1_spill": 0, "Node_287": 0, "Node_100": 0, "Node_374": 0, "DD2": 0, "DD2_spill": 0,
                 "DD2_release": 0, "Node_7005": 0, "Node_392": 0, "Node_402": 0, "Grootdraai_Dam": 0,
                 "Groot_spill": 0, "Groot_release": 0, "Node_412": 0}
    #storage nodes are stipulated as Pywr needs to know whether to pass volume or flow to the water quality model.
    #this solution is also not ideal as it is not generic and needs to be changed for every model application
    storage_nodes = ["DD1", "DD2", "Grootdraai_Dam"]
    integrated_Model = flow_WQ_integration.WQ_Flow_Integration(flow_model, wq_model, data_WQ, node_order, storage_nodes)
    integrated_Model.run()
    #saves flow data according to recorders set in the Pywr model JSON. Water quality outputs are saved in a different way
    with pandas.HDFStore(os.path.join('results', f"{base}_dataframes_results.h5"), mode='w') as store:
        for rec in flow_model.recorders:
            if hasattr(rec, 'to_dataframe'):
                df = rec.to_dataframe()
                store[rec.name] = df
    

    stop = timeit.default_timer()

    print('Time: ', stop - start)
