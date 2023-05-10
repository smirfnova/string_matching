import pandas as pd
import itertools
import re
import math
import json
import nltk
import numpy
import enchant

def convert_alpha(s):
    ret = ""
    for char in s:
        if char.isascii():
            ret = ret + char
    return ret

def lev_dis(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1
                
                if t1 < len(token1):
                    if(token1[t1-1] == "a" and token2[t2-1] == "o" and token1[t1]=="u"):
                        distances[t1][t2] = distances[t1][t2] - 1
                    
                if(token1[t1-2]== "a" and token2[t2-1] =="o" and token1[t1-1] == "u"):
                    distances[t1][t2] = distances[t1][t2] - 1
                
                if t2 < len(token2):
                    if(token1[t1-1] == "o" and token2[t2-1] == "a" and token2[t2] == "u"):
                        distances[t1][t2] = distances[t1][t2] - 1
                if token1[t1-1] == "o" and token2[t2-2] == "a" and token2[t2-1] == "u":
                    distances[t1][t2] = distances[t1][t2] - 1
                
                if t1 < len(token1):
                    if(token1[t1-1] == "a" and token2[t2-1] == "e" and token1[t1]=="i"):
                        distances[t1][t2] = distances[t1][t2] - 1
                    
                if(token1[t1-2]== "a" and token2[t2-1] =="e" and token1[t1-1] == "i"):
                    distances[t1][t2] = distances[t1][t2] - 1
                
                if t2 < len(token2):
                    if(token1[t1-1] == "e" and token2[t2-1] == "a" and token2[t2] == "i"):
                        distances[t1][t2] = distances[t1][t2] - 1
                if token1[t1-1] == "e" and token2[t2-2] == "a" and token2[t2-1] == "i":
                    distances[t1][t2] = distances[t1][t2] - 1

    return distances[len(token1)][len(token2)]

def get_potential(rest, d):
    lst = []
    rest = rest.split()
    for enum, elem in enumerate(rest):
        if elem.isalpha():
            if not d.check(elem):
                lst.append(elem)
        if enum < len(rest) - 1:
            next_elem = rest[enum + 1]
            if elem.isalpha() and next_elem.isalpha():
                if not d.check(elem) and not d.check(next_elem):
                    lst.append(elem + " " + next_elem)
    return lst

def extract_village(vil_lst, dict, rest):
    potential_villages = []
    #for v in vil_lst:
    for dis in dict:
        for block in dict[dis]:
            for vil in sorted(dict[dis][block]):                
                if dis == district:
                    spelling_lst = vil[2]
                                        #print(vill_lst, "is village")
                    tmp = vil[1] #dummy variable for village id
                    vill = vil[0]
                    indicator = vil[3]
                    min_str = vill + "|" + block + "|"+ dis
                    for s in spelling_lst:
                        if s in vil_lst:
                            return (min_str, tmp, indicator)
                    if vill in vil_lst:
                        return (min_str, tmp, indicator)
                    for v in vil_lst:
                        if block in rest:
                            distance = lev_dis(vill, v)
                            percent_diff = float(distance)/float(len(vill))
                            if percent_diff < .2:
                                potential_villages.append((min_str, distance, tmp, indicator))
                        else:
                            distance = lev_dis(vill, v)
                            percent_diff = float(distance)/float(len(vill))
                            if percent_diff < .2:
                                potential_villages.append((min_str, distance+2, tmp, indicator))
    
    #now check for lev distance
    min = 100
    min_str = ""
    haryana_id = ""
    indicator = False
    haryana_name = ""
    gp_code = ""
    for vil in potential_villages:
        if vil[1] < min:
            min = vil[1]
            min_str = vil[0]
            haryana_id = vil[2]
            indicator = vil[3]

    return (min_str, haryana_id, indicator)


#data = pd.read_csv("haryana_vill_town_coordinates.csv")

alt_df = pd.read_csv("alt_spellings.csv")
alt_dis = alt_df["dis"]
alt_bl = alt_df["bl"]
alt_vil = alt_df["vil"]

alt_dict = {}
for enum, dis in enumerate(alt_dis):
    
    dis_lst = dis.split("|")
    for d in dis_lst:
        
        vil = alt_vil[enum]
        vil_lst = vil.split("|")
        if d != "":
            d = d.strip().lower().replace(" ", "")
            if d in alt_dict:
                elem = []
                for v in vil_lst:
                    v = v.lower().strip()
                    elem.append(v)
                alt_dict[d].append(elem)
            else:
                elem = []
                for v in vil_lst:
                    v = v.lower().strip()
                    elem.append(v)
                alt_dict[d] = [elem]
        



#data_haryana = data.loc[data['state_name'] == "haryana"]
#data_haryana.to_csv("data_haryana.csv")
data_haryana = pd.read_csv("haryana_vill_town_coordinates.csv")

place = data_haryana["village"]
blocks = data_haryana["subdistrict"]
districts = data_haryana["district"]
state_name = data_haryana["StateNameInEnglish"]
ids = data_haryana["haryana_id"]


new_vill = []
for enum, vil in enumerate(place):
    indicator = 0
    if "Rural" in vil:
        indicator = 1
    sep = vil.split("(")
    item = sep[0].strip()
    item = item.split("-")[0].strip().lower()
    #item = item.lower()
    new_vill.append((item, indicator))

dict = {}
for enum, x in enumerate(new_vill):
    vil = x[0]
    indicator = x[1] 
    dis = districts[enum].lower().replace(" ", "")
    block = blocks[enum].lower()


    id = ids[enum]
    pot_alt_vil = []
    if dis in alt_dict:
        pot_alt_vil = alt_dict[dis] #potential alternate village spellings

    vill_lst = []
    for v_lst in pot_alt_vil:
        for v in v_lst:
            if v.lower() == vil:
                vill_lst = vill_lst + v_lst
    if dis in dict:
        if block in dict[dis]:
            dict[dis][block].append((vil, id, vill_lst, indicator))
        else:
            elem = [(vil, id, vill_lst, indicator)]
            dict[dis][block] = elem
    else:
        elem = {block: [(vil, id, vill_lst, indicator)]}
        dict[dis] = elem

    

#print(json.dumps(dict, indent = 4))
#print(sorted(dict["rewari"]["rewari"]))
df2 = pd.read_csv("perm_shrug.csv", encoding='cp1252')
df3 = pd.read_csv("perm2_shrug.csv", encoding='cp1252')
fir_id2 = df2["haryana_id"]
fir_id3 = df3["haryana_id"]

df1 = pd.read_csv("FIR_ArcGIS_permanent_withGP.csv")
perm_addresses = df1["permanent_address_clean"]
pres_addresses = df1["present_address_clean"]
fir_id = df1["fir_id"]
#nuh is mewat, gurgaon is gurugram
f = open("perm3_shrug_test.csv", "w")
d = enchant.Dict("en_US")

for enum, perm in enumerate(perm_addresses):
    id = fir_id[enum]
    if id not in fir_id2.values.tolist() and id not in fir_id3.values.tolist():
        if type(perm) == str:
            if "gali" not in perm.lower():            
                elems = perm.split(",")
                if len(elems) > 3:
                    country = elems[-1]
                    state = elems[-2]
                    district = elems[-3].lower()
                    rest = ",".join(elems[:-3]).lower()#rest of the address
                    rest = rest.replace(",", " ")
                    rest = convert_alpha(rest)
                    
                    village_lst = get_potential(rest, d)
                    if district == "nuh":
                        district = "mewat"
                    vill = extract_village(village_lst, dict, rest)
                    min_str = vill[0]
                    haryana_id = vill[1]
                    indicator = vill[2]
                    if min_str != "":
                        min_elems = min_str.split("|")
                        print(perm, min_str)
                        perm = convert_alpha(perm)
                        
                        items = min_str.split("|")
                        vill_name = items[0]
                        block_name = items[1]
                        district_name = items[2]
                        if vill_name == district_name:
                            indicator = 3
                        write = str(id) + "," + str(perm.replace(",", "|")) + "," + str(haryana_id) + "," + str(min_str.replace(",", "|")) + "," + str(indicator) + "\n"
                        f.write(write)

                    
                    