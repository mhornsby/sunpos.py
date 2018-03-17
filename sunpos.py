# 
# Based on sunposa.php http://www.weather-watch.com/smf/index.php/topic,39197.0.html
# contributors Breitling http://meteo.aerolugo.com/) , Jim McMurry http://www.jcweather.us/ 
# Chuck McGill http://www.westfordweather.net)


import ephem
import pytz
from datetime import datetime , time 
from matplotlib import pyplot as plt
from math import radians as rad,degrees as deg
from matplotlib._png import read_png
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from time import strftime

debug = 0

tz = pytz.timezone("Australia/Melbourne") # choose timezone
today = datetime.now(tz).date()
midnight = tz.localize(datetime.combine(today, time(0, 0)), is_dst=None)

home = ephem.Observer()
home.date = ephem.now()

sun = ephem.Sun()
   
# lat/long in decimal degrees
home.lat , home.long = '-37.8136' , '144.9631'
   
# South: converts to southern hemisphere
def hemisphere( deg ):
    if home.lat < 0 :
       deg = deg + 180
       if deg > 360:
           deg = deg - 360
    return deg

# draw a sun plot
def plotsun( home , plotdate , linecolour , label ):
    posy = []
    posx = []
    sunephem = ephem.Observer()
    sunephem.lat = home.lat
    sunephem.long = home.long
    sunephem.date = ephem.Date( plotdate.tuple()[0:3] )
    for i in range(24*4): # compute position for every 15 minutes
        sun.compute( sunephem )
        posx.append( hemisphere( deg(sun.az))  )
        posy.append(deg(sun.alt))
        sunephem.date += ephem.minute*15
    
    ax.plot( posx, posy , linecolour , label = label )  
 
 
suntime = ephem.Observer()
suntime.lat = home.lat
suntime.long = home.long
suntime.date = ephem.Date( midnight.astimezone(pytz.utc).strftime( '%Y-%m-%d %H:%M:%S' ))

# Find Sunrise / Sunset / Noon
sunrise = suntime.next_rising( ephem.Sun(suntime) ) 
noon = suntime.next_transit( ephem.Sun(suntime) , start=sunrise) 
sunset = suntime.next_setting( ephem.Sun(suntime) ) 
daylight = sunset.datetime() - sunrise.datetime()

# Find Civil Twilight
suntime.horizon = '-6'
beg_civil_twilight = suntime.next_rising( ephem.Sun(), use_center=True) #Begin civil twilight
end_civil_twilight = suntime.next_setting( ephem.Sun(), use_center=True) #End civil twilight

# Find Nautical Twilight
suntime.horizon = '-12'
beg_nautical_twilight = suntime.next_rising( ephem.Sun(), use_center=True) #Begin nautical twilight
end_nautical_twilight = suntime.next_setting( ephem.Sun(), use_center=True)  #End nautical twilight

# Find Astronomical Twilight
suntime.horizon = '-18'
beg_astronomical_twilight = suntime.next_rising(ephem.Sun(), use_center=True) #Begin astronomical twilight
end_astronomical_twilight = suntime.next_setting(ephem.Sun(), use_center=True) #End astronomical twilight

if debug > 0:
    print 'Sunrise : ', ephem.localtime( sunrise )
    print 'Local noon : ' , ephem.localtime( noon )
    print 'Sunset : ' ,  ephem.localtime( sunset )
    print 'Daylight {}:{} hrs'.format( daylight.seconds/3600 , daylight.seconds%60 ) 
    print 'Start Civil Twilight : ' , ephem.localtime( beg_civil_twilight )
    print 'End Civil Twilight : ' , ephem.localtime( end_civil_twilight )
    print 'Start Nautical Twilight : ' , ephem.localtime( beg_nautical_twilight )
    print 'End Nautical Twilight : '  , ephem.localtime( end_nautical_twilight )
    print 'Start Astronomical Twilight : ' , ephem.localtime( beg_astronomical_twilight )
    print 'End Astronomical Twilight : ' ,  ephem.localtime( end_astronomical_twilight )

fig,ax = plt.subplots(figsize=(8,5.5))


