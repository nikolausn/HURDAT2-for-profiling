#############################################################
# LIS590PR
# Assignment2
# Run our main function for Atlantic and Pacific, and other databases.

import datetime as dt
from pygeodesy import ellipsoidalVincenty as ev


def PhaseA1(storm:list, outputfile:str)->print(list):
    '''
    This function is for PhaseA1: calculating some stats data, which includes [ID, name,
    date_min,data_max, MSW, dt3,tm3, landfall_count]
    :param storm: is the storm in the format of list that just read from original text file.
    :param outputfile: the file to save the results to.
    :return: print parameter list of the storm [ID, name, date_min,data_max, MSW, dt3,tm3, landfall_count]
    '''
    ID = storm[0][0]
    name = storm[0][1]  # storm system name
    date_min = storm[1][0];
    data_max = storm[-1][0]; # for date range
    #    !highest MSW and when (date, time)
    MSW = 0;
    dt3 = [];
    tm3 = [];
    for incident in storm:
        try:
            if int(incident[6]) > MSW:
                MSW = int(incident[6]);
                dt3 = incident[0];
                tm3 = incident[1];
        except:
            continue
            #    !times of landfall
    landfall_count = 0
    for incident in storm:
        if incident[2] == ' L':
            landfall_count += 1
    with open(outputfile, 'a') as outp:
        print('Phase,   ID,                  name,   date_min,date_max, MSW, date, time, landfall_count',
              file=outp)
        print('PhaseA1:', ID, name, date_min, data_max, MSW, dt3, tm3, landfall_count, file=outp)


def PhaseA2(storm:list, st_count:dict, hu_count:dict, outputfile:str):
    """
    This function is to solve the PhaseA2.
    :param storm: ear
    :param st_count: accumulator for storms each year
    :param hu_count: accumulator for hurricanes each year
    :param outputfile: output file that saves the result.
    :return:
    """
    beg=1800
    fin=2017
    for year in range(beg,fin+1):
        for incident in storm:
            if incident[0][:4] == str(year):
                st_count[year] += 1
                break

    for year in range(beg,fin+1):
        for incident in storm:
            if incident[3] == ' HU':
                if incident[0][:4] == str(year):
                    hu_count[year]+=1
                    break

#    with open(outputfile, 'a') as output_file:
#        print('PhaseA:2', file=output_file)
#        print(st_count, file=output_file)
#        print(hu_count, file=output_file)

#    return st_count, hu_count

""" This is Phase B of assignment 2. Three tasks in all. """
# PhaseB.Task1
# maximum and mean speed that the storm center moved.
def time2(date:str,time:str):
    """
    This function is to transform two strings (date and time) in the textdata to time framedata.
    :param date: input date string, eg: 18510625
    :param time: input time string, eg: 0600
    :return: return class 'datetime.datetime', eg:1851-06-25 06:00:00
    """
    time2 = dt.datetime(int(date[:4]),int(date[4:6]),int(date[6:]),int(time[1:3]),int(time[3:]))
    return(time2)


def degree(storm:list) ->list:
    '''
    This function defines how to caluclate from text data to the time interval and distance interval
    between lines next to each other.
    :param storm: a list containing the whole information for a single strom. eg: list[0]
    :return: a list, a dataframe containing delta (unit: hour), delta_accu(unit:hour), dist(unit:meter),
    and dist_accu (unit:degree).
    '''
    # time is not processed yet.

    de=[]; dist_accu=0; delta_accu=0;
    for line in range(1,len(storm)-1):
        c = time2(storm[line][0],storm[line][1])
        d = time2(storm[line+1][0],storm[line+1][1])
        delta1 = d-c
        delta_accu = d-time2(storm[1][0],storm[1][1])
#        a = ev.LatLon(latlon(list[0][line][4]), latlon(list[0][line][5]))
#        b = ev.LatLon(latlon(list[0][line + 1][4]), latlon(list[0][line + 1][5]))
        a = ev.LatLon(storm[line][4],storm[line][5])
        b = ev.LatLon(storm[line+1][4],storm[line+1][5])
        if a!=b:
#           ee = a.distanceTo3(b)
#           dist1=ee[0];
#           degree1=ee[1];
            dist1 = a.distanceTo(b)
            degree1 = a.bearingTo(b)
            dist_accu+=dist1
            #de.append([delta1, delta_accu, dist1, dist_accu, degree1, velocity])
            de.append([delta1.total_seconds()/3600, delta_accu.total_seconds()/3600,
                   dist1, dist_accu, degree1, (dist1)/(delta1.total_seconds()/3600)])
        #else:
            #print('same location')

    return de

