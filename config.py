import os

if 'CMSSW_BASE' in os.environ:
    cmssw_base = os.environ['CMSSW_BASE']
else:
    cmssw_base = ''


cfg = {}

cfg['ntuplizer_cfg'] = cmssw_base + '/src/RecoEgamma/ElectronIdentification/python/Training/ElectronMVATrainingNtuplizer_cfg.py'

cfg['storage_site'] = 'T2_FR_GRIF_LLR'
cfg["submit_version"] = "20180323_EleMVATraining"
# Location of CRAB output files
cfg["crab_output_dir"] = '/store/user/rembserj/Egamma/%s' % cfg["submit_version"]
cfg["crab_output_dir_full"] = "/dpm/in2p3.fr/home/cms/trivcat%s" % cfg["crab_output_dir"]
# Where to store the ntuples and dmatrices
cfg["ntuple_dir"] = "/home/llr/cms/rembser/data/Egamma"
cfg['dmatrix_dir'] = "/home/llr/cms/rembser/data/Egamma"
cfg['out_dir'] = "out"

# The sample used for training and evaluating the xgboost classifier.
cfg["train_eval_sample"] = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1/MINIAODSIM'
cfg["train_eval_sample_request_name"] = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8'

# The fraction of this sample used for training.
cfg["train_size"] = 0.5

# The sample used for unbiased testing (performance plots).
cfg["test_sample"] = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10_ext1-v1/MINIAODSIM'
cfg["test_sample_request_name"] = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8-ext1'

cfg["selection_base"] = "genNpu > 1"
cfg[ "selection_sig"]  = "matchedToGenEle == 1"
cfg[ "selection_bkg"]  = "matchedToGenEle == 0 || matchedToGenEle == 3"

# Define lists of variables used for training
variables_base = [
             "ele_oldsigmaietaieta", "ele_oldsigmaiphiiphi",
             "ele_oldcircularity", "ele_oldr9", "ele_scletawidth",
             "ele_sclphiwidth", "ele_oldhe", "ele_kfhits", "ele_kfchi2",
             "ele_gsfchi2", "ele_fbrem", "ele_gsfhits",
             "ele_expected_inner_hits", "ele_conversionVertexFitProbability",
             "ele_ep", "ele_eelepout", "ele_IoEmIop", "ele_deltaetain",
             "ele_deltaphiin", "ele_deltaetaseed", "rho",
            ]

variables_ee_only = ["ele_psEoverEraw"]

variables_iso_only = ["ele_pfPhotonIso", "ele_pfChargedHadIso", "ele_pfNeutralHadIso"]

variables_noiso_eb = variables_base
variables_noiso_ee = variables_base + variables_ee_only
variables_iso_eb = variables_noiso_eb + variables_iso_only
variables_iso_eb = variables_noiso_ee + variables_iso_only

# Define sets of hyperparameters to be used in the training

params = {}
params["EB1_5"] = {
        'max_depth': 4,
        'min_child_weight' : 500.,
        'gamma' : 10,
        'balance_sample' : True,
        }
params["EB2_5"] = {
        'max_depth': 4,
        'min_child_weight' : 2000.,
        'gamma' : 15,
        'balance_sample' : True,
        }
params["EE_5"] = {
        'max_depth': 4,
        'min_child_weight' : 2000.,
        'gamma' : 15,
        'balance_sample' : True,
        }
params["EB1_10"] = {
        'max_depth': 4,
        'min_child_weight' : 500.,
        'gamma' : 0,
        }
params["EB2_10"] = params["EB1_10"]
params["EE_10"] = params["EB1_10"]

# Configure the different trainings.
# For each bin, you have:
#     - cut
#     - list of variables to use
#     - set of hyperparameters

cfg["trainings"] = {}

# NoIso ID
cfg["trainings"]["NoIso_EB1_5"] = {
        "cut": "ele_pt < 10. && abs(scl_eta) < 0.800",
        "variables": variables_noiso_eb,
        "params": params["EB1_5"],
        }

cfg["trainings"]["NoIso_EB2_5"] = {
        "cut": "ele_pt < 10. && abs(scl_eta) >= 0.800 && abs(scl_eta) < 1.479",
        "variables": variables_noiso_eb,
        "params": params["EB2_5"],
        }

cfg["trainings"]["NoIso_EE_5"] = {
        "cut": "ele_pt < 10. && abs(scl_eta) >= 1.479",
        "variables": variables_noiso_ee,
        "params": params["EE_5"],
        }

cfg["trainings"]["NoIso_EB1_10"] = {
        "cut": "ele_pt >= 10. && abs(scl_eta) < 0.800",
        "variables": variables_noiso_eb,
        "params": params["EB1_10"],
        }

cfg["trainings"]["NoIso_EB2_10"] = {
        "cut": "ele_pt >= 10. && abs(scl_eta) >= 0.800 && abs(scl_eta) < 1.479",
        "variables": variables_noiso_eb,
        "params": params["EB2_10"],
        }

cfg["trainings"]["NoIso_EE_10"] = {
        "cut": "ele_pt >= 10. && abs(scl_eta) >= 1.479",
        "variables": variables_noiso_ee,
        "params": params["EE_10"],
        }

# Iso ID
cfg["trainings"]["Iso_EB1_5"] = {
        "cut": "ele_pt < 10. && abs(scl_eta) < 0.800",
        "variables": variables_noiso_eb,
        "params": params["EB1_5"],
        }

cfg["trainings"]["Iso_EB2_5"] = {
        "cut": "ele_pt < 10. && abs(scl_eta) >= 0.800 && abs(scl_eta) < 1.479",
        "variables": variables_noiso_eb,
        "params": params["EB2_5"],
        }

cfg["trainings"]["Iso_EE_5"] = {
        "cut": "ele_pt < 10. && abs(scl_eta) >= 1.479",
        "variables": variables_noiso_ee,
        "params": params["EE_5"],
        }

cfg["trainings"]["Iso_EB1_10"] = {
        "cut": "ele_pt >= 10. && abs(scl_eta) < 0.800",
        "variables": variables_noiso_eb,
        "params": params["EB1_10"],
        }

cfg["trainings"]["Iso_EB2_10"] = {
        "cut": "ele_pt >= 10. && abs(scl_eta) >= 0.800 && abs(scl_eta) < 1.479",
        "variables": variables_noiso_eb,
        "params": params["EB2_10"],
        }

cfg["trainings"]["Iso_EE_10"] = {
        "cut": "ele_pt >= 10. && abs(scl_eta) >= 1.479",
        "variables": variables_noiso_ee,
        "params": params["EE_10"],
        }
