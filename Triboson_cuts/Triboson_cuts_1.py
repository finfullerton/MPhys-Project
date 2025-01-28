import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

def import_data():
    tree = uproot.open('../Delphes/delphes_output.root:Delphes')
    events = tree.arrays(['Event.Weight', 'Electron.PT', 'Muon.PT', 'Electron.Eta', 'Muon.Eta', 'Electron.Phi', 'Muon.Phi'])
    #print(tree.keys())

    return events

def lepton_cuts(events):
    muon_pt = ak.flatten(events['Muon.PT'])
    muon_pt_mask = ak.flatten(events['Muon.PT'] < 25)
    filtered_muon_pt = muon_pt[muon_pt_mask]
    print(len(muon_pt))
    print(len(filtered_muon_pt))
    plot_pt(muon_pt)
    plot_pt(filtered_muon_pt)

    #plt.hist(muon_pt, bins=50, range=(np.min(muon_pt), np.max(muon_pt)))
    plt.hist(filtered_muon_pt, bins=50, range=(np.min(filtered_muon_pt), np.max(filtered_muon_pt)))

    plt.xlabel('Mass [GeV]')
    plt.ylabel('Events')
    plt.show()
    plt.savefig("dimuon_mass.png")

def plot_pt(pt):
    plt.hist(pt,bins=50, range=(np.min(pt), np.max(pt)))

    plt.xlabel('Mass [GeV]')
    plt.ylabel('Events')
    plt.show()
    plt.savefig("dimuon_mass.png")

    
def main():
    events = import_data()
    lepton_cuts(events)

main()
