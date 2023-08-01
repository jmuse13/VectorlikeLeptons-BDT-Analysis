max_depth = {
        "Four_emu": 13,
        "Two_emuSSOF_One_ta": 5,
        "Two_emu_Two_ta": 11,
        "Two_emuOSSF_One_ta": 11,
        "Three_emu_One_ta": 15,
        "Two_emuOSOF_One_ta": 11,
        "Two_emuSSSF_One_ta": 7
}
max_features = {
        "Four_emu": 1.0,
        "Two_emuSSOF_One_ta": 0.8,
        "Two_emu_Two_ta": 0.8,
        "Two_emuOSSF_One_ta": 0.8,
        "Three_emu_One_ta": 0.8,
        "Two_emuOSOF_One_ta": 1.0,
        "Two_emuSSSF_One_ta": 0.6
}
min_samples_split = {
        "Four_emu": 0.6,
        "Two_emuSSOF_One_ta": 0.8,
        "Two_emu_Two_ta": 0.2,
        "Two_emuOSSF_One_ta": 0.2,
        "Three_emu_One_ta": 0.8,
        "Two_emuOSOF_One_ta": 0.8,
        "Two_emuSSSF_One_ta": 0.6
}
min_weight_fraction_leaf = {
        "Four_emu": 0.05,
        "Two_emuSSOF_One_ta": 0.05,
        "Two_emu_Two_ta": 0.2,
        "Two_emuOSSF_One_ta": 0.05,
        "Three_emu_One_ta": 0.05,
        "Two_emuOSOF_One_ta": 0.05,
        "Two_emuSSSF_One_ta": 0.05
}
learning_rate = {
        "Four_emu": 0.2,
        "Two_emuSSOF_One_ta": 0.2,
        "Two_emu_Two_ta": 0.2,
        "Two_emuOSSF_One_ta": 0.2,
        "Three_emu_One_ta": 0.2,
        "Two_emuOSOF_One_ta": 0.4,
        "Two_emuSSSF_One_ta": 0.2
}
n_estimators = {
        "Four_emu": 1510,
        "Two_emuSSOF_One_ta": 1010,
        "Two_emu_Two_ta": 1010,
        "Two_emuOSSF_One_ta": 1010,
        "Three_emu_One_ta": 1010,
        "Two_emuOSOF_One_ta": 1510,
        "Two_emuSSSF_One_ta": 510
}

