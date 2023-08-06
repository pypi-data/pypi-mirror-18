#ifndef BZ_INCLUDED
#define BZ_INCLUDED

#include <iostream>
#include <vector>
#include <complex>
#include <math.h>
#include <string>

class BZ{

  private:
    int kpts;
    int nk;
    double dk;
    double tNN;
    double tNNN;
    double tNNNN;
    double mu;

    int nw = 1;
    double wmin;
    double wmax;

    std::complex <double> ConstSelfEnergy=0;
    std::complex <double> LinSelfEnergy=0;
    
    std::string dispersion;

    std::string SelfEnergyFlag;

    std::vector < std::vector < std::complex <double> > > SelfEnergy;

    const double PI = 3.14159265;

  public:

    void buildSelfEnergy( std::vector < std::vector <std::complex <double> > > lowSelfEnergyFitParams, double wmin, double wmax, int nw );

    void setDispersion(std::string disp, double tNN, double tNNN, double tNNNN, double mu);

    double getDispersion(int kindex);

    double getFermiVelocityX( int kindex );

    double getFermiVelocityY( int kindex );

    double getFermiAccelerationYY( int kindex );

    double getFermiAccelerationXY( int kindex );

    int getKptsInOneDirection(){ return kpts; }

    std::vector <double> getK(int i);

    int getTotalKpts(){ return nk ; }

    int getNw(){ return nw ; }

    double getWmin(){ return wmin; }

    double getWmax(){ return wmax; } 

    BZ( int KptsInOneDirection ); 
    
    ~BZ(){ }

    void toString();

    void setWmin( double wmin){ this -> wmin = wmin;}

    void setNw( int nw){ this -> nw = nw; }
    
    void setWmax( double wmax){ this -> wmax = wmax; }

    void declareFreqGrid( double wmin, double wmax, int nw);

    void setSelfEnergy( std::complex <double> value, int  kindex, int windex );

    std::complex <double> getSelfEnergy( int  kindex, int windex );

    double getDk(){ return dk; }

    double Dispersion2dCubic( int kindex );
    
    double FermiVelocity2dCubicX( int kindex );
   
    double FermiVelocity2dCubicY( int kindex );

    double FermiAcceleration2dCubicYY( int kindex );

    double FermiAcceleration2dCubicXY( int kindex );

    std::vector < std::complex <double> > sumk_complex( std::vector < std::vector < std::complex <double> > > f_w_k, int nw);

    std::vector < double > sumk( std::vector <std::vector <double> > f_w_k, int nw);

};

#endif
