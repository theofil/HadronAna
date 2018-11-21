import ROOT
from CMGTools.HadronAna.analyzers.L1PurityTreeProducerBase import L1PurityTreeProducerBase
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi
from itertools import combinations

class kanalyzerTreeProducer(L1PurityTreeProducerBase):

    '''
    '''

    def declareVariables(self, setup):
        '''
        '''
        self.bookEvent(self.tree)
        
        self.bookParticle(self.tree, 'l1')
        self.var(self.tree, 'nTracks')
        
    def process(self, event):
        '''
        '''
        self.readCollections(event.input)
        self.tree.reset()

        self.fillEvent(self.tree, event)

        if len(event.electrons)>0: self.fillParticle(self.tree, 'l1', event.electrons[0])

        self.fill(self.tree, 'nTracks', len(event.alltracks))
                    
        self.fillTree(event)