regionNomVariables = {     
         "Four_emu": ['MET','LTMET','METsig','LT','Minv_light','Minv_light_tau','Minv_jetjet','pT_leadingLep','pT_SubleadingLep','NJet','NBJet','HT','LTHT','Minv_light_jet','Delphi_jet_et','pT_leadingJet','DelR_light_et','Delphi_light_et','DelR_light_light','Delphi_light_light','DelR_jet_light','Delphi_jet_light','MT','DelR_jet_et','pT_leadingTau','Delphi_tau_et','Delphi_tau_light','Delphi_tau_jet','DelR_tau_et','DelR_tau_light','DelR_tau_jet','Minv_tau_jet','LT_tau','mOSSF'],
         "Three_emu_One_ta": ['MET','LTMET','METsig','LT','Minv_light','Minv_light_tau','Minv_jetjet','pT_leadingLep','pT_SubleadingLep','NJet','NBJet','HT','LTHT','Minv_light_jet','Delphi_jet_et','pT_leadingJet','DelR_light_et','Delphi_light_et','DelR_light_light','Delphi_light_light','DelR_jet_light','Delphi_jet_light','MT','DelR_jet_et','pT_leadingTau','Delphi_tau_et','Delphi_tau_light','Delphi_tau_jet','DelR_tau_et','DelR_tau_light','DelR_tau_jet','Minv_tau_jet','LT_tau','mOSSF'],
         "Two_emuOSSF_One_ta": ['MET','LTMET','METsig','LT','Minv_light','Minv_light_tau','Minv_jetjet','pT_leadingLep','pT_SubleadingLep','NJet','NBJet','HT','LTHT','Minv_light_jet','Delphi_jet_et','pT_leadingJet','DelR_light_et','Delphi_light_et','DelR_light_light','Delphi_light_light','DelR_jet_light','Delphi_jet_light','MT','DelR_jet_et','pT_leadingTau','Delphi_tau_et','Delphi_tau_light','Delphi_tau_jet','DelR_tau_et','DelR_tau_light','DelR_tau_jet','Minv_tau_jet','LT_tau','mOSSF'],
         "Two_emuOSOF_One_ta": ['MET','LTMET','METsig','LT','Minv_light','Minv_light_tau','Minv_jetjet','pT_leadingLep','pT_SubleadingLep','NJet','NBJet','HT','LTHT','Minv_light_jet','Delphi_jet_et','pT_leadingJet','DelR_light_et','Delphi_light_et','DelR_light_light','Delphi_light_light','DelR_jet_light','Delphi_jet_light','MT','DelR_jet_et','pT_leadingTau','Delphi_tau_et','Delphi_tau_light','Delphi_tau_jet','DelR_tau_et','DelR_tau_light','DelR_tau_jet','Minv_tau_jet','LT_tau'],
         "Two_emuSSSF_One_ta": ['MET','LTMET','METsig','LT','Minv_light','Minv_light_tau','Minv_jetjet','pT_leadingLep','pT_SubleadingLep','NJet','NBJet','HT','LTHT','Minv_light_jet','Delphi_jet_et','pT_leadingJet','DelR_light_et','Delphi_light_et','DelR_light_light','Delphi_light_light','DelR_jet_light','Delphi_jet_light','MT','DelR_jet_et','pT_leadingTau','Delphi_tau_et','Delphi_tau_light','Delphi_tau_jet','DelR_tau_et','DelR_tau_light','DelR_tau_jet','Minv_tau_jet','LT_tau'],
         "Two_emuSSOF_One_ta": ['MET','LTMET','METsig','LT','Minv_light','Minv_light_tau','Minv_jetjet','pT_leadingLep','pT_SubleadingLep','NJet','NBJet','HT','LTHT','Minv_light_jet','Delphi_jet_et','pT_leadingJet','DelR_light_et','Delphi_light_et','DelR_light_light','Delphi_light_light','DelR_jet_light','Delphi_jet_light','MT','DelR_jet_et','pT_leadingTau','Delphi_tau_et','Delphi_tau_light','Delphi_tau_jet','DelR_tau_et','DelR_tau_light','DelR_tau_jet','Minv_tau_jet','LT_tau'],
         "Two_emu_Two_ta": ['MET','LTMET','METsig','LT','Minv_light','Minv_light_tau','Minv_jetjet','pT_leadingLep','pT_SubleadingLep','NJet','NBJet','HT','LTHT','Minv_light_jet','Delphi_jet_et','pT_leadingJet','DelR_light_et','Delphi_light_et','DelR_light_light','Delphi_light_light','DelR_jet_light','Delphi_jet_light','MT','DelR_jet_et','pT_leadingTau','Delphi_tau_et','Delphi_tau_light','Delphi_tau_jet','DelR_tau_et','DelR_tau_light','DelR_tau_jet','Minv_tau_jet','LT_tau','mOSSF']
}

