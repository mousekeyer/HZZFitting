#include "runAsymptoticsCLs.h"
#include "TFile.h"
#include "TROOT.h"
#include "RooWorkspace.h"
#include "RooAbsData.h"
#include "RooRandom.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <cmath>
#include <string>
void usage(){
   cout<<"./get_limits outputname inputfile wsname dataName mh muName] [fixMu "<<endl;
   cout<<"outputname:   name of output directory"<<endl;
   cout<<"inputfile:   name of workspace file"<<endl;
   cout<<"wsname:      name of workspace"<<endl;
   //cout<<"mcname:      name of ModelConfig"<<endl;
   cout<<"dataname:    name of obsData"<<endl;
   //cout<<"iscombined:  is combination's workspaces?[0/1]"<<endl;
   cout<<"mh:          mass of higgs"<<endl;
   cout<<"mu Name:     mu, mu_ggF, mu_VBFVH"<<endl;
   cout<<"fix other mu at 0? [0/1]" <<endl;
}

int main(int argc, char** argv){

   string inputfile = "";
   string wsName = "";
   string mcName = "";
   string dataName = "";
   string muName = "";
   string tag = "";
   bool noSyst = false;
   mcName = "ModelConfig";
   double mcStatThresh = 0.005;

   int iArg=1;

   string mhiggsFixedValue ="";
   if ( (argc<7) ){
      usage();
      exit(0);
   } else {
      cout<<iArg<<" "<<endl;
      tag = string(argv[iArg++]);
      cout<<iArg<<" tag "<<tag<<endl;
      inputfile = string(argv[iArg++]);
      cout<<iArg<<" inputfile "<<inputfile<<endl;
      wsName = string(argv[iArg++]);
      cout<<iArg<<" wsName "<<wsName<<endl;
      dataName = string(argv[iArg++]);
      cout<<iArg<<" dataName "<<dataName<<endl;
      mhiggsFixedValue = string(argv[iArg++]);
      cout<<iArg<<" mhiggsFixedValue "<<mhiggsFixedValue<<endl;
      muName = string(argv[iArg++]);
      cout<<iArg<<endl;
   }
   if (argc>6)
      mcStatThresh = atof(argv[iArg++]);

   cout<<"Input file: "<< inputfile <<endl;
   cout<<"wsname:     "<< wsName <<endl;
   cout<<"mcname:     "<< mcName <<endl;
   cout<<"dataname:   "<< dataName <<endl;
   cout<<"mh:         "<< mhiggsFixedValue <<endl;
   cout<<"muName:     "<< muName <<endl;
   cout<<"mcStatThresh:     "<< mcStatThresh <<endl;

   cout<<"running limits"<<endl;
   //makeAsimovData(combined,0,0);
//   runAsymptoticsCLs(inputfile.c_str(),
//		     wsName.c_str(), 
//		     mcName.c_str(),
//		     dataName.c_str(), 
//		    // "asimovDataFullModel",//"asimovData_0", 
//		     "asimovData_0",//"asimovData_0", 
//		     "conditionalGlobs_0", 
//		     "nominalGlobs", 
//		     tag, 
//		     mhiggsFixedValue, 
//		     0.95,
//		     muName.c_str(),
//             mcStatThresh);
   runAsymptoticsCLs(inputfile.c_str(),
		     wsName.c_str(), 
		     mcName.c_str(),
		     dataName.c_str(), 
		     "asimovDataFullModel",//"asimovData_0", 
		    // "asimovData_0",//"asimovData_0", 
		     "conditionalGlobs_0", 
		     "nominalGlobs", 
		     tag, 
		     mhiggsFixedValue, 
		     0.95             );

}
