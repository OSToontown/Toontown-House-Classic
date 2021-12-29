#coding: latin-1
#Translated by Jean #:P #GONNA RAPE YOU
from __future__ import unicode_literals
from L10NLocalizerFrenchCogs import data as CogData
from L10NLocalizerFrenchSC import data as SpeedChatData
from L10NLocalizerFrenchTips import data as TipData
from L10NLocalizerFrenchOld import data as OldData

NAMES_FILE_PATH = 'data/etc/languages/names_fr.l10n'

CATNameShopReview = '\
The Toontown House staff\nwill review your\nname.  \
Review may\ntake a few days.\nWhile you wait\nyour name will be\n '
CATNameShopContinueSubmission = 'Continuer l\'envoi'
CATNameShopChooseAnother = 'Choisir un autre nom'
CATAllNewNames = 'Tous les nouveaux noms sont\napprouv�s par un membre de l\'�quipe..'

DialogSpecial = 'ooo'
DialogExclamation = '!'
DialogQuestion = '?'

ToonSleepString = '. . . ZZZ . . .'

FishNames=(
           ('Poisson Clown','Poisson Clown Triste','Poisson Clown F�tif','Poisson Clown de cirque'),
           ('Poisson baudruche','Poisson baudruche � air chaud','Poisson baudruche m�t�o','Poisson baudruche � eau','Poisson baudruche rouge'),
           ('Poisson-chat','Poisson-chat Siamois','Poisson-chat de goutti�re','Poisson-chat Tigr�','Poisson-chat Tom'),
           ('Raie Diabolique',),
           ('Poisson Congel�',),
           ('�toile de m�r','�toile de m�r 5 �toiles','�toile de m�r Rock','�toile de m�r brillante','�toile de m�r Vedette'),
           ('Macaratrou',),
           ('Poisson Chien','Poisson Bull Dog','Poisson Chien Chaud','Poisson Dalamatien','Poisson Chiot'),
           ('Anguille Amore','Anguille Amore �lectrique'),
           ('Inferimi�re Requin','Inferimi�re Clara Requin','Inferimi�re Florence Requin'),
           ('Roi Crabe','Roi Crabe d\'Alaska','Vieux Roi Crabe'),
           ('Poisson Lune','Full Moon Fish','Half Moon Fish','New Moon Fish','Crescent Moon Fish','Harvest Moon Fish'),
           ('Hippocaval','Hippocaval Rock','Hippocaval Clydesdale','Hippocaval Ar�be'),
           ('Requin Billard','Requin Billard Tout-p\'tit','Requin Billard Nageant','Requin Billard Olympique'),
           ('Ours Brun Acuda','Ours Noir Acuda','Ours Koala Acuda','Ours � Miel Acuda','Ours Polaire Acuda','Ours Panda Acuda','Kodiac Bear Acuda','Ours des F�rets Acuda'),
           ('Truite Assassin','Captaine Truite Assassin','Truite Assassin Scorbut'),
           ('Pianthon','Pianthon Magnifique','Pianthon B�b� Magnifique','Pianthon Droit','Pianthon Joueur'),
           ('Beurre d\'arachide&Confiduse','Poisson B&C au Raisins','Poisson B&C Croustillant','Poisson B&C au Fraises','Poisson B&C au Raisins en harmonie'),
           )

FishingTankFull = 'Ton seau de p�che est plein. Va vendre tes poissons au marchand de l\'animalerie et reviens ici.'
FishingBroke = 'Tu n\'as plus assez de bonbons comme app�t. Va sur le tramway ou vends tes poissons au marchand de l\'animalerie pour recevoir plus de bonbons.'

FishPickerTotalValue = 'Seau: %s / %s\nValeur : %d bonbons'

FishingExit = 'Quitter'
FishingCast = 'Lancer'
FishingItemFound = 'Tu as attrap� :'
FishingBootItem = 'Une vielle botte'

FishGuiCancel = 'Annuler'
FishGuiOk = 'Vendre tout'

FishTankValue = 'Salut, %(name)s! Tu as %(num)s poissons dans ton seau, ce qui vaut un total de %(value)s bonbons. Veux-tu tous les vendre ?'

