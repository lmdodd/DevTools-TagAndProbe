import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

process = cms.Process("tnp")

###################################################################
options = dict()
varOptions = VarParsing('analysis')
varOptions.register(
    "isMC",
    True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Compute MC efficiencies"
    )

varOptions.parseArguments()

options['isMC']                    = varOptions.isMC
options['HLTProcessName']          = "HLT"
options['ELECTRON_COLL']           = "eleID"
options['ELECTRON_CUTS']           = "(abs(eta)<2.5)"
options['ELECTRON_ID_CUTS']        = "userFloat('PassID')"
options['ELECTRON_TAG_CUTS']       = "(abs(eta)<=2.5) && !(1.4442<=abs(eta)<=1.566) && pt >= 25.0"
options['SUPERCLUSTER_COLL']       = "reducedEgamma:reducedSuperClusters"
options['SUPERCLUSTER_CUTS']       = "abs(eta)<2.5 && !(1.4442< abs(eta) <1.566) && et>10.0"
options['MAXEVENTS']               = cms.untracked.int32(-1) 
options['useAOD']                  = cms.bool(False)
options['DOTRIGGER']               = cms.bool(True)
options['DORECO']                  = cms.bool(True)
options['DOID']                    = cms.bool(True)
options['OUTPUTEDMFILENAME']       = 'edmFile.root'
options['DEBUG']                   = cms.bool(False)

from PhysicsTools.TagAndProbe.treeMakerOptions_cfi import *

if (varOptions.isMC):
    options['INPUT_FILE_NAME']     = varOptions.inputFiles
    options['OUTPUT_FILE_NAME']    = varOptions.outputFile
    options['TnPPATHS']            = cms.vstring()#"HLT_Ele23_WPLoose_Gsf_v*")
    options['TnPHLTTagFilters']    = cms.vstring()#"hltEle23WPLooseGsfTrackIsoFilter")
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring()
    options['GLOBALTAG']           = 'auto:run2_mc'
    options['EVENTSToPROCESS']     = cms.untracked.VEventRange()
else:
    options['INPUT_FILE_NAME']     = varOptions.inputFiles 
    options['OUTPUT_FILE_NAME']    = varOptions.outputFile
    options['TnPPATHS']            = ["HLT_Ele23_WPLoose_Gsf_v*"]
    options['TnPHLTTagFilters']    = ["hltEle23WPLooseGsfTrackIsoFilter"]
    options['TnPHLTProbeFilters']  = cms.vstring()
    options['HLTFILTERTOMEASURE']  = cms.vstring("")
    options['GLOBALTAG']           = 'auto:run2_data'
    options['EVENTSToPROCESS']     = cms.untracked.VEventRange()
    options['json']                = 'Cert_271036-274421_13TeV_PromptReco_Collisions16_JSON.txt'

###################################################################

setModules(process, options)

# manually fix pileup
from SimGeneral.MixingModule.mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi import mix
pu_distribs = { "mc" : mix.input.nbPileupEvents.probValue }

