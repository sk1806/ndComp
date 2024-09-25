{ // Read in the nRooTracker tree

  // t1
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/t1/oa_xx_xxx_00000000_gu3osqnbivvj_sand_000.root";

  // t1_mod (SandGeant4Sim0.9.1)	
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/t1_mod/oa_xx_xxx_00000000_ih3ut3rrypme_sand_000.root";

  // t1_mod_SandGeant4Sim0.9.1
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/t1_mod_SandGeant4Sim0.9.1/oa_xx_xxx_00000000_gudq6p2zcrej_sand_000.root";
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/t_p7_nkiller/oa_xx_xxx_00000000_g3u5ked36jfn_sand_000.root";

  // t2
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/t2/oa_xx_xxx_00000000_k6et7az2lo35_sand_000.root";
  //t3
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/t3/oa_xx_xxx_00000000_hegti2fo4tse_sand_000.root";
  // t4
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/t4/oa_xx_xxx_00000000_qbigbmmtj5th_sand_000.root";

  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/t_p6_std_file2/oa_xx_xxx_00000000_3xwb5xel57xi_sand_000.root";

  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/t_nd280softwaremaster_centos7-13.23_sandFix_TestTree_sand/oa_xx_xxx_00000000_azxaj4t34m3e_sand_000.root";
  




  // p7_file1_unmodified
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/p7_file1_unmodified/oa_xx_xxx_00000000_gu3osqnbivvj_sand_000.root" ;

  // p7_file1_wo_nkiller
     TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/p7_file1_wo_nKiller/oa_xx_xxx_00000000_ryboemqgn3sg_sand_000.root";


  // p6_file1_unmodified
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/p6_file1_unmodified/oa_xx_xxx_00000000_w5adclweg2nw_sand_000.root" ;
  
  // p6_file1_wo_nkiller
  //TString infile = "/home/soph/work/nd280/prod_tests/sand/sandPropagate/tests/p6_file1_wo_nkiller/oa_xx_xxx_00000000_4xh3z6al4cwh_sand_000.root" ;



  TFile f(infile);
  TTree *tree;
  //tree = (TTree *)(f.Get("nRooTracker"));
  tree = (TTree *)(f.Get("OutTree"));

  // How many events are there
  Int_t nevents;
  nevents = tree->GetEntries();

  // Update total number of events
  //total_counter += nevents;

  std::cout<<"Processing file " <<infile <<" with " <<nevents <<" events." << std::endl;
  ////////////////////////////////////////////////////////////////
  // Set the interesting branches
  ////////////////////////////////////////////////////////////////

  // Interaction mode

  TString mode;
  TObjString * evtcode = NULL;

  tree->SetBranchAddress("EvtCode", &evtcode);

  // Total cross section
  Double_t x_sec;
  tree->SetBranchAddress("EvtXSec", &x_sec);

  // Number of final state particles + 3 (StdHepN = N_final + N_initial +1(for Target)= N_final + 2 + 1)
  Int_t nparticles;
  tree->SetBranchAddress("StdHepN", &nparticles);


  int max_nparticles = 0;
  for( int i = 0; i<nevents; i++){
   tree->GetEntry(i);
   mode = evtcode->GetString().Data();
   //   std::cout << i << " Mode: " << v->Data() << std::endl;
   int max = (max_nparticles <= nparticles) ? nparticles : max_nparticles;
   max_nparticles = max;
  }
  std::cout << "Maximal number or particles: " << max_nparticles << "\n";
  const int max_n = 100 ;max_nparticles;


  // Particle ID (PDG code). The second entry is the PDG code of the Target atom.
  Int_t PID[100];
  tree->SetBranchAddress("StdHepPdg", &PID);

  // Status of particles (0: initial particle, 1: final state particle) StdHep... only keeps the initial and
  // final particles but not the ones in between.
  Int_t Status[max_n];
  tree->SetBranchAddress("StdHepStatus", &Status);

  // 4 Momentum of the initial and final particles
  Double_t P4[max_n][4];
  tree->SetBranchAddress("StdHepP4", &P4);

  // Vertex flag of particles (including pre-FSI particles)
  Int_t Vertex[1000];
  tree->SetBranchAddress("NEiorgvc", &Vertex);

  // Number of all particles (including pre-FSI!)
  Int_t preFSI_nparticles;
  tree->SetBranchAddress("NEnvc", &preFSI_nparticles);

  // Alternative PID ordering (includes pre-FSI particles which get absorbed)
  Int_t preFSI_PID[1000];
  tree->SetBranchAddress("NEipvc", &preFSI_PID);

  // Pre FSI 3-momentas (includes pre-FSI particles which get absorbed)
  Float_t preFSI_p3[1000][3];
  tree->SetBranchAddress("NEpvc", &preFSI_p3);

  // nu vertex   x, y, z, t
  // distance in meters for numc  (for anal and HL2 it is in mm)
  Double_t vtxPos[4];
  tree->SetBranchAddress("EvtVtx", &vtxPos);



  // Particles
  //   StdHepStatus
  //     Status 0 - initial particle
  //     Status 1 - final particle
  //   Array
  //     [0] - neutrino
  //     [1] - target
  //     [>1] - intermediate and final state particles

  Int_t nInitialMu, nInitialAntiMu, nInitialProt, nInitialGamma, nInitialPiP, nInitialPiM, nInitialEpm, nInitialN = 0;
  Int_t nInterMu,   nInterAntiMu,   nInterProt,   nInterGamma,   nInterPiP,   nInterPiM,   nInterEpm,   nInterN   = 0;
  Int_t nMu,        nAntiMu,         nProt,       nGamma,        nPiP,        nPiM,        nEpm,        nN        = 0;

  Int_t nInitialOther1 = 0;
  Int_t nInterOther1 = 0;
  Int_t nOther1 = 0;




  Int_t nInitialNumu, nInitialAntiNumu, nInitialNue, nInitialAntiNue = 0;
  Int_t nInterNumu,   nInterAntiNumu,   nInterNue,   nInterAntiNue   = 0;
  Int_t nNumu,        nAntiNumu,        nNue,        nAntiNue        = 0;





  Int_t nInitialPiz,  nInitialKp, nInitialKm = 0;
  Int_t nInterPiz, nInterKp, nInterKm  = 0;
  Int_t nPiz, nKp, nKm = 0;

  Int_t      nInitial1000080160, nInitial1000140280, nInitial1000010020 = 0;
  Int_t      nInter1000080160,   nInter1000140280,   nInter1000010020   = 0;  
  Int_t      n1000080160,        n1000140280,        n1000010020        = 0;

  Int_t nInitialOther = 0;
  Int_t nInterOther = 0;
  Int_t nOther = 0;





  // Event loop.
  for(int i =0; i<nevents; i++){
    tree->GetEntry(i);
    mode = evtcode->GetString().Data();  
    std::cout<< "i = "<< i << ";  EvtCode = " << mode << "; StdHepN (#particles, including nu and target) = " << nparticles << std::endl;

  
    for(int p=0; p<nparticles; p++){
      //std::cout<<"All states:    p = " << p << ";  StdHepPdg = " << PID[p]  <<";  StdHepStatus = " << Status[p] << std::endl;


      if(Status[p] == 0){
        //std::cout<<"Initial state:    p = " << p << ";  StdHepPdg = " << PID[p]  <<";  StdHepStatus = " << Status[p] << std::endl;

        //bool other1 = false;
        if(PID[p] == 13) nInitialMu++;
        else if (PID[p] == -13) nInitialAntiMu++;
        else if (PID[p] == 2212) nInitialProt++;
        else if (PID[p] == 22) nInitialGamma++;
        else if (PID[p] == 211) nInitialPiP++;
        else if (PID[p] == -211) nInitialPiM++;
        else if (abs(PID[p]) == 11) nInitialEpm++;
        else if (PID[p] == 2112) nInitialN++;
        //else{
        //  nInitialOther1++;
        //  other1 = true;
        //}
        //if(other1 == true){
        //}
        else if (PID[p] == 1000080160) nInitial1000080160++;   
        else if (PID[p] == 1000140280) nInitial1000140280++;   
        else if (PID[p] == 1000010020) nInitial1000010020++;
        else if (PID[p] == 14) nInitialNumu++;
        else if (PID[p] == -14) nInitialAntiNumu++;
        else if (PID[p] == 12) nInitialNue++;
        else if (PID[p] == -12) nInitialAntiNue++;   
        else if (PID[p] == 111) nInitialPiz++;   
        else if (PID[p] == 321) nInitialKp++;   
        else if (PID[p] == -321) nInitialKm++;   
        else{
          nInitialOther++;
          //#std::cout<<"Initial Other particle:  "<< PID[p] << std::endl;
        }
      }
      if(Status[p] == 2){
        //std::cout<<"Intermediate state:    p = " << p << ";  StdHepPdg = " << PID[p]  <<";  StdHepStatus = " << Status[p] << std::endl;

        //bool other1 = false;
        if(PID[p] == 13) nInterMu++;
        else if (PID[p] == -13) nInterAntiMu++;
        else if (PID[p] == 2212) nInterProt++;
        else if (PID[p] == 22) nInterGamma++;
        else if (PID[p] == 211) nInterPiP++;
        else if (PID[p] == -211) nInterPiM++;
        else if (abs(PID[p]) == 11) nInterEpm++;
        else if (PID[p] == 2112) nInterN++;
        //else{
        //  nInterOther1++;
        //  other1 = true;
        //}
        //if(other1 == true){
        //}
        else if (PID[p] == 1000080160) nInter1000080160++;
        else if (PID[p] == 1000140280) nInter1000140280++;
        else if (PID[p] == 1000010020) nInter1000010020++;
        else if (PID[p] == 14) nInterNumu++;
        else if (PID[p] == -14) nInterAntiNumu++;
        else if (PID[p] == 12) nInterNue++;
        else if (PID[p] == -12) nInterAntiNue++;
        else if (PID[p] == 111) nInterPiz++;
        else if (PID[p] == 321) nInterKp++;
        else if (PID[p] == -321) nInterKm++;
        else{
          nInterOther++;
          //#std::cout<<"Intermediate Other particle:  "<< PID[p] << std::endl;

        }
      }
      if(Status[p] ==1){
        std::cout<<"Final state:    p = " << p << ";  StdHepPdg = " << PID[p]  <<";  StdHepStatus = " << Status[p] << std::endl;

        //bool other1 = false;
        if(PID[p] == 13) nMu++;
        else if (PID[p] == -13) nAntiMu++;
        else if (PID[p] == 2212) nProt++;
        else if (PID[p] == 22) nGamma++;
        else if (PID[p] == 211) nPiP++;
        else if (PID[p] == -211) nPiM++;
        else if (abs(PID[p]) == 11) nEpm++;
        else if (PID[p] == 2112){
            nN++;
            //std::cout<<"Neutron: "<<
        }
        //else{
        //  nOther1++;
        //  other1 = true;
        //}
        //if(other1 == true){
        //}
        else if (PID[p] == 1000080160) n1000080160++;   
        else if (PID[p] == 1000140280) n1000140280++;   
        else if (PID[p] == 1000010020) n1000010020++;
        else if (PID[p] == 14) nNumu++;
        else if (PID[p] == -14) nAntiNumu++;
        else if (PID[p] == 12) nNue++;
        else if (PID[p] == -12) nAntiNue++;   
        else if (PID[p] == 111) nPiz++;   
        else if (PID[p] == 321) nKp++;   
        else if (PID[p] == -321) nKm++;   
        else{
          nOther++;
          //#std::cout<<"Final Other particle:  "<< PID[p] << std::endl;
        }
      }	



      //if( PID[p] == 13
      //  or PID[p] == -13 
      //  or PID[p] == 2212
      //  or PID[p] == 22
      //  or PID[p] == 211
      //  or PID[p] == -211
      //  or abs(PID[p]) == 11
      //  or PID[p] == 2112
      //  or PID[p] == 2112
      //  or PID[p] == 14 
      //  or PID[p] == -14
      //  or PID[p] == 12
      //  or PID[p] == -12
      //  or PID[p] == 111
      //  or PID[p] == 321
      //  or PID[p] == -321
      //  or PID[p] == 1000080160
      //  or PID[p] == 1000140280
      //  or PID[p] == 1000010020 ) continue;
      //else
      //    std::cout<<"Al  Other particle:    p = " << p << ";  StdHepPdg = " << PID[p]  <<";  StdHepStatus = " << Status[p] << std::endl;
  

    } // for nparticles    

  } // for nevents

  std::cout<<"Note:  If running over sandPropagate/sandSimulation output then Initial, intermediate and final state particles should not be interpreted as if they came from a neutMC / genev !! "<<std::endl;
  std::cout<<""<<std::endl;

  std::cout<<"initial mu:         "<< nInitialMu << std::endl;
  std::cout<<"initial amu:        "<< nInitialAntiMu << std::endl;
  std::cout<<"initial Protons:    "<< nInitialProt << std::endl;
  std::cout<<"initial Gamma:      "<< nInitialGamma << std::endl;
  std::cout<<"initial Pi+:        "<< nInitialPiP << std::endl;
  std::cout<<"initial Pi-:        "<< nInitialPiM << std::endl;
  std::cout<<"initial e+-:        "<< nInitialEpm << std::endl;
  std::cout<<"initial Neutrons:   "<< nInitialN << std::endl;
  std::cout<<"Initial 1000080160  " <<  nInitial1000080160  <<std::endl;
  std::cout<<"Initial 1000140280  " <<  nInitial1000140280  <<std::endl;
  std::cout<<"Initial 1000010020  " <<  nInitial1000010020  <<std::endl;
  std::cout<<"Initial Numu        " <<  nInitialNumu        <<std::endl;
  std::cout<<"Initial AntiNumu    " <<  nInitialAntiNumu    <<std::endl;
  std::cout<<"Initial Nue         " <<  nInitialNue         <<std::endl;
  std::cout<<"Initial AntiNue     " <<  nInitialAntiNue     <<std::endl;
  std::cout<<"Initial Pi0         " <<  nInitialPiz         <<std::endl;
  std::cout<<"Initial K+          " <<  nInitialKp          <<std::endl;
  std::cout<<"Initial K-          " <<  nInitialKm          <<std::endl;
  std::cout<<"initial Other:      "<< nInitialOther << std::endl;

  std::cout<<""<<std::endl;
  std::cout<<"Intermediate mu:         " <<  nInterMu          << std::endl;
  std::cout<<"Intermediate amu:        " <<  nInterAntiMu      << std::endl;
  std::cout<<"Intermediate Protons:    " <<  nInterProt        << std::endl;
  std::cout<<"Intermediate Gamma:      " <<  nInterGamma       << std::endl;
  std::cout<<"Intermediate Pi+:        " <<  nInterPiP         << std::endl;
  std::cout<<"Intermediate Pi-:        " <<  nInterPiM         << std::endl;
  std::cout<<"Intermediate e+-:        " <<  nInterEpm         << std::endl;
  std::cout<<"Intermediate Neutrons:   " <<  nInterN           << std::endl;
  std::cout<<"Intermediate 1000080160  " <<  nInter1000080160  << std::endl;
  std::cout<<"Intermediate 1000140280  " <<  nInter1000140280  << std::endl;
  std::cout<<"Intermediate 1000010020  " <<  nInter1000010020  << std::endl;
  std::cout<<"Intermediate Numu        " <<  nInterNumu        << std::endl;
  std::cout<<"Intermediate AntiNumu    " <<  nInterAntiNumu    << std::endl;
  std::cout<<"Intermediate Nue         " <<  nInterNue         << std::endl;
  std::cout<<"Intermediate AntiNue     " <<  nInterAntiNue     << std::endl;
  std::cout<<"Intermediate Pi0         " <<  nInterPiz         << std::endl;
  std::cout<<"Intermediate K+          " <<  nInterKp          << std::endl;
  std::cout<<"Intermediate K-          " <<  nInterKm          << std::endl;
  std::cout<<"Intermediate Other:      " <<  nInterOther       << std::endl;

  std::cout<<""<<std::endl;
  std::cout<<"Final mu:         "<< nMu << std::endl;
  std::cout<<"Final amu:        "<< nAntiMu << std::endl;
  std::cout<<"Final Protons:    "<< nProt << std::endl;
  std::cout<<"Final Gamma:      "<< nGamma << std::endl;
  std::cout<<"Final Pi+:        "<< nPiP << std::endl;
  std::cout<<"Final Pi-:        "<< nPiM << std::endl;
  std::cout<<"Final e+-:        "<< nEpm << std::endl;
  std::cout<<"Final Neutrons:   "<< nN << std::endl;                             
  std::cout<<"Final 1000080160  " <<  n1000080160  << std::endl;
  std::cout<<"Final 1000140280  " <<  n1000140280  << std::endl;
  std::cout<<"Final 1000010020  " <<  n1000010020  << std::endl;
  std::cout<<"Final Numu        " <<  nNumu        << std::endl;
  std::cout<<"Final AntiNumu    " <<  nAntiNumu    << std::endl;
  std::cout<<"Final Nue         " <<  nNue         << std::endl;
  std::cout<<"Final AntiNue     " <<  nAntiNue     << std::endl;
  std::cout<<"Final Pi0         " <<  nPiz         << std::endl;
  std::cout<<"Final K+          " <<  nKp          << std::endl;
  std::cout<<"Final K-          " <<  nKm          << std::endl;
  std::cout<<"Final Other:      " <<  nOther       << std::endl;

  std::cout<<""<<std::endl;
  std::cout<<"Note:  If running over sandPropagate/sandSimulation output then Initial, intermediate and final state particles should not be interpreted as if they came from a neutMC / genev !! "<<std::endl;

}
