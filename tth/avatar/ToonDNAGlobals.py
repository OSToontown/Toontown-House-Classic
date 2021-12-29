from direct.directnotify.DirectNotifyGlobal import directNotify
from pandac.PandaModules import VBase4
import random

notify = directNotify.newCategory('ToonDNA')

toonSpeciesTypes = ('d', 'c', 'h', 'm', 'r', 'f', 'p', 'b', 's')
toonSpeciesNames = (
    'dog', 'cat', 'horse', 'mouse', 'rabbit', 'duck', 'monkey', 'bear', 'pig'
)

toonHeadTypes = (
    'dls', 'dss', 'dsl', 'dll', 'cls', 'css', 'csl', 'cll', 'hls', 'hss',
    'hsl', 'hll', 'mls', 'mss', 'rls', 'rss', 'rsl', 'rll', 'fls', 'fss',
    'fsl', 'fll', 'pls', 'pss', 'psl', 'pll', 'bls', 'bss', 'bsl', 'bll',
    'sls', 'sss', 'ssl', 'sll'
)
toonTorsoTypes = ('ss', 'ms', 'ls', 'sd', 'md', 'ld', 's', 'm', 'l')
toonLegTypes = ('s', 'm', 'l')

def getHeadList(species):
    return [head for head in toonHeadTypes if head[0] == species]

def getHeadStartIndex(species):
    for head in toonHeadTypes:
        if head[0] == species:
            return toonHeadTypes.index(head)

def getSpecies(head):
    return head[0]

def getSpeciesName(head):
    species = getSpecies(head)
    speciesNameIndex = toonSpeciesTypes.index(species)
    return toonSpeciesNames[speciesNameIndex]

toonHeadAnimalIndices = (0, 4, 8, 12, 14, 18, 22, 26, 30)
toonHeadAnimalIndicesTrial = (0, 4, 12, 14, 18, 30)
allToonHeadAnimalIndices = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33
)
allToonHeadAnimalIndicesTrial = (
    0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 30, 31, 32,
    33
)

