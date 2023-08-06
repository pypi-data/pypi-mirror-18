#include "functions.h"
#include "brillouin_zone.h"

#include "cmpl_vector.h"
#include <boost/python.hpp>

#include <iostream>
#include <vector>
#include <complex>
#include <math.h>
#include <string>


typedef std::complex<double> Cmpl;
typedef std::__1::complex<double> CmplArg;
typedef std::__1::vector<std::__1::vector<std::__1::complex<double>, std::__1::allocator<std::__1::complex<double> > >, std::__1::allocator<std::__1::vector<std::__1::complex<double>, std::__1::allocator<std::__1::complex<double> > > > > cmpl_matrixArg;
typedef std::__1::vector<std::__1::vector<int, std::__1::allocator<int> >, std::__1::allocator<std::__1::vector<int, std::__1::allocator<int> > > > int_matrixArg;
typedef std::__1::vector<double, std::__1::allocator<double> > double_vecArg;


BOOST_PYTHON_MODULE(brillouin_zone)
{

  namespace py = boost::python;
  // set the docstring of the current module scope
  py::scope().attr("__doc__") = "A module to define a lattice and certain operations on it including summation over all k. The kindex corresponds to the fully reduced wedge of the Brillouin Zone with k=(0,0) (kindex=0), k=(dk_x,0) (kindex=1), ..., k=(pi,pi) (kindex=kmax).\n";


  // converting python input to cpp std::vector in function argument
  iterable_converter()
    .from_python< std::vector<double> >()
    .from_python< std::vector<std::vector<double>> >()
    .from_python< std::vector< Cmpl > >()
    .from_python< std::vector< std::vector<Cmpl> > >()
    ;
/*
  // converting returning std::vector and std::complex to python object
  py::class_< std::vector<double> >("Double_vector")
    .def( py::vector_indexing_suite< std::vector<double> >() )
    ;
  py::class_< std::vector<std::vector<double>> >("Double_matrix")
    .def( py::vector_indexing_suite< std::vector<std::vector<double>> >() )
    ;
  py::class_< std::vector< Cmpl > >("Complex_vector")
    .def( py::vector_indexing_suite< std::vector< Cmpl > >() )
    ;
  py::class_< std::vector< std::vector< Cmpl > > >("Complex_matrix")
    .def( py::vector_indexing_suite< std::vector< std::vector<Cmpl> > >() )
    ;
*/

  // brillouin_zone.h
  py::class_<BZ>("bz",
		"The object bz is primarily defined by the number of k points in one direction (kpts). Hence it is initialized by >>__init>><< :\n\n * brillouin_zone.bz( (int)kpts )\n",        
		py::init< int >()    )

    //.def( "buildSelfEnergy",            &BZ::buildSelfEnergy            )
    .def( "dispersion",              &BZ::setDispersion,
		  py::args( "2dcubic", "t", "t'", "t''", "mu" ) )
    .def( "dispersion",              &BZ::getDispersion,
		  py::args("kindex")   )
    //.def( "getFermiVelocityX",          &BZ::getFermiVelocityX          )
    //.def( "getFermiVelocityY",          &BZ::getFermiVelocityY          )
    //.def( "getFermiAccelerationYY",     &BZ::getFermiAccelerationYY     )
    //.def( "getFermiAccelerationXY",     &BZ::getFermiAccelerationXY     )
    .def( "kpts",      &BZ::getKptsInOneDirection,
		  "Returns the number of k points in one direction"      )

    .def( "k",                       &BZ::getK,
		  py::args("kindex"),
          "Returns {kx,ky} at kindex."                 )

    .def( "nk",               &BZ::getTotalKpts,
		  "Returns the total number of k points in the the fully reduced wedge."    )

    .def( "nw",                      &BZ::getNw,
          "Retuns the number of real frequencies."                      )

    .def( "nw",                      &BZ::setNw,                      
		  "Sets the number of real frequencies."                      )

    .def( "wmin",                    &BZ::getWmin,
		  "Returns the lowest real frequency"                    )

    .def( "wmin",                    &BZ::setWmin,
		  py::args( "wmin" ),             
		  "Sets the lowest real frequency" )

    .def( "wmax",                    &BZ::getWmax,
		  "Returns the highest real frequency"                     )

    .def( "wmax",                    &BZ::setWmax, 
		  py::args( "wmax" ),
		 "Sets the highest real frequency" )

    //.def( "toString",                   &BZ::toString                   )
    .def( "linfreq",            &BZ::declareFreqGrid,
		  py::args( "wmin", "wmax", "nw" ),
		  "Declares a frequency grid."            )

    .def( "selfenergy",              &BZ::setSelfEnergy,
		  py::args( "value", "kindex", "windex" ),
          "Sets the self energy (on the real axis according to >>linfreq<<) at kindex and windex." )
    
     .def( "selfenergy",              &BZ::getSelfEnergy,
		  py::args( "kindex", "windex" ), 
		  "Returns the self energy (on the real axis according to >>linfreq<<) at kindex and windex." )
    
    .def( "dk",                      &BZ::getDk,
          "Returns PI/(kpts-1)"            )

    //.def( "Dispersion2dCubic",          &BZ::Dispersion2dCubic          )
    //.def( "FermiVelocity2dCubicX",      &BZ::FermiVelocity2dCubicX      )
    //.def( "FermiVelocity2dCubicY",      &BZ::FermiVelocity2dCubicY      )
    //.def( "FermiAcceleration2dCubicYY", &BZ::FermiAcceleration2dCubicYY )
    //.def( "FermiAcceleration2dCubicXY", &BZ::FermiAcceleration2dCubicXY )
    
	.def( "sumk",               &BZ::sumk_complex,
		  py::args( "f[kindex][windex]", "nw" ),
          "Performs a k summation over the entire 1 BZ by means of the appropriate weight factor in the fully reduced wedge. (complex)"              )
    
    //.def( "sumk",                       &BZ::sumk,
    //      "Performs a k summation over the entire 1 BZ by means of the appropriate weight factor in the fully reduced wedge. (float)"                       )
    ;

  // functions.h
  //py::def( "gfReFreq",                       gfReFreq                    );
  //py::def( "spectralFunction",               spectralFunction            );
  //py::def( "FermiFunction",                  FermiFunction               );
  //py::def( "FermiFunctionDerivative",        FermiFunctionDerivative     );
  //py::def( "BodeIntegration",                BodeIntegration             );
  //py::def( "extendedSimpsonIntegration",     extendedSimpsonIntegration  );
  //py::def( "getConductivityKubo",            getConductivityKubo         );
  //py::def( "getConductivityLongLifeLimit",   getConductivityLongLifeLimit);
  //py::def( "getHallConductivity",            getHallConductivity         );
  //py::def( "getParameters",                  getParameters               );
  //py::def( "computeLowEnergySelfEnergy",     computeLowEnergySelfEnergy  );
  //py::def( "readLowSelfEnergyFit",           readLowSelfEnergyFit        );
  //py::def( "saveAloc",                       saveAloc                    );
  //py::def( "buildSelfEnergy",                buildSelfEnergy             );

}
