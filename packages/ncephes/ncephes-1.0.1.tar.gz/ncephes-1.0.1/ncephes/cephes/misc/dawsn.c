/*							dawsn.c
 *
 *	Dawson's Integral
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, dawsn();
 *
 * y = dawsn( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Approximates the integral
 *
 *                             x
 *                             -
 *                      2     | |        2
 *  dawsn(x)  =  exp( -x  )   |    exp( t  ) dt
 *                          | |
 *                           -
 *                           0
 *
 * Three different rational approximations are employed, for
 * the intervals 0 to 3.25; 3.25 to 6.25; and 6.25 up.
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0,10        10000       6.9e-16     1.0e-16
 *    DEC       0,10         6000       7.4e-17     1.4e-17
 *
 *
 */

/*							dawsn.c */


/*
Cephes Math Library Release 2.8:  June, 2000
Copyright 1984, 1987, 1989, 2000 by Stephen L. Moshier
*/

#include "mconf.h"
/* Dawson's integral, interval 0 to 3.25 */
#ifdef UNK
static double AN[10] = {
 1.13681498971755972054E-11,
 8.49262267667473811108E-10,
 1.94434204175553054283E-8,
 9.53151741254484363489E-7,
 3.07828309874913200438E-6,
 3.52513368520288738649E-4,
-8.50149846724410912031E-4,
 4.22618223005546594270E-2,
-9.17480371773452345351E-2,
 9.99999999999999994612E-1,
};
static double AD[11] = {
 2.40372073066762605484E-11,
 1.48864681368493396752E-9,
 5.21265281010541664570E-8,
 1.27258478273186970203E-6,
 2.32490249820789513991E-5,
 3.25524741826057911661E-4,
 3.48805814657162590916E-3,
 2.79448531198828973716E-2,
 1.58874241960120565368E-1,
 5.74918629489320327824E-1,
 1.00000000000000000539E0,
};
#endif
#ifdef DEC
static unsigned short AN[40] = {
0027107,0176630,0075752,0107612,
0030551,0070604,0166707,0127727,
0031647,0002210,0117120,0056376,
0033177,0156026,0141275,0140627,
0033516,0112200,0037035,0165515,
0035270,0150613,0016423,0105634,
0135536,0156227,0023515,0044413,
0037055,0015273,0105147,0064025,
0137273,0163145,0014460,0166465,
0040200,0000000,0000000,0000000,
};
static unsigned short AD[44] = {
0027323,0067372,0115566,0131320,
0030714,0114432,0074206,0006637,
0032137,0160671,0044203,0026344,
0033252,0146656,0020247,0100231,
0034303,0003346,0123260,0022433,
0035252,0125460,0173041,0155415,
0036144,0113747,0125203,0124617,
0036744,0166232,0143671,0133670,
0037442,0127755,0162625,0000100,
0040023,0026736,0003604,0106265,
0040200,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short AN[40] = {
0x51f1,0x0f7d,0xffb3,0x3da8,
0xf5fb,0x9db8,0x2e30,0x3e0d,
0x0ba0,0x13ca,0xe091,0x3e54,
0xb833,0xd857,0xfb82,0x3eaf,
0xbd6a,0x07c3,0xd290,0x3ec9,
0x7174,0x63a2,0x1a31,0x3f37,
0xa921,0xe4e9,0xdb92,0xbf4b,
0xed03,0x714c,0xa357,0x3fa5,
0x1da7,0xa326,0x7ccc,0xbfb7,
0x0000,0x0000,0x0000,0x3ff0,
};
static unsigned short AD[44] = {
0xd65a,0x536e,0x6ddf,0x3dba,
0xc1b4,0x4f10,0x9323,0x3e19,
0x659c,0x2910,0xfc37,0x3e6b,
0xf013,0xc414,0x59b5,0x3eb5,
0x04a3,0xd4d6,0x60dc,0x3ef8,
0x3b62,0x1ec4,0x5566,0x3f35,
0x7532,0xf550,0x92fc,0x3f6c,
0x36f7,0x58f7,0x9d93,0x3f9c,
0xa008,0xbcb2,0x55fd,0x3fc4,
0x9197,0xc0f0,0x65bb,0x3fe2,
0x0000,0x0000,0x0000,0x3ff0,
};
#endif
#ifdef MIEEE
static unsigned short AN[40] = {
0x3da8,0xffb3,0x0f7d,0x51f1,
0x3e0d,0x2e30,0x9db8,0xf5fb,
0x3e54,0xe091,0x13ca,0x0ba0,
0x3eaf,0xfb82,0xd857,0xb833,
0x3ec9,0xd290,0x07c3,0xbd6a,
0x3f37,0x1a31,0x63a2,0x7174,
0xbf4b,0xdb92,0xe4e9,0xa921,
0x3fa5,0xa357,0x714c,0xed03,
0xbfb7,0x7ccc,0xa326,0x1da7,
0x3ff0,0x0000,0x0000,0x0000,
};
static unsigned short AD[44] = {
0x3dba,0x6ddf,0x536e,0xd65a,
0x3e19,0x9323,0x4f10,0xc1b4,
0x3e6b,0xfc37,0x2910,0x659c,
0x3eb5,0x59b5,0xc414,0xf013,
0x3ef8,0x60dc,0xd4d6,0x04a3,
0x3f35,0x5566,0x1ec4,0x3b62,
0x3f6c,0x92fc,0xf550,0x7532,
0x3f9c,0x9d93,0x58f7,0x36f7,
0x3fc4,0x55fd,0xbcb2,0xa008,
0x3fe2,0x65bb,0xc0f0,0x9197,
0x3ff0,0x0000,0x0000,0x0000,
};
#endif

/* interval 3.25 to 6.25 */
#ifdef UNK
static double BN[11] = {
 5.08955156417900903354E-1,
-2.44754418142697847934E-1,
 9.41512335303534411857E-2,
-2.18711255142039025206E-2,
 3.66207612329569181322E-3,
-4.23209114460388756528E-4,
 3.59641304793896631888E-5,
-2.14640351719968974225E-6,
 9.10010780076391431042E-8,
-2.40274520828250956942E-9,
 3.59233385440928410398E-11,
};
static double BD[10] = {
/*  1.00000000000000000000E0,*/
-6.31839869873368190192E-1,
 2.36706788228248691528E-1,
-5.31806367003223277662E-2,
 8.48041718586295374409E-3,
-9.47996768486665330168E-4,
 7.81025592944552338085E-5,
-4.55875153252442634831E-6,
 1.89100358111421846170E-7,
-4.91324691331920606875E-9,
 7.18466403235734541950E-11,
};
#endif
#ifdef DEC
static unsigned short BN[44] = {
0040002,0045342,0113762,0004360,
0137572,0120346,0172745,0144046,
0037300,0151134,0123440,0117047,
0136663,0025423,0014755,0046026,
0036157,0177561,0027535,0046744,
0135335,0161052,0071243,0146535,
0034426,0154060,0164506,0135625,
0133420,0005356,0100017,0151334,
0032303,0066137,0024013,0046212,
0131045,0016612,0066270,0047574,
0027435,0177025,0060625,0116363,
};
static unsigned short BD[40] = {
/*0040200,0000000,0000000,0000000,*/
0140041,0140101,0174552,0037073,
0037562,0061503,0124271,0160756,
0137131,0151760,0073210,0110534,
0036412,0170562,0117017,0155377,
0135570,0101374,0074056,0037276,
0034643,0145376,0001516,0060636,
0133630,0173540,0121344,0155231,
0032513,0005602,0134516,0007144,
0131250,0150540,0075747,0105341,
0027635,0177020,0012465,0125402,
};
#endif
#ifdef IBMPC
static unsigned short BN[44] = {
0x411e,0x52fe,0x495c,0x3fe0,
0xb905,0xdebc,0x541c,0xbfcf,
0x13c5,0x94e4,0x1a4b,0x3fb8,
0xa983,0x633d,0x6562,0xbf96,
0xa9bd,0x25eb,0xffee,0x3f6d,
0x79ac,0x4e54,0xbc45,0xbf3b,
0xd773,0x1d28,0xdb06,0x3f02,
0xfa5b,0xd001,0x015d,0xbec2,
0x6991,0xe501,0x6d8b,0x3e78,
0x09f0,0x4d97,0xa3b1,0xbe24,
0xb39e,0xac32,0xbfc2,0x3dc3,
};
static unsigned short BD[40] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x47c7,0x3f2d,0x3808,0xbfe4,
0x3c3e,0x7517,0x4c68,0x3fce,
0x122b,0x0ed1,0x3a7e,0xbfab,
0xfb60,0x53c1,0x5e2e,0x3f81,
0xc7d8,0x8f05,0x105f,0xbf4f,
0xcc34,0xc069,0x795f,0x3f14,
0x9b53,0x145c,0x1eec,0xbed3,
0xc1cd,0x5729,0x6170,0x3e89,
0xf15c,0x0f7c,0x1a2c,0xbe35,
0xb560,0x02a6,0xbfc2,0x3dd3,
};
#endif
#ifdef MIEEE
static unsigned short BN[44] = {
0x3fe0,0x495c,0x52fe,0x411e,
0xbfcf,0x541c,0xdebc,0xb905,
0x3fb8,0x1a4b,0x94e4,0x13c5,
0xbf96,0x6562,0x633d,0xa983,
0x3f6d,0xffee,0x25eb,0xa9bd,
0xbf3b,0xbc45,0x4e54,0x79ac,
0x3f02,0xdb06,0x1d28,0xd773,
0xbec2,0x015d,0xd001,0xfa5b,
0x3e78,0x6d8b,0xe501,0x6991,
0xbe24,0xa3b1,0x4d97,0x09f0,
0x3dc3,0xbfc2,0xac32,0xb39e,
};
static unsigned short BD[40] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0xbfe4,0x3808,0x3f2d,0x47c7,
0x3fce,0x4c68,0x7517,0x3c3e,
0xbfab,0x3a7e,0x0ed1,0x122b,
0x3f81,0x5e2e,0x53c1,0xfb60,
0xbf4f,0x105f,0x8f05,0xc7d8,
0x3f14,0x795f,0xc069,0xcc34,
0xbed3,0x1eec,0x145c,0x9b53,
0x3e89,0x6170,0x5729,0xc1cd,
0xbe35,0x1a2c,0x0f7c,0xf15c,
0x3dd3,0xbfc2,0x02a6,0xb560,
};
#endif