data_pu_distribs = { "golden_v2" : [2.2566754964100775, 1950.7101413328778, 17511.456675455047, 27074.20916127319, 31295.38904638094, 53522.20431560162, 35220.460642050515, 90928.4505886674, 158090.51550539696, 244779.69121570754, 475446.24468129413, 1032094.7569565654, 2867278.6011298, 8427431.69028668, 17066351.233420365, 24027307.400081296, 28582023.0191919, 31161312.562541533, 29834230.38765881, 24016276.70437407, 16773532.053158931, 10934908.81338181, 6882987.985089145, 4078652.637076056, 2188705.6729904166, 1038844.4766897545, 433153.3500083798, 160781.35010697396, 56761.72710812498, 23088.051876630037, 13703.115979318482, 11160.425830582903, 10107.562092362476, 9265.663899467123, 8452.643876626442, 7708.148529163162, 7083.028042403028, 6599.59737809236, 6251.554972113813, 6013.330098038255, 5850.7412552672895, 5728.700884743008, 5612.778750900018, 5486.076394019967, 5335.204681008237, 5152.708506844515, 4936.573628932316, 4688.59937381231, 4413.05262576535, 4115.649709073904, 3802.8200587118135, 3481.1800882296766, 3157.154600542835, 2836.702560279824, 2525.1215607577033, 2226.9167983369393, 1945.7261608204267, 1684.2949902672606, 1444.4940213184038, 1227.3732210270105, 1033.2435191116354, 861.7780761805193, 712.1249032724896, 583.0232918504774, 472.9175407256343, 380.0627464092443, 302.61882216537015, 238.730305964887, 186.5908075849736, 144.49205632995265, 110.85839804233966, 84.26823511318716, 63.464311178194166, 47.35493604185581, 35.00826099036062, 25.641591111449614, 18.607501788495206, 13.378250655929659, 9.529677972026128, 6.725494537916399] }

process.pileupReweightingProducer.pileupMC = cms.vdouble(pu_distribs['mc'])
process.pileupReweightingProducer.PileupData = cms.vdouble(data_pu_distribs["golden_v2"])

from PhysicsTools.TagAndProbe.treeContent_cfi import *

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, options['GLOBALTAG'], '')


process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

process.MessageLogger.cerr.threshold = ''
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options['INPUT_FILE_NAME']),
                            eventsToProcess = options['EVENTSToPROCESS']
                            )

if not varOptions.isMC :
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/'+options['json']).getVLuminosityBlockRange()


process.maxEvents = cms.untracked.PSet( input = options['MAXEVENTS'])

###################################################################
## ID
###################################################################

from PhysicsTools.TagAndProbe.electronIDModules_cfi import *
setIDs(process, options)

# update the collection
eSrc= "eleID"
process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(eSrc)
process.electronMVAValueMapProducer.srcMiniAOD = cms.InputTag(eSrc)
process.electronRegressionValueMapProducer.srcMiniAOD = cms.InputTag(eSrc)
    
process.goodElectronsPROBEMVA80ID = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBEMVA80ID.selection = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80")
process.goodElectronsPROBEMVA80ID.cut = options['ELECTRON_ID_CUTS']

process.goodElectronsPROBEHTTID = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBEHTTID.selection = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80")
process.goodElectronsPROBEHTTID.cut = cms.string("userFloat('PassID')")

process.goodElectronsPROBEHTTISO = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBEHTTISO.selection = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80")
process.goodElectronsPROBEHTTISO.cut = cms.string("userFloat('PassISO')")

process.goodElectronsPROBEHTTIDISO = process.goodElectronsPROBECutBasedVeto.clone()
process.goodElectronsPROBEHTTIDISO.selection = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80")
process.goodElectronsPROBEHTTIDISO.cut = cms.string("userFloat('PassIDISO')")



###############
### Trigger ###
###############
process.goodElectronsMeasureHLT = cms.Sequence()

process.goodElectronsMeasureHLTEle23 = cms.EDProducer("PatElectronTriggerCandProducer",
                                                filterNames = cms.vstring("hltEle23WPLooseGsfTrackIsoFilter"),
                                                inputs      = cms.InputTag("goodElectronsProbeMeasureHLT"),
                                                bits        = cms.InputTag('TriggerResults::HLT'),
                                                objects     = cms.InputTag('selectedPatTrigger'),
                                                dR          = cms.double(0.1),
                                                isAND       = cms.bool(False)
                                                )
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle23

