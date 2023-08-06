// Sample vegas integrand written in C
// compile with: cc -fPIC -shared -o cfcn.so cfcn.c (or equivalent)

#include <math.h>

double fcn(double x[], int dim)
{
      int i;
      double xsq = 0.0;
      for(i=0; i<dim; i++)
            xsq += x[i] * x[i] ;
      return exp(-100. * sqrt(xsq)) * pow(100.,dim);
}

/*
# Copyright (c) 2016 G. Peter Lepage.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version (see <http://www.gnu.org/licenses/>).
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
*/