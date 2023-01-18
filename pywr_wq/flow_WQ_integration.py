#import logging


class WQ_Flow_Integration:
    """!
    Integrates the Pywr model with the water quality model. 
    """
    
    def __init__(self, pywrmodel, wq_model, data_WQ, node_order, storage_nodes):
        self.flow_model = pywrmodel
        pywrmodel.parent = self
        self.wq_model = wq_model
        wq_model.parent = self
        self.data_WQ = data_WQ
        self.node_order = node_order
        self.storage_nodes = storage_nodes
        
    def setup(self, profile=False, profile_dump_filename=None):
        profilers = {}

        # Setup the Pywr model    
        #_ = self.flow_model.setup(profile=profile)
        _ = self.flow_model.setup()
        # Setup the WQ model??
        self.wq_model.setup(self.data_WQ)
        self.wq_model.set_node_order(self.node_order)
        # Perform any other checks??
        
    def reset(self):        
        self.flow_model.reset()
        # Reset the WQ model??
        # self.wq_model.reset() 

    def _step(self, timestep):
        # Run one time-step of the Pywr flow model
        #logger.debug(f"Starting time-step of flow-model")
        self.flow_model.before()
        ret = self.flow_model.solve()
        self.flow_model.after()
        #logger.debug(f"Finished time-step of flow-model")
        
        # Now run one time-step of the WQ model
        # Pass the current flows on the network to the WQ model.
        node_flows = {}
        for node in self.flow_model.nodes:
            if node.name in self.storage_nodes:
                node_flows[node.name] = node.volume
            else:
                node_flows[node.name] = node.flow
        self.wq_model.step(node_flows, timestep)
        #print("step")
        return ret

    @property
    def dirty(self) -> bool:
        """Returns true if any of the Pywr model is 'dirty'."""
        return self.flow_model.dirty

    def run(self):
        """Run the flow-wq simulation"""
        #logger.info("Start multi model run ...")

        try:
            if self.dirty:
                self.setup()
            else:
                self.reset()
            
            # Begin time-stepping (this uses the Pywr model time-steps)
            for timestep in self.flow_model.timestepper:
                self.flow_model.timestep = timestep
                # Perform the internal timestep
                _ = self._step(timestep)
            
        finally:            
            self.flow_model.finish()
            # Is there a `.finish()` method on the WQ model?
            self.wq_model.finish()
        return
