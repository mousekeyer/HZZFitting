// vim: ts=4:sw=4
/**********************************************************************************
 * Project: HistFitter - A ROOT-based package for statistical data analysis       *
 * Package: HistFitter                                                            *
 * Namespace: Util                                                                *
 *                                                                                *
 * Description:                                                                   *
 *      Implementation (see header for description)                               *
 *                                                                                *
 * Authors:                                                                       *
 *      HistFitter group, CERN, Geneva, Switzerland                               *
 *      Lorenzo Moneta, CERN, Geneva  <Lorenzo.Moneta@cern.h>                     *
 *           See: FitPdf()                                                        *
 *      Wouter Verkerke, Nikhef, Amsterdam <verkerke@nikhef.nl>                   *
 *           See: GetPropagatedError()                                            *
 *                                                                                *
 * See corresponding .h file for author and license information                   *
 **********************************************************************************/

#include "TtHFitter/Utils.h"

#include "TMap.h"
#include "TString.h"
#include "TObjString.h"
#include "TObjArray.h"

#include "RooArgSet.h"
#include "TIterator.h"
#include "RooAbsReal.h"
#include "RooAbsPdf.h"
#include "RooAbsArg.h"
#include "RooFitResult.h"
#include "RooRealVar.h"
#include "RooWorkspace.h"
#include "RooSimultaneous.h"
#include "RooProdPdf.h"
#include "RooAddPdf.h"
#include "RooDataSet.h"
#include "RooPlot.h"
#include "RooProduct.h"
#include "RooMCStudy.h"
#include "Roo1DTable.h"
#include "RooCategory.h"
#include "RooRealSumPdf.h"
#include "RooGaussian.h"
#include "RooCurve.h"
#include "RooHist.h"
#include "RooMinimizer.h"
#include "RooConstVar.h"
#include "RooNumIntConfig.h"
#include "RooMinuit.h"

#include "RooStats/ModelConfig.h"
#include "RooStats/ProfileLikelihoodTestStat.h"
#include "RooStats/ProfileLikelihoodCalculator.h"
#include "RooStats/LikelihoodInterval.h"
#include "RooStats/ToyMCSampler.h"
#include "RooStats/SamplingDistPlot.h"
#include "RooStats/HypoTestInverterResult.h"
#include "RooStats/HypoTestResult.h"
#include "RooStats/RooStatsUtils.h"
#include "RooStats/HistFactory/PiecewiseInterpolation.h"

#include "TF1.h"
#include "TH2D.h"
#include "TTree.h"
#include "TBranch.h"
#include "TGraph2D.h"
#include "TGraphAsymmErrors.h"
#include "TPad.h"
#include "TStyle.h"

#include "TVectorD.h"
#include "TFile.h"
#include "TLine.h"
#include "TLatex.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLegendEntry.h"

#include "TROOT.h"


#include <iostream>
#include <fstream>

using namespace std;
using namespace RooFit;
using namespace RooStats;

//________________________________________________________________________________________________
RooStats::ModelConfig* Util::GetModelConfig( const RooWorkspace* w, const TString& mcName  ) {
    if (w==0) {
        std::cout << "Workspace is a null pointer." << std::endl;
        return NULL;
    }

    TObject* obj = w->obj( mcName.Data() ) ;
    if (obj==0) {
        std::cout<<  "Cannot open ModelConfig <" << mcName << "> from workspace." << std::endl;
        return NULL;
    }

    RooStats::ModelConfig* mc = (RooStats::ModelConfig *)(obj);
    if ( mc==0 ) {
        std::cout <<  "Cannot open ModelConfig <" << mcName << "> from workspace" << std::endl;
        return NULL;
    }

    return mc;
}



//_____________________________________________________________________________
void 
Util::SetInterpolationCode(RooWorkspace* w, Int_t code)
{
    if(w==NULL){
        std::cout<<  "Workspace is NULL. Return." << std::endl;
        return;
    }

    RooArgSet funcs = w->allFunctions();
    TIterator* iter = funcs.createIterator() ;

    RooAbsArg* parg(0);  
    while((parg=(RooAbsArg*)iter->Next())) {
        if ( parg->ClassName()!=TString("PiecewiseInterpolation") ) { continue; }    
        PiecewiseInterpolation* p = (PiecewiseInterpolation*)w->function( parg->GetName() ); // something I can modifiy :)
        p->setAllInterpCodes(code);
    }

    delete iter;
}



//_____________________________________________________________________________
void
Util::resetAllErrors( RooWorkspace* wspace )
{
    RooStats::ModelConfig* mc  = Util::GetModelConfig(wspace);
    if (mc==0) return;

    const RooArgSet* obsSet = mc->GetObservables();
    if (obsSet==0) return;

    RooAbsPdf* pdf = mc->GetPdf();
    if (pdf==0) return;

    RooArgList floatParList = Util::getFloatParList( *pdf, *obsSet );

    Util::resetError(wspace,floatParList);
}


