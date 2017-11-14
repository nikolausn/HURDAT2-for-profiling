# Assignment 2 - Hurricane Data Analysis

# Notice: It would take several minutes for running, especially for atlantic files, due to the large calculation
# workload for distance and directional changes.
# The program is NOT stuck. We've tested it before submission. It just needs more time.


f='hurdat2-1851-2016-041117-SHORT.txt'      # a sample from the Atlantic data for testing and profiling
# f='hurdat2-1851-2016-041117.txt'          # Full Atlantic data file
# f='hurdat2-nepac-1949-2016-041317.txt'    # Eastern Pacific data file

with open(f, 'r') as input_file:
    df = input_file.read().splitlines(keepends=False)

from pygeodesy import ellipsoidalVincenty as ev
import datetime as datetime

# Functions
def SplitStrip (line):
    """
    Split data(one line each time) and return a clean data without space
    :param line: Data waiting for dealing
    :return: newline: Data after removing unnecessary spaces
    """
    newline=[]
    LSplit=line.split(',')
    for w in LSplit:
        newline.append(w.strip())
    return newline


def addvalue(dic,key,value):
    """
    A function to add key and values in dictionary
    :param dic: Dictionary waiting for adding values
    :param key: The key in dic, where we would add values in
    :param value: The values for adding
    :return: dic: Dictionary after adding values
    """
    if key not in dic:
        dic[key]=[value]
    else:
        dic[key].append(value)
    return dic


def get_distance(list):
    """
     Get a list whose elements are distances between each two adjacent samples, according to given latitude and longitude pairs.
    :param list: A list whose elements are sublists. Each sublist has two elements, latitude (string) and longitude (string).
    :return: distance: A list which elements are distances (nautical miles).
    """
    loc = []
    distance=[]
    for i in range (len(list)):
        loc.append(ev.LatLon(list[i][0],list[i][1]))
    for j in range(len(loc)-1): # Only N-1 distances would be got if N pairs of latitude and longitude pairs are given
        if loc[j] != loc[j+1]:
            d = loc[j].distanceTo(loc[j+1]) / 1852.0
            distance.append(d)
        else:
            distance.append(int(0))
    return distance


def get_time(list):
    """
    Get a list, whose elements are time lags of each two adjacent samples.
    :param list: A list whose elements are sublists. Each sublist has two element, date (string) and time (string)
    :return: A list whose elements are times lags (in hours)
    """
    timelist =[]
    dt = []
    for i in range(len(list)):
        dt.append(list[i][0]+list[i][1])
    for j in range(0,len(dt)-1):
        a = (datetime.datetime.strptime(dt[j+1], "%Y%m%d%H%M")-datetime.datetime.strptime(dt[j], "%Y%m%d%H%M")).total_seconds()/3600
        timelist.append(a)
    return timelist


def get_LL(dictionary,start,end):
    """
    Get a dictionary, whose keys are Storm IDs, and whose values are latitudes and longitudes pairs, or date and time pairs,
    according to parameters start and end
    :param dictionary: Usually would be LL.
    :param start: Starting index of sublists
    :param end:Ending index of sublists.
    parameters start and end together determines what we want to extract from LL.
    :return: a list
    """

    "the complexity of this algorithm is n2"
    ll_list={}
    for i in dictionary:
        for j in dictionary[i]:
            line = SplitStrip(j)
            #line = j
            addvalue(ll_list,i,line[start:end])
    return ll_list

def get_LL_new(dictionary,start,end,index):
    """
    Get a dictionary, whose keys are Storm IDs, and whose values are latitudes and longitudes pairs, or date and time pairs,
    according to parameters start and end
    :param dictionary: Usually would be LL.
    :param start: Starting index of sublists
    :param end:Ending index of sublists.
    parameters start and end together determines what we want to extract from LL.
    :return: a list
    """

    "the complexity of this algorithm is n2"
    """
    ll_list={}
    for i in dictionary:
        for j in dictionary[i]:
            line = SplitStrip(j)
            #line = j
            addvalue(ll_list,i,line[start:end])
    """
    #print(dictionary[index])
    line = []
    for x in dictionary[index]:
        line.append(SplitStrip(x)[start:end])
    #return ll_list
    return line


def c_storm_hurri(idlist):
    """
    Generate an dictionary, whose keys are years and values
    are number of storms/hurricanes happened during that year
    :param idlist: Storm ID list
    :return: count: A dictionary whose keys are years and whose values are total number of storms (or hurricanes) happend during that year
    """
    count={}
    for item in idlist:
        if item[-4:] in count.keys():
            count[item[-4:]]+=1
        else:
            count[item[-4:]]=1
    return count


