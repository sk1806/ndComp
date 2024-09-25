#include <TGeoManager.h>
#include <TFile.h>
#include <TBrowser.h>
#include <TSystem.h>


//const char * geomfile = "~/files/hyperk/loose/iwcd/geom/iwcd_id_geometry_short_v2.root";
//const char * geomfile = "~/files/hyperk/loose/iwcd/geom/wc_nuprism_segment_long.root";
//const char * geomanager = "NuPrismGeometry";

//const char * geomfile = "nd280geometry.root";
//const char * geomanager = "ND280Geometry";

const char * geomfile = "iwcd_geometry.root";
const char * geomanager = "GeomManager";

void geom_draw(const char* geomfile, const char* geomanager) {
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

    // Draw the geometry explicitly
    geom->Draw();

    // Open a TBrowser
    TBrowser* browser = new TBrowser();
    browser->Add(geom);

    // Keep the file open so the browser can access the geometry
    // Do not close the file here, as it would make the geometry inaccessible in the TBrowser
}