Shirts = (
    'phase_3/maps/desat_shirt_1.jpg',
    'phase_3/maps/desat_shirt_2.jpg',
    'phase_3/maps/desat_shirt_3.jpg',
    'phase_3/maps/desat_shirt_4.jpg',
    'phase_3/maps/desat_shirt_5.jpg',
    'phase_3/maps/desat_shirt_6.jpg',
    'phase_3/maps/desat_shirt_7.jpg',
    'phase_3/maps/desat_shirt_8.jpg',
    'phase_3/maps/desat_shirt_9.jpg',
    'phase_3/maps/desat_shirt_10.jpg',
    'phase_3/maps/desat_shirt_11.jpg',
    'phase_3/maps/desat_shirt_12.jpg',
    'phase_3/maps/desat_shirt_13.jpg',
    'phase_3/maps/desat_shirt_14.jpg',
    'phase_3/maps/desat_shirt_15.jpg',
    'phase_3/maps/desat_shirt_16.jpg',
    'phase_3/maps/desat_shirt_17.jpg',
    'phase_3/maps/desat_shirt_18.jpg',
    'phase_3/maps/desat_shirt_19.jpg',
    'phase_3/maps/desat_shirt_20.jpg',
    'phase_3/maps/desat_shirt_21.jpg',
    'phase_3/maps/desat_shirt_22.jpg',
    'phase_3/maps/desat_shirt_23.jpg',
    'phase_4/maps/female_shirt1b.jpg',
    'phase_4/maps/female_shirt2.jpg',
    'phase_4/maps/female_shirt3.jpg',
    'phase_4/maps/male_shirt1.jpg',
    'phase_4/maps/male_shirt2_palm.jpg',
    'phase_4/maps/male_shirt3c.jpg',
    'phase_4/maps/shirt_ghost.jpg',
    'phase_4/maps/shirt_pumkin.jpg',
    'phase_4/maps/holiday_shirt1.jpg',
    'phase_4/maps/holiday_shirt2b.jpg',
    'phase_4/maps/holidayShirt3b.jpg',
    'phase_4/maps/holidayShirt4.jpg',
    'phase_4/maps/female_shirt1b.jpg',
    'phase_4/maps/female_shirt5New.jpg',
    'phase_4/maps/shirtMale4B.jpg',
    'phase_4/maps/shirt6New.jpg',
    'phase_4/maps/shirtMaleNew7.jpg',
    'phase_4/maps/femaleShirtNew6.jpg',
    'phase_4/maps/Vday1Shirt5.jpg',
    'phase_4/maps/Vday1Shirt6SHD.jpg',
    'phase_4/maps/Vday1Shirt4.jpg',
    'phase_4/maps/Vday_shirt2c.jpg',
    'phase_4/maps/shirtTieDyeNew.jpg',
    'phase_4/maps/male_shirt1.jpg',
    'phase_4/maps/StPats_shirt1.jpg',
    'phase_4/maps/StPats_shirt2.jpg',
    'phase_4/maps/ContestfishingVestShirt2.jpg',
    'phase_4/maps/ContestFishtankShirt1.jpg',
    'phase_4/maps/ContestPawShirt1.jpg',
    'phase_4/maps/CowboyShirt1.jpg',
    'phase_4/maps/CowboyShirt2.jpg',
    'phase_4/maps/CowboyShirt3.jpg',
    'phase_4/maps/CowboyShirt4.jpg',
    'phase_4/maps/CowboyShirt5.jpg',
    'phase_4/maps/CowboyShirt6.jpg',
    'phase_4/maps/4thJulyShirt1.jpg',
    'phase_4/maps/4thJulyShirt2.jpg',
    'phase_4/maps/shirt_Cat7_01.jpg',
    'phase_4/maps/shirt_Cat7_02.jpg',
    'phase_4/maps/contest_backpack3.jpg',
    'phase_4/maps/contest_leder.jpg',
    'phase_4/maps/contest_mellon2.jpg',
    'phase_4/maps/contest_race2.jpg',
    'phase_4/maps/PJBlueBanana2.jpg',
    'phase_4/maps/PJRedHorn2.jpg',
    'phase_4/maps/PJGlasses2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_valentine1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_valentine2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_desat4.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_gardening1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_gardening2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_party1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_party2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racing1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racing2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_summer1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_summer2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_golf1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_golf2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_marathon1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_toonTask1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_toonTask2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_trolley1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_trolley2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_winter1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween3.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween4.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_valentine3.jpg',
    'phase_4/maps/tt_t_chr_shirt_scientistC.jpg',
    'phase_4/maps/tt_t_chr_shirt_scientistA.jpg',
    'phase_4/maps/tt_t_chr_shirt_scientistB.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_mailbox.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_trashcan.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_loonyLabs.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_hydrant.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_whistle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_cogbuster.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated01.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_victoryParty01.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_victoryParty02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_sellbotIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_sellbotVPIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_sellbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_jellyBeans.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_doodle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween5.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloweenTurtle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_greentoon1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_getConnectedMoverShaker.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racingGrandPrix.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_lawbotIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_lawbotVPIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_lawbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_bee.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_pirate.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_supertoon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_vampire.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_dinosaur.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_golf03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racing03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding3.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_trolley03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_golf04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween06.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_winter03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_halloween07.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_winter02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing06.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_fishing07.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_golf05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_racing05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_trolley04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_trolley05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding4.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_saveBuilding05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirt_anniversary.jpg',
)
BoyShirts = (
    (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (8, 8), (9, 9), (10, 0),
    (11, 0), (14, 10), (16, 0), (17, 0), (18, 12), (19, 13)
)
GirlShirts = (
    (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7), (9, 9), (12, 0),
    (13, 11), (15, 11), (16, 0), (20, 0), (21, 0), (22, 0)
)

def isValidBoyShirt(index):
    for pair in BoyShirts:
        if pair[0] == index:
            return True
    return False

def isValidGirlShirt(index):
    for pair in GirlShirts:
        if index == pair[0]:
            return True
    return False

Sleeves = (
    'phase_3/maps/desat_sleeve_1.jpg',
    'phase_3/maps/desat_sleeve_2.jpg',
    'phase_3/maps/desat_sleeve_3.jpg',
    'phase_3/maps/desat_sleeve_4.jpg',
    'phase_3/maps/desat_sleeve_5.jpg',
    'phase_3/maps/desat_sleeve_6.jpg',
    'phase_3/maps/desat_sleeve_7.jpg',
    'phase_3/maps/desat_sleeve_8.jpg',
    'phase_3/maps/desat_sleeve_9.jpg',
    'phase_3/maps/desat_sleeve_10.jpg',
    'phase_3/maps/desat_sleeve_15.jpg',
    'phase_3/maps/desat_sleeve_16.jpg',
    'phase_3/maps/desat_sleeve_19.jpg',
    'phase_3/maps/desat_sleeve_20.jpg',
    'phase_4/maps/female_sleeve1b.jpg',
    'phase_4/maps/female_sleeve2.jpg',
    'phase_4/maps/female_sleeve3.jpg',
    'phase_4/maps/male_sleeve1.jpg',
    'phase_4/maps/male_sleeve2_palm.jpg',
    'phase_4/maps/male_sleeve3c.jpg',
    'phase_4/maps/shirt_Sleeve_ghost.jpg',
    'phase_4/maps/shirt_Sleeve_pumkin.jpg',
    'phase_4/maps/holidaySleeve1.jpg',
    'phase_4/maps/holidaySleeve3.jpg',
    'phase_4/maps/female_sleeve1b.jpg',
    'phase_4/maps/female_sleeve5New.jpg',
    'phase_4/maps/male_sleeve4New.jpg',
    'phase_4/maps/sleeve6New.jpg',
    'phase_4/maps/SleeveMaleNew7.jpg',
    'phase_4/maps/female_sleeveNew6.jpg',
    'phase_4/maps/Vday5Sleeve.jpg',
    'phase_4/maps/Vda6Sleeve.jpg',
    'phase_4/maps/Vday_shirt4sleeve.jpg',
    'phase_4/maps/Vday2cSleeve.jpg',
    'phase_4/maps/sleeveTieDye.jpg',
    'phase_4/maps/male_sleeve1.jpg',
    'phase_4/maps/StPats_sleeve.jpg',
    'phase_4/maps/StPats_sleeve2.jpg',
    'phase_4/maps/ContestfishingVestSleeve1.jpg',
    'phase_4/maps/ContestFishtankSleeve1.jpg',
    'phase_4/maps/ContestPawSleeve1.jpg',
    'phase_4/maps/CowboySleeve1.jpg',
    'phase_4/maps/CowboySleeve2.jpg',
    'phase_4/maps/CowboySleeve3.jpg',
    'phase_4/maps/CowboySleeve4.jpg',
    'phase_4/maps/CowboySleeve5.jpg',
    'phase_4/maps/CowboySleeve6.jpg',
    'phase_4/maps/4thJulySleeve1.jpg',
    'phase_4/maps/4thJulySleeve2.jpg',
    'phase_4/maps/shirt_sleeveCat7_01.jpg',
    'phase_4/maps/shirt_sleeveCat7_02.jpg',
    'phase_4/maps/contest_backpack_sleeve.jpg',
    'phase_4/maps/Contest_leder_sleeve.jpg',
    'phase_4/maps/contest_mellon_sleeve2.jpg',
    'phase_4/maps/contest_race_sleeve.jpg',
    'phase_4/maps/PJSleeveBlue.jpg',
    'phase_4/maps/PJSleeveRed.jpg',
    'phase_4/maps/PJSleevePurple.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_desat4.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_party1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_party2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_summer1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_summer2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_marathon1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley2.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_winter1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween3.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween4.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine3.jpg',
    'phase_4/maps/tt_t_chr_shirtSleeve_scientist.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_mailbox.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_trashcan.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_loonyLabs.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_hydrant.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_whistle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_cogbuster.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated01.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty01.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotVPIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_jellyBeans.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_doodle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween5.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloweenTurtle.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_greentoon1.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_getConnectedMoverShaker.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racingGrandPrix.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_lawbotIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_lawbotVPIcon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_lawbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_bee.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_pirate.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_supertoon.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_vampire.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_dinosaur.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding3.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween06.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_winter03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween07.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_winter02.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing06.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing07.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_golf05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_racing05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated03.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley04.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding4.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding05.jpg',
    'phase_4/maps/tt_t_chr_avt_shirtSleeve_anniversary.jpg',
)
BoyShorts = (
    'phase_3/maps/desat_shorts_1.jpg',
    'phase_3/maps/desat_shorts_2.jpg',
    'phase_3/maps/desat_shorts_4.jpg',
    'phase_3/maps/desat_shorts_6.jpg',
    'phase_3/maps/desat_shorts_7.jpg',
    'phase_3/maps/desat_shorts_8.jpg',
    'phase_3/maps/desat_shorts_9.jpg',
    'phase_3/maps/desat_shorts_10.jpg',
    'phase_4/maps/VdayShorts2.jpg',
    'phase_4/maps/shorts4.jpg',
    'phase_4/maps/shorts1.jpg',
    'phase_4/maps/shorts5.jpg',
    'phase_4/maps/CowboyShorts1.jpg',
    'phase_4/maps/CowboyShorts2.jpg',
    'phase_4/maps/4thJulyShorts1.jpg',
    'phase_4/maps/shortsCat7_01.jpg',
    'phase_4/maps/Blue_shorts_1.jpg',
    'phase_4/maps/Red_shorts_1.jpg',
    'phase_4/maps/Purple_shorts_1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_winter1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_winter2.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_winter3.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_winter4.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_valentine1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_valentine2.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_fishing1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_gardening1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_party1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_racing1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_summer1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_golf1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_halloween1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_halloween2.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_saveBuilding1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_trolley1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_halloween4.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_halloween3.jpg',
    'phase_4/maps/tt_t_chr_shorts_scientistA.jpg',
    'phase_4/maps/tt_t_chr_shorts_scientistB.jpg',
    'phase_4/maps/tt_t_chr_shorts_scientistC.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_cogbuster.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_sellbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_halloween5.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_halloweenTurtle.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_greentoon1.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_racingGrandPrix.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_lawbotCrusher.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_bee.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_pirate.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_supertoon.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_vampire.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_dinosaur.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_golf03.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_racing03.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_golf04.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_golf05.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_racing04.jpg',
    'phase_4/maps/tt_t_chr_avt_shorts_racing05.jpg',
)

SHORTS = 0
SKIRT = 1

GirlBottoms = (
    ('phase_3/maps/desat_skirt_1.jpg', SKIRT),
    ('phase_3/maps/desat_skirt_2.jpg', SKIRT),
    ('phase_3/maps/desat_skirt_3.jpg', SKIRT),
    ('phase_3/maps/desat_skirt_4.jpg', SKIRT),
    ('phase_3/maps/desat_skirt_5.jpg', SKIRT),
    ('phase_3/maps/desat_shorts_1.jpg', SHORTS),
    ('phase_3/maps/desat_shorts_5.jpg', SHORTS),
    ('phase_3/maps/desat_skirt_6.jpg', SKIRT),
    ('phase_3/maps/desat_skirt_7.jpg', SKIRT),
    ('phase_3/maps/desat_shorts_10.jpg', SHORTS),
    ('phase_4/maps/female_skirt1.jpg', SKIRT),
    ('phase_4/maps/female_skirt2.jpg', SKIRT),
    ('phase_4/maps/female_skirt3.jpg', SKIRT),
    ('phase_4/maps/VdaySkirt1.jpg', SKIRT),
    ('phase_4/maps/skirtNew5.jpg', SKIRT),
    ('phase_4/maps/shorts5.jpg', SHORTS),
    ('phase_4/maps/CowboySkirt1.jpg', SKIRT),
    ('phase_4/maps/CowboySkirt2.jpg', SKIRT),
    ('phase_4/maps/4thJulySkirt1.jpg', SKIRT),
    ('phase_4/maps/skirtCat7_01.jpg', SKIRT),
    ('phase_4/maps/Blue_shorts_1.jpg', SHORTS),
    ('phase_4/maps/Red_shorts_1.jpg', SHORTS),
    ('phase_4/maps/Purple_shorts_1.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_skirt_winter1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_winter2.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_winter3.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_winter4.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_valentine1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_valentine2.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_fishing1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_gardening1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_party1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_racing1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_summer1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_golf1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_halloween1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_halloween2.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_saveBuilding1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_trolley1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_halloween3.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_halloween4.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_shorts_scientistA.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_shorts_scientistB.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_shorts_scientistC.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_cogbuster.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_sellbotCrusher.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_halloween5.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_halloweenTurtle.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_skirt_greentoon1.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_racingGrandPrix.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_shorts_lawbotCrusher.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_bee.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_pirate.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_skirt_pirate.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_shorts_supertoon.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_vampire.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_shorts_dinosaur.jpg', SHORTS),
    ('phase_4/maps/tt_t_chr_avt_skirt_golf02.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_racing03.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_golf03.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_golf04.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_racing04.jpg', SKIRT),
    ('phase_4/maps/tt_t_chr_avt_skirt_racing05.jpg', SKIRT)
)
ClothesColors = (
    VBase4(0.933594, 0.265625, 0.28125, 1),
    VBase4(0.863281, 0.40625, 0.417969, 1),
    VBase4(0.710938, 0.234375, 0.4375, 1),
    VBase4(0.992188, 0.480469, 0.167969, 1),
    VBase4(0.996094, 0.898438, 0.320312, 1),
    VBase4(0.550781, 0.824219, 0.324219, 1),
    VBase4(0.242188, 0.742188, 0.515625, 1),
    VBase4(0.433594, 0.90625, 0.835938, 1),
    VBase4(0.347656, 0.820312, 0.953125, 1),
    VBase4(0.191406, 0.5625, 0.773438, 1),
    VBase4(0.285156, 0.328125, 0.726562, 1),
    VBase4(0.460938, 0.378906, 0.824219, 1),
    VBase4(0.546875, 0.28125, 0.75, 1),
    VBase4(0.570312, 0.449219, 0.164062, 1),
    VBase4(0.640625, 0.355469, 0.269531, 1),
    VBase4(0.996094, 0.695312, 0.511719, 1),
    VBase4(0.832031, 0.5, 0.296875, 1),
    VBase4(0.992188, 0.480469, 0.167969, 1),
    VBase4(0.550781, 0.824219, 0.324219, 1),
    VBase4(0.433594, 0.90625, 0.835938, 1),
    VBase4(0.347656, 0.820312, 0.953125, 1),
    VBase4(0.96875, 0.691406, 0.699219, 1),
    VBase4(0.996094, 0.957031, 0.597656, 1),
    VBase4(0.855469, 0.933594, 0.492188, 1),
    VBase4(0.558594, 0.589844, 0.875, 1),
    VBase4(0.726562, 0.472656, 0.859375, 1),
    VBase4(0.898438, 0.617188, 0.90625, 1),
    VBase4(1, 1, 1, 1),
    VBase4(0, 0.2, 0.956862, 1),
    VBase4(0.972549, 0.094117, 0.094117, 1),
    VBase4(0.447058, 0, 0.90196, 1)
)

ShirtStyles = {
    'sa_ss55':[150, 137, [(27, 27)]],
    'sa_ss54':[149, 136, [(27, 27)]],
    'sa_ss51':[146, 133, [(27, 27)]],
    'sa_ss22':[92, 81, [(27, 27)]],
    'sa_ss53':[148, 135, [(27, 27)]],
    'sa_ss52':[147, 134, [(27, 27)]],
    'bss12':[16, 0, [
            (27, 27), (27, 4), (27, 5), (27, 6), (27, 7), (27, 8), (27, 9)
        ]
    ],
    'bss13':[17, 0, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)
        ]
    ],
    'bss10':[11, 0, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (27, 27)
        ]
    ],
    'bss11':[14, 10, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)
        ]
    ],
    'pj_ss3':[68, 57, [(27, 27)]],
    'pj_ss2':[67, 56, [(27, 27)]],
    'bss14':[18, 12, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (8, 8),
            (9, 9), (11, 11), (12, 12), (27, 27)
        ]
    ],
    'bss15':[19, 13, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (27, 27)
        ]
    ],
    'sa_ss11':[81, 70, [(27, 27)]],
    'wh_ss1':[31, 22, [(27, 27)]],
    'wh_ss2':[32, 22, [(27, 27)]],
    'wh_ss3':[33, 23, [(27, 27)]],
    'wh_ss4':[34, 23, [(27, 27)]],
    'sa_ss14':[84, 73, [(27, 27)]],
    'sa_ss17':[87, 76, [(27, 27)]],
    'vd_ss2':[42, 31, [(27, 27)]],
    'sa_ss19':[89, 78, [(27, 27)]],
    'sa_ss18':[88, 77, [(27, 27)]],
    'sa_ss49':[144, 116, [(27, 27)]],
    'j4_ss2':[59, 48, [(27, 27)]],
    'j4_ss1':[58, 47, [(27, 27)]],
    'sa_ss50':[145, 131, [(27, 27)]],
    'sil_4':[103, 90, [(27, 27)]],
    'c_ss11':[57, 46, [(27, 27)]],
    'c_ss10':[56, 45, [(27, 27)]],
    'c_ss13':[61, 50, [(27, 27)]],
    'c_ss12':[60, 49, [(27, 27)]],
    'vd_ss3':[43, 32, [(27, 27)]],
    'sa_ss33':[128, 115, [(27, 27)]],
    'sc_1':[97, 86, [(27, 27)]],
    'sa_ss12':[82, 71, [(27, 27)]],
    'sil_5':[104, 91, [(27, 27)]],
    'sil_6':[105, 92, [(27, 27)]],
    'sil_7':[107, 94, [(27, 27)]],
    'sil_1':[100, 87, [(27, 27)]],
    'sil_2':[101, 88, [(27, 27)]],
    'sil_3':[102, 89, [(27, 27)]],
    'sa_ss34':[129, 116, [(27, 27)]],
    'sil_8':[108, 95, [(27, 27)]],
    'sa_ss42':[137, 124, [(27, 27)]],
    'sa_ss5':[75, 64, [(27, 27)]],
    'sa_ss40':[135, 122, [(27, 27)]],
    'sa_ss41':[136, 123, [(27, 27)]],
    'sa_ss24':[94, 83, [(27, 27)]],
    'sa_ss47':[142, 129, [(27, 27)]],
    'sa_ss44':[139, 126, [(27, 27)]],
    'sa_ss4':[74, 63, [(27, 27)]],
    'c_bss1':[26, 17, [(27, 27)]],
    'c_bss2':[28, 19, [(27, 27)]],
    'c_bss3':[37, 26, [(27, 27)]],
    'c_bss4':[39, 28, [(27, 27)]],
    'sa_ss7':[77, 66, [(27, 27)]],
    'emb_us2':[100, 87, [(27, 27)]],
    'bss1':[0, 0, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (27, 27)
        ]
    ],
    'bss2':[1, 1, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)
        ]
    ],
    'bss3':[2, 2, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)
        ]
    ],
    'bss4':[3, 3, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)
        ]
    ],
    'bss5':[4, 4, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (9, 9),
            (10, 10), (11, 11), (12, 12)
        ]
    ],
    'bss6':[5, 5, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)
        ]
    ],
    'bss7':[8, 8, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (8, 8),
            (9, 9), (11, 11), (12, 12), (27, 27)
        ]
    ],
    'bss8':[9, 9, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)
        ]
    ],
    'bss9':[10, 0, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (27, 27)
        ]
    ],
    'vd_ss1':[41, 30, [(27, 27)]],
    'vd_ss7':[96, 85, [(27, 27)]],
    'vd_ss6':[70, 59, [(27, 27)]],
    'vd_ss5':[69, 58, [(27, 27)]],
    'vd_ss4':[44, 33, [(27, 27)]],
    'sa_ss37':[132, 119, [(27, 27)]],
    'sa_ss25':[95, 84, [(27, 27)]],
    'sa_ss3':[73, 62, [(27, 27)]],
    'sa_ss10':[80, 69, [(27, 27)]],
    'ugcms':[117, 104, [(27, 27)]],
    'pj_ss1':[66, 55, [(27, 27)]],
    'sa_ss2':[72, 61, [(27, 27)]],
    'sa_ss13':[83, 72, [(27, 27)]],
    'emb_us1':[103, 90, [(27, 27)]],
    'tc_ss1':[49, 38, [(27, 27)]],
    'sa_ss15':[85, 74, [(27, 27)]],
    'sa_ss32':[127, 114, [(27, 27)]],
    'sa_ss26':[106, 93, [(27, 27)]],
    'sa_ss30':[121, 108, [(27, 27)]],
    'sa_ss31':[118, 105, [(27, 27)]],
    'sd_ss1':[47, 36, [(27, 27)]],
    'sa_ss16':[86, 75, [(27, 27)]],
    'sd_ss2':[48, 37, [(27, 27)]],
    'tc_ss2':[50, 39, [(27, 27)]],
    'tc_ss3':[51, 40, [(27, 27)]],
    'sa_ss35':[130, 117, [(27, 27)]],
    'sd_ss3':[116, 103, [(27, 27)]],
    'tc_ss6':[64, 53, [(27, 27)]],
    'tc_ss7':[65, 54, [(27, 27)]],
    'tc_ss4':[62, 51, [(27, 27)]],
    'tc_ss5':[63, 52, [(27, 27)]],
    'sa_ss36':[131, 118, [(27, 27)]],
    'sa_ss46':[141, 128, [(27, 27)]],
    'jb_2':[113, 100, [(27, 27)]],
    'sa_ss27':[110, 97, [(27, 27)]],
    'sa_ss38':[133, 120, [(27, 27)]],
    'hw_ss2':[30, 21, [(27, 27)]],
    'hw_ss3':[114, 101, [(27, 27)]],
    'sa_ss45':[140, 127, [(27, 27)]],
    'hw_ss1':[29, 20, [(27, 27)]],
    'hw_ss6':[123, 110, [(27, 27)]],
    'hw_ss7':[124, 111, [(27, 27)]],
    'hw_ss4':[115, 102, [(27, 27)]],
    'hw_ss5':[122, 109, [(27, 27)]],
    'hw_ss8':[125, 112, [(27, 27)]],
    'hw_ss9':[126, 113, [(27, 27)]],
    'lb_1':[119, 106, [(27, 27)]],
    'jb_1':[112, 99, [(27, 27)]],
    'sc_3':[99, 86, [(27, 27)]],
    'sa_ss39':[134, 121, [(27, 27)]],
    'emb_us3':[101, 88, [(27, 27)]],
    'sa_ss48':[143, 130, [(27, 27)]],
    'gss13':[20, 0, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (21, 21), (22, 22),
            (23, 23), (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss12':[16, 0, [
            (27, 27), (27, 4), (27, 5), (27, 6), (27, 7), (27, 8), (27, 9)
        ]
    ],
    'gss11':[15, 11, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (21, 21), (22, 22),
            (23, 23), (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss10':[13, 11, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (21, 21), (22, 22),
            (23, 23), (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss15':[22, 0, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (21, 21), (22, 22),
            (23, 23), (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss14':[21, 0, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (21, 21), (22, 22),
            (23, 23), (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss7':[7, 7, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (11, 11), (12, 12), (21, 21), (22, 22), (23, 23),
            (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss6':[6, 6, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (11, 11), (12, 12), (21, 21), (22, 22), (23, 23),
            (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss5':[5, 5, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (11, 11), (12, 12), (21, 21), (22, 22), (23, 23),
            (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss4':[3, 3, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (11, 11), (12, 12), (21, 21), (22, 22), (23, 23),
            (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss3':[2, 2, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (11, 11), (12, 12), (21, 21), (22, 22), (23, 23),
            (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss2':[1, 1, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (11, 11), (12, 12), (21, 21), (22, 22), (23, 23),
            (24, 24), (25, 25), (26, 26)
        ]
    ],
    'gss1':[0, 0, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (11, 11), (12, 12), (21, 21), (22, 22), (23, 23),
            (24, 24), (25, 25), (26, 26), (27, 27)
        ]
    ],
    'sa_ss23':[93, 82, [(27, 27)]],
    'sa_ss28':[111, 98, [(27, 27)]],
    'sa_ss29':[120, 107, [(27, 27)]],
    'gss9':[12, 0, [(27, 27)]],
    'gss8':[9, 9, [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (8, 8), (9, 9), (11, 11), (12, 12), (21, 21), (22, 22), (23, 23),
            (24, 24), (25, 25), (26, 26)
        ]
    ],
    'c_gss3':[35, 24, [(27, 27)]],
    'c_gss2':[24, 15, [(27, 27)]],
    'c_gss1':[23, 14, [(27, 27)]],
    'sa_ss6':[76, 65, [(27, 27)]],
    'sa_ss1':[71, 60, [(27, 27)]],
    'sc_2':[98, 86, [(27, 27)]],
    'c_gss5':[40, 29, [(27, 27)]],
    'c_gss4':[36, 25, [(27, 27)]],
    'sa_ss9':[79, 68, [(27, 27)]],
    'sa_ss8':[78, 67, [(27, 27)]],
    'sa_ss43':[138, 125, [(27, 27)]],
    'c_ss5':[46, 35, [(27, 27)]],
    'c_ss4':[45, 34, [(27, 27)]],
    'c_ss7':[53, 42, [(27, 27)]],
    'c_ss6':[52, 41, [(27, 27)]],
    'c_ss1':[25, 16, [(27, 27)]],
    'c_ss3':[38, 27, [(27, 27)]],
    'c_ss2':[27, 18, [(27, 27)]],
    'sa_ss20':[90, 79, [(27, 27)]],
    'sb_1':[109, 96, [(27, 27)]],
    'c_ss9':[55, 44, [(27, 27)]],
    'c_ss8':[54, 43, [(27, 27)]],
    'sa_ss21':[91, 80, [(27, 27)]],
}
BottomStyles = {
    'bbs1':[0, [
            0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
        ]
    ],
    'bbs2':[1, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]],
    'bbs3':[2, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]],
    'bbs4':[3, [0, 1, 2, 4, 6, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 20, 27]],
    'bbs5':[4, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]],
    'bbs6':[5, [0, 1, 2, 4, 6, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 27]],
    'bbs7':[6, [0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 27]],
    'bbs8':[7, [
            0, 1, 2, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27
        ]
    ],
    'vd_bs1':[8, [27]],
    'vd_bs2':[23, [27]],
    'vd_bs3':[24, [27]],
    'c_bs1':[9, [27]],
    'c_bs2':[10, [27]],
    'c_bs5':[15, [27]],
    'sd_bs1':[11, [27]],
    'sd_bs2':[44, [27]],
    'pj_bs1':[16, [27]],
    'pj_bs2':[17, [27]],
    'pj_bs3':[18, [27]],
    'wh_bs1':[19, [27]],
    'wh_bs2':[20, [27]],
    'wh_bs3':[21, [27]],
    'wh_bs4':[22, [27]],
    'hw_bs1':[47, [27]],
    'hw_bs2':[48, [27]],
    'hw_bs5':[49, [27]],
    'hw_bs6':[50, [27]],
    'hw_bs7':[51, [27]],
    'gsk1':[0, [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26, 27
        ]
    ],
    'gsk2':[1, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26]],
    'gsk3':[2, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26]],
    'gsk4':[3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26]],
    'gsk5':[4, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26]],
    'gsk6':[7, [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26, 27
        ]
    ],
    'gsk7':[8, [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26, 27
        ]
    ],
    'gsh1':[5, [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26, 27
        ]
    ],
    'gsh2':[6, [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26, 27
        ]
    ],
    'gsh3':[9, [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 21, 22, 23, 24, 25, 26, 27
        ]
    ],
    'c_gsk1':[10, [27]],
    'c_gsk2':[11, [27]],
    'c_gsk3':[12, [27]],
    'vd_gs1':[13, [27]],
    'vd_gs2':[27, [27]],
    'vd_gs3':[28, [27]],
    'c_gsk4':[14, [27]],
    'sd_gs1':[15, [27]],
    'sd_gs2':[48, [27]],
    'c_gsk5':[16, [27]],
    'c_gsk6':[17, [27]],
    'c_bs3':[12, [27]],
    'c_bs4':[13, [27]],
    'j4_bs1':[14, [27]],
    'j4_gs1':[18, [27]],
    'c_gsk7':[19, [27]],
    'pj_gs1':[20, [27]],
    'pj_gs2':[21, [27]],
    'pj_gs3':[22, [27]],
    'wh_gsk1':[23, [27]],
    'wh_gsk2':[24, [27]],
    'wh_gsk3':[25, [27]],
    'wh_gsk4':[26, [27]],
    'sa_bs1':[25, [27]],
    'sa_bs2':[26, [27]],
    'sa_bs3':[27, [27]],
    'sa_bs4':[28, [27]],
    'sa_bs5':[29, [27]],
    'sa_bs6':[30, [27]],
    'sa_bs7':[31, [27]],
    'sa_bs8':[32, [27]],
    'sa_bs9':[33, [27]],
    'sa_bs10':[34, [27]],
    'sa_bs11':[35, [27]],
    'sa_bs12':[36, [27]],
    'sa_bs13':[41, [27]],
    'sa_bs14':[46, [27]],
    'sa_bs15':[45, [27]],
    'sa_bs16':[52, [27]],
    'sa_bs17':[53, [27]],
    'sa_bs18':[54, [27]],
    'sa_bs19':[55, [27]],
    'sa_bs20':[56, [27]],
    'sa_bs21':[57, [27]],
    'sa_gs1':[29, [27]],
    'sa_gs2':[30, [27]],
    'sa_gs3':[31, [27]],
    'sa_gs4':[32, [27]],
    'sa_gs5':[33, [27]],
    'sa_gs6':[34, [27]],
    'sa_gs7':[35, [27]],
    'sa_gs8':[36, [27]],
    'sa_gs9':[37, [27]],
    'sa_gs10':[38, [27]],
    'sa_gs11':[39, [27]],
    'sa_gs12':[40, [27]],
    'sa_gs13':[45, [27]],
    'sa_gs14':[50, [27]],
    'sa_gs15':[49, [27]],
    'sa_gs16':[57, [27]],
    'sa_gs17':[58, [27]],
    'sa_gs18':[59, [27]],
    'sa_gs19':[60, [27]],
    'sa_gs20':[61, [27]],
    'sa_gs21':[62, [27]],
    'sc_bs1':[37, [27]],
    'sc_bs2':[38, [27]],
    'sc_bs3':[39, [27]],
    'sc_gs1':[41, [27]],
    'sc_gs2':[42, [27]],
    'sc_gs3':[43, [27]],
    'sil_bs1':[40, [27]],
    'sil_gs1':[44, [27]],
    'hw_bs3':[42, [27]],
    'hw_gs3':[46, [27]],
    'hw_bs4':[43, [27]],
    'hw_gs4':[47, [27]],
    'hw_gs1':[51, [27]],
    'hw_gs2':[52, [27]],
    'hw_gs5':[54, [27]],
    'hw_gs6':[55, [27]],
    'hw_gs7':[56, [27]],
    'hw_gsk1':[53, [27]]
}