def max_mean_velo(degree:list)->str:
    '''
    calculate the mean and max velo for each storm
    :param degree: the list generate by the degree function.
    :return: mean and max values.
    '''
    max_velo=0;
    mean_velo = degree[-1][3]/degree[-1][1];
    for i in range(len(degree)):
        if degree[i][5] > max_velo:
            max_velo = degree[i][5]
    return [max_velo,mean_velo]

def PhaseB1(storm:list,outputfile):
    """

    :param storm:
    :param outputfile:
    :return:
    """
    if len(storm)<3:
        with open(outputfile, 'a') as output_file:
            print('PhaseB1: This storm has only one record.', file = output_file)
    elif (storm[1][4]==storm[2][4])&(storm[1][5]==storm[2][5]):
        with open(outputfile, 'a') as output_file:
            print('PhaseB1: Identical lat & lon for different records.', file = output_file)
    else:
        with open(outputfile, 'a') as output_file:
            print('PhaseB1: For', storm[0][0], ', the maximum speed that the storm center moved is',
                  max_mean_velo(degree(storm))[0] / 1852, 'knots.', file = output_file)
            # 1 knot = 1852 meter per hour
            print('         For', storm[0][0], ', the average speed that the storm center moved is',
                  max_mean_velo(degree(storm))[1] / 1852, 'knots.', file=output_file)

def PhaseB2(storm:list,outputfile:str):
    """
    total distance for the single storm
    :param storm: each storm just read,. eg: read from main function.
    :param output: output file address. eg: 'solution_b_output.txt'
    :return: return the distance that each single storm moved.
    """
    if len(storm)<3:
        with open(outputfile, 'a') as output_file:
            print('PhaseB2: This storm has only one record.', file = output_file)
    elif (storm[1][4]==storm[2][4])&(storm[1][5]==storm[2][5]):
        with open(outputfile, 'a') as output_file:
            print('PhaseB2: Identical lat & lon for different records.', file = output_file)
    else:
        with open(outputfile, 'a') as output_file:
            print('PhaseB2: For', storm[0][0], ', the accumulated distance that the storm was tracked is',
                  degree(storm)[-1][3]/1000, 'km.', file=output_file)


def max_directional_change(listb2:list)->list:
    """
    This function is to design, for each storm, the greatest directional change (gdc) per unit time.
    The idea flow is as below: degree_from_imported_list -> delta_degree -> transform to solve the (359-1=2 problem)
    -> calculate the gdc/time [fixed_delta_degree/sum_of_time] -> find the max.
    :param listb2: This list the degree list generated from the degree function for each storm. (see PhaseB2)
    :return: the max value and the index when it occurs in the storm text data.
    """
    mdc = [];
    listb3 = [];
    if listb2 != []:
        for line in range(len(listb2) - 1):
            delta_degree = abs(listb2[line][4] - listb2[line + 1][4])
            if delta_degree < 180:
                delta_degree2 = delta_degree
            else:
                delta_degree2 = 360 - delta_degree
            mdc.append(delta_degree2 / abs(listb2[line][0] + listb2[line + 1][0]))

        # max(mdc) # max_direction_change_per_hour
        # mdc.index(max(mdc)) # index of the mdc
        # mdc.index(max(mdc)) + 2 # index of the record line in orginal text
        listb3 = [max(mdc), mdc.index(max(mdc)) + 2]  ###### this is very important 0.271866295
        # listb3=[max(mdc),mdc.index(max(mdc)) + 1]###### another try 0.279665738
        # listb3 = [max(mdc), mdc.index(max(mdc))] ###### 0.26963788
        #    else:
        #        with open('test.txt', 'a') as output_file:
        #            print('Lat and lon info of this storm are not correct.', file = output_file)
    return listb3
# print(max_directional_change(degree(storm)))


