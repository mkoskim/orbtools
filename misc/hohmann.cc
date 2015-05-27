/********************************************************************
 *
 * Calculate Hohmann transfer trajectory results
 *
 ********************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <math.h>

typedef double FLOAT;
#define PI 3.1415926535894

/* Translating times etc.
 */
#define mins(a)   ((a)*60)
#define hours(a)  ((a)*60*60)
#define days(a)   ((a)*24*60*60)
#define years(a)  ((a)*365*24*60*60)

#define AU(a) ((a)*149.6e9)
#define kg(a) (6.67e-11*(a))


FLOAT expn(FLOAT a, FLOAT b) { return exp(log(a)*b); }
FLOAT fmin(FLOAT a, FLOAT b) { return a<b?a:b; }

void ERROR(char *fmt, ...)
{
   va_list ap;
   va_start(ap, fmt);
   vprintf(fmt, ap);
   va_end(ap);
   exit(-1);
}

/********************************************************************
 *
 * Basic orbital calculations
 *
 ********************************************************************/

 
/*-------------------------------------------------------------------
 * Calculate escape velocity at given distance r
 *-------------------------------------------------------------------
 */
FLOAT v_escape(FLOAT myy, FLOAT r) 
{
   return sqrt(2*myy/r);
}

/*-------------------------------------------------------------------
 * Calculate orbital speed at given distance r. I don't know, if
 * this is correct.
 *-------------------------------------------------------------------
 */
FLOAT v_orbit(FLOAT myy, FLOAT a, FLOAT r) 
{ 
   return v_escape(myy,r)*sqrt(1-r/(2*a));
}

/*-------------------------------------------------------------------
 * Calculate major semiaxis, when given the maximum and minimum
 * distance of ellipse.
 *-------------------------------------------------------------------
 */
FLOAT a_orbit(FLOAT r_min, FLOAT r_max)
{
   return (r_min + r_max)/2.0;
}

/*-------------------------------------------------------------------
 * Calculate period (P)
 *-------------------------------------------------------------------
 */
FLOAT P_orbit(FLOAT myy, FLOAT a)
{
   return sqrt(expn(a,3)*4*PI*PI/myy);
}

/*-------------------------------------------------------------------
 * Calculate the interval (period) of launch window. Seems to
 * give somewhat correct results.
 *-------------------------------------------------------------------
 */
FLOAT P_window(FLOAT myy, FLOAT r1, FLOAT r2)
{
   FLOAT w1 = 1/P_orbit(myy, r1);
   FLOAT w2 = 1/P_orbit(myy, r2);

   return 1/fabs(w2-w1);
}

/*-------------------------------------------------------------------
 * Calculate orbital speed for circular orbit at distance r
 *-------------------------------------------------------------------
 */
FLOAT v_circle(FLOAT myy, FLOAT r)
{
   return sqrt(myy/r);
}

/********************************************************************
 *
 * Special orbital calculations
 *
 ********************************************************************/

/*-------------------------------------------------------------------
 * Calculate distance (r) from specified period (P) to find
 * synchronous orbits. For example, P_GEO is 24h and the
 * distance should be close to 30 000 km.
 *-------------------------------------------------------------------
 */
FLOAT r_from_P(FLOAT myy, FLOAT P)
{
   FLOAT t=expn(P,2)*myy/(4*PI*PI);
   return expn(t,1/3.0);
}

/********************************************************************
 *
 * Hohmann trajectory calculations
 *
 ********************************************************************/

/*-------------------------------------------------------------------
 * Calculate transfer time from distance r1 to distance r2
 *-------------------------------------------------------------------
 */
FLOAT t_hohmann(FLOAT myy, FLOAT r1, FLOAT r2)
{
   return P_orbit(myy, a_orbit(r1,r2))/2;
}

/********************************************************************
 *
 * Formatting the results
 *
 ********************************************************************/

typedef struct
{
   FLOAT max;
   FLOAT divider;
   char *unit;
} FORMATTER;

FORMATTER time_formats[] = {
   { 60,         1,        "s" },
   { hours(2),   mins(1),  "mins" },
   { days(2),    hours(1), "hours" },
   { years(1.5), days(1),  "days" },
   { years(2.5), days(30), "months" },
   { 0,          years(1), "years" }
   };

FORMATTER distance_formats[] = {
   { 1e6*1000, 1000,  "km" },
   { 0,        AU(1), "AU" }
   };

FORMATTER velocity_formats[] = {
   { 0, 1000, "km/s" }};

