from flask import Flask, request
import os
import time
import json
import random
import subprocess

app = Flask(__name__)

def ranstr(num):
	H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	salt = ''
	for i in range(num):
		salt += random.choice(H)
	return salt


@app.route('/')
def index():
	return '''
    <a href="/genkey">genkey</a><br/>
    '''

@app.route('/genkey')
def genkey():
	alias = ranstr(3)
	keypass = str(time.time())
	keystore = "static/k%s.jks" % time.strftime('%Y%m%d%M%I%S')

	L = random.choice(list(US_CITIES))
	name = "CN={0}, OU={0}{1}, O={2}, L={3}, ST={4}, C=US".format(
		ranstr(3), ranstr(3), ranstr(5), L, random.choice(list(US_CITIES[L])))

	common = 'keytool -genkey -alias %s -keypass %s -storepass %s -dname "%s" -keyalg RSA -validity 2000000 -keystore %s' % (
		alias, keypass, keypass, name, keystore)
	info = subprocess.Popen(
		common, shell=True, stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT).communicate()
	common = 'keytool -exportcert -alias %s -keystore "%s" -storepass %s | openssl sha1 -binary | openssl base64' % (
		alias, keystore, keypass)
	info = subprocess.Popen(
		common, shell=True, stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT).communicate()
	html = name
	html += '<pre>%s</pre><a href="/%s">download</a>' % (info[0], keystore)
	html += "<pre>keyAlias '{1}'\nkeyPassword '{0}'\nstoreFile file('{2}')\nstorePassword '{0}'</pre>".format(
		keypass, alias, keystore[7:])
	return html

