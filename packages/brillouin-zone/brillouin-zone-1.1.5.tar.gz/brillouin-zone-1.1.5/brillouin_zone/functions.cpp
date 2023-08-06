#include "functions.h"

std::vector < std::vector < std::complex <double> > > gfReFreq( BZ grid ){
  int nw = grid.getNw();
  double wmin = grid.getWmin();
  double wmax = grid.getWmax();
  int nk = grid.getTotalKpts();
  std::vector < std::vector < std::complex <double> > >  
         gf(nk, std::vector < std::complex <double> > (nw) );
  double dw = ( ( wmax - wmin )/(nw-1) ) ;

  std::complex <double> w ( wmin ) , eps, sigma;


  for( int kindex=0; kindex < nk; kindex++){
    eps = (grid.getDispersion( kindex )) ;

    for( int windex=0; windex < nw; windex++){
     
      w = (wmin) + (windex*dw) ;

      sigma = grid.getSelfEnergy( kindex, windex );

      gf[kindex][windex] = 1./( w - eps - sigma);

    }
  
  }

  return gf; 
}

std::vector <std::vector <double>> spectralFunction( std::vector < std::vector < std::complex <double> > > gfReFreq, int nk, int nw){
  
  std::vector < std::vector <double> >  
         aw(nk, std::vector <double> (nw) );
  const double PI = 3.14159265;

  for( int kindex=0; kindex < nk; kindex++){
    
    for( int windex=0; windex < nw; windex++){
      
      aw[kindex][windex] = gfReFreq[kindex][windex].imag()/PI;

    }
  }

  return aw; 
}

double FermiFunction( double w, double beta ){
  return 1./( std::exp(beta * w) + 1 );
}

double FermiFunctionDerivative( double w, double beta ){
  double x = std::exp(beta * w);
  return - beta * x / ( ( x + 1 ) * ( x + 1 ) );
}

double BodeIntegration( std::vector < double > f_w, double wmin, double wmax, int nw ){
  double dw =  (wmax - wmin)/( (nw - 1));
  double I = 0, a=14.0/45, b=64.0/45, c=24.0/45;

  for( int windex=0; windex < nw; windex+=4){

    I += dw*( a * (f_w[windex] + f_w[windex+4]) + b * (f_w[windex+1] + f_w[windex+3]) + c * f_w[windex+2] ) ;

  }
  return I;
}

double extendedSimpsonIntegration( std::vector < double > f_w, double wmin, double wmax, int nw ){
  double dw =  (wmax - wmin)/( (nw - 1));
  double I = 0, a=3.0/8, b=7.0/6, c=23.0/24;
  int windex = 0;

  I += dw * a * f_w[windex];

  windex++ ;

  I += dw * b * f_w[windex];

  windex++ ;

  I += dw * c * f_w[windex];

  for( windex = 3; windex < (nw-3); windex++){

    I += dw* f_w[windex] ;

  }

  windex++ ;

  I += dw * c * f_w[windex];

  windex++ ;

  I += dw * b * f_w[windex];

  windex++ ;

  I += dw * a * f_w[windex];

  return I;
}

double getConductivityKubo( std::vector < std::vector <double> > A_w_k, BZ grid,  double beta ){
    double wmin = grid.getWmin(), wmax = grid.getWmax();
    int nw = grid.getNw();
    double dw = (wmax - wmin)/(nw - 1), w, nk = (grid.getTotalKpts() ), vXsquared;
    std::vector < double > negDf_w(nw);
    std::vector <double> FreqIntegralKernel;
    std::vector < std::vector <double> > ksumKernel(nk, std::vector <double> (nw) ); 

    for(int kindex=0; kindex < nk; kindex++){

      for(int windex=0; windex < nw; windex++){
        
        vXsquared = grid.getFermiVelocityX( kindex );
        vXsquared = vXsquared * vXsquared;
        
        ksumKernel[kindex][windex] = A_w_k[kindex][windex] * A_w_k[kindex][windex] * vXsquared;

      }

    }

    FreqIntegralKernel = grid.sumk( ksumKernel, nw);
    
    for(int windex=0; windex < nw; windex++){

      w = wmin + windex * dw;

      negDf_w[windex] = -1 * FermiFunctionDerivative( w, beta );

      FreqIntegralKernel[windex] = FreqIntegralKernel[windex] * negDf_w[windex];
    }

    return BodeIntegration( FreqIntegralKernel, wmin, wmax, nw);
}

