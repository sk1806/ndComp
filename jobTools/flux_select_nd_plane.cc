#include <TFile.h>
#include <TTree.h>
#include <TList.h>
#include <TKey.h>
#include <TSystem.h>
#include <TString.h>

class FileProcessor {
public:
    static void process_file(const char* input_filename, const char* output_filename, int idfd_value) {
        // Open the input ROOT file
        TFile* input_file = TFile::Open(input_filename, "READ");

        // Create a new ROOT file for output
        TFile* output_file = new TFile(output_filename, "RECREATE");

        // Copy the h3000 and h1000 TTrees to the new file
        TTree* h3000 = (TTree*)input_file->Get("h3000");
        TTree* h1000 = (TTree*)input_file->Get("h1000");
        h3000->CloneTree()->Write();
        h1000->CloneTree()->Write();

        // Process and copy the h3002 TTree
        TTree* h3002 = (TTree*)input_file->Get("h3002");
        TTree* new_tree = h3002->CloneTree(0);  // Create an empty tree with the same branches

        // Set up a branch to read the idfd variable
        int idfd;
        h3002->SetBranchAddress("idfd", &idfd);

        // Loop through entries in h3002 and copy only those with idfd == idfd_value
        Long64_t n_entries = h3002->GetEntries();
        for (Long64_t i = 0; i < n_entries; i++) {
            h3002->GetEntry(i);
            if (idfd == idfd_value) {
                new_tree->Fill();
            }
        }
        new_tree->Write();

        // Copy the histograms to the new file
        TList* list = input_file->GetListOfKeys();
        TIter next(list);
        TKey* key;
        while ((key = (TKey*)next())) {
            TObject* obj = key->ReadObj();
            if (obj->InheritsFrom("TH1") || obj->InheritsFrom("TH2")) {
                obj->Write();
            }
        }

        // Close the files
        output_file->Close();
        input_file->Close();
    }

    static void process_all_files(const char* input_dir, const char* output_dir, const char* original_prefix, const char* original_suffix, const char* newfile_prefix, const char* newfile_suffix, int idfd_value) {
        void* dirp = gSystem->OpenDirectory(input_dir);
        const char* entry;
        while ((entry = gSystem->GetDirEntry(dirp))) {
            TString filename(entry);
            if (!filename.Contains(original_prefix) || !filename.Contains(original_suffix)) continue;

            // Extract the UNIQUE part
            TString unique = filename;
            unique.ReplaceAll(original_prefix, "");
            unique.ReplaceAll(original_suffix, "");

            // Form the output filename
            TString output_filename = TString(output_dir) + "/" + newfile_prefix + unique + newfile_suffix + ".root";

            // Process the file
            process_file(TString(input_dir) + "/" + filename, output_filename, idfd_value);
        }
        gSystem->FreeDirectory(dirp);
    }
};

int main() {
    const char* input_dir = "/home/sophieking/files/hyperk/loose/flux/laurence_2024_v1/p320";   // "/path/to/input/folder";
    const char* output_dir = "/home/sophieking/files/hyperk/loose/flux/laurence_2024_v1/p320_nd25";  // "/path/to/output/folder";
    const char* original_prefix = "newtargetmc_run13_";
    const char* original_suffix = "_rn001_noname_bch1.root";
    const char* newfile_prefix = "nu.newtargetmc_run13_nd25_";
    const char* newfile_suffix = "_rn001_noname_bch1.root";
    int idfd_value = 25;  // Example value for idfd

    // Call the static method directly without creating an instance of FileProcessor
    FileProcessor::process_all_files(input_dir, output_dir, original_prefix, original_suffix, newfile_prefix, newfile_suffix, idfd_value);

    return 0;
}