void print_formatted(FORMATTER *tbl, char *hdr, FLOAT v)
{
   FORMATTER *i = tbl;
   for(;tbl->max; tbl++)
   {
      if(v < tbl->max) break;
   }
   printf("%s %0.3f %s\n",hdr,v/tbl->divider,tbl->unit);
}

#define print_t(f,t) print_formatted(time_formats, f, t)
#define print_r(f,r) print_formatted(distance_formats, f, r)
#define print_v(f,v) print_formatted(velocity_formats, f, v)

/********************************************************************
 *
 * Handling bodies in the solar system (currently our database
 * contains only our Solar system).
 *
 ********************************************************************/

typedef struct
{
   char *name;
   FLOAT mass;
   FLOAT radius;
   FLOAT rotate;

   char *orbits;
   FLOAT distance;

} BODY;

BODY bodies[] = {
   /*Name             Mass(kg) radius(m)   rotate(s)  orbits distance(m) */

   { "Sun",     kg(1.9890e30),    695e6, days(24.6),   NULL,           0 },

   { "Mercury",   kg(3.30e23),   2440e3, days(58.6),  "Sun",  AU(  0.38) },
   { "Venus",     kg(4.87e24),   6052e3, days(-243),  "Sun",  AU(  0.72) },
   { "Earth",     kg(5.97e24),   6378e3, days(0.99),  "Sun",  AU(  1.00) },
   { "Mars",      kg(6.42e23),   3397e3, days(1.03),  "Sun",  AU(  1.52) },
   { "Jupiter",   kg(1.90e27),  71492e3, days(0.41),  "Sun",  AU(  5.20) },
   { "Saturn",    kg(5.68e26),  60268e3, days(0.45),  "Sun",  AU(  9.54) },
   { "Uranus",    kg(8.68e25),  25559e3, days(-0.72), "Sun",  AU(19.218) },
   { "Neptune",   kg(1.02e26),  24766e3, days(0.67),  "Sun",  AU( 30.06) },
   { "Pluto",     kg(1.27e22),   1137e3, days(-6.39), "Sun",  AU( 39.50) },

   { "Moon",      kg(7.35e22),   1738e3, 0,           "Earth",  384400e3 },

   { "Phobos",    kg(1.08e16),     11e3, 0,           "Mars",        9e6 },
   { "Deimos",    kg(1.80e15),      6e3, 0,           "Mars",       23e6 },

   { "Metis",     kg(9.56e16),     20e3, 0,           "Jupiter",   128e6 },
   { "Adrastea",  kg(1.91e16),     10e3, 0,           "Jupiter",   129e6 },
   { "Amalthea",  kg(7.17e18),     94e3, 0,           "Jupiter",   181e6 },
   { "Thebe",     kg(7.77e17),     50e3, 0,           "Jupiter",   222e6 },
   { "Io",        kg(8.93e22),   1821e3, 0,           "Jupiter",   422e6 },
   { "Europa",    kg(4.80e22),   1565e3, 0,           "Jupiter",   671e6 },
   { "Ganymede",  kg(1.48e23),   2634e3, 0,           "Jupiter",  1070e6 },
   { "Callisto",  kg(1.08e23),   2403e3, 0,           "Jupiter",  1883e6 },
   { "Leda",      kg(5.68e15),      8e3, 0,           "Jupiter", 11094e6 },
   { "Himalia",   kg(9.56e18),     93e3, days(0.4),   "Jupiter", 11480e6 },
   { "Lysithea",  kg(7.77e16),     18e3, 0,           "Jupiter", 11720e6 },
   { "Elara",     kg(7.77e17),     38e3, days(0.5),   "Jupiter", 11737e6 },
   { "Ananke",    kg(3.82e16),     15e3, 0,           "Jupiter", 21200e6 },
   { "Carme",     kg(9.56e16),     20e3, 0,           "Jupiter", 22600e6 },
   { "Pasiphae",  kg(1.91e17),     25e3, 0,           "Jupiter", 23500e6 },
   { "Sinope",    kg(7.77e16),     18e3, 0,           "Jupiter", 23700e6 },

/*
"Pan            10     ?       ?   .5    ?       ? 
"Atlas          15     ?       ?   .9   18.0     ?    20 x 10
"Prometheus     46  2.70e17  0.7   .6   15.8     ?    72 x 43 x 32
"Pandora        42  2.20e17  0.7   .9   16.5     ?    57 x 42 x 31
"Epimetheus     57  5.59e17  0.6   .8   15.7     S    69 x 55 x 55
"Janus          89  1.98e18  0.65  .8   14.5     S    99 x 96 x 76
"Mimas         199  3.75e19  1.14  .5   12.9     S
"Enceladus     249  7.30e19  1.12  .99  11.7     S
"Tethys        530  6.22e20  1.00  .9   10.2     S
"Telesto        15     ?       ?   .5   18.7     ?    17 x 14 x 13
"Calypso        13     ?       ?   .6   19.0     ?    17 x 11 x 11
"Dione         560  1.05e21  1.44  .7   10.4     S
"Helene         16     ?       ?   .7   18.4     ?    18 x 16 x 15
"Rhea          764  2.31e21  1.24  .7    9.7     S
"Titan        2575  1.35e23  1.88  .21   8.3     S
"Hyperion      143  1.77e19  1.4   .3   14.2  chaotic 185 x 140 x 113
"Iapetus       718  1.59e21  1.02  .2   11.1     S    (y)
"Phoebe        110  4.00e18  0.7   .06  16.5    0.4          115 x 110 x 105

"Cordelia       13     ?       ?   .07  24.0     ?
"Ophelia        16     ?       ?   .07  24.0     ?
"Bianca         22     ?       ?   .07  23.0     ?
"Cressida       33     ?       ?   .07  22.0     ?
"Desdemona      29     ?       ?   .07  22.0     ?
"Juliet         42     ?       ?   .07  22.0     ?
"Portia         55     ?       ?   .07  21.0     ?
"Rosalind       27     ?       ?   .07  22.0     ?
"Belinda        34     ?       ?   .07  22.0     ?
"1986U10        20
"Puck           77     ?       ?   .07  20.0     ?
"Miranda       236  6.59e19  1.20  .27  16.5     S    240 x 234 x 233
"Ariel         581  1.35e21  1.67  .34  14.4     S    581 x 578 x 578
"Umbriel       585  1.17e21  1.40  .18  15.3     S
"Titania       789  3.53e21  1.71  .27  14.0     S
"Oberon        761  3.01e21  1.63  .24  14.2     S
"Caliban        30                 .07  22
"1999U1         10
"Sycorax        60                 .07  20
"1999U2         10

"Naiad          29     ?       ?   .06  25.0     ?
"Thalassa       40     ?       ?   .06  24.0     ?
"Despina        74     ?       ?   .06  23.0     ?
"Galatea        79     ?       ?   .06  23.0     ?
"Larissa        96     ?       ?   .06  21.0     ?    104 x 89
"Proteus       209     ?       ?   .06  20.0     ?    218 x 208 x 201
"Triton       1353  2.15e22  2.05  .7   13.6     S
"Nereid        170     ?       ?   .2   18.7     ?

Charon        586  1.90e21  2.24  .32  15.5     S    (z)
*/

   /* Some asteroids */
   { "Aten",            kg(0),    0.5e3,          0,  "Sun",    144514e6 },
   { "Amun",            kg(0),    0.0e3,          0,  "Sun",    145710e6 },
   { "Icarus",          kg(0),    0.7e3,          0,  "Sun",    161269e6 },
   { "Gaspra",          kg(0),      8e3,          0,  "Sun",    205000e6 },
   { "Apollo",          kg(0),    0.7e3,          0,  "Sun",    220061e6 },
   { "Ida",             kg(0),     35e3,          0,  "Sun",    270000e6 },
   { "Hephaistos",      kg(0),    4.4e3,          0,  "Sun",    323884e6 },
   { "Vesta",     kg(3.00e20),    265e3,          0,  "Sun",    353400e6 },
   { "Juno",            kg(0),    123e3,          0,  "Sun",    399400e6 },
   { "Eunomia",   kg(8.30e18),    136e3,          0,  "Sun",    395500e6 },
   { "Ceres",     kg(8.70e20),    466e3,          0,  "Sun",    413900e6 },
   { "Pallas",    kg(3.18e20),    261e3,          0,  "Sun",    414500e6 },
/* { "Europa",          kg(0),    156e3,          0,  "Sun",    463300e6 },*/
   { "Hygiea",    kg(9.30e19),    215e3,          0,  "Sun",    470300e6 },
   { "Davida",          kg(0),    168e3,          0,  "Sun",    475400e6 },
   { "Agamemnon",       kg(0),     88e3,          0,  "Sun",    778100e6 },
   { "Chiron",          kg(0),     85e3,          0,  "Sun",   2051900e6 },

   { NULL }};

