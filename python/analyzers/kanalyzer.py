import ROOT
from itertools import product, combinations
import math
from copy import deepcopy as dc

from PhysicsTools.Heppy.analyzers.core.Analyzer      import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle    import AutoHandle
###from PhysicsTools.HeppyCore.utils.deltar             import deltaR, deltaR2, bestMatch
###from PhysicsTools.Heppy.physicsobjects.Muon          import Muon
from PhysicsTools.Heppy.physicsobjects.Electron      import Electron
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject


from pdb import set_trace # debug set_trace()

##########################################################################################
class kanalyzer(Analyzer):
    '''
    '''
    def __init__(self, *args, **kwargs):
        super(kanalyzer, self).__init__(*args, **kwargs)

    def declareHandles(self):
        super(kanalyzer, self).declareHandles()

        # miniAOD collections
        self.handles['electrons' ] = AutoHandle('slimmedElectrons'             , 'std::vector<pat::Electron>'       )
##        self.handles['muons'     ] = AutoHandle('slimmedMuons'                 , 'std::vector<pat::Muon>'           )
        self.handles['losttracks'] = AutoHandle('lostTracks'                   , 'std::vector<pat::PackedCandidate>')
        self.handles['pfcands'   ] = AutoHandle('packedPFCandidates'           , 'std::vector<pat::PackedCandidate>')
        self.handles['pvs'       ] = AutoHandle('offlineSlimmedPrimaryVertices', 'std::vector<reco::Vertex>'        )
        
        # AOD collections
        self.handles['beamspot'  ] = AutoHandle('offlineBeamSpot', 'reco::BeamSpot')

    def beginLoop(self, setup):
        super(kanalyzer, self).beginLoop(setup)
        self.counters.addCounter('kanalyzer')
        count = self.counters.counter('kanalyzer')
        count.register('all events')
        count.register('>= 1 electron')

    def process(self, event):
        self.readCollections(event.input)

        self.counters.counter('kanalyzer').inc('all events')

        # vertex stuff
        event.pvs         = self.handles['pvs'     ].product()
        event.beamspot    = self.handles['beamspot'].product()

        # get the tracks
#        allpf      = self.handles['pfcands'   ].product()
        allpf      = map(PhysicsObject, self.handles['pfcands'   ].product())
        losttracks      = map(PhysicsObject, self.handles['losttracks'   ].product())

        # merge the track collections
        event.alltracks = sorted([tt for tt in allpf + losttracks if tt.charge() != 0 and abs(tt.pdgId()) not in (11,13)], key = lambda x : x.pt(), reverse = True)
        
        # get the offline electrons and muons
        event.electrons = map(Electron, self.handles['electrons'].product())

        # it sems that the electron mass is derived from E^2 - p^2 and this
        # causes artificial fluctuations up to 20 MeV that can be relevant for our case
        for ele in event.electrons:
            ele.setMass(0.000511)


        # preselect electrons
        event.electrons = [ele for ele in event.electrons if self.testEle(ele)]

        # at least two electrons  
        if len(event.electrons)>0: 
            self.counters.counter('kanalyzer').inc('>= 1 electron')

        # build all di-ele pairs
        #dieles = [(ele1, ele2) for ele1, ele2 in combinations(event.electrons, 2)]
        # opposite sign di-muon
        #dieles = [(ele1, ele2) for ele1, ele2 in dieles if ele1.charge() != ele2.charge()]
        return True

    
    def testEle(self, ele):
        return ele.pt()>2.        and \
               abs(ele.eta())<2.5 
    
    
    