MAKE_A_TOON = 1
TAMMY_TAILOR = 2004
LONGJOHN_LEROY = 1007
TAILOR_HARMONY = 4008
BONNIE_BLOSSOM = 5007
WARREN_BUNDLES = 3008
WORNOUT_WAYLON = 9010

TailorCollections = {
    MAKE_A_TOON:[
        ['bss1', 'bss2'],
        ['gss1', 'gss2'],
        ['bbs1', 'bbs2'],
        ['gsk1', 'gsh1']
    ],
    TAMMY_TAILOR:[
        ['bss1', 'bss2'],
        ['gss1', 'gss2'],
        ['bbs1', 'bbs2'],
        ['gsk1', 'gsh1']
    ],
    LONGJOHN_LEROY:[
        ['bss3', 'bss14'],
        ['gss3', 'gss14'],
        ['bbs3', 'bbs4'],
        ['gsk2', 'gsh2']
    ],
    TAILOR_HARMONY:[
        ['bss5', 'bss6', 'bss10'],
        ['gss5', 'gss6', 'gss9'],
        ['bbs5'],
        ['gsk3', 'gsh3']
    ],
    BONNIE_BLOSSOM:[
        ['bss7', 'bss8', 'bss12'],
        ['gss8', 'gss10', 'gss12'],
        ['bbs6'],
        ['gsk4', 'gsk5']
    ],
    WARREN_BUNDLES:[
        ['bss9', 'bss13'],
        ['gss7', 'gss11'],
        ['bbs7'],
        ['gsk6']
    ],
    WORNOUT_WAYLON:[
        ['bss11', 'bss15'],
        ['gss13', 'gss15'],
        ['bbs8'],
        ['gsk7']
    ]
}

