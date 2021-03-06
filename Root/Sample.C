#include "TtHFitter/Sample.h"

// -------------------------------------------------------------------------------------------------
// Sample

//__________________________________________________________________________________
//
Sample::Sample(string name,int type){
    fName = name;
    fTitle = name;
    fGroup = "";
    fType = type;
    fFillColor = kWhite;
    fLineColor = kBlack;
    fNSyst = 0;
    fNNorm = 0;
    fNormalizedByTheory = true;
    fRegions.clear();
    fLumiScales.clear();
    fIgnoreSelection = false;
    fUseMCStat = true;
    fUseSystematics = true;
    fDivideBy = "";
    fMultiplyBy = "";
    fSmooth = false;
    //
    // ntuples
    fSelection = "1";
    fMCweight = "1";
    fNtuplePaths.clear();
    fNtupleFiles.clear();
    fNtupleNames.clear();
    fNtuplePathSuffs.clear();
    fNtupleFileSuffs.clear();
    fNtupleNameSuffs.clear();
    //
    // histograms
    fHistoPaths.clear();
    fHistoFiles.clear();
    fHistoNames.clear();
    fHistoPathSuffs.clear();
    fHistoFileSuffs.clear();
    fHistoNameSuffs.clear();
    //
    fNormFactors.clear();
    fSystematics.clear();
}
    
//__________________________________________________________________________________
//
Sample::~Sample(){
    for(unsigned int i=0;i<fNormFactors.size();++i){
        if(fNormFactors[i]){
            delete fNormFactors[i];
        }
    }
    for(unsigned int i=0;i<fSystematics.size();++i){
        if(fSystematics[i]){
            delete fSystematics[i];
        }
    }
}

//__________________________________________________________________________________
// cosmetics
void Sample::SetTitle(string title){
    fTitle = title;
}

//__________________________________________________________________________________
//
void Sample::SetFillColor(int color){
    fFillColor = color;
}

//__________________________________________________________________________________
//
void Sample::SetLineColor(int color){
    fLineColor = color;
}

//__________________________________________________________________________________
//
void Sample::NormalizedByTheory(const bool norm ){
    fNormalizedByTheory = norm;
}

//__________________________________________________________________________________
// read from ntuples
void Sample::SetMCweight(string weight){
    fMCweight = weight;
}

//__________________________________________________________________________________
//
void Sample::SetSelection(string selection){
    fSelection = selection;
}

//__________________________________________________________________________________
//
void Sample::AddNtuplePath(string path){
    fNtuplePaths.push_back(path);
}

//__________________________________________________________________________________
//
void Sample::AddNtupleFile(string file){
    fNtupleFiles.push_back(file);
}

//__________________________________________________________________________________
//
void Sample::AddNtupleName(string name){
    fNtupleNames.push_back(name);
}

//__________________________________________________________________________________
// read from histograms
void Sample::AddHistoPath(string path){
    fHistoPaths.push_back(path);
}

//__________________________________________________________________________________
//
void Sample::AddHistoFile(string file){
    fHistoFiles.push_back(file);
}

//__________________________________________________________________________________
//
void Sample::AddHistoName(string name){
    fHistoNames.push_back(name);
}

//__________________________________________________________________________________
// norm factors and systs
void Sample::AddNormFactor(NormFactor* normFactor){
    fNormFactors.push_back(normFactor);
    fNNorm ++;
}

//__________________________________________________________________________________
//
void Sample::AddSystematic(Systematic* syst){
    fSystematics.push_back(syst);
    fNSyst++;
}

//__________________________________________________________________________________
//
NormFactor* Sample::AddNormFactor(string name,float nominal,float min,float max,bool isConst){
    fNormFactors.push_back(new NormFactor(name,nominal,min,max,isConst));
    fNNorm ++;
    return fNormFactors[fNNorm-1];
}

//__________________________________________________________________________________
//
Systematic* Sample::AddSystematic(string name,int type,float up,float down){
    fSystematics.push_back(new Systematic(name,type,up,down));
    fNSyst++;
    return fSystematics[fNSyst-1];
}
