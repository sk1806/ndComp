#include "G4RunManager.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4GDMLParser.hh"
#include "G4RotationMatrix.hh"
#include "G4VUserDetectorConstruction.hh"
#include "TGeoManager.h"
#include "TFile.h"
#include "TGeoBBox.h"
#include "TGeoTube.h"
#include <fstream>
#include <string>
#include <iostream>

class MyDetectorConstruction : public G4VUserDetectorConstruction {
public:
    G4VPhysicalVolume* Construct() override {

        // World volume
        G4double worldDx = 6050 * mm;
        G4double worldDy = 13390 * mm;
        G4double worldDz = 6050 * mm;

        // Detector volume
        G4double detectorRmin = 0 * mm;
        G4double detectorRmax = 6000 * mm;
        G4double detectorDz = 13340 * mm;
        // Detector rotation
	
        G4NistManager* nist = G4NistManager::Instance();

        G4Material* vacuum = nist->FindOrBuildMaterial("G4_Galactic");

	G4Box* solidWorld = new G4Box("World", worldDx, worldDy, worldDz);
        G4LogicalVolume* logicWorld = new G4LogicalVolume(solidWorld, vacuum, "World");
        G4VPhysicalVolume* physWorld = new G4PVPlacement(0, G4ThreeVector(), logicWorld, "World", 0, false, 0);

        G4Material* water = nist->FindOrBuildMaterial("G4_WATER");

        G4Tubs* solidDetector = new G4Tubs("logicDetector", detectorRmin, detectorRmax, detectorDz, 0. * deg, 360. * deg);
        G4LogicalVolume* logicDetector = new G4LogicalVolume(solidDetector, water, "logicDetector");

        // Apply rotation
	// 90 degrees around x-axis --> aligned along y-axis with the top going to -ve y
        G4RotationMatrix* rotX = new G4RotationMatrix();
        rotX->rotateX(90 * deg);

        new G4PVPlacement(rotX, G4ThreeVector(), logicDetector, "logicDetector", logicWorld, false, 0);

        return physWorld;
    }
};

void export_to_gdml(G4RunManager* runManager, std::string name) {
    G4GDMLParser parser;
    std::string gdmlname = name + ".gdml";
    parser.Write(gdmlname, const_cast<G4VUserDetectorConstruction*>(runManager->GetUserDetectorConstruction())->Construct());
    G4cout << "Geometry exported to geometry.gdml" << G4endl;
}



void convert_units_in_gdml(const std::string& input_filename, const std::string& output_filename) {
// ROOT defaults to cm but we want it in mm
// Trick it by changing units to cm, without changing the numbers, to get an extra factor of 10

    std::ifstream infile(input_filename);
    std::ofstream outfile(output_filename);

    if (!infile.is_open()) {
        std::cerr << "Could not open input file: " << input_filename << std::endl;
        return;
    }
    if (!outfile.is_open()) {
        std::cerr << "Could not open output file: " << output_filename << std::endl;
        return;
    }

    std::string line;
    while (getline(infile, line)) {
        size_t pos = 0;
        while ((pos = line.find("\"mm\"", pos)) != std::string::npos) {
            line.replace(pos, 4, "\"cm\"");
            pos += 4;
        }
        outfile << line << std::endl;
    }

    infile.close();
    outfile.close();
}

void import_gdml_and_export_to_root( bool convert_mm_to_cm, std::string name) {

    // Import the GDML file into ROOT
    std::string gdmlname = name + ".gdml";
    TGeoManager::Import(gdmlname.c_str());
    gGeoManager->SetName("MyGeoManager");


    if (convert_mm_to_cm) {
	std::string newgdmlname = name + "_mm.gdml";
        convert_units_in_gdml(gdmlname.c_str(), newgdmlname.c_str());
        TGeoManager::Import(newgdmlname.c_str());  // Re-import after conversion
        gGeoManager->SetName("MyGeoManager");
    }

    // Save the geometry to a ROOT file
    std::string rootname = name + ".root";
    TFile* file = TFile::Open(rootname.c_str(), "RECREATE");
    gGeoManager->Write();
    file->Close();

    G4cout << "Geometry imported to ROOT and saved as " << rootname << G4endl;
}

int main(int /*argc*/, char** /*argv*/) {
    // Create the Geant4 geometry
    G4RunManager* runManager = new G4RunManager();
    MyDetectorConstruction* detector = new MyDetectorConstruction();
    runManager->SetUserInitialization(detector);

    std::string name = "soph_wc_nuprism_segment_long_2_CONVERSION";
    // Export the geometry to GDML
    export_to_gdml(runManager, name);

    // Import GDML and export to ROOT with optional scaling
    import_gdml_and_export_to_root(true, name);

    delete runManager;
    return 0;
}