process.goodElectronsMeasureHLTEle22Eta2p1 = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle22Eta2p1.filterNames = cms.vstring("hltSingleEle22WPLooseGsfTrackIsoFilter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle22Eta2p1

process.goodElectronsMeasureHLTEle24Eta2p1 = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle24Eta2p1.filterNames = cms.vstring("hltSingleEle24WPLooseGsfTrackIsoFilter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle24Eta2p1

process.goodElectronsMeasureHLTEle25Eta2p1 = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle25Eta2p1.filterNames = cms.vstring("hltEle25erWPLooseGsfTrackIsoFilter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle25Eta2p1

process.goodElectronsMeasureHLTEle25Eta2p1Tight = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle25Eta2p1Tight.filterNames = cms.vstring("hltEle25erWPTightGsfTrackIsoFilter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle25Eta2p1Tight


process.goodElectronsMeasureHLTEle27 = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle27.filterNames = cms.vstring("hltEle27noerWPLooseGsfTrackIsoFilter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle27

process.goodElectronsMeasureHLTEle35 = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle35.filterNames = cms.vstring("hltEle35WPLooseGsfTrackIsoFilter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle35

# double electron
process.goodElectronsMeasureHLTEle17 = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle17.filterNames = cms.vstring("hltEle17CaloIdLTrackIdLIsoVLTrackIsoFilter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle17

process.goodElectronsMeasureHLTEle12 = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle12.filterNames = cms.vstring("hltEle12CaloIdLTrackIdLIsoVLTrackIsoFilter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle12

process.goodElectronsMeasureHLTEle17Ele12Leg1 = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle17Ele12Leg1.filterNames = cms.vstring("hltEle17Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg1Filter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle17Ele12Leg1

#process.goodElectronsMeasureHLTEle17Ele12Leg1L1EG15 = cms.EDProducer("PatElectronL1CandProducer",
#        inputs = cms.InputTag("goodElectronsMeasureHLTEle17Ele12Leg1"),
#        isoObjects = cms.InputTag("l1extraParticles:Isolated"),
#        nonIsoObjects = cms.InputTag("l1extraParticles:NonIsolated"),
#        minET = cms.double(15.),
#        dRmatch = cms.double(.5)
#        )
#process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle17Ele12Leg1L1EG15

process.goodElectronsMeasureHLTEle17Ele12Leg2 = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTEle17Ele12Leg2.filterNames = cms.vstring("hltEle17Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg2Filter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTEle17Ele12Leg2

process.goodElectronsMeasureHLTMu17Ele12ELeg = process.goodElectronsMeasureHLTEle23.clone()
process.goodElectronsMeasureHLTMu17Ele12ELeg.filterNames = cms.vstring("hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter")
process.goodElectronsMeasureHLT += process.goodElectronsMeasureHLTMu17Ele12ELeg

###################################################################
## SEQUENCES
###################################################################
process.eleID = cms.EDProducer(
    "MiniAODElectronVIDEmbedder",
    src = cms.InputTag("slimmedElectrons"),
    vertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)


process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(options['ELECTRON_COLL'])
process.ele_sequence = cms.Sequence(
    process.goodElectrons +
    process.egmGsfElectronIDSequence +
    process.goodElectronsPROBECutBasedVeto +
    process.goodElectronsPROBECutBasedLoose +
    process.goodElectronsPROBECutBasedMedium +
    process.goodElectronsPROBECutBasedTight +
    process.goodElectronsPROBEMVA80 +
    process.goodElectronsPROBEMVA80ID +
    process.goodElectronsPROBEMVA90 +
    process.goodElectronsPROBEHTTID +
    process.goodElectronsPROBEHTTISO +
    process.goodElectronsPROBEHTTIDISO +
    process.goodElectronsTAGCutBasedVeto +
    process.goodElectronsTAGCutBasedLoose +
    process.goodElectronsTAGCutBasedMedium +
    process.goodElectronsTAGCutBasedTight +
    process.goodElectronsTagHLT +
    process.goodElectronsProbeHLT +
    process.goodElectronsProbeMeasureHLT +
    process.goodElectronsMeasureHLT
    )

process.sc_sequence = cms.Sequence(process.superClusterCands +
                                   process.goodSuperClusters +
                                   process.goodSuperClustersHLT +
                                   process.GsfMatchedSuperClusterCands
                                   )

###################################################################
## TnP PAIRS
###################################################################

process.allTagsAndProbes = cms.Sequence()

if (options['DOTRIGGER']):
    process.allTagsAndProbes *= process.tagTightHLT

if (options['DORECO']):
    process.allTagsAndProbes *= process.tagTightSC

if (options['DOID']):
    process.allTagsAndProbes *= process.tagTightRECO

process.mc_sequence = cms.Sequence()

#if (varOptions.isMC):
#    process.mc_sequence *= (process.McMatchHLT + process.McMatchTag + process.McMatchSC + process.McMatchRECO)

##########################################################################
## TREE MAKER OPTIONS
##########################################################################
if (not varOptions.isMC):
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(False)
        )

# remove sc stuff that is broken
del CommonStuffForGsfElectronProbe.variables.probe_sc_energy
del CommonStuffForGsfElectronProbe.variables.probe_sc_et
del CommonStuffForGsfElectronProbe.variables.probe_sc_eta
del CommonStuffForGsfElectronProbe.variables.probe_sc_abseta
del CommonStuffForGsfElectronProbe.tagVariables.sc_energy
del CommonStuffForGsfElectronProbe.tagVariables.sc_et
del CommonStuffForGsfElectronProbe.tagVariables.sc_eta
del CommonStuffForGsfElectronProbe.tagVariables.sc_abseta
del CommonStuffForSuperClusterProbe.tagVariables.sc_energy
del CommonStuffForSuperClusterProbe.tagVariables.sc_et
del CommonStuffForSuperClusterProbe.tagVariables.sc_eta
del CommonStuffForSuperClusterProbe.tagVariables.sc_abseta

process.GsfElectronToTrigger = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                              CommonStuffForSuperClusterProbe, mcTruthCommonStuff,
                                              tagProbePairs = cms.InputTag("tagTightHLT"),
                                              arbitration   = cms.string("Random2"),
                                              flags         = cms.PSet(
                                                  passingHLTEle22Eta2p1    = cms.InputTag("goodElectronsMeasureHLTEle22Eta2p1"),
                                                  passingHLTEle24Eta2p1    = cms.InputTag("goodElectronsMeasureHLTEle24Eta2p1"),
                                                  passingHLTEle25Eta2p1    = cms.InputTag("goodElectronsMeasureHLTEle25Eta2p1"),
                                                  passingHLTEle25Eta2p1Tight    = cms.InputTag("goodElectronsMeasureHLTEle25Eta2p1Tight"),
                                                  passingHLTEle23    = cms.InputTag("goodElectronsMeasureHLTEle23"),
                                                  passingHLTEle27    = cms.InputTag("goodElectronsMeasureHLTEle27"),
                                                  passingHLTEle35    = cms.InputTag("goodElectronsMeasureHLTEle35"),
                                                  passingHLTEle17    = cms.InputTag("goodElectronsMeasureHLTEle17"),
                                                  passingHLTEle12    = cms.InputTag("goodElectronsMeasureHLTEle12"),
                                                  passingHLTEle17Ele12Leg1    = cms.InputTag("goodElectronsMeasureHLTEle17Ele12Leg1"),
                                                  passingHLTEle17Ele12Leg2    = cms.InputTag("goodElectronsMeasureHLTEle17Ele12Leg2"),
                                                  passingHLTMu17Ele12ELeg     = cms.InputTag("goodElectronsMeasureHLTMu17Ele12ELeg"),
                                                                       ),                                               
                                              allProbes     = cms.InputTag("goodElectronsProbeMeasureHLT"),
                                              )

if (varOptions.isMC):
    #process.GsfElectronToTrigger.probeMatches  = cms.InputTag("McMatchHLT")
    process.GsfElectronToTrigger.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToTrigger.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")

process.GsfElectronToSC = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                         CommonStuffForSuperClusterProbe, mcTruthCommonStuff,
                                         tagProbePairs = cms.InputTag("tagTightSC"),
                                         arbitration   = cms.string("Random2"),
                                         flags         = cms.PSet(passingRECO   = cms.InputTag("GsfMatchedSuperClusterCands", "superclusters"),         
                                                                  ),                                               
                                         allProbes     = cms.InputTag("goodSuperClustersHLT"),
                                         )

if (varOptions.isMC):
    #process.GsfElectronToSC.probeMatches  = cms.InputTag("McMatchSC")
    process.GsfElectronToSC.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToSC.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")

process.GsfElectronToRECO = cms.EDAnalyzer("TagProbeFitTreeProducer",
                                           mcTruthCommonStuff, CommonStuffForGsfElectronProbe,
                                           tagProbePairs = cms.InputTag("tagTightRECO"),
                                           arbitration   = cms.string("Random2"),
                                           flags         = cms.PSet(passingVeto   = cms.InputTag("goodElectronsPROBECutBasedVeto"),
                                                                    passingLoose  = cms.InputTag("goodElectronsPROBECutBasedLoose"),
                                                                    passingMedium = cms.InputTag("goodElectronsPROBECutBasedMedium"),
                                                                    passingTight  = cms.InputTag("goodElectronsPROBECutBasedTight"),
                                                                    passingMVA80  = cms.InputTag("goodElectronsPROBEMVA80"),
                                                                    passingMVA90  = cms.InputTag("goodElectronsPROBEMVA90"),
                                                                    passingMVA80ID  = cms.InputTag("goodElectronsPROBEMVA80ID"),
                                                                    passingHTTID  = cms.InputTag("goodElectronsPROBEHTTID"),
                                                                    passingHTTIDISO  = cms.InputTag("goodElectronsPROBEHTTIDISO"),
                                                                    passingHTTISO  = cms.InputTag("goodElectronsPROBEHTTISO")
                                                                    ),                                               
                                           allProbes     = cms.InputTag("goodElectronsProbeHLT"),
                                           )

if (varOptions.isMC):
    #process.GsfElectronToRECO.probeMatches  = cms.InputTag("McMatchRECO")
    process.GsfElectronToRECO.eventWeight   = cms.InputTag("generator")
    process.GsfElectronToRECO.PUWeightSrc   = cms.InputTag("pileupReweightingProducer","pileupWeights")

process.tree_sequence = cms.Sequence()
if (options['DOTRIGGER']):
    process.tree_sequence *= process.GsfElectronToTrigger

if (options['DORECO']):
    process.tree_sequence *= process.GsfElectronToSC

if (options['DOID']):
    process.tree_sequence *= process.GsfElectronToRECO

##########################################################################
## PATHS
##########################################################################

process.out = cms.OutputModule("PoolOutputModule", 
                               fileName = cms.untracked.string(options['OUTPUTEDMFILENAME']),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring("p"))
                               )
process.outpath = cms.EndPath(process.out)
if (not options['DEBUG']):
    process.outpath.remove(process.out)

if (varOptions.isMC):
    process.p = cms.Path(
        process.sampleInfo +
        process.hltFilter +
        process.eleID +
        process.ele_sequence + 
        process.sc_sequence +
        process.allTagsAndProbes +
        process.pileupReweightingProducer +
        process.mc_sequence +
        process.eleVarHelper +
        process.tree_sequence
        )
else:
    process.p = cms.Path(
        process.sampleInfo +
        process.hltFilter +
        process.eleID +
        process.ele_sequence + 
        process.sc_sequence +
        process.allTagsAndProbes +
        process.mc_sequence +
        process.eleVarHelper +
        process.tree_sequence
        )

process.TFileService = cms.Service(
    "TFileService", fileName = cms.string(options['OUTPUT_FILE_NAME']),
    closeFileFast = cms.untracked.bool(True)
    )