BODY *find_body(char *name)
{
   BODY *i;

   if(!name) ERROR("NULL body name specified.\n");

   for(i = bodies; i->name; i++)
   {
      if(strcasecmp(name,i->name) == 0) return i;
   }

   ERROR("Body '%s' not found.\n", name);
}

void show_body_info( char *name )
{
   BODY *b = find_body( name );
   BODY *o;
   
   printf ("Name.................: %s\n", b->name);
   printf ("Surface gravity (g)..: %0.3f g\n", b->mass/expn(b->radius,2)/9.81);
   print_v("Escape velocity (ve).:",v_escape(b->mass,b->radius));

   if(!b->orbits) return ;

   o = find_body(b->orbits);
   printf ("Orbits...............: %s\n",b->orbits);
   print_r("At distance..........:",b->distance);
   print_t("Period...............:",P_orbit (o->mass + b->mass,b->distance));
   print_v("Orbital speed (v)....:",v_circle(o->mass + b->mass,b->distance));
}

/********************************************************************
 *
 * Ship trajectory calculations
 *
 ********************************************************************/

/* Engine parameters
 */
typedef struct { FLOAT ve, thrust, mass; } ENGINE;

struct
{
   /* Ship's position in system */
   BODY *central;
   FLOAT r;
   FLOAT v;