def PhaseB3(storm : list, outputfile:str, indi:list):
    if len(storm)<4: # you have to have more than 3 effective lines of record to calculate the directional change.
        JW_indicator = 'd'
        with open(outputfile, 'a') as output_file:
            print('PhaseB3: Not enough data for calculating the greatest direction change.', file = output_file)
            print('', file=output_file)
    elif (storm[1][4]==storm[2][4])&(storm[1][5]==storm[2][5]): # same geological info cannot afford the calculation.
        JW_indicator = 'd'
        with open(outputfile, 'a') as output_file:
            print('PhaseB3: Identical lat & lon for different records.', file = output_file)
            print('', file=output_file)
    else: # all calculatable storms.
        # print the greatest direction change.
        # print whether it is after a landfall, or there's no landfall for the storm
        JW_indicator = 'a'
        judgement = '         And there is no landfall in this storm.'
        for line in storm[:max_directional_change(degree(storm))[1]]:
            if ' HU' in line:
                JW_indicator = 'b'
                judgement = '         And it is after a landfall.'
                break
        for line in storm[max_directional_change(degree(storm))[1]:]:
            if ' HU' in line:
                JW_indicator = 'c'
                judgement = '         And it is not after a landfall.'
                break
        with open(outputfile, 'a') as output_file:
            print('PhaseB3: For', storm[0][0], ', the greatest directional change per unit time is',
                  max_directional_change(degree(storm))[0], 'degree per hour.', file=output_file)
            print(judgement, file=output_file)
            print('', file=output_file)

    indi=indi.append(JW_indicator)
    return(indi)


def Main(filestr:str):
    """
    This is the main program for this assignment.
    :param filestr: the file name for different filenames. eg: Main('hurdat2-1851-2016-041117.txt') # AL
    :return: no need to return, the output has been written in the target file.
    """

    # get ready for the output
    outputfile = 'solution_b_output.txt';
    with open(outputfile, 'w') as output_file:
        print('Assignment2 ', file=output_file)
        print('Hurricane databases for Atlantic and Pacific Ocean (HURDAT2)', file=output_file)
        print('Notice: the summary results for PhaseA2 and PhaseB3 are at the bottom of the document.', file=output_file)
        print('', file=output_file)


    # main loop for the structural reading. (line by line, and for each storm, analyze and then erase the variable)
    f = open(filestr, 'r')
    storm = []
    a = f.readline()
    storm.append(a.split(','))
    a = f.readline()
    #def read_storm(a,storm):
    #print(len(a.split(',')));

    # initialize some parameters.
    st_count = {}; # for PhaseA2
    hu_count = {}; # for PhaseA2
    beg = 1800  # Not satisfied. I did the manual input. In future use, the data can be early than 1800.
    # But in our case, no earlier than 1851
    fin = 2017  # Not satisfied. I did the manual input. In future use, the data can be later than 2017.
    # But in our case, no later than 2016
    for year in range(beg, fin + 1):
        st_count[year] = 0;
        hu_count[year] = 0;
    indi=[]

    while len(a.split())>0:
        while len(a.split(',')) >4:
            storm.append(a.split(','))
            a=f.readline()
            #print(a)
        else:
            #print(storm[1][4])
            """
            Insert other functions with the storm as the input. eg: function PhaseA1
            """
            PhaseA1(storm,'solution_b_output.txt')
            #PhaseA2(storm,st_count,hu_count,'solution_b_output.txt')
            PhaseA2(storm,st_count,hu_count,'solution_b_output.txt')
            PhaseB1(storm,'solution_b_output.txt')
            PhaseB2(storm,'solution_b_output.txt')
            PhaseB3(storm,'solution_b_output.txt',indi)

            storm = []
            storm.append(a.split(','))
            a = f.readline()
    else:
        ## print function()
        with open(outputfile, 'a') as output_file:
            print('PhaseA2 result: summary of storms and hurricanes in each year.', file=output_file)
            print('storm summary (those years without storms are omitted.)', file=output_file)
            st_count = {k: v for k, v in st_count.items() if v}
            print(st_count, file=output_file)
            print('hurricane summary  (those years without storms are omitted.)', file=output_file)
            hu_count = {k: v for k, v in hu_count.items() if v}
            print(hu_count, file=output_file)
            print('PhaseB3: hypothesis testing on theorem by JW.', file=output_file)
            print('Among all the records in the dataset, there are', indi.count('a')+indi.count('d'), 'storms that have'
            ' either no land falls or not enough data for calculating greatest directional change. And for those storms'
            ' that fulfill both requirements, there are', indi.count('b'),'storms have a landfall before its greatest'
            ' directional change, and', indi.count('c'),  'storms do not have a landfall before its greatest directional change.'
            ' Therefore, for this dataset,', format(indi.count('b')/(indi.count('b')+indi.count('c')),'.2%'),'data go for JW hypothesis.', file=output_file)
        print('well done')

Main('hurdat2-1851-2016-041117-SHORT.txt')  # Shortened sample from Atlantic data file
#Main('hurdat2-1851-2016-041117.txt')       # Atlantic storms
#Main('hurdat2-nepac-1949-2016-041317.txt') # Eastern Pacific storms