# Set Colours 
ax.set_facecolor("black")
fig.patch.set_facecolor('black')
skyword ="Night"

# Work out the Graph background Colour
if home.date >= beg_astronomical_twilight:
    ax.set_facecolor('midnightblue')
    fig.patch.set_facecolor('black')
    skyword ="Astronomical Twilight"
    
if home.date >= beg_nautical_twilight:
    ax.set_facecolor('#191970')
    fig.patch.set_facecolor('black')
    skyword ="Nautical Twilight"
    
if home.date >= beg_civil_twilight:
    ax.set_facecolor("skyblue")
    fig.patch.set_facecolor('orange')
    skyword ="Civil Twilight"
    
if home.date >= beg_civil_twilight and home.date <= sunrise:
    ax.set_facecolor("skyblue")
    fig.patch.set_facecolor('darkorange')
    skyword ="Dawn"

if home.date >= sunrise:
    ax.set_facecolor('lightskyblue')
    fig.patch.set_facecolor('blue')
    skyword ="Day"
        
if home.date >= sunset:
    ax.set_facecolor("skyblue")
    fig.patch.set_facecolor('darkorange')
    skyword ="Dusk"
        
if home.date >= end_civil_twilight:
    ax.set_facecolor('skyblue')
    fig.patch.set_facecolor('orange')
    skyword ="Civil Twilight"
        
if home.date >= end_nautical_twilight:
    ax.set_facecolor('skyblue')
    ffig.patch.set_facecolor('black')
    skyword ="Nautical Twilight"

if home.date >= end_nautical_twilight and home.date <= end_astronomical_twilight:
    ax.set_facecolor("#191970")
    fig.patch.set_facecolor('black')
    skyword ="Astronomical Twilight"
    
if home.date >= end_astronomical_twilight:
    ax.set_facecolor("black")
    fig.patch.set_facecolor('black')
    skyword ="Night"
     
        
# plot the sun
plotsun( home , home.date , 'red' , ephem.localtime(home.date).strftime("%d %b") ) 

# plot the Summer Solstice
plotsun( home ,  ephem.next_summer_solstice( home.date ) , 'cyan' , "Dec 21")

# plot the Winter Solstice
plotsun( home , ephem.next_winter_solstice( home.date ) , 'magenta' , "June 21")

# add the sun image to the plot
sunimage = read_png('sun.png')
imagebox = OffsetImage(sunimage , zoom=.1)
sun.compute( home )
xy = [ hemisphere(deg(sun.az)) ,  deg(sun.alt)   ]   
      
ab = AnnotationBbox(imagebox, xy,
    xybox=(0., 0.),
    xycoords='data',
    frameon=False,
    boxcoords="offset points")                                  
ax.add_artist(ab)

# Create the Axis Labels
xticks = [i for i in range(0,361, 20)]
xtick_labels = ['{}'.format(t+180) if t < 180 else '{}'.format(t-180) for t in xticks]
ax.tick_params(color='white', labelcolor='white')
ax.xaxis.label.set_color('white')
ax.set_xticks(xticks)
ax.set_xticklabels(xtick_labels)

# this can be useful for plotting problems
if debug < 2:
    ax.set_xlim([0,360])
    ax.set_ylim([0,90])

ax.legend()

# Create the label titles
xlabeline1 = "Sun AZ {:.1f}       Sun Alt {:.1f}".format( deg(sun.az) , deg(sun.alt) )
xlabeline2 = 'Sunset: {}          Daylight {}:{} hrs          Sunrise {}'.format( ephem.localtime(sunset).strftime("%H:%M") , daylight.seconds/3600 , daylight.seconds%60, ephem.localtime(sunrise).strftime("%H:%M") )
plt.title("Sun Path {}     {}".format(ephem.localtime(home.date).strftime("%d %b %Y %H:%M") , skyword ) ,  color='white' )
plt.xlabel( "{} \n {}".format( xlabeline1 , xlabeline2 ) )

plt.rc('xtick', labelsize=10) 
plt.rc('ytick', labelsize=10) 
plt.grid(b=True)
plt.show()
    