# In[241]:

def get_speed(dis,t):
    """
    Get a dictionary named speed, whose keys are Storm IDs. It contains every storm who has more than one samples.
    For each storm, we calculate the speed during every two adjacent sampled times/locations.
    :param dis:
    :param t:
    :return:
    """
    for key in dis.keys():
        for inx in range(len(dis[key][0])):
            addvalue(speed,key,dis[key][0][inx]/t[key][0][inx])
            # Calculating speed using distance/time lag


# In[242]:

def get_degree(points):
    """
    Calculating directional changes between samples
    :param points: A list of latitude and longitude pairs
    :return:  degree: a list of diretional changes.
    """
    loc = []
    degree=[]
    for i in range (len(points)):
        loc.append(ev.LatLon(points[i][0],points[i][1]))
    for j in range(len(loc)-1):
        if loc[j] != loc[j+1]:
            d = loc[j].bearingTo(loc[j+1])
            if d<=180:
                degree.append(d)
            else:
                degree.append(360-d) # For example, a directional change of 200 degrees, clockwise,
                # in fact, would be the same with a directional change of 160 degrees, anticlockwise.
        else:
            degree.append(int(0)) # bearingTo funcion would report error when two same latitude and longitude pairs are given
    return degree


# Use Data

name={}
Date={} # Date range record
Timepoints={} # Help to solve Phase B 3.
landfall={}
MSW={} # Maximum sustained wind(in knots) & occurred(date & time)
LL={} # get latitude and longitude pairs and date and time pairs. It is a dictionary, whose keys are Storm IDs, and whose values are also lists.
# It stores latitudes, longitudes, dates and times for each sample of each storm, as long as the storm has more than one record.
HU=[]
countLF=0
start=1 
line0=SplitStrip(df[0])
Id=line0[0]
name[Id]=line0[1]
LineNum=int(line0[2])
end=start+LineNum
DT_FirstLandfall={}

# split strip only once
df_strip=[]
for line in df:
    df_strip.append(SplitStrip(line))

df = df_strip

while end <= len(df):
    for line in df[start:end]:
        #cleanline=SplitStrip(line)
        cleanline = line
        addvalue(Date,Id,cleanline[0])
        addvalue(Timepoints,Id, cleanline[1])
        addvalue(MSW,Id,cleanline[6]+', '+cleanline[0])
        if (end-start) > 1:
            #Get the LatLon and time only when the storm has more than 1 record
            #otheriwise, with only one pair of latitude and longitude, we cannot calculate
            #the distance, speed or directional change
            addvalue(LL,Id,cleanline[4]+', '+cleanline[5]+', '+cleanline[0]+', '+cleanline[1])
        if cleanline[2] == 'L':
            countLF += 1 
            if countLF == 1:
                dt=datetime.datetime.strptime(cleanline[0]+cleanline[1], "%Y%m%d%H%M")
                addvalue(DT_FirstLandfall,Id,dt)# Generate a dictionary, whose keys are Storm ID, and whose values are lists.
                # Each list has only one element, which is the date and time of first landfall. Storm who had no landfall would not be in this dictionary.
        if cleanline[3] == 'HU':
            if Id not in HU:
                HU.append(Id)
    addvalue(landfall,Id,countLF)
    if end != len(df): 
        #LineNum=int(SplitStrip(df[end])[2])
        LineNum = int(df[end][2])
        #Id=SplitStrip(df[end])[0]
        Id = df[end][0]
        #name[Id]=SplitStrip(df[end])[1]
        name[Id] = df[end][1]
        countLF=0
        start=end+1
        end=start+LineNum
    else:
        break


time={}
distance={}
# this is wrong, it tries to compute all dictionary  and return new list, instead we can optimize for just the focus index only
"""
for i in LL:
    print(get_LL(LL,0,2)[i])
    print(get_LL_new(LL, 0, 2, i))
    addvalue(distance,i,get_distance(get_LL(LL,0,2)[i]))
    addvalue(time,i,get_time(get_LL(LL,2,4)[i]))
"""
for i in LL:
    addvalue(distance,i,get_distance(get_LL_new(LL,0,2,i)))
    addvalue(time,i,get_time(get_LL_new(LL,2,4,i)))


# Deal with highest Maximum sustained wind (in knots) and when it occurred (date & time)