//_____________________________________________________________________________
void
Util::resetAllValues( RooWorkspace* wspace )
{
    RooStats::ModelConfig* mc  = Util::GetModelConfig(wspace);
    if (mc==0) return;

    const RooArgSet* obsSet = mc->GetObservables();
    if (obsSet==0) return;

    RooAbsPdf* pdf = mc->GetPdf();
    if (pdf==0) return;

    RooArgList floatParList = Util::getFloatParList( *pdf, *obsSet );

    Util::resetValue(wspace,floatParList);
}


//_____________________________________________________________________________
void
Util::resetAllNominalValues( RooWorkspace* wspace )
{
    RooStats::ModelConfig* mc  = Util::GetModelConfig(wspace);
    if (mc==0) return;

    const RooArgSet* gobsSet = mc->GetGlobalObservables();
    if (gobsSet==0) return;

    gobsSet->Print("v");

    Util::resetNominalValue( wspace,*gobsSet );
}


//_____________________________________________________________________________
RooArgList 
Util::getFloatParList( const RooAbsPdf& pdf, const RooArgSet& obsSet )
{
    RooArgList floatParList;

    const RooArgSet* pars = pdf.getParameters( obsSet );
    if (pars==0) { return floatParList; }

    TIterator* iter = pars->createIterator() ;
    RooAbsArg* arg ;
    while( (arg=(RooAbsArg*)iter->Next()) ) {
        if(arg->InheritsFrom("RooRealVar") && !arg->isConstant()){
            floatParList.add( *arg );
        }
    }
    delete iter;

    return floatParList;
}



//_____________________________________________________________________________
void 
Util::resetError( RooWorkspace* wspace, const RooArgList& parList, const RooArgList& vetoList ) 

{
    /// For the given workspace,
    /// find the input systematic with
    /// the given name and shift that
    /// systematic by 1-sigma

    std::cout <<  " starting with workspace: " << wspace->GetName() << "   parList.getSize(): " << parList.getSize() << "  vetoList.size() = " << vetoList.getSize() << std::endl;

    TIterator* iter = parList.createIterator() ;
    RooAbsArg* arg ;
    while( (arg=(RooAbsArg*)iter->Next()) ) {

        std::string UncertaintyName;
        if(arg->InheritsFrom("RooRealVar") && !arg->isConstant()){
            UncertaintyName = arg->GetName();
        } else { continue; }

        if ( vetoList.FindObject( UncertaintyName.c_str() )!=0 ) { continue; }

        RooRealVar* var = wspace->var( UncertaintyName.c_str() );
        if( ! var ) {
            std::cout<<  "Could not find variable: " << UncertaintyName
                << " in workspace: " << wspace->GetName() << ": " << wspace
                << std::endl;
        }

        // Initialize
        double val_hi  = FLT_MAX;
        double val_low = FLT_MIN;
        double sigma = 0.;
        bool resetRange(false);

        if( UncertaintyName == "" ) {
            std::cout<<  "No Uncertainty Name provided" << std::endl;
            throw -1;
        }
        // If it is a standard (gaussian) uncertainty
        else if( string(UncertaintyName).find("alpha")!=string::npos ){ 
            // Assume the values are +1, -1
            val_hi  =  1.0;
            val_low = -1.0;      
            sigma = 1.0;
            resetRange = true;
        }
        // If it is Lumi:
        else if( UncertaintyName == "Lumi" ) {
            // Get the Lumi's constraint term:
            RooGaussian* lumiConstr = (RooGaussian*) wspace->pdf("lumiConstraint");
            if(!lumiConstr){
                std::cout<<  "Could not find wspace->pdf('lumiConstraint') "
                    << " in workspace: " << wspace->GetName() << ": " << wspace
                    << " when trying to reset error for parameter: Lumi"
                    << std::endl;
                continue;
            }
            // Get the uncertainty on the Lumi:
            RooRealVar* lumiSigma = (RooRealVar*) lumiConstr->findServer(0);
            sigma = lumiSigma->getVal();

            RooRealVar* nominalLumi = wspace->var("nominalLumi");
            double val_nom = nominalLumi->getVal();

            val_hi  = val_nom + sigma;
            val_low = val_nom - sigma; 
            resetRange = true;
        }
        // If it is a stat uncertainty (gamma)
        else if( string(UncertaintyName).find("gamma")!=string::npos ){

            // Get the constraint and check its type:
            RooAbsReal* constraint = (RooAbsReal*) wspace->obj( (UncertaintyName+"_constraint").c_str() );
            std::string ConstraintType ="";
            if(constraint != 0){ ConstraintType=constraint->IsA()->GetName(); }

            if( ConstraintType == "" ) {
                std::cout<<  "Assuming parameter :" << UncertaintyName << ": is a ShapeFactor and so unconstrained" << std::endl;
                continue;
            }
            else if( ConstraintType == "RooGaussian" ){
                RooAbsReal* sigmaVar = (RooAbsReal*) wspace->obj( (UncertaintyName+"_sigma").c_str() );
                sigma = sigmaVar->getVal();

                // Symmetrize shifts
                val_hi = 1 + sigma;
                val_low = 1 - sigma;
                resetRange = true;
            }
            else if( ConstraintType == "RooPoisson" ){
                RooAbsReal* nom_gamma = (RooAbsReal*) wspace->obj( ("nom_" + UncertaintyName).c_str() );
                double nom_gamma_val = nom_gamma->getVal();

                sigma = 1/TMath::Sqrt( nom_gamma_val );
                val_hi = 1 + sigma;
                val_low = 1 - sigma;
                resetRange = true;
            } 
            else {
                std::cout<<  "Strange constraint type for Stat Uncertainties: " << ConstraintType << std::endl;
                throw -1;
            }

        } // End Stat Error
        else {
            // Some unknown uncertainty
            std::cout<< "Couldn't identify type of uncertainty for parameter: " << UncertaintyName << ". Assuming a normalization factor." << std::endl;
            std::cout<<  "Setting uncertainty to 0.0001 before the fit for parameter: " << UncertaintyName << std::endl;
            sigma = 0.0001;
            val_low = var->getVal() - sigma;
            val_hi = var->getVal() + sigma;
            resetRange = false;
        }

        var->setError(abs(sigma));
        if (resetRange) {
            double minrange = var->getMin();
            double maxrange = var->getMax();
            double newmin = var->getVal() - 6.*sigma;
            double newmax = var->getVal() + 6.*sigma;
            if (minrange<newmin) var->setMin(newmin);
            if (newmax<maxrange) var->setMax(newmax);
        }

        std::cout<<  "Uncertainties on parameter: " << UncertaintyName
            << " low: "  << val_low
            << " high: " << val_hi
            << " sigma: " << sigma
            << " min range: " << var->getMin()
            << " max range: " << var->getMax()
            << std::endl;

        // Done
    } // end loop

    delete iter ;
}