double getHallConductivity( std::vector < std::vector <double> > A_w_k, BZ grid , double beta ){
    double wmin = grid.getWmin(), wmax = grid.getWmax();
    int nw = grid.getNw();   
    double dw = (wmax - wmin)/(nw - 1), w, nk = (grid.getTotalKpts() ), vXsquared;
    double vYsquared, aYY, aXY;
    std::vector < double > Df_w(nw);
    std::vector <double> FreqIntegralKernel;
    std::vector < std::vector <double> > ksumKernel(nk, std::vector <double> (nw) ); 

    for(int kindex=0; kindex < nk; kindex++){

      for(int windex=0; windex < nw; windex++){
        
        vXsquared = grid.getFermiVelocityX( kindex );
        vXsquared = vXsquared * vXsquared;

        vYsquared = grid.getFermiVelocityY( kindex );
        vYsquared = vYsquared * vYsquared;

        aYY = grid.getFermiAccelerationYY( kindex );

        aXY = grid.getFermiAccelerationXY( kindex );
        
        ksumKernel[kindex][windex] = 
          A_w_k[kindex][windex] * A_w_k[kindex][windex] * A_w_k[kindex][windex]
          * vXsquared 
          * ( aYY - vYsquared * aXY );

      }

    }

    FreqIntegralKernel = grid.sumk( ksumKernel, nw);
    
    for(int windex=0; windex < nw; windex++){

      w = wmin + windex * dw;

      Df_w[windex] = FermiFunctionDerivative( w, beta );

      FreqIntegralKernel[windex] = FreqIntegralKernel[windex] * Df_w[windex];
    }

    return BodeIntegration( FreqIntegralKernel, wmin, wmax, nw);
}


double getConductivityLongLifeLimit( BZ grid , double gamma, double beta ){
    double nk = ( grid.getTotalKpts() ), vXsquared;
    double negDf_w, w, S;
    //std::complex <double> lifetime = grid.getSelfEnergy( 0 );
    std::vector < std::vector <double> > ksumKernel(nk, std::vector <double> (1) );
    const double PI = 3.14159265;

    for(int kindex=0; kindex < nk; kindex++){

      vXsquared = grid.getFermiVelocityX( kindex );
      vXsquared = vXsquared * vXsquared;
      
      w = grid.getDispersion( kindex );
      negDf_w = -1 * FermiFunctionDerivative( w, beta );

      ksumKernel[kindex][0] = vXsquared * negDf_w;

    }

    S = grid.sumk( ksumKernel, 1)[0];

    return S / ( 2 * PI * gamma );
}

void getParameters(std::string paramFile, std::string phaseptFile, int* kpts, int* nw, double* t, double* tp, double* tpp, double* mu, double* filling, double* wmin, double* wmax, double* beta, std::string* disp){

    std::ifstream param( paramFile );
    std::string dummy;

    if (! param.is_open() ){
        std::cout << "error: file " << paramFile
          << " cannot be opened" << std::endl;
    }

    param >> dummy >> *kpts;
    param >> dummy >> *t; 
    param >> dummy >> *tp;
    param >> dummy >> *tpp;
    param >> dummy >> *disp;
    param >> dummy >> *wmin;
    param >> dummy >> *wmax;
    param >> dummy >> *nw;

    param.close();

    std::ifstream pt( phaseptFile );

    if (! pt.is_open() ){
      std::cout << "error: file " << phaseptFile 
        << " cannot be opened" << std::endl;
    }

    getline( pt , dummy);

    pt >> *beta >> *mu >> *filling;

    pt.close();

}


std::vector < std::vector <std::complex <double> > > readLowSelfEnergyFit(std::string paramFile ){

  std::ifstream param( paramFile );
  std::string header;
  double a, b, c;
  std::complex <double> value0, value1;
  std::vector < std::vector <std::complex <double> > > P;


  if (! param.is_open() ){
    std::cout << "error: file Parameters.in cannot be opened" << std::endl;
  }

  getline( param , header);

  while( param >> a >> b >> c ){
   
    value0 = { a, b };
    
    value1 = { c, 0 };
    
    P.push_back( {value0, value1} );
  
  } 

  param.close();

  return P;

}


void saveAloc(std::string fname2, std::vector < std::vector <double> > A_w_k, BZ grid, int nw, double wmin, double wmax){

    std::vector <double> Aloc;
    double dw = ( (wmax - wmin)/(nw - 1) );

    Aloc = grid.sumk( A_w_k, nw );

    std::ofstream spectral2txt( fname2 );

    if(! spectral2txt) {

      std::cout << "error: file not open" << std::endl;

    } else {

      spectral2txt << "# w, Aw" << std::endl;

      for(int windex=0; windex < nw; windex++){

        spectral2txt << (wmin + windex * dw) << "\t" << Aloc[windex] << std::endl;

      }

      spectral2txt.close();

    }

}

