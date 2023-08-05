/*							ellie.c
 *
 *	Incomplete elliptic integral of the second kind
 *
 *
 *
 * SYNOPSIS:
 *
 * double phi, m, y, ellie();
 *
 * y = ellie( phi, m );
 *
 *
 *
 * DESCRIPTION:
 *
 * Approximates the integral
 *
 *
 *                phi
 *                 -
 *                | |
 *                |                   2
 * E(phi_\m)  =    |    sqrt( 1 - m sin t ) dt
 *                |
 *              | |    
 *               -
 *                0
 *
 * of amplitude phi and modulus m, using the arithmetic -
 * geometric mean algorithm.
 *
 *
 *
 * ACCURACY:
 *
 * Tested at random arguments with phi in [-10, 10] and m in
 * [0, 1].
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC        0,2         2000       1.9e-16     3.4e-17
 *    IEEE     -10,10      150000       3.3e-15     1.4e-16
 *
 *
 */


/*
Cephes Math Library Release 2.8:  June, 2000
Copyright 1984, 1987, 1993, 2000 by Stephen L. Moshier
*/

/*	Incomplete elliptic integral of second kind	*/
#include "mconf.h"
extern double NCEPHES_PI, NCEPHES_PIO2, MACHEP;
#ifdef ANSIPROT
extern double sqrt ( double );
extern double fabs ( double );
extern double log ( double );
extern double sin ( double x );
extern double tan ( double x );
extern double atan ( double );
extern double floor ( double );
extern double ellpe ( double );
extern double ellpk ( double );
double ellie ( double, double );
#else
double sqrt(), fabs(), log(), sin(), tan(), atan(), floor();
double ellpe(), ellpk(), ellie();
#endif

double 
ellie (double phi, double m)
{
double a, b, c, e, temp;
double lphi, t, E;
int d, mod, npio2, sign;

if( m == 0.0 )
	return( phi );
lphi = phi;
npio2 = floor( lphi/NCEPHES_PIO2 );
if( npio2 & 1 )
	npio2 += 1;
lphi = lphi - npio2 * NCEPHES_PIO2;
if( lphi < 0.0 )
	{
	lphi = -lphi;
	sign = -1;
	}
else
	{
	sign = 1;
	}
a = 1.0 - m;
E = ellpe( a );
if( a == 0.0 )
	{
	temp = sin( lphi );
	goto done;
	}
t = tan( lphi );
b = sqrt(a);
/* Thanks to Brian Fitzgerald <fitzgb@mml0.meche.rpi.edu>
   for pointing out an instability near odd multiples of pi/2.  */
if( fabs(t) > 10.0 )
	{
	/* Transform the amplitude */
	e = 1.0/(b*t);
	/* ... but avoid multiple recursions.  */
	if( fabs(e) < 10.0 )
		{
		e = atan(e);
		temp = E + m * sin( lphi ) * sin( e ) - ellie( e, m );
		goto done;
		}
	}
c = sqrt(m);
a = 1.0;
d = 1;
e = 0.0;
mod = 0;

while( fabs(c/a) > MACHEP )
	{
	temp = b/a;
	lphi = lphi + atan(t*temp) + mod * NCEPHES_PI;
	mod = (lphi + NCEPHES_PIO2)/NCEPHES_PI;
	t = t * ( 1.0 + temp )/( 1.0 - temp * t * t );
	c = ( a - b )/2.0;
	temp = sqrt( a * b );
	a = ( a + b )/2.0;
	b = temp;
	d += d;
	e += c * sin(lphi);
	}

temp = E / ellpk( 1.0 - m );
temp *= (atan(t) + mod * NCEPHES_PI)/(d * a);
temp += e;

done:

if( sign < 0 )
	temp = -temp;
temp += npio2 * E;
return( temp );
}