#When we get npcs out, i'll translate this shit out >_< #HUH NOPE
lHQOfficerM = lHQOfficerF = "Officier du QG"
NPCToonNames = {20000: 'Tutoriel Tom',
 999: 'Toon Tailor',
 1000: '<lToonHq>',
 20001: 'Flippy',
 2001: 'Flippy',
 2002: 'Bob le banquier',
 2003: 'Professeur Pete',
 2004: 'Tammy the Tailor',
 2005: 'Librarian Larry',
 2006: 'Clerk Clark',
 2011: 'Clerk Clara',
 2007: lHQOfficerM,
 2008: lHQOfficerM,
 2009: lHQOfficerF,
 2010: lHQOfficerF,
 2012: 'Fisherman Freddy',
 2018: 'Duff..err..TIP Man',
 2013: 'Clerk Poppy',
 2014: 'Clerk Peppy',
 2015: 'Clerk Pappy',
 2016: 'Party Planner Pumpkin',
 2017: 'Party Planner Polly',
 2018: 'Doctor Surlee',
 2019: 'Doctor Dimm',
 2020: 'Professor Prepostera',
 2101: 'Dentist Daniel',
 2102: 'Sheriff Sherry',
 2103: 'Sneezy Kitty',
 2104: lHQOfficerM,
 2105: lHQOfficerM,
 2106: lHQOfficerF,
 2107: lHQOfficerF,
 2108: 'Canary Coalmine',
 2109: 'Babbles Blowhard',
 2110: 'Bill Board',
 2111: 'Dancing Diego',
 2112: 'Dr. Tom',
 2113: 'Rollo The Amazing',
 2114: 'Roz Berry',
 2115: 'Patty Papercut',
 2116: 'Bruiser McDougal',
 2117: 'Ma Putrid',
 2118: 'Jesse Jester',
 2119: 'Honey Haha',
 2120: 'Professor Binky',
 2121: 'Madam Chuckle',
 2122: 'Harry Ape',
 2123: 'Spamonia Biggles',
 2124: 'T.P. Rolle',
 2125: 'Lazy Hal',
 2126: 'Professor Guffaw',
 2127: 'Woody Nickel',
 2128: 'Loony Louis',
 2129: 'Frank Furter',
 2130: 'Joy Buzzer',
 2131: 'Feather Duster',
 2132: 'Daffy Don',
 2133: 'Dr. Euphoric',
 2134: 'Silent Simone',
 2135: 'Mary',
 2136: 'Sal Snicker',
 2137: 'Happy Heikyung',
 2138: 'Muldoon',
 2139: 'Dan Dribbles',
 2140: 'Fisherman Billy',
 2201: 'Postmaster Pete',
 2202: 'Shirley U. Jest',
 2203: lHQOfficerM,
 2204: lHQOfficerM,
 2205: lHQOfficerF,
 2206: lHQOfficerF,
 2207: 'Will Wiseacre',
 2208: 'Sticky Lou',
 2209: 'Charlie Chortle',
 2210: 'Tee Hee',
 2211: 'Sally Spittake',
 2212: 'Weird Warren',
 2213: 'Lucy Tires',
 2214: 'Sam Stain',
 2215: 'Sid Seltzer',
 2216: 'Nona Seeya',
 2217: 'Sharky Jones',
 2218: 'Fanny Pages',
 2219: 'Chef Knucklehead',
 2220: 'Rick Rockhead',
 2221: 'Clovinia Cling',
 2222: 'Shorty Fuse',
 2223: 'Sasha Sidesplitter',
 2224: 'Smokey Joe',
 2225: 'Fisherman Droopy',
 2301: 'Dr. Pulyurleg',
 2302: 'Professor Wiggle',
 2303: 'Nurse Nancy',
 2304: lHQOfficerM,
 2305: lHQOfficerM,
 2306: lHQOfficerF,
 2307: lHQOfficerF,
 2308: 'Nancy Gas',
 2309: 'Big Bruce',
 2311: 'Franz Neckvein',
 2312: 'Dr. Sensitive',
 2313: 'Lucy Shirtspot',
 2314: 'Ned Slinger',
 2315: 'Chewy Morsel',
 2316: 'Cindy Sprinkles',
 2318: 'Tony Maroni',
 2319: 'Zippy',
 2320: 'Crunchy Alfredo',
 2321: 'Fisherman Punchy',
 1001: 'Clerk Will',
 1002: 'Clerk Bill',
 1003: lHQOfficerM,
 1004: lHQOfficerF,
 1005: lHQOfficerM,
 1006: lHQOfficerF,
 1007: 'Longjohn Leroy',
 1008: 'Fisherman Furball',
 1009: 'Clerk Barky',
 1010: 'Clerk Purr',
 1011: 'Clerk Bloop',
 1012: 'Party Planner Pickles',
 1013: 'Party Planner Patty',
 1101: 'Billy Budd',
 1102: 'Captain Carl',
 1103: 'Fishy Frank',
 1104: 'Doctor Squall',
 1105: 'Admiral Hook',
 1106: 'Mrs. Starch',
 1107: 'Cal Estenicks',
 1108: lHQOfficerM,
 1109: lHQOfficerF,
 1110: lHQOfficerM,
 1111: lHQOfficerF,
 1112: 'Gary Glubglub',
 1113: 'Lisa Luff',
 1114: 'Charlie Chum',
 1115: 'Sheila Squid, Atty',
 1116: 'Barnacle Bessie',
 1117: 'Captain Yucks',
 1118: 'Choppy McDougal',
 1121: 'Linda Landlubber',
 1122: 'Salty Stan',
 1123: 'Electra Eel',
 1124: 'Flappy Docksplinter',
 1125: 'Eileen Overboard',
 1126: 'Fisherman Barney',
 1201: 'Barnacle Barbara',
 1202: 'Art',
 1203: 'Ahab',
 1204: 'Rocky Shores',
 1205: lHQOfficerM,
 1206: lHQOfficerF,
 1207: lHQOfficerM,
 1208: lHQOfficerF,
 1209: 'Professor Plank',
 1210: 'Gang Wei',
 1211: 'Wynn Bag',
 1212: 'Toby Tonguestinger',
 1213: 'Dante Dolphin',
 1214: 'Gusty Kate',
 1215: 'Dinah Down',
 1216: 'Rod Reel',
 1217: 'CC Weed',
 1218: 'Pacific Tim',
 1219: 'Brian Beachead',
 1220: 'Carla Canal',
 1221: 'Blisters McKee',
 1222: 'Shep Ahoy',
 1223: 'Sid Squid',
 1224: 'Emily Eel',
 1225: 'Bonzo Bilgepump',
 1226: 'Heave Ho',
 1227: 'Coral Reef',
 1228: 'Fisherman Reed',
 1301: 'Alice',
 1302: 'Melville',
 1303: 'Claggart',
 1304: 'Svetlana',
 1305: lHQOfficerM,
 1306: lHQOfficerF,
 1307: lHQOfficerM,
 1308: lHQOfficerF,
 1309: 'Seafoam',
 1310: 'Ted Tackle',
 1311: 'Topsy Turvey',
 1312: 'Ethan Keel',
 1313: 'William Wake',
 1314: 'Rusty Ralph',
 1315: 'Doctor Drift',
 1316: 'Wilma Wobble',
 1317: 'Paula Pylon',
 1318: 'Dinghy Dan',
 1319: 'Davey Drydock',
 1320: 'Ted Calm',
 1321: 'Dinah Docker',
 1322: 'Whoopie Cushion',
 1323: 'Stinky Ned',
 1324: 'Pearl Diver',
 1325: 'Ned Setter',
 1326: 'Felicia Chips',
 1327: 'Cindy Splat',
 1328: 'Fred Flounder',
 1329: 'Shelly Seaweed',
 1330: 'Porter Hole',
 1331: 'Rudy Rudder',
 1332: 'Fisherman Shane',
 3001: 'Betty Freezes',
 3002: lHQOfficerM,
 3003: lHQOfficerF,
 3004: lHQOfficerM,
 3005: lHQOfficerM,
 3006: 'Clerk Lenny',
 3007: 'Clerk Penny',
 3008: 'Warren Bundles',
 3009: 'Fisherman Frizzy',
 3010: 'Clerk Skip',
 3011: 'Clerk Dip',
 3012: 'Clerk Kipp',
 3013: 'Party Planner Pete',
 3014: 'Party Planner Penny',
 3101: 'Mr. Cow',
 3102: 'Auntie Freeze',
 3103: 'Fred',
 3104: 'Bonnie',
 3105: 'Frosty Freddy',
 3106: 'Gus Gooseburger',
 3107: 'Patty Passport',
 3108: 'Toboggan Ted',
 3109: 'Kate',
 3110: 'Chicken Boy',
 3111: 'Snooty Sinjin',
 3112: 'Lil Oldman',
 3113: 'Hysterical Harry',
 3114: 'Henry the Hazard',
 3115: lHQOfficerM,
 3116: lHQOfficerF,
 3117: lHQOfficerM,
 3118: lHQOfficerM,
 3119: 'Creepy Carl',
 3120: 'Mike Mittens',
 3121: 'Joe Shockit',
 3122: 'Lucy Luge',
 3123: 'Frank Lloyd Ice',
 3124: 'Lance Iceberg',
 3125: 'Colonel Crunchmouth',
 3126: 'Colestra Awl',
 3127: 'Ifalla Yufalla',
 3128: 'Sticky George',
 3129: 'Baker Bridget',
 3130: 'Sandy',
 3131: 'Lazy Lorenzo',
 3132: 'Ashy',
 3133: 'Dr. Friezeframe',
 3134: 'Lounge Lassard',
 3135: 'Soggy Nell',
 3136: 'Happy Sue',
 3137: 'Mr. Freeze',
 3138: 'Chef Bumblesoup',
 3139: 'Granny Icestockings',
 3140: 'Fisherman Lucille',
 3201: 'Aunt Arctic',
 3202: 'Shakey',
 3203: 'Walt',
 3204: 'Dr. Ivanna Cee',
 3205: 'Bumpy Noggin',
 3206: 'Vidalia VaVoom',
 3207: 'Dr. Mumbleface',
 3208: 'Grumpy Phil',
 3209: 'Giggles McGhee',
 3210: 'Simian Sam',
 3211: 'Fanny Freezes',
 3212: 'Frosty Fred',
 3213: lHQOfficerM,
 3214: lHQOfficerF,
 3215: lHQOfficerM,
 3216: lHQOfficerM,
 3217: 'Sweaty Pete',
 3218: 'Blue Lou',
 3219: 'Tom Tandemfrost',
 3220: 'Mr. Sneeze',
 3221: 'Nelly Snow',
 3222: 'Mindy Windburn',
 3223: 'Chappy',
 3224: 'Freida Frostbite',
 3225: 'Blake Ice',
 3226: 'Santa Paws',
 3227: 'Solar Ray',
 3228: 'Wynne Chill',
 3229: 'Hernia Belt',
 3230: 'Balding Benjy',
 3231: 'Choppy',
 3232: 'Fisherman Albert',
 3301: 'Paisley Patches',
 3302: 'Bjorn Bord',
 3303: 'Dr. Peepers',
 3304: 'Eddie the Yeti',
 3305: 'Mack Ramay',
 3306: 'Paula Behr',
 3307: 'Fisherman Fredrica',
 3308: 'Donald Frump',
 3309: 'Bootsy',
 3310: 'Professor Flake',
 3311: 'Connie Ferris',
 3312: 'March Harry',
 3313: lHQOfficerM,
 3314: lHQOfficerF,
 3315: lHQOfficerM,
 3316: lHQOfficerF,
 3317: 'Kissy Krissy',
 3318: 'Johnny Cashmere',
 3319: 'Sam Stetson',
 3320: 'Fizzy Lizzy',
 3321: 'Pickaxe Paul',
 3322: 'Flue Lou',
 3323: 'Dallas Borealis',
 3324: 'Snaggletooth Stu',
 3325: 'Groovy Garland',
 3326: 'Blanche',
 3327: 'Chuck Roast',
 3328: 'Shady Sadie',
 3329: 'Treading Ed',
 4001: 'Molly Molloy',
 4002: lHQOfficerM,
 4003: lHQOfficerF,
 4004: lHQOfficerF,
 4005: lHQOfficerF,
 4006: 'Clerk Doe',
 4007: 'Clerk Ray',
 4008: 'Tailor Harmony',
 4009: 'Fisherman Fanny',
 4010: 'Clerk Chris',
 4011: 'Clerk Neil',
 4012: 'Clerk Westin Girl',
 4013: 'Party Planner Preston',
 4014: 'Party Planner Penelope',
 4101: 'Tom',
 4102: 'Fifi',
 4103: 'Dr. Fret',
 4104: lHQOfficerM,
 4105: lHQOfficerF,
 4106: lHQOfficerF,
 4107: lHQOfficerF,
 4108: 'Cleff',
 4109: 'Carlos',
 4110: 'Metra Gnome',
 4111: 'Tom Hum',
 4112: 'Fa',
 4113: 'Madam Manners',
 4114: 'Offkey Eric',
 4115: 'Barbara Seville',
 4116: 'Piccolo',
 4117: 'Mandy Lynn',
 4118: 'Attendant Abe',
 4119: 'Moe Zart',
 4120: 'Viola Padding',
 4121: 'Gee Minor',
 4122: 'Minty Bass',
 4123: 'Lightning Ted',
 4124: 'Riff Raff',
 4125: 'Melody Wavers',
 4126: 'Mel Canto',
 4127: 'Happy Feet',
 4128: 'Luciano Scoop',
 4129: 'Tootie Twostep',
 4130: 'Metal Mike',
 4131: 'Abraham Armoire',
 4132: 'Lowdown Sally',
 4133: 'Scott Poplin',
 4134: 'Disco Dave',
 4135: 'Sluggo Songbird',
 4136: 'Patty Pause',
 4137: 'Tony Deff',
 4138: 'Cliff Cleff',
 4139: 'Harmony Swell',
 4140: 'Clumsy Ned',
 4141: 'Fisherman Jed',
 4201: 'Tina',
 4202: 'Barry',
 4203: 'Lumber Jack',
 4204: lHQOfficerM,
 4205: lHQOfficerF,
 4206: lHQOfficerF,
 4207: lHQOfficerF,
 4208: 'Hedy',
 4209: 'Corny Canter',
 4211: 'Carl Concerto',
 4212: 'Detective Dirge',
 4213: 'Fran Foley',
 4214: 'Tina Toehooks',
 4215: 'Tim Tailgater',
 4216: 'Gummy Whistle',
 4217: 'Handsome Anton',
 4218: 'Wilma Wind',
 4219: 'Sid Sonata',
 4220: 'Curtis Finger',
 4221: 'Moe Madrigal',
 4222: 'John Doe',
 4223: 'Penny Prompter',
 4224: 'Jungle Jim',
 4225: 'Holly Hiss',
 4226: 'Thelma Throatreacher',
 4227: 'Quiet Francesca',
 4228: 'August Winds',
 4229: 'June Loon',
 4230: 'Julius Wheezer',
 4231: 'Steffi Squeezebox',
 4232: 'Hedly Hymn',
 4233: 'Charlie Carp',
 4234: 'Leed Guitar',
 4235: 'Fisherman Larry',
 4301: 'Yuki',
 4302: 'Anna',
 4303: 'Leo',
 4304: lHQOfficerM,
 4305: lHQOfficerF,
 4306: lHQOfficerF,
 4307: lHQOfficerF,
 4308: 'Tabitha',
 4309: 'Marshall',
 4310: 'Martha Mopp',
 4311: 'Sea Shanty',
 4312: 'Moe Saj',
 4313: 'Dumb Dolph',
 4314: 'Dana Dander',
 4315: 'Karen Clockwork',
 4316: 'Tim Tango',
 4317: 'Stubby Toe',
 4318: 'Bob Marlin',
 4319: 'Rinky Dink',
 4320: 'Cammy Coda',
 4321: 'Luke Lute',
 4322: 'Randy Rythm',
 4323: 'Hanna Hogg',
 4324: 'Ellie',
 4325: 'Banker Bran',
 4326: 'Fran Fret',
 4327: 'Flim Flam',
 4328: 'Wagner',
 4329: 'Telly Prompter',
 4330: 'Quentin',
 4331: 'Mellow Costello',
 4332: 'Ziggy',
 4333: 'Harry',
 4334: 'Fast Freddie',
 4335: 'Fisherman Walden',
 5001: lHQOfficerM,
 5002: lHQOfficerM,
 5003: lHQOfficerF,
 5004: lHQOfficerF,
 5005: 'Clerk Peaches',
 5006: 'Clerk Herb',
 5007: 'Bonnie Blossom',
 5008: 'Fisherman Flora',
 5009: 'Clerk Bo Tanny',
 5010: 'Clerk Tom A. Dough',
 5011: 'Clerk Doug Wood',
 5012: 'Party Planner Pierce',
 5013: 'Party Planner Peggy',
 5101: 'Artie',
 5102: 'Susan',
 5103: 'Bud',
 5104: 'Flutterby',
 5105: 'Jack',
 5106: 'Barber Bjorn',
 5107: 'Postman Felipe',
 5108: 'Innkeeper Janet',
 5109: lHQOfficerM,
 5110: lHQOfficerM,
 5111: lHQOfficerF,
 5112: lHQOfficerF,
 5113: 'Dr. Spud',
 5114: 'Wilt',
 5115: 'Honey Dew',
 5116: 'Vegetable Vern',
 5117: 'Petal',
 5118: 'Pop Corn',
 5119: 'Barry Medly',
 5120: 'Gopher',
 5121: 'Paula Peapod',
 5122: 'Leif Pyle',
 5123: 'Diane Vine',
 5124: 'Soggy Bottom',
 5125: 'Sanjay Splash',
 5126: 'Madam Mum',
 5127: 'Polly Pollen',
 5128: 'Shoshanna Sap',
 5129: 'Fisherman Sally',
 5201: 'Jake',
 5202: 'Cynthia',
 5203: 'Lisa',
 5204: 'Bert',
 5205: 'Dan D. Lion',
 5206: 'Vine Green',
 5207: 'Sofie Squirt',
 5208: 'Samantha Spade',
 5209: lHQOfficerM,
 5210: lHQOfficerM,
 5211: lHQOfficerF,
 5212: lHQOfficerF,
 5213: 'Big Galoot',
 5214: 'Itchie Bumps',
 5215: 'Tammy Tuber',
 5216: 'Stinky Jim',
 5217: 'Greg Greenethumb',
 5218: 'Rocky Raspberry',
 5219: 'Lars Bicep',
 5220: 'Lacy Underalls',
 5221: 'Pink Flamingo',
 5222: 'Whiny Wilma',
 5223: 'Wet Will',
 5224: 'Uncle Bumpkin',
 5225: 'Pamela Puddle',
 5226: 'Pete Moss',
 5227: 'Begonia Biddlesmore',
 5228: 'Digger Mudhands',
 5229: 'Fisherman Lily',
 5301: lHQOfficerM,
 5302: lHQOfficerM,
 5303: lHQOfficerM,
 5304: lHQOfficerM,
 5305: 'Crystal',
 5306: 'S. Cargo',
 5307: 'Fun Gus',
 5308: 'Naggy Nell',
 5309: 'Ro Maine',
 5310: 'Timothy',
 5311: 'Judge McIntosh',
 5312: 'Eugene',
 5313: 'Coach Zucchini',
 5314: 'Aunt Hill',
 5315: 'Uncle Mud',
 5316: 'Uncle Spud',
 5317: 'Detective Lima',
 5318: 'Caesar',
 5319: 'Rose',
 5320: 'April',
 5321: 'Professor Ivy',
 5322: 'Fisherman Rose',
 8001: 'Graham Pree',
 8002: 'Ivona Race',
 8003: 'Anita Winn',
 8004: 'Phil Errup',
 9001: "Snoozin' Susan",
 9002: 'Sleeping Tom',
 9003: 'Drowsy Dennis',
 9004: lHQOfficerF,
 9005: lHQOfficerF,
 9006: lHQOfficerM,
 9007: lHQOfficerM,
 9008: 'Clerk Jill',
 9009: 'Clerk Phil',
 9010: 'Worn Out Waylon',
 9011: 'Fisherman Freud',
 9012: 'Clerk Sarah Snuze',
 9013: 'Clerk Kat Knap',
 9014: 'Clerk R. V. Winkle',
 9015: 'Party Planner Pebbles',
 9016: 'Party Planner Pearl',
 9101: 'Ed',
 9102: 'Big Mama',
 9103: 'P.J.',
 9104: 'Sweet Slumber',
 9105: 'Professor Yawn',
 9106: 'Max',
 9107: 'Snuggles',
 9108: 'Winky Wilbur',
 9109: 'Dreamy Daphne',
 9110: 'Kathy Nip',
 9111: 'Powers Erge',
 9112: 'Lullaby Lou',
 9113: 'Jacques Clock',
 9114: 'Smudgy Mascara',
 9115: 'Babyface MacDougal',
 9116: 'Dances with Sheep',
 9117: 'Afta Hours',
 9118: 'Starry Knight',
 9119: 'Rocco',
 9120: 'Sarah Slumber',
 9121: 'Serena Shortsheeter',
 9122: 'Puffy Ayes',
 9123: 'Teddy Blair',
 9124: 'Nina Nitelight',
 9125: 'Dr. Bleary',
 9126: 'Wyda Wake',
 9127: 'Tabby Tucker',
 9128: "Hardy O'Toole",
 9129: 'Bertha Bedhog',
 9130: 'Charlie Chamberpot',
 9131: 'Susan Siesta',
 9132: lHQOfficerF,
 9133: lHQOfficerF,
 9134: lHQOfficerF,
 9135: lHQOfficerF,
 9136: 'Fisherman Taylor',
 9201: 'Bernie',
 9202: 'Orville',
 9203: 'Nat',
 9204: 'Claire de Loon',
 9205: 'Zen Glen',
 9206: 'Skinny Ginny',
 9207: 'Jane Drain',
 9208: 'Drowsy Dave',
 9209: 'Dr. Floss',
 9210: 'Master Mike',
 9211: 'Dawn',
 9212: 'Moonbeam',
 9213: 'Rooster Rick',
 9214: 'Dr. Blinky',
 9215: 'Rip',
 9216: 'Cat',
 9217: 'Lawful Linda',
 9218: 'Waltzing Matilda',
 9219: 'The Countess',
 9220: 'Grumpy Gordon',
 9221: 'Zari',
 9222: 'Cowboy George',
 9223: 'Mark the Lark',
 9224: 'Sandy Sandman',
 9225: 'Fidgety Bridget',
 9226: 'William Teller',
 9227: 'Bed Head Ted',
 9228: 'Whispering Willow',
 9229: 'Rose Petals',
 9230: 'Tex',
 9231: 'Harry Hammock',
 9232: 'Honey Moon',
 9233: lHQOfficerM,
 9234: lHQOfficerM,
 9235: lHQOfficerM,
 9236: lHQOfficerM,
 9237: 'Fisherman Jung',
 9301: 'Phil Bettur',
 9302: 'Emma Phatic',
 9303: 'GiggleMesh',
 9304: 'Anne Ville',
 9305: 'Bud Erfingerz',
 9306: 'J.S. Bark',
 9307: 'Bea Sharpe',
 9308: 'Otto Toon',
 9309: 'Al Capella',
 9310: 'Des Traction',
 9311: 'Dee Version',
 9312: 'Bo Nanapeel',
 7001: 'N. Prisoned',
 7002: 'R.E. Leaseme',
 7003: 'Lemmy Owte',
 7004: 'T. Rapped',
 7005: 'Little Helphere',
 7006: 'Gimmy Ahand',
 7007: 'Dewin Tymme',
 7008: 'Ima Cagedtoon',
 7009: 'Jimmy Thelock'}

Gloves = "Gants"

FishermanSaleCancel = "Reviens ici pour vendre tes poissons � l'Animalerie pour des bonbons."
FishermanSaleDone = "Merci ! L'Animalerie va les adorer ! Au revoir !"
FishermanSaleBonus = "WOW ! Tu as eu %s poissons sur un total de 70 ! Cela m�rite un bonus de rigolpoints et un troph�e !"
NPCTimeout = "Besoin de plus de temps pour r�fl�chir ?"
