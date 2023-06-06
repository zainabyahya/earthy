import heapq
from flask_login import current_user
from earthy.models import Plastic


class item:

    # Constructor
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight


def getItemWeight(itemName):
    if itemName == 'plasticBottle':
        return 9.9
    elif itemName == 'plasticBag':
        return 7
    elif itemName == 'plasticWrap':
        return 15
    elif itemName == 'yoghurtBox':
        return 15
    elif itemName == 'cottonSwab':
        return 1
    elif itemName == 'detergentBottle':
        return 120
    elif itemName == 'shampooBottle':
        return 80
    elif itemName == 'toothbrush':
        return 20
    elif itemName == 'toothpaste':
        return 15
    elif itemName == 'takeawayBox':
        return 33
    elif itemName == 'takeawayWrap':
        return 20
    elif itemName == 'straw':
        return 0.5
    elif itemName == 'disposableCutlery':
        return 3.9
    elif itemName == 'plasticPlate':
        return 24
    return 1

# Get Total Item Grams

def getItemTotalGrams(weight, quantity, frequency):
    if frequency == 'day':
        frequency = 365
    elif frequency == 'week':
        frequency = 52.14
    elif frequency == 'month':
        frequency = 12
    elif frequency == 'year':
        frequency = 1
    else:
        frequency = 52.14
    return weight*quantity*frequency


def getTotalWeight(items):
    totalWeight = 0
    for item in items:
        totalWeight += item.weight
    plasticKg = totalWeight
    return round(plasticKg, 3)


def lowerAverageLocally(totalWeightPerYear):
    localAverage = 28.4  # kg/year/person
    difference = localAverage-totalWeightPerYear
    if difference > 0:
        return True
    else:
        return False


def lowerAverageNationally(totalWeightPerYear):
    internationalAverage = 50.6  # kg/year/person
    difference = internationalAverage-totalWeightPerYear
    if difference >0:
        return True
    else:
        return False


def getNewTrackingSession(items):
    plasticBottle = items[0].weight
    plasticBag = items[1].weight
    plasticWrap = items[2].weight
    yoghurtBox = items[3].weight
    cottonSwab = items[4].weight
    detergentBottle = items[5].weight
    shampooBottle = items[6].weight
    toothbrush = items[7].weight
    toothpaste = items[8].weight
    takeawayBox = items[9].weight
    takeawayWrap = items[10].weight
    straw = items[11].weight
    disposableCutlery = items[12].weight
    plasticPlate = items[13].weight

    trackingSession = Plastic(user=current_user, plasticBottle=plasticBottle, plasticBag=plasticBag, plasticWrap=plasticWrap, yoghurtBox=yoghurtBox, cottonSwab=cottonSwab, detergentBottle=detergentBottle,
                              shampooBottle=shampooBottle, toothbrush=toothbrush, toothpaste=toothpaste, takeawayBox=takeawayBox, takeawayWrap=takeawayWrap, straw=straw, disposableCutlery=disposableCutlery, plasticPlate=plasticPlate)

    return trackingSession

def getMax(items):
    maxItems=sorted(items, key=lambda x: x.weight, reverse=True)
    return maxItems[0:3]

def getSuggestions(items):
    s=""
    if any(item.name == "Plastic Bottle" for item in items):
        s+="Try using a reusable water bottle, they cost $5-10, which equals 10-20 plastic water bottles. You will be saving movey after 20 days of using a reusable bottle! "
    if any(item.name == "Plastic Bag" for item in items):
        s+="There are plenty of reusable bags, with different sizes and patterns, that last much longer than a plastic bag whose average age is 10-15 minutes. "
    if any(item.name =="Plastic Wrap" for item in items):
        s+="You can use wax paper or silicon covers instead of plastic wraps, they last longer and won't be thrown away after one use. "
    if any(item.name == 'Yoghurt Box' or item.name == 'Detergent Bottle' or item.name == 'Shampoo Bottle' for item in items):
        s+="Try to buy the larger boxes since they consume less plastic than many boxes of small sizes."
    if any(item.name == 'Cotton Swab' for item in items):
        s+="There are cotton swab whose stick made of bamboo, try them. Or use a tissue since it has less plastic. "
    if any(item.name == 'Toothbrush' for item in items):
        s+="There are toothbrushes made of bamboo instead of plastic, so if you throw them, they can degrade unlike plastic toothbrushes. "
    if any(item.name == 'Toothpaste' for item in items):
        s+="Try to buy the larger tubes since they consume less plastic than many tubes of small sizes. "
    if any(item.name == 'Takeaway Box' or item.name == 'Takeaway Wrap' for item in items):
        s+="Choose sustainable restuarants, limit deliveries and choose dine-in instead, or ask them to limit package and disposable cutlery as much as possible. "
    if any(item.name == 'Straw' for item in items):
        s+="Use a reusable straw! There are straws made of glass, bamboo or steel, choose what suits you! "
    if any(item.name == 'Disposable Cutlery' for item in items):
        s+="Use your own set! there are many sets that are pocket friendly and come in different designs and sizes. "
    if any(item.name == 'Plastic Plate' for item in items):
        s+="If it's becuase of restuarant deliveries, try to choose sustainable resuarants. If you use them excessivly at home, you should replace them with the usual plates. "
    return s

