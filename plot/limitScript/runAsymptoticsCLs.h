#ifndef RUNASYMPTOTICSCLS_H
#define RUNASYMPTOTICSCLS_H

#include "RooNLLVar.h"
#include "RooDataSet.h"
#include "RooAbsReal.h"
#include <string>

using namespace std;
using namespace RooFit;

void doExpected(bool isExpected);
void doBetterBands(bool isBetterBands);
void doInjection(bool injection);



//main
void runAsymptoticsCLs(const char* infile,
		       const char* workspaceName,
		       const char* modelConfigName,
		       const char* dataName,
		       const char* asimovDataName,
		       string folder,
		       string mass,
		       double CL);

 //for backwards compatibility
void runAsymptoticsCLs(const char* infile,
		       const char* workspaceName = "combined",
		       const char* modelConfigName = "ModelConfig",
		       const char* dataName = "obsData",
		       const char* asimovDataName = "asimovData_0",
		       const char* conditionalSnapshot = "conditionalGlobs_0",
		       const char* nominalSnapshot = "nominalGlobs",
		       string folder = "test",
		       string mass = "130",
		       double CL = 0.95);

double getLimit(RooNLLVar* nll, double initial_guess = 0);
double getSigma(RooNLLVar* nll, double mu, double muhat, double& qmu);
double getQmu(RooNLLVar* nll, double mu);
void saveSnapshot(RooNLLVar* nll, double mu);
void loadSnapshot(RooNLLVar* nll, double mu);
void doPredictiveFit(RooNLLVar* nll, double mu1, double m2, double mu);
RooNLLVar* createNLL(RooDataSet* _data);
double getNLL(RooNLLVar* nll);
double findCrossing(double sigma_obs, double sigma, double muhat);
void setMu(double mu);
double getQmu95_brute(double sigma, double mu);
double getQmu95(double sigma, double mu);
double calcCLs(double qmu_tilde, double sigma, double mu);
double calcPmu(double qmu_tilde, double sigma, double mu);
double calcPb(double qmu_tilde, double sigma, double mu);
double calcDerCLs(double qmu, double sigma, double mu);
int minimize(RooNLLVar* nll);
int minimize(RooAbsReal* nll);
//RooDataSet* makeAsimovData2(RooDataSet* conditioningData, double mu_true, double mu_prof = -999, string* mu_str = NULL, string* mu_prof_str = NULL);
//RooDataSet* makeAsimovData2(RooNLLVar* conditioningNLL, double mu_true, double mu_prof = -999, string* mu_str = NULL, string* mu_prof_str = NULL);

void unfoldConstraints(RooArgSet& initial, RooArgSet& final, RooArgSet& obs, RooArgSet& nuis, int& counter);
RooDataSet* makeAsimovData(bool doConditional, RooNLLVar* conditioning_nll, double mu_val, string* mu_str = NULL, string* mu_prof_str = NULL, double mu_val_profile = -999, bool doFit = true, double mu_injection = -1);

#endif 