/* 6.25 to infinity */
#ifdef UNK
static double CN[5] = {
-5.90592860534773254987E-1,
 6.29235242724368800674E-1,
-1.72858975380388136411E-1,
 1.64837047825189632310E-2,
-4.86827613020462700845E-4,
};
static double CD[5] = {
/* 1.00000000000000000000E0,*/
-2.69820057197544900361E0,
 1.73270799045947845857E0,
-3.93708582281939493482E-1,
 3.44278924041233391079E-2,
-9.73655226040941223894E-4,
};
#endif
#ifdef DEC
static unsigned short CN[20] = {
0140027,0030427,0176477,0074402,
0040041,0012617,0112375,0162657,
0137461,0000761,0074120,0135160,
0036607,0004325,0117246,0115525,
0135377,0036345,0064750,0047732,
};
static unsigned short CD[20] = {
/*0040200,0000000,0000000,0000000,*/
0140454,0127521,0071653,0133415,
0040335,0144540,0016105,0045241,
0137711,0112053,0155034,0062237,
0037015,0002102,0177442,0074546,
0135577,0036345,0064750,0052152,
};
#endif
#ifdef IBMPC
static unsigned short CN[20] = {
0xef20,0xffa7,0xe622,0xbfe2,
0xbcb6,0xf29f,0x22b1,0x3fe4,
0x174e,0x2f0a,0x203e,0xbfc6,
0xd36b,0xb3d4,0xe11a,0x3f90,
0x09fb,0xad3d,0xe79c,0xbf3f,
};
static unsigned short CD[20] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x76e2,0x2e75,0x95ea,0xc005,
0xa954,0x0388,0xb92c,0x3ffb,
0x8c94,0x7b43,0x3285,0xbfd9,
0x4f2d,0x5fe4,0xa088,0x3fa1,
0x0a8d,0xad3d,0xe79c,0xbf4f,
};
#endif
#ifdef MIEEE
static unsigned short CN[20] = {
0xbfe2,0xe622,0xffa7,0xef20,
0x3fe4,0x22b1,0xf29f,0xbcb6,
0xbfc6,0x203e,0x2f0a,0x174e,
0x3f90,0xe11a,0xb3d4,0xd36b,
0xbf3f,0xe79c,0xad3d,0x09fb,
};
static unsigned short CD[20] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0xc005,0x95ea,0x2e75,0x76e2,
0x3ffb,0xb92c,0x0388,0xa954,
0xbfd9,0x3285,0x7b43,0x8c94,
0x3fa1,0xa088,0x5fe4,0x4f2d,
0xbf4f,0xe79c,0xad3d,0x0a8d,
};
#endif

#ifdef ANSIPROT
extern double chbevl ( double, void *, int );
extern double sqrt ( double );
extern double fabs ( double );
extern double polevl ( double, void *, int );
extern double p1evl ( double, void *, int );
#else
double chbevl(), sqrt(), fabs(), polevl(), p1evl();
#endif
extern double NCEPHES_PI, MACHEP;

double 
dawsn (double xx)
{
double x, y;
int sign;


sign = 1;
if( xx < 0.0 )
	{
	sign = -1;
	xx = -xx;
	}

if( xx < 3.25 )
{
x = xx*xx;
y = xx * polevl( x, AN, 9 )/polevl( x, AD, 10 );
return( sign * y );
}


x = 1.0/(xx*xx);

if( xx < 6.25 )
	{
	y = 1.0/xx + x * polevl( x, BN, 10) / (p1evl( x, BD, 10) * xx);
	return( sign * 0.5 * y );
	}


if( xx > 1.0e9 )
	return( (sign * 0.5)/xx );

/* 6.25 to infinity */
y = 1.0/xx + x * polevl( x, CN, 4) / (p1evl( x, CD, 5) * xx);
return( sign * 0.5 * y );
}