   /* Cumulative values for delta-v and transfer time */
   FLOAT dv;
   FLOAT dt;

   /* Values to calculate propellant requirements */
   FLOAT mass;    /* Mass (kg) */
   ENGINE engine; /* Engine parameters */
} ship;

/* ------------------------------------------------------------------
 * Calculate propellant usage
 * ------------------------------------------------------------------
 */
FLOAT M_propellant( void )
{
   return
      (ship.mass + ship.engine.mass) *
      (exp(ship.dv/ship.engine.ve) - 1);
}

/* ------------------------------------------------------------------
 * Calculate velocity using propellant mass
 * ------------------------------------------------------------------
 */

FLOAT v_propellant( FLOAT m )
{
    FLOAT m_empty = ship.mass + ship.engine.mass;
    FLOAT m_full  = m_empty + m;

    return ship.engine.ve * log( m_full / m_empty );
}

/* ------------------------------------------------------------------
 * Ship launch position
 * ------------------------------------------------------------------
 */
void ship_launch(BODY *b, FLOAT r)
{
   ship.central = b;
   ship.dv = 0;
   ship.dt = 0;
   ship.r = b->radius + r;

   printf("Ship starts from: %s\n",b->name);

   if(r)
   {
      ship.v = v_circle(b->mass, ship.r);
   }
   else if(b->rotate)
   {
      ship.v = fabs(2*PI*b->radius/b->rotate);
   }
   else
   {
      ship.v = 0;
   }
   print_r("  Distance (r):", ship.r - ship.central->radius);
   print_v("  Velocity (v):", ship.v);
}

/* ------------------------------------------------------------------
 * Ship escapes from the gravity well of given body
 * ------------------------------------------------------------------
 */
void ship_escape( BODY *dest )
{
again:
   {
      BODY *t = dest;

      for(;;)
      {
         if(t == ship.central) return ;
         if(!t->orbits) break;
         t = find_body(t->orbits);
      }
   }

   {
      BODY *b = find_body(ship.central->orbits);
      FLOAT v_dest = v_escape(ship.central->mass, ship.r);
      FLOAT dv = fabs(v_dest - ship.v);

      ship.dv += dv;
      ship.r = ship.central->distance + b->radius;
      ship.v = v_circle(b->mass, ship.r);

      printf ("Escape: %s->%s\n", ship.central->name, b->name);
      print_v("  dv..:",dv);
      ship.central = b;
   }
   goto again;
}

/* ------------------------------------------------------------------
 * Ship uses Hohmann transfer to given distance r
 * ------------------------------------------------------------------
 */
void ship_hohmann(FLOAT r)
{
   FLOAT myy = ship.central->mass;
   FLOAT R   = ship.central->radius;
   FLOAT r1  = ship.r;
   FLOAT r2  = R + r;
   FLOAT a   = a_orbit(r1, r2);
   FLOAT v_dest1 = v_orbit(myy,a,r1);
   FLOAT v_dest2 = v_orbit(myy,a,r2);
   FLOAT dv = fabs(ship.v - v_dest1);
   FLOAT dt = t_hohmann(myy, r1, r2);

   printf("Hohmann transfer: %s\n",ship.central->name);

   print_r("  r1......:", r1-R);
   print_r("  r2......:", r2-R);
   print_v("  v1......:", ship.v);
   print_v("  v_dest1.:", v_dest1);
   print_v("  v_dest2.:", v_dest2);
   print_v("  dv......:", dv);
   print_t("  t.......:", dt);
   print_t("  window P:", P_window(myy,r1,r2));

   ship.dv += dv;
   ship.dt += dt;
   ship.v   = v_dest2;
   ship.r   = r2;
}