BOY_SHIRTS = 0
GIRL_SHIRTS = 1

BOY_SHORTS = 2
GIRL_BOTTOMS = 3

HAT = 1
GLASSES = 2
BACKPACK = 4
SHOES = 8

MakeAToonBoyBottoms = []
MakeAToonBoyShirts = []

MakeAToonGirlBottoms = []
MakeAToonGirlShirts = []
MakeAToonGirlSkirts = []
MakeAToonGirlShorts = []

# Combine all tailors into MAKE_A_TOON tailor.
for tailor in TailorCollections:
    for girlBottoms in TailorCollections[tailor][GIRL_BOTTOMS]:
        if girlBottoms not in TailorCollections[MAKE_A_TOON][GIRL_BOTTOMS]:
            TailorCollections[MAKE_A_TOON][GIRL_BOTTOMS].append(girlBottoms)
    for boyShorts in TailorCollections[tailor][BOY_SHORTS]:
        if boyShorts not in TailorCollections[MAKE_A_TOON][BOY_SHORTS]:
            TailorCollections[MAKE_A_TOON][BOY_SHORTS].append(boyShorts)
    for girlShirts in TailorCollections[tailor][GIRL_SHIRTS]:
        if girlShirts not in TailorCollections[MAKE_A_TOON][GIRL_SHIRTS]:
            TailorCollections[MAKE_A_TOON][GIRL_SHIRTS].append(girlShirts)
    for boyShirts in TailorCollections[tailor][BOY_SHIRTS]:
        if boyShirts not in TailorCollections[MAKE_A_TOON][BOY_SHIRTS]:
            TailorCollections[MAKE_A_TOON][BOY_SHIRTS].append(boyShirts)

