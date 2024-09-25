#include <iostream>
#include <TGeoManager.h>
#include <TGeoVolume.h>
#include <TGeoNode.h>
#include <TObjArray.h>
#include <TIterator.h>


//const char * geomfile = "/home/sophieking/files/hyperk/loose/iwcd/geom/iwcd_id_geometry_short_v2.root";
//const char * geomfile = "/home/sophieking/files/hyperk/loose/iwcd/geom/wc_nuprism_segment_long.root";
//const char * geomfile = "/home/sophieking/files/hyperk/loose/iwcd/geom/NuPRISM_Phase0_Geometry.root";
//const char * geomanager = "NuPrismGeometry";

//const char * geomfile = "/home/sophieking/files/t2k/loose/geom/v6r3-baseline-2015-08_geom-adf9c13e-c3e89f46-2902d8f1-8ef5f449-babbe6d4.root";
// const char * geomfile = "/home/sophieking/work/prod_tests/iwcd_prod/2024_prod_v1/geom/7.6-baseline-2024_geom-cbf9ffe8-b4a327f6-31bb2f3a-e7c09131-34f5af5f.root";
//const char * geomanager = "ND280Geometry";

const char * geomfile = "/home/sophieking/work/prod_tests/iwcd_prod/2024_prod_v1/geom/soph_wc_nuprism_segment_long_1_CONVERSION.root";
const char * geomanager = "MyGeoManager";



void inspectVolume(TGeoVolume *volume, int depth = 0, const Double_t* parentTranslation = nullptr) {
    if (!volume) {
        std::cerr << "Error: Null volume pointer passed." << std::endl;
        return;
    }

    std::string indent(depth * 2, ' '); // create indentation based on the depth
    std::cout << indent << "\nInspecting volume: " << volume->GetName() << std::endl;

    // Print shape and material details
    TGeoShape* shape = volume->GetShape();
    TGeoMaterial* material = volume->GetMaterial();
    if (shape) {
        std::cout << indent << "  Shape: " << shape->ClassName() << std::endl;
        shape->InspectShape();  // If available, or use specific methods for dimensions
    }
    if (material) {
        std::cout << indent << "  Material: " << material->GetName() << std::endl;
        std::cout << indent << "    Density: " << material->GetDensity() << " g/cm^3" << std::endl;
        std::cout << indent << "    A: " << material->GetA() << std::endl;
        std::cout << indent << "    Z: " << material->GetZ() << std::endl;
    }

    TObjArray *daughters = volume->GetNodes();
    if (!daughters) {
        std::cout << indent << "No daughter nodes for volume: " << volume->GetName() << std::endl;
        return; // Exit if there are no daughters
    }

    int numDaughters = daughters->GetEntriesFast();
    std::cout << indent << "Number of daughter nodes: " << numDaughters << std::endl;

    // Ensure all daughter nodes are processed
    for (int i = 0; i < numDaughters; ++i) {
        TGeoNode* node = (TGeoNode*)daughters->At(i);
        if (node) {
            std::cout << indent << "\n\nProcessing node: " << node->GetName() << std::endl;

            // Get the transformation matrix and print it
            TGeoMatrix *matrix = node->GetMatrix();
            const Double_t *translation = nullptr;
            if (matrix) {
                translation = matrix->GetTranslation();
                const Double_t *rotation = matrix->GetRotationMatrix();
                std::cout << indent << "  Translation: ("
                          << translation[0] << ", "
                          << translation[1] << ", "
                          << translation[2] << ")" << std::endl;
                std::cout << indent << "  Rotation Matrix: " << std::endl;
                for (int r = 0; r < 3; ++r) {
                    std::cout << indent << "    [";
                    for (int c = 0; c < 3; ++c) {
                        std::cout << rotation[3*r+c] << (c < 2 ? ", " : "");
                    }
                    std::cout << "]" << std::endl;
                }
            } else {
                std::cout << indent << "  No transformation matrix." << std::endl;
            }

            // Accumulate global translation
            Double_t globalTranslation[3] = {0, 0, 0};
            Double_t previousGlobalTranslation[3] = {0, 0, 0};
            if (parentTranslation) {
                globalTranslation[0] = parentTranslation[0];
                globalTranslation[1] = parentTranslation[1];
                globalTranslation[2] = parentTranslation[2];

                previousGlobalTranslation[0] = parentTranslation[0];
                previousGlobalTranslation[1] = parentTranslation[1];
                previousGlobalTranslation[2] = parentTranslation[2];
            }
            if (translation) {
                globalTranslation[0] += translation[0];
                globalTranslation[1] += translation[1];
                globalTranslation[2] += translation[2];
            }

            std::cout << indent << "  Global Origin: ("
                      << previousGlobalTranslation[0] << ", "
                      << previousGlobalTranslation[1] << ", "
                      << previousGlobalTranslation[2] << ") + ("
                      << (translation ? translation[0] : 0) << ", "
                      << (translation ? translation[1] : 0) << ", "
                      << (translation ? translation[2] : 0) << ") = ("
                      << globalTranslation[0] << ", "
                      << globalTranslation[1] << ", "
                      << globalTranslation[2] << ")" << std::endl;

            inspectVolume(node->GetVolume(), depth + 1, globalTranslation); // Recursive call with updated translation
        } else {
            std::cout << indent << "Warning: Null node encountered at index " << i << std::endl;
        }
    }
}

void geom_inspect() {

    std::cout<<""<<std::endl;
    TFile *file = TFile::Open(geomfile);
    if (!file || file->IsZombie()) {
        std::cerr << "Failed to open file." << std::endl;
        return;
    }

    TGeoManager *geom = (TGeoManager*)file->Get(geomanager);
    if (!geom) {
        std::cerr << "TGeoManager not found." << std::endl;
        return;
    }

    TGeoVolume *topVolume = geom->GetTopVolume();
    if (!topVolume) {
        std::cerr << "Error: Top volume not found." << std::endl;
        return;
    }

    std::cout<<"-------------------------------------------------"<< std::endl;
    std::cout<<"Printing details of top voume with GetTopVolume: \n"<< std::endl;
    geom->GetTopVolume()->Print(); // print details of the top volume
    
    // Browse the geometry in TBrowser if not in batch mode
    if (!gROOT->IsBatch()) {
        geom->Browse(nullptr); // Opens a TBrowser if possible
    }
    std::cout<<"-------------------------------------------------"<< std::endl;
    std::cout<<"\n\n\n\n"<<std::endl;
    inspectVolume(topVolume);

    // Close if in batch mode
    // If not in batch mode, I want TBrowser left open
    if (gROOT->IsBatch()) {
      file->Close();
      delete file;
    }
}


void browseGeometry(const char* geomfile, const char* geomanager) {
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
    geom->SetVisLevel(4); // Increase the visibility level if needed
    geom->SetVisOption(10); // Set visualization options (0 is usually default)
    geom->Draw();

    // Open a TBrowser
    TBrowser* browser = new TBrowser();
    browser->Add(geom);


    TCanvas *canvas = new TCanvas("Canvas1", "Geometry View", 800, 600);
    geom->GetTopVolume()->Draw("ogl"); // Using OpenGL renderer if available
    canvas->Modified();
    canvas->Update();

    // Keep the file open so the browser can access the geometry
    // Do not close the file here, as it would make the geometry inaccessible in the TBrowser
}