void ship_body_in( BODY *b )
{
   FLOAT R = b->distance + ship.central->radius;
   FLOAT V = v_circle(ship.central->mass, R);

   if(find_body(b->orbits) != ship.central)
      ERROR("%s doesn't orbit %s.\n", b->name,ship.central->name);

   printf ("Transform: %s -> %s\n", ship.central->name, b->name);
   print_v("  V..:",V);
   print_v("  v1.:",ship.v);
   print_v("  v2.:",fabs(ship.v - V));

   ship.v = fabs(ship.v - V);
   ship.r = fabs(ship.r - R);
   ship.central = b;
}

void ship_hohmann_in(BODY *b, FLOAT r)
{
   if(b == ship.central)
   {
      ship_hohmann(r);
   }
   else
   {
      BODY *b1 = find_body(b->orbits);

      printf("Hohmann -> %s\n",b->name);
      if(b1 == ship.central)
      {
         ship_hohmann(b->distance - (r + b->radius));
      }
      else
      {
         ship_hohmann_in(b1,b->distance + r + b->radius);
      }
      ship_body_in( b );
   }
}

void ship_land( void )
{
   FLOAT v_dest;
   FLOAT dv;

   if(ship.r > ship.central->radius)
   {
      v_dest = v_circle(ship.central->mass, ship.r);
      printf ("Orbiting.: %s\n",ship.central->name);
      print_r("  r......:",ship.r-ship.central->radius);
      print_v("  vc.....:",v_dest);
      print_t("  P......:",P_orbit(ship.central->mass, ship.r));
   }
   else
   {
      printf ("Landing..: %s\n",ship.central->name);

      if(ship.central->rotate)
      {
         v_dest = fabs(2*PI*ship.central->radius/ship.central->rotate);
      }
      else
      {
         v_dest = 0;
      }
   }
   dv = fabs(ship.v - v_dest);

   print_v("  v......:",ship.v);
   print_v("  dv.....:",dv);

   ship.dv += dv;
   ship.v = v_dest;
}

void ship_result( void )
{
   FLOAT M_p = M_propellant();
   FLOAT Isp = ship.engine.ve/9.81;
   FLOAT kgf = ship.engine.thrust*1000/9.81;

   printf ("End...............: %s\n",ship.central->name);
   print_v("  Total dv........:",ship.dv);
   print_t("  Total t.........:",ship.dt);
   printf ("  Propellant mass.: %0.3f\n",M_p);
   printf ("  Consumption.....: %0.3f kg/s\n",kgf/Isp);
   print_t("  Burn time.......:",M_p/(kgf/Isp));
}

void ship_transfer(char *name1, FLOAT r1, char *name2, FLOAT r2)
{
   BODY *b1 = find_body(name1);
   BODY *b2 = find_body(name2);

   printf ("Ship transfer:\n");
   printf ("from body....: %s\n", name1);
   print_r("     distance:", r1);
   printf ("to   body....: %s\n", name2);
   print_r("     distance:", r2);

   ship_launch(b1, r1);

   ship_escape(b2);
   ship_hohmann_in(b2,r2);

   ship_land();
   ship_result();
}

#define ISP(a)  ((a)*9.81)
#define ve(a)   (a)
#define kgf(a)  ((a)*9.81/1000)
#define kN(a)   (a)
                    /*    ve        thrust         mass */
ENGINE shuttle_engine = { ISP(455), 3*kgf(232301),    0 };
ENGINE ion_engine     = { ve(30e3),   kN(0.50e-3),    0 };
ENGINE foton_engine   = { 300e6,                0,    0 };

int main( void )
{
   ship.mass = /*(114 + 29.5)*1e3*/ 10000;
   ship.engine = ion_engine;

   //printf("dv = %.3f\n", v_propellant( 50 ));

#if 0
   /* Ekin = 0.5*m*v^2 --> 2E/v^2 = m */
   printf("%g mg\n", (2*2.5e3/expn(30000,2))*1e6);
   return ;
#endif

#if 0
   show_body_info("Earth");
#elif 0
   ship_transfer("Earth", 150e3, "Sun", AU(5.2));
#else
   ship_transfer("Sun", AU(1.1), "Sun", AU(1.0));
#endif
   return 0;
}