regionVariables = {
        "Four_emu": ['MET', 'LTMET', 'METsig', 'LT', 'Minv_light_tau', 'pT_leadingLep', 'NJet', 'NBJet', 'HT', 'Minv_light_jet', 'Delphi_jet_et', 'pT_leadingJet', 'DelR_light_et', 'Delphi_light_et', 'DelR_light_light', 'Delphi_light_light', 'DelR_jet_light', 'Delphi_jet_light', 'MT', 'DelR_jet_et', 'Minv_tau_jet', 'mOSSF'],
        "Two_emuSSOF_One_ta": ['MET', 'LTMET', 'METsig', 'LT', 'Minv_light', 'Minv_light_tau', 'Minv_jetjet', 'pT_leadingLep', 'pT_SubleadingLep', 'NJet', 'NBJet', 'HT', 'LTHT', 'Minv_light_jet', 'pT_leadingJet', 'DelR_light_et', 'Delphi_light_et', 'DelR_light_light', 'Delphi_light_light', 'DelR_jet_light', 'Delphi_jet_light', 'MT', 'DelR_jet_et', 'pT_leadingTau', 'Delphi_tau_et', 'Delphi_tau_light', 'Delphi_tau_jet', 'DelR_tau_et', 'DelR_tau_light', 'DelR_tau_jet', 'Minv_tau_jet', 'LT_tau'],
        "Two_emu_Two_ta": ['MET', 'LTMET', 'METsig', 'LT', 'Minv_light', 'Minv_light_tau', 'Minv_jetjet', 'pT_leadingLep', 'pT_SubleadingLep', 'NJet', 'NBJet', 'HT', 'LTHT', 'Minv_light_jet', 'Delphi_jet_et', 'pT_leadingJet', 'DelR_light_et', 'Delphi_light_et', 'DelR_light_light', 'Delphi_light_light', 'DelR_jet_light', 'Delphi_jet_light', 'MT', 'DelR_jet_et', 'pT_leadingTau', 'Delphi_tau_et', 'Delphi_tau_light', 'Delphi_tau_jet', 'DelR_tau_et', 'DelR_tau_light', 'DelR_tau_jet', 'Minv_tau_jet', 'mOSSF'],
        "Two_emuOSSF_One_ta": ['MET', 'LTMET', 'METsig', 'Minv_light', 'Minv_light_tau', 'Minv_jetjet', 'NJet', 'NBJet', 'LTHT', 'Minv_light_jet', 'pT_leadingJet', 'DelR_light_et', 'Delphi_light_et', 'DelR_light_light', 'Delphi_light_light', 'DelR_jet_light', 'Delphi_jet_light', 'MT', 'DelR_jet_et', 'pT_leadingTau', 'Delphi_tau_et', 'Delphi_tau_light', 'Delphi_tau_jet', 'DelR_tau_et', 'DelR_tau_light', 'DelR_tau_jet', 'Minv_tau_jet', 'mOSSF'],
        "Three_emu_One_ta": ['MET', 'LTMET', 'METsig', 'Minv_light', 'Minv_light_tau', 'Minv_jetjet', 'pT_leadingLep', 'NJet', 'NBJet', 'HT', 'Minv_light_jet', 'pT_leadingJet', 'DelR_light_et', 'Delphi_light_et', 'Delphi_light_light', 'Delphi_jet_light', 'MT', 'pT_leadingTau', 'Delphi_tau_et', 'Delphi_tau_light', 'DelR_tau_et', 'DelR_tau_light', 'DelR_tau_jet', 'Minv_tau_jet', 'mOSSF'],
        "Two_emuOSOF_One_ta": ['MET', 'LTMET', 'METsig', 'Minv_light', 'Minv_light_tau', 'Minv_jetjet', 'NJet', 'NBJet', 'HT', 'LTHT', 'Minv_light_jet', 'Delphi_jet_et', 'pT_leadingJet', 'DelR_light_et', 'Delphi_light_et', 'DelR_light_light', 'Delphi_light_light', 'DelR_jet_light', 'Delphi_jet_light', 'MT', 'DelR_jet_et', 'pT_leadingTau', 'Delphi_tau_et', 'Delphi_tau_jet', 'DelR_tau_et', 'DelR_tau_light', 'DelR_tau_jet', 'Minv_tau_jet', 'LT_tau'],
        "Two_emuSSSF_One_ta": ['MET', 'LTMET', 'METsig', 'LT', 'Minv_light', 'Minv_light_tau', 'Minv_jetjet', 'pT_leadingLep', 'pT_SubleadingLep', 'NJet', 'NBJet', 'Minv_light_jet', 'pT_leadingJet', 'DelR_light_et', 'Delphi_light_et', 'DelR_light_light', 'Delphi_light_light', 'DelR_jet_light', 'Delphi_jet_light', 'MT', 'DelR_jet_et', 'pT_leadingTau', 'Delphi_tau_et', 'Delphi_tau_jet', 'DelR_tau_et', 'DelR_tau_light', 'DelR_tau_jet', 'Minv_tau_jet', 'LT_tau']
}
