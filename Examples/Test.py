def muon_cuts(events):
    total_weight = len(events['Event.Weight'])
    electron_size_mask = events['Electron_size'] == 1
    muon_size_mask = events['Muon_size'] == 1
    unfiltered_electron_events = events[electron_size_mask]  # Just one electrons selected
    unfiltered_muon_events = events[muon_size_mask]  # Just one muons selected

    electron_pt = unfiltered_electron_events['Electron.PT']
    electron_eta = unfiltered_electron_events['Electron.Eta']
    muon_pt = unfiltered_muon_events['Muon.PT']
    muon_eta = unfiltered_muon_events['Muon.Eta']

    muon_pt_mask = muon_pt > 20
    muon_eta_mask = np.abs(muon_eta) < 2.5


    total_mask = muon_pt_mask & muon_eta_mask
    filtered_mask = ak.sum(total_mask, axis=1) == 2  # Ensure there are exactly 2 muons passing the cuts

    filtered_muon_pt=muon_pt[total_mask]
    filtered_events = unfiltered_events[filtered_mask]

    filtered_muons = vector.zip({
        'pt': filtered_events['Muon.PT'],
        'eta': filtered_events['Muon.Eta'],
        'phi': filtered_events['Muon.Phi'],
        'mass': m_mu
    })

    unfiltered_muons = vector.zip({
        'pt': unfiltered_events['Muon.PT'],
        'eta': unfiltered_events['Muon.Eta'],
        'phi': unfiltered_events['Muon.Phi'],
        'mass': m_mu
    })

    dimuon_mass = invariant_mass_calc(unfiltered_muons)
    filtered_dimuon_mass = invariant_mass_calc(filtered_muons)
    plot_pt(muon_pt, filtered_muon_pt, "Muon")
    plot_mass(total_weight, dimuon_mass, filtered_dimuon_mass, "Dimuon")