for style in TailorCollections[MAKE_A_TOON][BOY_SHORTS]:
    index = BottomStyles[style][0]
    MakeAToonBoyBottoms.append(index)

for style in TailorCollections[MAKE_A_TOON][BOY_SHIRTS]:
    index = ShirtStyles[style][0]
    MakeAToonBoyShirts.append(index)

for style in TailorCollections[MAKE_A_TOON][GIRL_BOTTOMS]:
    index = BottomStyles[style][0]
    MakeAToonGirlBottoms.append(index)

for style in TailorCollections[MAKE_A_TOON][GIRL_SHIRTS]:
    index = ShirtStyles[style][0]
    MakeAToonGirlShirts.append(index)

for index in MakeAToonGirlBottoms:
    flag = GirlBottoms[index][1]
    if flag == SKIRT:
        MakeAToonGirlSkirts.append(index)
    elif flag == SHORTS:
        MakeAToonGirlShorts.append(index)
    else:
        notify.error('Invalid flag')

def getGirlBottomType(style):
    return GirlBottoms[BottomStyles[style][0]][1]

def getRandomTop(gender, tailorId=MAKE_A_TOON, generator=None):
    if not generator:
        generator = random
    collection = TailorCollections[tailorId]
    if gender == 'm':
        style = generator.choice(collection[BOY_SHIRTS])
    else:
        style = generator.choice(collection[GIRL_SHIRTS])
    styleList = ShirtStyles[style]
    colors = generator.choice(styleList[2])
    return (styleList[0], colors[0], styleList[1], colors[1])

