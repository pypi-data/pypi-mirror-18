#include "brillouin_zone.h"

void BZ::buildSelfEnergy( std::vector < std::vector <std::complex <double> > > lowSelfEnergyFitParams, double wmin, double wmax, int nw ){

  std::complex <double> value;
  double w, dw = (wmax - wmin) / (nw - 1) ;

  this -> nw = nw;
  this -> wmin = wmin;
  this -> wmax = wmax;

  if ( int(lowSelfEnergyFitParams.size()) == this -> nk ) {

    this -> SelfEnergyFlag = "k-dep";

    for ( int kindex=0; kindex < nk; kindex++) {

      for ( int windex=0; windex < nw; windex++) {

        w = wmin + windex * dw;

        value = lowSelfEnergyFitParams[kindex][0] + lowSelfEnergyFitParams[kindex][1] * w ;

        setSelfEnergy( value , kindex, windex );

      }

    }

  } else if ( lowSelfEnergyFitParams.size() == 1 ) {

    this -> SelfEnergyFlag = "k-indep";

    for ( int windex=0; windex < nw; windex++) {

      w = wmin + windex * dw;

      value = lowSelfEnergyFitParams[0][0] + lowSelfEnergyFitParams[0][1] * w ;

      setSelfEnergy( value , 0, windex );

    }
  
  } else {

    std::cout << "error: Number of lines in lowSelfenergy.fit must be 1 or equal the total number of k points" << std::endl;

  }

}



std::vector  <double>  BZ::sumk( std::vector < std::vector  <double> > f_w_k, int nw){

  std::vector <double> f_w( nw ) ;
  bool diagWithoutEnds = false;
  int help, help2;
  double factor;
  double Nk = (double) ( (this -> kpts)*(this -> kpts) );

  help2 = (int) (0.5 * (this -> kpts) * ( (this -> kpts) - 1 ));

  for(int windex=0; windex < nw; windex++){

    for(int kindex=0; kindex < this -> nk; kindex++){

      help = (int) ( sqrt( 0.25 + (double) 2 * kindex ) - 0.5 );
      diagWithoutEnds = ( ( ( 0.5 * help * (help + 1) + help ) - kindex ) == 0 );

      if( kindex == 0 ){
        factor = 0.25;
      } else if( diagWithoutEnds ) {
        if( kindex == (nk-1) ) {
          factor = 0.5;
        } else {
          factor = 1.0;
        }
      } else if( kindex > help2 ) {
        factor = 1.0;
      } else {
        factor = 2.0;
      }
      
      f_w[windex] += ( factor * f_w_k[kindex][windex] );

    }

    f_w[windex] = f_w[windex]/ Nk;

  }

  return f_w;
}

void BZ::declareFreqGrid( double wmin, double wmax, int nw){

    this -> wmin = wmin;
    this -> wmax = wmax;
    this -> nw = nw;

}

void BZ::setSelfEnergy(std::complex <double> value, int  kindex, int windex ){
  
  int current_largest_kindex = this -> SelfEnergy.size() - 1 ;

  std::vector <std::complex <double> > dummy(windex+1, {0,0} );

  
  if ( current_largest_kindex >= 0 ) {
    int current_largest_windex = SelfEnergy[current_largest_kindex].size() -1 ;
  
    while ( (current_largest_windex - windex ) < 0 ){

        for (int i = 0; i <= current_largest_kindex ; i++){
  
            SelfEnergy[i].push_back( {0,0} );
   
        }
    
        current_largest_windex = SelfEnergy[current_largest_kindex].size() - 1;
  
    }
  }
  
  while ( (current_largest_kindex - kindex) <= 0 ){
  
    SelfEnergy.push_back( dummy );
  
    current_largest_kindex = SelfEnergy.size();
  
  }

  SelfEnergy[kindex][windex] = value;

}

std::complex <double> BZ::getSelfEnergy( int kindex, int windex ){
  
  if ( SelfEnergyFlag == "k-indep" ) {
    
    kindex = 0;
  
  }

  int current_largest_kindex = SelfEnergy.size() - 1;
  int current_largest_windex = SelfEnergy[current_largest_kindex].size() -1 ;

  if ( ( (current_largest_windex - windex ) < 0 ) || ( ( current_largest_kindex - kindex) < 0 ) ) {

    std::cout << "error: index of self-energy out of range" << std::endl;

  }

  return SelfEnergy[kindex][windex] ;

}


std::vector < std::complex <double> > BZ::sumk_complex( std::vector < std::vector < std::complex <double> > > f_w_k, int nw){

  std::vector < std::complex <double> > f_w( nw ) ;
  bool diagWithoutEnds = false;
  int help, help2;
  double factor;
  double Nk = (double) ( (this -> kpts)*(this -> kpts) );

  help2 = (int) (0.5 * (this -> kpts) * ( (this -> kpts) - 1 ));

  for(int windex=0; windex < nw; windex++){

    for(int kindex=0; kindex < this -> nk; kindex++){

      help = (int) ( sqrt( 0.25 + (double) 2 * kindex ) - 0.5 );
      diagWithoutEnds = ( ( ( 0.5 * help * (help + 1) + help ) - kindex ) == 0 );

      if( kindex == 0 ){
        factor = 0.25;
      } else if( diagWithoutEnds ) {
        if( kindex == (nk-1) ) {
          factor = 0.5;
        } else {
          factor = 1.0;
        }
      } else if( kindex > help2 ) {
        factor = 1.0;
      } else {
        factor = 2.0;
      }
      
      f_w[windex] += ( factor * f_w_k[kindex][windex] );

    }

    f_w[windex] = f_w[windex]/Nk;

  }

  return f_w;
}

