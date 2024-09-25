#include <TGeoManager.h>
#include <TFile.h>
#include <TBrowser.h>
#include <TSystem.h>

void geom_draw_new() {
    //const char *geomfile = "/home/sophieking/files/hyperk/loose/iwcd/geom/wc_nuprism_segment_long.root";
    //const char *geomanager = "NuPrismGeometry";

    const char *geomfile = "iwcd_geometry.root";
    const char *geomanager = "GeomManager";

    TFile* file = TFile::Open(geomfile);
    if (!file || file->IsZombie()) {
        std::cerr << "Error opening file." << std::endl;
        return;
    }
    TGeoManager* geom = (TGeoManager*)file->Get(geomanager);
    if (!geom) {
        std::cerr << "Geometry manager not found." << std::endl;
        return;
    }

    // Ensure ROOT is not in batch mode
    gROOT->SetBatch(false);

    // Draw all volumes in the geometry
    geom->GetTopNode()->Draw("ogl");

    // Open a TBrowser to inspect the geometry
    TBrowser* browser = new TBrowser();
    browser->Add(geom);

    // Keep the file open so the browser can access the geometry
}