def getRandomBottom(gender, tailorId=MAKE_A_TOON, generator=None,
                    girlBottomType=None):
    if not generator:
        generator = random
    collection = TailorCollections[tailorId]

    if gender == 'm':
        style = generator.choice(collection[BOY_SHORTS])
    elif girlBottomType == None:
        style = generator.choice(collection[GIRL_BOTTOMS])
    elif girlBottomType == SKIRT:
        skirtCollection = filter(
            lambda style:getGirlBottomType(style) == SKIRT,
            collection[GIRL_BOTTOMS]
        )
        style = generator.choice(skirtCollection)
    elif girlBottomType == SHORTS:
        shortsCollection = filter(
            lambda style:getGirlBottomType(style) == SHORTS,
            collection[GIRL_BOTTOMS]
        )
        style = generator.choice(shortsCollection)
    else:
        notify.error('Bad girlBottomType:%s' % girlBottomType)

    styleList = BottomStyles[style]
    color = generator.choice(styleList[1])
    return (styleList[0], color)

def getRandomGirlBottom(bottomType):
    bottoms = []
    for i, bottom in enumerate(GirlBottoms):
        if bottom[1] == bottomType:
            bottoms.append(i)
    return random.choice(bottoms)

def getRandomGirlBottomAndColor(bottomType):
    bottoms = []
    typeStr = choice(bottomType == SHORTS, 'gsh', 'gsk')
    for bottom in BottomStyles.keys():
        if typeStr in bottom:
            bottoms.append(bottom)
    style = BottomStyles[random.choice(bottoms)]
    return (style[0], random.choice(style[1]))

def getRandomizedTops(gender, tailorId=MAKE_A_TOON, generator=None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    if gender == 'm':
        collection = collection[BOY_SHIRTS][:]
    else:
        collection = collection[GIRL_SHIRTS][:]
    tops = []
    random.shuffle(collection)
    for style in collection:
        colors = ShirtStyles[style][2][:]
        random.shuffle(colors)
        for color in colors:
            tops.append(
                (ShirtStyles[style][0], color[0],
                 ShirtStyles[style][1], color[1])
            )
    return tops

def getRandomizedBottoms(gender, tailorId=MAKE_A_TOON, generator=None):
    if generator == None:
        generator = random
    collection = TailorCollections[tailorId]
    if gender == 'm':
        collection = collection[BOY_SHORTS][:]
    else:
        collection = collection[GIRL_BOTTOMS][:]
    bottoms = []
    random.shuffle(collection)
    for style in collection:
        colors = BottomStyles[style][1][:]
        random.shuffle(colors)
        for color in colors:
            bottoms.append((BottomStyles[style][0], color))
    return bottoms

def getTops(gender, tailorId=MAKE_A_TOON):
    if gender == 'm':
        collection = TailorCollections[tailorId][BOY_SHIRTS]
    else:
        collection = TailorCollections[tailorId][GIRL_SHIRTS]
    tops = []
    for style in collection:
        for color in ShirtStyles[style][2]:
            tops.append(
                (ShirtStyles[style][0], color[0],
                 ShirtStyles[style][1], color[1])
            )
    return tops

def getAllTops(gender):
    tops = []
    for style in ShirtStyles.keys():
        if gender == 'm':
            if (style[0] == 'g') or (style[:3] == 'c_g'):
                continue
        elif (style[0] == 'b') or (style[:3] == 'c_b'):
            continue
        for color in ShirtStyles[style][2]:
            tops.append(
                (ShirtStyles[style][0], color[0],
                 ShirtStyles[style][1], color[1])
            )
    return tops

def getBottoms(gender, tailorId=MAKE_A_TOON):
    if gender == 'm':
        collection = TailorCollections[tailorId][BOY_SHORTS]
    else:
        collection = TailorCollections[tailorId][GIRL_BOTTOMS]
    bottoms = []
    for style in collection:
        for color in BottomStyles[style][1]:
            bottoms.append((BottomStyles[style][0], color))
    return bottoms

def getAllBottoms(gender, output='both'):
    bottoms = []
    for style in BottomStyles.keys():

        if gender == 'm':
            if (style[0] == 'g') or (style[:3] == 'c_g') or (
                style[:4] == 'vd_g') or (style[:4] == 'sd_g') or (
                style[:4] == 'j4_g') or (style[:4] == 'pj_g') or (
                style[:4] == 'wh_g') or (style[:4] == 'sa_g') or (
                style[:4] == 'sc_g') or (style[:5] == 'sil_g') or (
                style[:4] == 'hw_g'):
                continue
        elif (style[0] == 'b') or (style[:3] == 'c_b') or (
              style[:4] == 'vd_b') or (style[:4] == 'sd_b') or (
              style[:4] == 'j4_b') or (style[:4] == 'pj_b') or (
              style[:4] == 'wh_b') or (style[:4] == 'sa_b') or (
              style[:4] == 'sc_b') or (style[:5] == 'sil_b') or (
              style[:4] == 'hw_b'):
            continue

        bottomIdx = BottomStyles[style][0]
        if gender == 'f':
            textureType = GirlBottoms[bottomIdx][1]
        else:
            textureType = SHORTS
        if (output == 'both') or ((output == 'skirts') and (
            textureType == SKIRT)) or ((output == 'shorts') and (
            textureType == SHORTS)):
            for color in BottomStyles[style][1]:
                bottoms.append((bottomIdx, color))
    return bottoms

allColorsList = (
    VBase4(1, 1, 1, 1),
    VBase4(0.96875, 0.691406, 0.699219, 1),
    VBase4(0.933594, 0.265625, 0.28125, 1),
    VBase4(0.863281, 0.40625, 0.417969, 1),
    VBase4(0.710938, 0.234375, 0.4375, 1),
    VBase4(0.570312, 0.449219, 0.164062, 1),
    VBase4(0.640625, 0.355469, 0.269531, 1),
    VBase4(0.996094, 0.695312, 0.511719, 1),
    VBase4(0.832031, 0.5, 0.296875, 1),
    VBase4(0.992188, 0.480469, 0.167969, 1),
    VBase4(0.996094, 0.898438, 0.320312, 1),
    VBase4(0.996094, 0.957031, 0.597656, 1),
    VBase4(0.855469, 0.933594, 0.492188, 1),
    VBase4(0.550781, 0.824219, 0.324219, 1),
    VBase4(0.242188, 0.742188, 0.515625, 1),
    VBase4(0.304688, 0.96875, 0.402344, 1),
    VBase4(0.433594, 0.90625, 0.835938, 1),
    VBase4(0.347656, 0.820312, 0.953125, 1),
    VBase4(0.191406, 0.5625, 0.773438, 1),
    VBase4(0.558594, 0.589844, 0.875, 1),
    VBase4(0.285156, 0.328125, 0.726562, 1),
    VBase4(0.460938, 0.378906, 0.824219, 1),
    VBase4(0.546875, 0.28125, 0.75, 1),
    VBase4(0.726562, 0.472656, 0.859375, 1),
    VBase4(0.898438, 0.617188, 0.90625, 1),
    VBase4(0.7, 0.7, 0.8, 1),
    VBase4(0.3, 0.3, 0.35, 1)
)
defaultBoyColorList = (
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
    22, 23, 24
)
defaultGirlColorList = defaultBoyColorList
defaultGloveColorList = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26
)