double BZ::getDispersion(int kindex){
  double eps=0.; 

  if(this -> dispersion == "2dcubic"){
    eps = this -> Dispersion2dCubic( kindex );
  } else {
    std::cout << "error : set dispersion" << std::endl;
  }
  return eps;
}

double BZ::getFermiVelocityX(int kindex){
  double v=0.; 

  if(this -> dispersion == "2dcubic"){
    v = this -> FermiVelocity2dCubicX( kindex );
  } else {
    std::cout << "error : set dispersion" << std::endl;
  }
  return v;
}

double BZ::getFermiVelocityY(int kindex){
  double v=0.; 

  if(this -> dispersion == "2dcubic"){
    v = this -> FermiVelocity2dCubicY( kindex );
  } else {
    std::cout << "error : set dispersion" << std::endl;
  }
  return v;
}

double BZ::getFermiAccelerationYY(int kindex){
  double v=0.; 

  if(this -> dispersion == "2dcubic"){
    v = this -> FermiAcceleration2dCubicYY( kindex );
  } else {
    std::cout << "error : set dispersion" << std::endl;
  }
  return v;
}

double BZ::getFermiAccelerationXY(int kindex){
  double v=0.; 

  if(this -> dispersion == "2dcubic"){
    v = this -> FermiAcceleration2dCubicXY( kindex );
  } else {
    std::cout << "error : set dispersion" << std::endl;
  }
  return v;
}

void BZ::setDispersion(std::string disp, double tNN, double tNNN=0, double tNNNN=0, double mu=0){
    
    this -> dispersion = disp;
    this -> tNN = tNN;
    this -> tNNN = tNNN;
    this -> tNNNN = tNNNN;
    this -> mu = mu;

}

BZ::BZ( int KptsInOneDirection ){ 
    
      kpts = KptsInOneDirection; 
      dk = this -> PI/(kpts-1);
      nk = (int) ( 0.5 * kpts * ( kpts + 1 ) );

}

void BZ::toString(){
         
      std::cout << "Total amount of k points is " 
          << this -> getTotalKpts()  <<  ", when choosing " 
          << this -> getKptsInOneDirection() 
          << " in one direction." << std::endl;
}

double BZ::Dispersion2dCubic( int kindex ){
    
    std::vector <double> k(2);   
        
    k = this -> getK(kindex);

    return - ( this -> mu )
           + 2. * this -> tNN * ( std::cos(k[0]) + std::cos(k[1]) ) 
           + 4. * this -> tNNN * std::cos(k[0]) * std::cos(k[1])
           + 2. * this -> tNNNN * ( std::cos(2.*k[0]) + std::cos(2.*k[1]) ) ;
}

double BZ::FermiVelocity2dCubicX( int kindex ){
    
    std::vector <double> k(2);   
        
    k = this -> getK(kindex);

    return   2. * std::sin(k[0])*
           ( 2. * this -> tNN *  std::cos(k[1])   
             + 4. * this -> tNNNN * std::cos(k[0])
             + this -> tNNN ) ;
}

double BZ::FermiVelocity2dCubicY( int kindex ){
    
    std::vector <double> k(2);   
        
    k = this -> getK(kindex);

    return   2. * std::sin(k[1])*
           ( 2. * this -> tNN * ( std::cos(k[0]) )  
             + 4. * this -> tNNNN * ( std::cos(k[1]) )
             + this -> tNNN ) ;
}

double BZ::FermiAcceleration2dCubicYY( int kindex ){
    
    std::vector <double> k(2);   
        
    k = this -> getK(kindex);

    return  4. * this -> tNNN * ( std::cos(k[0]) * std::cos(k[1]) )  
            + 8. * this -> tNNNN * std::cos(2.*k[1])
            + 2. * this -> tNN * std::cos(k[1]) ;
}

double BZ::FermiAcceleration2dCubicXY( int kindex ){
    
    std::vector <double> k(2);   
        
    k = this -> getK(kindex);

    return - 4. * (this -> tNNN) * std::sin(k[0]) * std::sin(k[1]) ;
}

std::vector <double> BZ::getK( int i ){
  std::vector <double> k(2);
  int xindex, yindex = 0;
  
  if( i >= this -> getTotalKpts() ){

    std::cout << "ERROR: Index out of bounds" << std::endl;

  } else {

    xindex = (int) ( sqrt( 0.25 + (double) 2 * i ) - 0.5 );
    yindex = 0.5 * xindex * ( xindex + 1 );
    yindex = i - yindex ;

    k[0] = xindex * this -> dk;
    k[1] = yindex * this -> dk;

  }

  return k;
}