MSW_speed={}
MSW_time={}
compare_s=0
compare_t=0
for i in MSW:
    for j in MSW[i]:
        #line=SplitStrip(j)
        line = j
        if int(line[0])>compare_s:
            compare_s = int(line[0])
            compare_t = int(line[1])
    addvalue(MSW_speed,i,compare_s)
    addvalue(MSW_time,i,compare_t) 


# PHASE B

# * 2 . Get the total distances for each storm


total_distance={}
for key in distance.keys():
    addvalue(total_distance,key,sum(distance[key][0]))

# * 1 . Get the speed (list). For mean speed, using total distance/total time


speed={}
get_speed(distance,time)
mean_speed={} # Calculating using total distance / total time lag
for key in total_distance.keys():
    addvalue(mean_speed,key,total_distance[key][0]/sum(time[key][0]))


# * 3 . Calculate the percentage of number of storms whose greatest directional change per unit time happened after first landfall, in total number of storms who had landfall(s).


deg_change={}
Loc=get_LL(LL,0,2)

# Since we only get latitudes and longitudes of those storms who have more than one records (to calculate changes between
# records, we need at least two records), for those storms who have only one record but had landfall, their IDs are in
# dictionary DT_FirstLandfall, but not in dictionary LL. Therefore, an error message would appear. They would be taken into account when counting number of storms who had
# landfall(s), but definitely would not affect the total amount of storms whose greatest directional changes happened after
# first landfall.

for key in DT_FirstLandfall.keys():
    # Only calculate directional changes for those storms who had landfall(s).
    if key in Loc.keys():
        addvalue(deg_change,key,get_degree(Loc[key])) # Get a dictionary, whose keys are Storm ID, and whose values are lists, the elements of which are directional changes between samples.


unit_dir_change={} # Directional changes per unit time (in minute)
for key in DT_FirstLandfall.keys():
    if key in time.keys():
        for inx in range(len(time[key][0])):# Only calculate directional changes for those storms who had landfall(s).
            addvalue(unit_dir_change,key, deg_change[key][0][inx]/time[key][0][inx]) # Get a dictionary, whose keys are Storm ID, and whose values are lists, elements of which are directional changes per unit time (per minute).


Count=0 # Count the number of storms whose greates directional change happened after first landfall.
for key in unit_dir_change.keys():
    maxchg=0
    for inx in range(len(unit_dir_change[key])):
        if unit_dir_change[key][inx]>maxchg:
            maxchg=unit_dir_change[key][inx]
            dt_maxchg=datetime.datetime.strptime(Date[key][inx]+Timepoints[key][inx], "%Y%m%d%H%M")
    if DT_FirstLandfall[key][0]<dt_maxchg:
        Count+=1


# Print out results

# * 1. Each Storm
# Storm Id, Name
# Date ranges
# Highest Maximum Sustained Wind
# Times of landfall
# Total distance tracked
# Maximum speed
# Mean speed

for i in name:
    print('Storm ID: ',i,'\nStorm Name: ',name[i],'\nDate Range Recorded: from ',min(Date[i]),' to ',max(Date[i]),'\nHighest Maximum Sustained Wind(in knots): Speed: ',MSW_speed[i],' Time: ',MSW_time[i],'\nLandfall: ',landfall[i],' time(s)\n')
    if i in LL.keys():
        print('Total distance tracked:',round(total_distance[i][0],2),'nm',
              '\nMaximum Speed:',round(max(speed[i]),2),'knots',
              '\nMean Speed:',round(mean_speed[i][0],2),'knots\n')
    else:
        print('Since there is only one record for the storm, total distance tracked, maximum speed, and mean speed cannot be calculated.\n')


# * 2 . Summary
# Number of storm each year
# Number of hurricane each year
# Percantage of storms where greatest directional change occurred after the first lanfall

EachY_Storm = c_storm_hurri(list(name.keys()))#The whole storm id in the file
EachY_HU = c_storm_hurri(HU)#The Hurricane storm id in the file
for i in EachY_Storm:
    if i not in EachY_HU.keys():
        print('Year: ',i,'\nNumber of Storms: ',EachY_Storm[i],'\nNumber of Hurricanes: None\n')
    else:
        print('Year: ',i,'\nNumber of Storms: ',EachY_Storm[i],'\nNumber of Hurricanes: ',EachY_HU[i],'\n')
print("The percentage of storms where greatest directional change occurred after the first landfall:",Count/len(DT_FirstLandfall)*100,"%\n")

# END.