defaultColorIndex = 25
blackColorIndex = 26
whiteColorIndex = 0

def getColorApproximation(color):
    (r, g, b, a) = color
    return VBase4(round(r, 3), round(g, 3), round(b, 3), round(a, 3))

allColorsListApproximations = map(getColorApproximation, allColorsList)
allowedColors = set(
    map(
        lambda x:allColorsListApproximations[x],
        set((0,) + defaultBoyColorList + defaultGirlColorList + (26,))
    )
)

HatModels = (
    None,
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_baseball',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_safari',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_ribbon',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_heart',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_topHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_anvil',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_flowerPot',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sandbag',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_weight',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_fez',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_golfHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_partyHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pillBox',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_crown',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_cowboyHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pirateHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_propellerHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_fishingHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sombreroHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_strawHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sunHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_antenna',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_beeHiveHairdo',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_bowler',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_chefsHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_detective',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_feathers',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_fedora',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_mickeysBandConductorHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_nativeAmericanFeather',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pompadorHairdo',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_princess',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_robinHoodHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_romanHelmet',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_spiderAntennaThingy',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_tiara',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_vikingHelmet',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_witch',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_wizard',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_conquistadorHelmet',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_firefighterHelmet',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_foilPyramid',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_minersHardhatWithLight',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_napoleonHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_pilotsCap',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_policeHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_rainbowAfroWig',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_sailorHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_carmenMirandaFruitHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_bobbyHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_jugheadHat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_winter',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_bandana',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_dinosaur',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_band',
    'phase_4/models/accessories/tt_m_chr_avt_acc_hat_birdNest'
)
HatTextures = (
    None,
    'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonRed.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonPurple.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_heartYellow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_topHatBlue.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_safariBrown.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_safariGreen.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_baseballBlue.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_baseballOrange.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonYellow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonChecker.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonLtRed.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonRainbow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_baseballYellow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_baseballRed.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_baseballTeal.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonPinkDots.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_baseballPurple.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_ribbonCheckerGreen.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_partyToon.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_hat_bowlerRoger.jpg'
)
GlassesModels = (
    None,
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_roundGlasses',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_miniblinds',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_narrowGlasses',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_starGlasses',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_3dGlasses',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_aviator',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_catEyeGlasses',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_dorkGlasses',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_jackieOShades',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_scubaMask',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_goggles',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_grouchoMarxEyebrow',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_heartGlasses',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_insectEyeGlasses',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_masqueradeTypeMask',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_masqueradeTypeMask3',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_monocle',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_mouthGlasses',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_squareRims',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_eyepatch',
    'phase_4/models/accessories/tt_m_chr_avt_acc_msk_alienGlasses'
)
GlassesTextures = (
    None,
    'phase_4/maps/tt_t_chr_avt_acc_msk_masqueradeTypeMask2.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_msk_masqueradeTypeMask4.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_msk_masqueradeTypeMask5.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_msk_eyepatchGems.jpg'
)
BackpackModels = (
    None,
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_backpack',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_batWings',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_beeWings',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_dragonFlyWings',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_scubaTank',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_sharkFin',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_angelWings',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_backpackWithToys',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_butterflyWings',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_dragonWing',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_jetPack',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_spiderLegs',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_stuffedAnimalBackpackA',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_birdWings',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_stuffedAnimalBackpackCat',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_stuffedAnimalBackpackDog',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_airplane',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_woodenSword',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_supertoonCape',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_vampireCape',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_dinosaurTail',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_band',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_gags',
    'phase_4/models/accessories/tt_m_chr_avt_acc_pac_flunky'
)
BackpackTextures = (
    None,
    'phase_4/maps/tt_t_chr_avt_acc_pac_backpackOrange.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_pac_backpackPurple.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_pac_backpackPolkaDotRed.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_pac_backpackPolkaDotYellow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_pac_angelWingsMultiColor.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_pac_butterflyWingsStyle2.jpg'
)
ShoesModels = ('feet', 'shoes', 'boots_short', 'boots_long')
ShoesTextures = (
    'phase_3/maps/tt_t_chr_avt_acc_sho_athleticGreen.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_athleticRed.jpg',
    'phase_3/maps/tt_t_chr_avt_acc_sho_docMartinBootsGreen.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleGreen.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_wingtips.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoes.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_deckShoes.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_athleticYellow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleBlack.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleWhite.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_converseStylePink.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_cowboyBoots.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPurple.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_hiTopSneakers.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesBrown.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesRed.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_superToonRedBoots.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesGreen.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesPink.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleRed.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsAqua.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsBrown.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsYellow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsBlueSquares.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreenHearts.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreyDots.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsOrangeStars.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPinkStars.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_loafers.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesPurple.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_motorcycleBoots.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_oxfords.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsPink.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_santaBoots.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsBeige.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsPink.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_workBoots.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleYellow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsPink.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_hiTopSneakersPink.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsRedDots.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesPurple.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesViolet.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesYellow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsBlue.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsYellow.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_athleticBlack.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_pirate.jpg',
    'phase_4/maps/tt_t_chr_avt_acc_sho_dinosaur.jpg'
)

