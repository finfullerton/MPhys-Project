import uproot
import awkward as ak
import vector
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const

m_e = const.electron_mass / 1000
m_mu = 0.105658

def import_data():
    tree = uproot.open('../Delphes/delphes_output_WWW_QCD=inf.root:Delphes')
    events = tree.arrays(['Event.Weight', 'Electron_size', 'Muon_size', 'Electron.PT', 'Muon.PT', 'Electron.Eta', 'Muon.Eta', 'Electron.Phi', 'Muon.Phi'])

    return events, tree

def electron_cuts(events):
    # Mask to select events with exactly 2 electrons
    electron_size_mask = events['Electron_size'] == 2
    filtered_events = events[electron_size_mask]

    # Apply electron cuts within each event without flattening
    electron_pt = filtered_events['Electron.PT']
    electron_eta = filtered_events['Electron.Eta']

    # Create per-electron mask for PT and Eta
    electron_pt_mask = electron_pt > 20
    electron_eta_mask = np.abs(electron_eta) < 2.47
    exclusion_mask = (np.abs(electron_eta) < 1.37) | (np.abs(electron_eta) > 1.52)
    total_mask = electron_pt_mask & electron_eta_mask & exclusion_mask

    # Apply the per-electron mask to each electron array within each event
    filtered_electron_pt = electron_pt[total_mask]
    filtered_electron_eta = electron_eta[total_mask]

    # Only keep events where exactly two electrons pass the cuts
    valid_event_mask = ak.num(filtered_electron_pt) == 2
    filtered_events = filtered_events[valid_event_mask]
    electrons = vector.zip({
        'pt': filtered_events['Electron.PT'],
        'eta': filtered_events['Electron.Eta'],
        'phi': filtered_events['Electron.Phi'],
        'mass': m_e
    })

    # Compute invariant masses for dielectron pairs
    dielectron_mass = (electrons[:, 0] + electrons[:, 1]).mass

    # Plotting
    plot_mass(dielectron_mass, dielectron_mass, "Electron")


def plot_mass(raw_mass, filtered_mass, flavour):
    plt.hist(raw_mass, bins=50, range=(np.min(raw_mass), np.max(raw_mass)), label="Raw Data")
    plt.hist(filtered_mass, bins=50, range=(np.min(filtered_mass), np.max(filtered_mass)), label="Filtered Data")
    
    # Properly format the title as a single string
    plt.title(f"Raw vs Filtered {flavour} Data")
    plt.xlabel('Mass [GeV]')
    plt.ylabel('Events')
    plt.legend()
    plt.savefig("raw_vs_filtered_electron.png", dpi=1000)
    plt.show()


def __main__():
    events, tree = import_data()
    electron_cuts(events)
    #print_branches(tree)

if __name__ == '__main__':
    __main__()