//_____________________________________________________________________________
    void
Util::resetValue( RooWorkspace* wspace, const RooArgList& parList, const RooArgList& vetoList )

{
    /// For the given workspace,
    /// find the input systematic with
    /// the given name and shift that
    /// systematic by 1-sigma

    TIterator* iter = parList.createIterator() ;
    RooAbsArg* arg ;
    while( (arg=(RooAbsArg*)iter->Next()) ) {

        std::string UncertaintyName;
        if(arg->InheritsFrom("RooRealVar") && !arg->isConstant()){
            UncertaintyName = arg->GetName();
        } else { continue; }

        if ( vetoList.FindObject( UncertaintyName.c_str() )!=0 ) { continue; }

        RooRealVar* var = wspace->var( UncertaintyName.c_str() );
        if( ! var ) {
            std::cout<<  "Could not find variable: " << UncertaintyName
                << " in workspace: " << wspace->GetName() << ": " << wspace
                << std::endl;
        }

        // Initialize
        double valnom = 0.;

        if( UncertaintyName == "" ) {
            std::cout<<  "No Uncertainty Name provided" << std::endl;
            throw -1;
        }
        // If it is a standard (gaussian) uncertainty
        else if( string(UncertaintyName).find("alpha")!=string::npos ) {
            valnom = 0.0;
        }
        // If it is Lumi:
        else if( UncertaintyName == "Lumi" ) {
            valnom = 1.0;
        }
        // If it is a stat uncertainty (gamma)
        else if( string(UncertaintyName).find("gamma")!=string::npos ){
            valnom = 1.0;
        } // End Stat Error
        else {
            // Some unknown uncertainty
            valnom = 1.0;
        }

        var->setVal(valnom);
        // Done
    } // end loop

    delete iter ;
}


//_____________________________________________________________________________
    void 
Util::resetNominalValue( RooWorkspace* wspace, const RooArgSet& globSet ) 
{
    /// For the given workspace,
    /// find the input systematic with
    /// the given name and shift that
    /// systematic by 1-sigma

    TIterator* iter = globSet.createIterator() ;
    RooAbsArg* arg ;
    while( (arg=(RooAbsArg*)iter->Next()) ) {

        TString UncertaintyName;
        if(arg->InheritsFrom("RooRealVar") && arg->isConstant()){
            UncertaintyName = arg->GetName();
        } else { continue; }

        RooRealVar* var = wspace->var( UncertaintyName.Data() );
        if( ! var ) {
            std::cout<< "Could not find variable: " << UncertaintyName
                << " in workspace: " << wspace->GetName() << ": " << wspace
                << std::endl;
        }

        // Initialize
        double valnom = 0.;

        if( UncertaintyName == "" ) {
            std::cout<< "No Uncertainty Name provided" << std::endl;
            throw -1;
        }
        // If it is Lumi:
        else if( UncertaintyName == TString("nominalLumi") ) {
            valnom = 1.0;
        }
        // If it is a standard (gaussian) uncertainty
        else if ( UncertaintyName.BeginsWith("nom_gamma_stat") ) {
            valnom = 1.0;
        }
        // If it is a standard (gaussian) uncertainty
        else if ( UncertaintyName.BeginsWith("nom") ) {
            valnom = 0.0;
        }
        var->setVal(valnom);

        std::cout<<  "Now resetting: " << UncertaintyName << " to " << valnom << std::endl;
        // Done
    } // end loop

    delete iter ;
}