HatStyles = {
    'none':[0, 0, 0],
    'hbb1':[1, 0, 0],
    'hsf1':[2, 0, 0],
    'hsf2':[2, 5, 0],
    'hsf3':[2, 6, 0],
    'hht1':[4, 0, 0],
    'hht2':[4, 3, 0],
    'htp1':[5, 0, 0],
    'htp2':[5, 4, 0],
    'hav1':[6, 0, 0],
    'hfp1':[7, 0, 0],
    'hsg1':[8, 0, 0],
    'hwt1':[9, 0, 0],
    'hfz1':[10, 0, 0],
    'hgf1':[11, 0, 0],
    'hpt1':[12, 0, 0],
    'hpt2':[12, 19, 0],
    'hpb1':[13, 0, 0],
    'hcr1':[14, 0, 0],
    'hbb2':[1, 7, 0],
    'hbb3':[1, 8, 0],
    'hcw1':[15, 0, 0],
    'hpr1':[16, 0, 0],
    'hpp1':[17, 0, 0],
    'hfs1':[18, 0, 0],
    'hsb1':[19, 0, 0],
    'hst1':[20, 0, 0],
    'hat1':[22, 0, 0],
    'hhd1':[23, 0, 0],
    'hbw1':[24, 0, 0],
    'hch1':[25, 0, 0],
    'hdt1':[26, 0, 0],
    'hft1':[27, 0, 0],
    'hfd1':[28, 0, 0],
    'hmk1':[29, 0, 0],
    'hft2':[30, 0, 0],
    'hhd2':[31, 0, 0],
    'hrh1':[33, 0, 0],
    'hhm1':[34, 0, 0],
    'hat2':[35, 0, 0],
    'htr1':[36, 0, 0],
    'hhm2':[37, 0, 0],
    'hwz1':[38, 0, 0],
    'hwz2':[39, 0, 0],
    'hhm3':[40, 0, 0],
    'hhm4':[41, 0, 0],
    'hfp2':[42, 0, 0],
    'hhm5':[43, 0, 0],
    'hnp1':[44, 0, 0],
    'hpc2':[45, 0, 0],
    'hph1':[46, 0, 0],
    'hwg1':[47, 0, 0],
    'hbb4':[1, 13, 0],
    'hbb5':[1, 14, 0],
    'hbb6':[1, 15, 0],
    'hsl1':[48, 0, 0],
    'hfr1':[49, 0, 0],
    'hby1':[50, 0, 0],
    'hjh1':[51, 0, 0],
    'hbb7':[1, 17, 0],
    'hwt2':[52, 0, 0],
    'hhw2':[54, 0, 0],
    'hob1':[55, 0, 0],
    'hbn1':[56, 0, 0],
    'hrb1':[3, 0, 0],
    'hrb2':[3, 1, 0],
    'hrb3':[3, 2, 0],
    'hsu1':[21, 0, 0],
    'hrb4':[3, 9, 0],
    'hrb5':[3, 10, 0],
    'hrb6':[3, 11, 0],
    'hrb7':[3, 12, 0],
    'hpc1':[32, 0, 0],
    'hrb8':[3, 16, 0],
    'hrb9':[3, 18, 0],
    'hhw1':[53, 0, 0]
}
GlassesStyles = {
    'none':[0, 0, 0],
    'grd1':[1, 0, 0],
    'gmb1':[2, 0, 0],
    'gnr1':[3, 0, 0],
    'gst1':[4, 0, 0],
    'g3d1':[5, 0, 0],
    'gav1':[6, 0, 0],
    'gjo1':[9, 0, 0],
    'gsb1':[10, 0, 0],
    'ggl1':[11, 0, 0],
    'ggm1':[12, 0, 0],
    'ghg1':[13, 0, 0],
    'gie1':[14, 0, 0],
    'gmt1':[15, 0, 0],
    'gmt2':[15, 1, 0],
    'gmt3':[16, 0, 0],
    'gmt4':[16, 2, 0],
    'gmt5':[16, 3, 0],
    'gmn1':[17, 0, 0],
    'gmo1':[18, 0, 0],
    'gsr1':[19, 0, 0],
    'gce1':[7, 0, 0],
    'gdk1':[8, 0, 0],
    'gag1':[21, 0, 0],
    'ghw1':[20, 0, 0],
    'ghw2':[20, 4, 0]
}
BackpackStyles = {
    'none':[0, 0, 0],
    'bpb1':[1, 0, 0],
    'bpb2':[1, 1, 0],
    'bpb3':[1, 2, 0],
    'bpd1':[1, 3, 0],
    'bpd2':[1, 4, 0],
    'bwg1':[2, 0, 0],
    'bwg2':[3, 0, 0],
    'bwg3':[4, 0, 0],
    'bst1':[5, 0, 0],
    'bfn1':[6, 0, 0],
    'baw1':[7, 0, 0],
    'baw2':[7, 5, 0],
    'bwt1':[8, 0, 0],
    'bwg4':[9, 0, 0],
    'bwg5':[9, 6, 0],
    'bwg6':[10, 0, 0],
    'bjp1':[11, 0, 0],
    'blg1':[12, 0, 0],
    'bsa1':[13, 0, 0],
    'bwg7':[14, 0, 0],
    'bsa2':[15, 0, 0],
    'bsa3':[16, 0, 0],
    'bap1':[17, 0, 0],
    'bhw1':[18, 0, 0],
    'bhw2':[19, 0, 0],
    'bhw3':[20, 0, 0],
    'bhw4':[21, 0, 0],
    'bob1':[22, 0, 0],
    'bfg1':[23, 0, 0],
    'bfl1':[24, 0, 0]
}
ShoesStyles = {
    'none':[0, 0, 0],
    'sat1':[1, 0, 0],
    'sat2':[1, 1, 0],
    'smb1':[3, 2, 0],
    'scs1':[2, 3, 0],
    'sdk1':[1, 6, 0],
    'sat3':[1, 7, 0],
    'scs2':[2, 8, 0],
    'scs3':[2, 9, 0],
    'scs4':[2, 10, 0],
    'scb1':[3, 11, 0],
    'sht1':[2, 13, 0],
    'ssb1':[3, 16, 0],
    'sts1':[1, 17, 0],
    'sts2':[1, 18, 0],
    'scs5':[2, 19, 0],
    'smb2':[3, 20, 0],
    'smb3':[3, 21, 0],
    'smb4':[3, 22, 0],
    'slf1':[1, 28, 0],
    'smt1':[3, 30, 0],
    'sox1':[1, 31, 0],
    'srb1':[3, 32, 0],
    'sst1':[3, 33, 0],
    'swb1':[3, 34, 0],
    'swb2':[3, 35, 0],
    'swk1':[2, 36, 0],
    'scs6':[2, 37, 0],
    'smb5':[3, 38, 0],
    'sht2':[2, 39, 0],
    'srb2':[3, 40, 0],
    'sts3':[1, 41, 0],
    'sts4':[1, 42, 0],
    'sts5':[1, 43, 0],
    'srb3':[3, 44, 0],
    'srb4':[3, 45, 0],
    'sat4':[1, 46, 0],
    'shw1':[3, 47, 0],
    'shw2':[3, 48, 0],
    'swt1':[1, 4, 0],
    'smj1':[2, 5, 0],
    'sfb1':[3, 12, 0],
    'smj2':[2, 14, 0],
    'smj3':[2, 15, 0],
    'sfb2':[3, 23, 0],
    'sfb3':[3, 24, 0],
    'sfb4':[3, 25, 0],
    'sfb5':[3, 26, 0],
    'sfb6':[3, 27, 0],
    'smj4':[2, 29, 0]
}

MATGirlHats = [
    [0, 0, 0], [3, 0, 0], [3, 1, 0], [42, 0, 0], [5, 0, 0], [5, 4, 0],
    [48, 0, 0], [2, 0, 0], [45, 0, 0], [4, 0, 0], [11, 0, 0]
]
MATGirlGlasses = [
    [0, 0, 0], [18, 0, 0], [15, 0, 0], [19, 0, 0], [20, 4, 0], [7, 0, 0],
    [17, 0, 0]
]
MATGirlBackpacks = [
    [0, 0, 0], [23, 0, 0], [1, 4, 0], [7, 0, 0], [18, 0, 0], [20, 0, 0],
    [2, 0, 0], [10, 0, 0], [12, 0, 0]
]
MATGirlShoes = [
    [0, 0, 0], [1, 4, 0], [3, 11, 0], [3, 47, 0], [3, 34, 0], [3, 35, 0],
    [1, 41, 0], [2, 36, 0], [2, 9, 0], [2, 8, 0]
]

MATBoyHats = [
    [0, 0, 0], [55, 0, 0], [42, 0, 0], [5, 0, 0], [5, 4, 0], [48, 0, 0],
    [33, 0, 0], [2, 0, 0], [45, 0, 0], [11, 0, 0]
]
MATBoyGlasses = [
    [0, 0, 0], [15, 0, 0], [19, 0, 0], [20, 4, 0], [17, 0, 0], [3, 0, 0],
    [6, 0, 0]
]
MATBoyBackpacks = [
    [0, 0, 0], [23, 0, 0], [7, 0, 0], [5, 0, 0], [18, 0, 0], [20, 0, 0],
    [2, 0, 0], [10, 0, 0], [12, 0, 0]
]
MATBoyShoes = [
    [0, 0, 0], [3, 11, 0], [3, 47, 0], [1, 41, 0], [2, 36, 0], [2, 9, 0],
    [2, 8, 0]
]

def isValidHat(itemIdx, textureIdx, colorIdx):
    return (itemIdx, textureIdx, colorIdx) in HatStyles.values()

def isValidGlasses(itemIdx, textureIdx, colorIdx):
    return (itemIdx, textureIdx, colorIdx) in GlassesStyles.values()

def isValidBackpack(itemIdx, textureIdx, colorIdx):
    return (itemIdx, textureIdx, colorIdx) in BackpackStyles.values()

def isValidShoes(itemIdx, textureIdx, colorIdx):
    return (itemIdx, textureIdx, colorIdx) in ShoesStyles.values()

def isValidAccessory(itemIdx, textureIdx, colorIdx, which):
    if which == HAT:
        return isValidHat(itemIdx, textureIdx, colorIdx)
    elif which == GLASSES:
        return isValidGlasses(itemIdx, textureIdx, colorIdx)
    elif which == BACKPACK:
        return isValidBackpack(itemIdx, textureIdx, colorIdx)
    elif which == SHOES:
        return isValidShoes(itemIdx, textureIdx, colorIdx)
    else:
        return False