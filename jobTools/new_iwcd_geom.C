#include <TFile.h>
#include <TGeoManager.h>
#include <TGeoMaterial.h>
#include <TGeoMedium.h>
#include <TGeoVolume.h>
#include <TGeoMatrix.h>
#include <TGeoCompositeShape.h>

void new_iwcd_geom() {
    // Dimensions of the World volume (half-lengths in mm)
    const double worldDx = 6050.0;
    const double worldDy = 13390.0;
    const double worldDz = 6050.0;

    // Dimensions of the logicDetector volume
    const double detectorRmin = 0.0;
    const double detectorRmax = 6000.0;
    const double detectorDz = 13340.0;

    // Material properties for Vacuum
    const double vacuumA = 1.00794;  // To match original output
    const double vacuumZ = 1.0;
    const double vacuumDensity = 1e-25; // g/cm^3

    // Material properties for Water
    const double waterA = 14.3337;
    const double waterZ = 7.22222;
    const double waterDensity = 1.0; // g/cm^3

    // Rotation angle (degrees)
    const double rotationX = 90.0;

    // Step 1: Create the TGeoManager
    TGeoManager *geom = new TGeoManager("NuPrismGeometry", "Geometry for NuPRISM segment");

    // Step 2: Define materials
    TGeoMaterial *matVacuum = new TGeoMaterial("Vacuum", vacuumA, vacuumZ, vacuumDensity);
    TGeoMaterial *matWater = new TGeoMaterial("Water", waterA, waterZ, waterDensity);

    // Define media
    TGeoMedium *Vacuum = new TGeoMedium("Vacuum", 1, matVacuum);
    TGeoMedium *Water = new TGeoMedium("Water", 2, matWater);

    // Step 3: Create the World volume
    // We'll create it as a TGeoCompositeShape to match the original as closely as possible.
    TGeoBBox *worldBox = new TGeoBBox("solidWorld", worldDx, worldDy, worldDz);
    TGeoCompositeShape *worldShape = new TGeoCompositeShape("solidWorld", "solidWorld");
    TGeoVolume *top = new TGeoVolume("World", worldBox, Vacuum);
    geom->SetTopVolume(top);

    // Step 4: Create the logicDetector volume
    TGeoVolume *logicDetector = geom->MakeTube("logicDetector", Water, detectorRmin, detectorRmax, detectorDz);

    // Step 5: Apply the rotation
    TGeoRotation *rot = new TGeoRotation();
    rot->RotateX(rotationX);

    // Step 6: Position the logicDetector in the World volume
    top->AddNode(logicDetector, 1, new TGeoCombiTrans(0, 0, 0, rot));

    // Step 7: Close the geometry
    geom->CloseGeometry();

    // Step 8: Save the geometry to a ROOT file
    TFile *file = TFile::Open("soph_wc_nuprism_segment_long.root", "RECREATE");
    geom->Write();
    file->Close();

    // Clean up
    delete geom;
    delete file;
}

int main() {
    new_iwcd_geom();
    return 0;
}