US_CITIES = json.loads("{\"New York\":[\"New York\",\"Buffalo\",\"Rochester\",\"Yonkers\",\"Syracuse\",\"Albany\",\"New Rochelle\",\"Mount Vernon\",\"Schenectady\",\"Utica\",\"White Plains\",\"Hempstead\",\"Troy\",\"Niagara Falls\",\"Binghamton\",\"Freeport\",\"Valley Stream\"],\"California\":[\"Los Angeles\",\"San Diego\",\"San Jose\",\"San Francisco\",\"Fresno\",\"Sacramento\",\"Long Beach\",\"Oakland\",\"Bakersfield\",\"Anaheim\",\"Santa Ana\",\"Riverside\",\"Stockton\",\"Chula Vista\",\"Irvine\",\"Fremont\",\"San Bernardino\",\"Modesto\",\"Fontana\",\"Oxnard\",\"Moreno Valley\",\"Huntington Beach\",\"Glendale\",\"Santa Clarita\",\"Garden Grove\",\"Oceanside\",\"Rancho Cucamonga\",\"Santa Rosa\",\"Ontario\",\"Lancaster\",\"Elk Grove\",\"Corona\",\"Palmdale\",\"Salinas\",\"Pomona\",\"Hayward\",\"Escondido\",\"Torrance\",\"Sunnyvale\",\"Orange\",\"Fullerton\",\"Pasadena\",\"Thousand Oaks\",\"Visalia\",\"Simi Valley\",\"Concord\",\"Roseville\",\"Victorville\",\"Santa Clara\",\"Vallejo\",\"Berkeley\",\"El Monte\",\"Downey\",\"Costa Mesa\",\"Inglewood\",\"Carlsbad\",\"San Buenaventura (Ventura)\",\"Fairfield\",\"West Covina\",\"Murrieta\",\"Richmond\",\"Norwalk\",\"Antioch\",\"Temecula\",\"Burbank\",\"Daly City\",\"Rialto\",\"Santa Maria\",\"El Cajon\",\"San Mateo\",\"Clovis\",\"Compton\",\"Jurupa Valley\",\"Vista\",\"South Gate\",\"Mission Viejo\",\"Vacaville\",\"Carson\",\"Hesperia\",\"Santa Monica\",\"Westminster\",\"Redding\",\"Santa Barbara\",\"Chico\",\"Newport Beach\",\"San Leandro\",\"San Marcos\",\"Whittier\",\"Hawthorne\",\"Citrus Heights\",\"Tracy\",\"Alhambra\",\"Livermore\",\"Buena Park\",\"Menifee\",\"Hemet\",\"Lakewood\",\"Merced\",\"Chino\",\"Indio\",\"Redwood City\",\"Lake Forest\",\"Napa\",\"Tustin\",\"Bellflower\",\"Mountain View\",\"Chino Hills\",\"Baldwin Park\",\"Alameda\",\"Upland\",\"San Ramon\",\"Folsom\",\"Pleasanton\",\"Union City\",\"Perris\",\"Manteca\",\"Lynwood\",\"Apple Valley\",\"Redlands\",\"Turlock\",\"Milpitas\",\"Redondo Beach\",\"Rancho Cordova\",\"Yorba Linda\",\"Palo Alto\",\"Davis\",\"Camarillo\",\"Walnut Creek\",\"Pittsburg\",\"South San Francisco\",\"Yuba City\",\"San Clemente\",\"Laguna Niguel\",\"Pico Rivera\",\"Montebello\",\"Lodi\",\"Madera\",\"Santa Cruz\",\"La Habra\",\"Encinitas\",\"Monterey Park\",\"Tulare\",\"Cupertino\",\"Gardena\",\"National City\",\"Rocklin\",\"Petaluma\",\"Huntington Park\",\"San Rafael\",\"La Mesa\",\"Arcadia\",\"Fountain Valley\",\"Diamond Bar\",\"Woodland\",\"Santee\",\"Lake Elsinore\",\"Porterville\",\"Paramount\",\"Eastvale\",\"Rosemead\",\"Hanford\",\"Highland\",\"Brentwood\",\"Novato\",\"Colton\",\"Cathedral City\",\"Delano\",\"Yucaipa\",\"Watsonville\",\"Placentia\",\"Glendora\",\"Gilroy\",\"Palm Desert\",\"Cerritos\",\"West Sacramento\",\"Aliso Viejo\",\"Poway\",\"La Mirada\",\"Rancho Santa Margarita\",\"Cypress\",\"Dublin\",\"Covina\",\"Azusa\",\"Palm Springs\",\"San Luis Obispo\",\"Ceres\",\"San Jacinto\",\"Lincoln\",\"Newark\",\"Lompoc\",\"El Centro\",\"Danville\",\"Bell Gardens\",\"Coachella\",\"Rancho Palos Verdes\",\"San Bruno\",\"Rohnert Park\",\"Brea\",\"La Puente\",\"Campbell\",\"San Gabriel\",\"Beaumont\",\"Morgan Hill\",\"Culver City\",\"Calexico\",\"Stanton\",\"La Quinta\",\"Pacifica\",\"Montclair\",\"Oakley\",\"Monrovia\",\"Los Banos\",\"Martinez\"],\"Illinois\":[\"Chicago\",\"Aurora\",\"Rockford\",\"Joliet\",\"Naperville\",\"Springfield\",\"Peoria\",\"Elgin\",\"Waukegan\",\"Cicero\",\"Champaign\",\"Bloomington\",\"Arlington Heights\",\"Evanston\",\"Decatur\",\"Schaumburg\",\"Bolingbrook\",\"Palatine\",\"Skokie\",\"Des Plaines\",\"Orland Park\",\"Tinley Park\",\"Oak Lawn\",\"Berwyn\",\"Mount Prospect\",\"Normal\",\"Wheaton\",\"Hoffman Estates\",\"Oak Park\",\"Downers Grove\",\"Elmhurst\",\"Glenview\",\"DeKalb\",\"Lombard\",\"Belleville\",\"Moline\",\"Buffalo Grove\",\"Bartlett\",\"Urbana\",\"Quincy\",\"Crystal Lake\",\"Plainfield\",\"Streamwood\",\"Carol Stream\",\"Romeoville\",\"Rock Island\",\"Hanover Park\",\"Carpentersville\",\"Wheeling\",\"Park Ridge\",\"Addison\",\"Calumet City\"],\"Texas\":[\"Houston\",\"San Antonio\",\"Dallas\",\"Austin\",\"Fort Worth\",\"El Paso\",\"Arlington\",\"Corpus Christi\",\"Plano\",\"Laredo\",\"Lubbock\",\"Garland\",\"Irving\",\"Amarillo\",\"Grand Prairie\",\"Brownsville\",\"Pasadena\",\"McKinney\",\"Mesquite\",\"McAllen\",\"Killeen\",\"Frisco\",\"Waco\",\"Carrollton\",\"Denton\",\"Midland\",\"Abilene\",\"Beaumont\",\"Round Rock\",\"Odessa\",\"Wichita Falls\",\"Richardson\",\"Lewisville\",\"Tyler\",\"College Station\",\"Pearland\",\"San Angelo\",\"Allen\",\"League City\",\"Sugar Land\",\"Longview\",\"Edinburg\",\"Mission\",\"Bryan\",\"Baytown\",\"Pharr\",\"Temple\",\"Missouri City\",\"Flower Mound\",\"Harlingen\",\"North Richland Hills\",\"Victoria\",\"Conroe\",\"New Braunfels\",\"Mansfield\",\"Cedar Park\",\"Rowlett\",\"Port Arthur\",\"Euless\",\"Georgetown\",\"Pflugerville\",\"DeSoto\",\"San Marcos\",\"Grapevine\",\"Bedford\",\"Galveston\",\"Cedar Hill\",\"Texas City\",\"Wylie\",\"Haltom City\",\"Keller\",\"Coppell\",\"Rockwall\",\"Huntsville\",\"Duncanville\",\"Sherman\",\"The Colony\",\"Burleson\",\"Hurst\",\"Lancaster\",\"Texarkana\",\"Friendswood\",\"Weslaco\"],\"Pennsylvania\":[\"Philadelphia\",\"Pittsburgh\",\"Allentown\",\"Erie\",\"Reading\",\"Scranton\",\"Bethlehem\",\"Lancaster\",\"Harrisburg\",\"Altoona\",\"York\",\"State College\",\"Wilkes-Barre\"],\"Arizona\":[\"Phoenix\",\"Tucson\",\"Mesa\",\"Chandler\",\"Glendale\",\"Scottsdale\",\"Gilbert\",\"Tempe\",\"Peoria\",\"Surprise\",\"Yuma\",\"Avondale\",\"Goodyear\",\"Flagstaff\",\"Buckeye\",\"Lake Havasu City\",\"Casa Grande\",\"Sierra Vista\",\"Maricopa\",\"Oro Valley\",\"Prescott\",\"Bullhead City\",\"Prescott Valley\",\"Marana\",\"Apache Junction\"],\"Florida\":[\"Jacksonville\",\"Miami\",\"Tampa\",\"Orlando\",\"St. Petersburg\",\"Hialeah\",\"Tallahassee\",\"Fort Lauderdale\",\"Port St. Lucie\",\"Cape Coral\",\"Pembroke Pines\",\"Hollywood\",\"Miramar\",\"Gainesville\",\"Coral Springs\",\"Miami Gardens\",\"Clearwater\",\"Palm Bay\",\"Pompano Beach\",\"West Palm Beach\",\"Lakeland\",\"Davie\",\"Miami Beach\",\"Sunrise\",\"Plantation\",\"Boca Raton\",\"Deltona\",\"Largo\",\"Deerfield Beach\",\"Palm Coast\",\"Melbourne\",\"Boynton Beach\",\"Lauderhill\",\"Weston\",\"Fort Myers\",\"Kissimmee\",\"Homestead\",\"Tamarac\",\"Delray Beach\",\"Daytona Beach\",\"North Miami\",\"Wellington\",\"North Port\",\"Jupiter\",\"Ocala\",\"Port Orange\",\"Margate\",\"Coconut Creek\",\"Sanford\",\"Sarasota\",\"Pensacola\",\"Bradenton\",\"Palm Beach Gardens\",\"Pinellas Park\",\"Coral Gables\",\"Doral\",\"Bonita Springs\",\"Apopka\",\"Titusville\",\"North Miami Beach\",\"Oakland Park\",\"Fort Pierce\",\"North Lauderdale\",\"Cutler Bay\",\"Altamonte Springs\",\"St. Cloud\",\"Greenacres\",\"Ormond Beach\",\"Ocoee\",\"Hallandale Beach\",\"Winter Garden\",\"Aventura\"],\"Indiana\":[\"Indianapolis\",\"Fort Wayne\",\"Evansville\",\"South Bend\",\"Carmel\",\"Bloomington\",\"Fishers\",\"Hammond\",\"Gary\",\"Muncie\",\"Lafayette\",\"Terre Haute\",\"Kokomo\",\"Anderson\",\"Noblesville\",\"Greenwood\",\"Elkhart\",\"Mishawaka\",\"Lawrence\",\"Jeffersonville\",\"Columbus\",\"Portage\"],\"Ohio\":[\"Columbus\",\"Cleveland\",\"Cincinnati\",\"Toledo\",\"Akron\",\"Dayton\",\"Parma\",\"Canton\",\"Youngstown\",\"Lorain\",\"Hamilton\",\"Springfield\",\"Kettering\",\"Elyria\",\"Lakewood\",\"Cuyahoga Falls\",\"Middletown\",\"Euclid\",\"Newark\",\"Mansfield\",\"Mentor\",\"Beavercreek\",\"Cleveland Heights\",\"Strongsville\",\"Dublin\",\"Fairfield\",\"Findlay\",\"Warren\",\"Lancaster\",\"Lima\",\"Huber Heights\",\"Westerville\",\"Marion\",\"Grove City\"],\"North Carolina\":[\"Charlotte\",\"Raleigh\",\"Greensboro\",\"Durham\",\"Winston-Salem\",\"Fayetteville\",\"Cary\",\"Wilmington\",\"High Point\",\"Greenville\",\"Asheville\",\"Concord\",\"Gastonia\",\"Jacksonville\",\"Chapel Hill\",\"Rocky Mount\",\"Burlington\",\"Wilson\",\"Huntersville\",\"Kannapolis\",\"Apex\",\"Hickory\",\"Goldsboro\"],\"Michigan\":[\"Detroit\",\"Grand Rapids\",\"Warren\",\"Sterling Heights\",\"Ann Arbor\",\"Lansing\",\"Flint\",\"Dearborn\",\"Livonia\",\"Westland\",\"Troy\",\"Farmington Hills\",\"Kalamazoo\",\"Wyoming\",\"Southfield\",\"Rochester Hills\",\"Taylor\",\"Pontiac\",\"St. Clair Shores\",\"Royal Oak\",\"Novi\",\"Dearborn Heights\",\"Battle Creek\",\"Saginaw\",\"Kentwood\",\"East Lansing\",\"Roseville\",\"Portage\",\"Midland\",\"Lincoln Park\",\"Muskegon\"],\"Tennessee\":[\"Memphis\",\"Nashville-Davidson\",\"Knoxville\",\"Chattanooga\",\"Clarksville\",\"Murfreesboro\",\"Jackson\",\"Franklin\",\"Johnson City\",\"Bartlett\",\"Hendersonville\",\"Kingsport\",\"Collierville\",\"Cleveland\",\"Smyrna\",\"Germantown\",\"Brentwood\"],\"Massachusetts\":[\"Boston\",\"Worcester\",\"Springfield\",\"Lowell\",\"Cambridge\",\"New Bedford\",\"Brockton\",\"Quincy\",\"Lynn\",\"Fall River\",\"Newton\",\"Lawrence\",\"Somerville\",\"Waltham\",\"Haverhill\",\"Malden\",\"Medford\",\"Taunton\",\"Chicopee\",\"Weymouth Town\",\"Revere\",\"Peabody\",\"Methuen\",\"Barnstable Town\",\"Pittsfield\",\"Attleboro\",\"Everett\",\"Salem\",\"Westfield\",\"Leominster\",\"Fitchburg\",\"Beverly\",\"Holyoke\",\"Marlborough\",\"Woburn\",\"Chelsea\"],\"Washington\":[\"Seattle\",\"Spokane\",\"Tacoma\",\"Vancouver\",\"Bellevue\",\"Kent\",\"Everett\",\"Renton\",\"Yakima\",\"Federal Way\",\"Spokane Valley\",\"Bellingham\",\"Kennewick\",\"Auburn\",\"Pasco\",\"Marysville\",\"Lakewood\",\"Redmond\",\"Shoreline\",\"Richland\",\"Kirkland\",\"Burien\",\"Sammamish\",\"Olympia\",\"Lacey\",\"Edmonds\",\"Bremerton\",\"Puyallup\"],\"Colorado\":[\"Denver\",\"Colorado Springs\",\"Aurora\",\"Fort Collins\",\"Lakewood\",\"Thornton\",\"Arvada\",\"Westminster\",\"Pueblo\",\"Centennial\",\"Boulder\",\"Greeley\",\"Longmont\",\"Loveland\",\"Grand Junction\",\"Broomfield\",\"Castle Rock\",\"Commerce City\",\"Parker\",\"Littleton\",\"Northglenn\"],\"District of Columbia\":[\"Washington\"],\"Maryland\":[\"Baltimore\",\"Frederick\",\"Rockville\",\"Gaithersburg\",\"Bowie\",\"Hagerstown\",\"Annapolis\"],\"Kentucky\":[\"Louisville/Jefferson County\",\"Lexington-Fayette\",\"Bowling Green\",\"Owensboro\",\"Covington\"],\"Oregon\":[\"Portland\",\"Eugene\",\"Salem\",\"Gresham\",\"Hillsboro\",\"Beaverton\",\"Bend\",\"Medford\",\"Springfield\",\"Corvallis\",\"Albany\",\"Tigard\",\"Lake Oswego\",\"Keizer\"],\"Oklahoma\":[\"Oklahoma City\",\"Tulsa\",\"Norman\",\"Broken Arrow\",\"Lawton\",\"Edmond\",\"Moore\",\"Midwest City\",\"Enid\",\"Stillwater\",\"Muskogee\"],\"Wisconsin\":[\"Milwaukee\",\"Madison\",\"Green Bay\",\"Kenosha\",\"Racine\",\"Appleton\",\"Waukesha\",\"Eau Claire\",\"Oshkosh\",\"Janesville\",\"West Allis\",\"La Crosse\",\"Sheboygan\",\"Wauwatosa\",\"Fond du Lac\",\"New Berlin\",\"Wausau\",\"Brookfield\",\"Greenfield\",\"Beloit\"],\"Nevada\":[\"Las Vegas\",\"Henderson\",\"Reno\",\"North Las Vegas\",\"Sparks\",\"Carson City\"],\"New Mexico\":[\"Albuquerque\",\"Las Cruces\",\"Rio Rancho\",\"Santa Fe\",\"Roswell\",\"Farmington\",\"Clovis\"],\"Missouri\":[\"Kansas City\",\"St. Louis\",\"Springfield\",\"Independence\",\"Columbia\",\"Lee's Summit\",\"O'Fallon\",\"St. Joseph\",\"St. Charles\",\"St. Peters\",\"Blue Springs\",\"Florissant\",\"Joplin\",\"Chesterfield\",\"Jefferson City\",\"Cape Girardeau\"],\"Virginia\":[\"Virginia Beach\",\"Norfolk\",\"Chesapeake\",\"Richmond\",\"Newport News\",\"Alexandria\",\"Hampton\",\"Roanoke\",\"Portsmouth\",\"Suffolk\",\"Lynchburg\",\"Harrisonburg\",\"Leesburg\",\"Charlottesville\",\"Danville\",\"Blacksburg\",\"Manassas\"],\"Georgia\":[\"Atlanta\",\"Columbus\",\"Augusta-Richmond County\",\"Savannah\",\"Athens-Clarke County\",\"Sandy Springs\",\"Roswell\",\"Macon\",\"Johns Creek\",\"Albany\",\"Warner Robins\",\"Alpharetta\",\"Marietta\",\"Valdosta\",\"Smyrna\",\"Dunwoody\"],\"Nebraska\":[\"Omaha\",\"Lincoln\",\"Bellevue\",\"Grand Island\"],\"Minnesota\":[\"Minneapolis\",\"St. Paul\",\"Rochester\",\"Duluth\",\"Bloomington\",\"Brooklyn Park\",\"Plymouth\",\"St. Cloud\",\"Eagan\",\"Woodbury\",\"Maple Grove\",\"Eden Prairie\",\"Coon Rapids\",\"Burnsville\",\"Blaine\",\"Lakeville\",\"Minnetonka\",\"Apple Valley\",\"Edina\",\"St. Louis Park\",\"Mankato\",\"Maplewood\",\"Moorhead\",\"Shakopee\"],\"Kansas\":[\"Wichita\",\"Overland Park\",\"Kansas City\",\"Olathe\",\"Topeka\",\"Lawrence\",\"Shawnee\",\"Manhattan\",\"Lenexa\",\"Salina\",\"Hutchinson\"],\"Louisiana\":[\"New Orleans\",\"Baton Rouge\",\"Shreveport\",\"Lafayette\",\"Lake Charles\",\"Kenner\",\"Bossier City\",\"Monroe\",\"Alexandria\"],\"Hawaii\":[\"Honolulu\"],\"Alaska\":[\"Anchorage\"],\"New Jersey\":[\"Newark\",\"Jersey City\",\"Paterson\",\"Elizabeth\",\"Clifton\",\"Trenton\",\"Camden\",\"Passaic\",\"Union City\",\"Bayonne\",\"East Orange\",\"Vineland\",\"New Brunswick\",\"Hoboken\",\"Perth Amboy\",\"West New York\",\"Plainfield\",\"Hackensack\",\"Sayreville\",\"Kearny\",\"Linden\",\"Atlantic City\"],\"Idaho\":[\"Boise City\",\"Nampa\",\"Meridian\",\"Idaho Falls\",\"Pocatello\",\"Caldwell\",\"Coeur d'Alene\",\"Twin Falls\"],\"Alabama\":[\"Birmingham\",\"Montgomery\",\"Mobile\",\"Huntsville\",\"Tuscaloosa\",\"Hoover\",\"Dothan\",\"Auburn\",\"Decatur\",\"Madison\",\"Florence\",\"Gadsden\"],\"Iowa\":[\"Des Moines\",\"Cedar Rapids\",\"Davenport\",\"Sioux City\",\"Iowa City\",\"Waterloo\",\"Council Bluffs\",\"Ames\",\"West Des Moines\",\"Dubuque\",\"Ankeny\",\"Urbandale\",\"Cedar Falls\"],\"Arkansas\":[\"Little Rock\",\"Fort Smith\",\"Fayetteville\",\"Springdale\",\"Jonesboro\",\"North Little Rock\",\"Conway\",\"Rogers\",\"Pine Bluff\",\"Bentonville\"],\"Utah\":[\"Salt Lake City\",\"West Valley City\",\"Provo\",\"West Jordan\",\"Orem\",\"Sandy\",\"Ogden\",\"St. George\",\"Layton\",\"Taylorsville\",\"South Jordan\",\"Lehi\",\"Logan\",\"Murray\",\"Draper\",\"Bountiful\",\"Riverton\",\"Roy\"],\"Rhode Island\":[\"Providence\",\"Warwick\",\"Cranston\",\"Pawtucket\",\"East Providence\",\"Woonsocket\"],\"Mississippi\":[\"Jackson\",\"Gulfport\",\"Southaven\",\"Hattiesburg\",\"Biloxi\",\"Meridian\"],\"South Dakota\":[\"Sioux Falls\",\"Rapid City\"],\"Connecticut\":[\"Bridgeport\",\"New Haven\",\"Stamford\",\"Hartford\",\"Waterbury\",\"Norwalk\",\"Danbury\",\"New Britain\",\"Meriden\",\"Bristol\",\"West Haven\",\"Milford\",\"Middletown\",\"Norwich\",\"Shelton\"],\"South Carolina\":[\"Columbia\",\"Charleston\",\"North Charleston\",\"Mount Pleasant\",\"Rock Hill\",\"Greenville\",\"Summerville\",\"Sumter\",\"Goose Creek\",\"Hilton Head Island\",\"Florence\",\"Spartanburg\"],\"New Hampshire\":[\"Manchester\",\"Nashua\",\"Concord\"],\"North Dakota\":[\"Fargo\",\"Bismarck\",\"Grand Forks\",\"Minot\"],\"Montana\":[\"Billings\",\"Missoula\",\"Great Falls\",\"Bozeman\"],\"Delaware\":[\"Wilmington\",\"Dover\"],\"Maine\":[\"Portland\"],\"Wyoming\":[\"Cheyenne\",\"Casper\"],\"West Virginia\":[\"Charleston\",\"Huntington\"],\"Vermont\":[\"Burlington\"]}")

if __name__ == '__main__':
	app.run(port=81, host='0.0.0.0')
