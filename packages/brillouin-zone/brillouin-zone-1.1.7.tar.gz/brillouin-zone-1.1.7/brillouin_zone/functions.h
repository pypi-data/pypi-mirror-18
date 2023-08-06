#ifndef FUNCTIONS_INCLUDED
#define FUNCTIONS_INCLUDED

#include "brillouin_zone.h"
#include <iostream>
#include <vector>
#include <complex>
#include <math.h>
#include <string>
#include <fstream>

std::vector < std::vector < std::complex <double> > > gfReFreq( BZ grid );

std::vector <std::vector <double>> spectralFunction( std::vector < std::vector < std::complex <double> > > gfReFreq, int nk, int nw);

double FermiFunction( double w, double beta );

double FermiFunctionDerivative( double w, double beta );

double BodeIntegration( std::vector < double > f_w, double wmin, double wmax, int nw );

double extendedSimpsonIntegration( std::vector < double > f_w, double wmin, double wmax, int nw );

double getConductivityKubo( std::vector < std::vector <double> > A_w_k, BZ grid , double beta );

double getConductivityLongLifeLimit( BZ grid, double eta , double beta );

double getHallConductivity( std::vector < std::vector <double> > A_w_k, BZ grid , double beta );

void getParameters(std::string paramFile, std::string phaseptFile, int* kpts, int* nw, double* t, double* tp, double* tpp, double* mu, double* filling, double* wmin, double* wmax, double* beta, std::string* disp);

std::complex <double> computeLowEnergySelfEnergy( double w, std::complex <double> order0 , std::complex <double> order1);

std::vector < std::vector <std::complex <double> > > readLowSelfEnergyFit( std::string paramFile );

void saveAloc(std::string fname2, std::vector < std::vector <double> > A_w_k, BZ grid, int nw, double wmin, double wmax);

BZ buildSelfEnergy( BZ grid, std::vector < std::vector <std::complex <double> > > lowSelfEnergyFitParams, double wmin, double wmax, int nw );

#endif
