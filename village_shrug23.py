import pandas as pd
import itertools
import re
import math
import json
import nltk
import numpy

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

def isvalid(s):
    for char in s:
        if char.isnumeric() or char == "/":
            return False
    return True

def convert_alpha(s):
    ret = ""
    for char in s:
        if char.isascii():
            ret = ret + char
    return ret

def isvillage(elems):
    if "gaon " == elems[0][:5].lower() or "vill" == elems[0][:4].lower() or "vil" == elems[0][:3].lower() or "village" == elems[0][:7].lower() or "vila " == elems[0][:5].lower() or "vilage" == elems[0][:6].lower() or "will " == elems[0][:5].lower() or "vilalge" == elems[0][:7].lower():
        return True
    return False

def isvillage2(s, vill, dict, district):
    
    s = s.lower()
    vill = vill.lower()
    district = district.lower().replace(" ", "")
    if not isvalid(s):
        return False
    

    violate = ["atm ", "block", "ps", "police", "road", "near", "office", "post", " cia ", "shop", "bank", "staff", "cell", "market", "hospital",
    "distt", "district", "judge", "court", "station", "behind", "hospital", "department"]
    for v in violate:
        if v in s:
            return False

    if vill == "amb":
        return False

    if vill == "bwn":
        return False
    
    if vill == "ktl":
        return False
    
    if vill == "kkr":
        return False

    if len(vill) == 0:
        return False
    
    vill_list = []
    if district in dict or district =="nuh":
        blocks = []
        if district != "nuh":
            blocks = dict[district]
        for b in blocks:
            for v in blocks[b]:
                vill_list.append(v[0])
        
        if district == "nuh":
            blocks = dict["mewat"]
            for b in blocks:
                for v in blocks[b]:
                    vill_list.append(v[0])
        if district == "mewat":
            blocks = dict["nuh"]
            for b in blocks:
                for v in blocks[b]:
                    vill_list.append(v[0])
        if district == "gurugram":
            blocks = dict["gurgaon"]
            for b in blocks:
                for v in blocks[b]:
                    vill_list.append(v[0])
        for vil in vill_list:            
            dis = lev_dis(vil, vill)
            percent_diff = float(dis)/float(len(vill))
            if percent_diff < .4:
                return True

    return False



def double(s): #if a letter appears twice in a row
    prev = ""
    for enum, char in enumerate(s):
        if enum > 0:
            prev = s[enum-1]
            if char == prev:
                return True
    return False


def separate_dis(district, vill, dict, s):
    tmp = vill.lower().strip()
    vill = tmp.split(s)[0]
    district_tmp = tmp.split(s)[-1] 
    if district_tmp in dict:
        return district_tmp
    else:
        return district

def extract_village(vill):
    #ret = ""
    if "village" in vill:
        vill = vill.split("village")[1].strip()
    if "vill" in vill:
        vill = vill.split("vill")[1].strip()
    if "vilage" in vill:
        vill = vill.split("vilage")[1].strip()
    
    if "vilalge" in vill:
        vill = vill.split("vilalge")[1].strip()
    if vill[0:5] == "will ":
        vill = vill[5:]
    if vill[0:5] == "gaon ":
        vill = vill[5:]
    return vill
    
    

def four_elem(elems, perm, dict, f, id):
    country = elems[-1]
    state = elems[-2]
    district = elems[-3].replace(" ", "")
    vill = elems[0]
    if vill[0:3] == "pp ":
        vill = vill[3:]
    if state == "haryana":
        if isvillage(elems):
            #print("isvillage")
            vill = vill.lower()
            vill = vill.replace("blb", "").replace("fbd", "").replace("flb", "").replace("fdb", "")
            vill = extract_village(vill)
            if isvillage2(perm, vill, dict, district):            
                if len(vill) > 0:
                    if " ps " in vill:
                        vill = vill.split("ps")[0].strip()
                    if " police station " in vill:
                        vill = vill.split("police station")[0].strip()
                    if "distt" in vill.lower():
                        tmp = vill.lower().strip()
                        vill = tmp.split("distt")[0]
                        district_tmp = tmp.split("distt")[-1] 
                        if district_tmp in dict:
                            district = district_tmp
                    if "disst" in vill.lower():
                            tmp = vill.lower().strip()
                            vill = tmp.split("disst")[0]
                            district_tmp = tmp.split("disst")[-1] 
                            if district_tmp in dict:
                                district = district_tmp
                    if "district" in vill.lower():
                        tmp = vill.lower().strip()
                        vill = tmp.split("district")[0]
                        district_tmp = tmp.split("district")[-1] 
                        if district_tmp in dict:
                            district = district_tmp
                
                    if " teh " in vill:
                        vill = vill.split(" teh ")[0]
                    
                    min = 100
                    min_str = ""
                    haryana_id = "" #id of village name
                    for dis in dict:
                        for block in dict[dis]:
                            for vil in sorted(dict[dis][block]):
                                if district.lower().replace(" ", "") == dis.replace(" ", ""): #restrict to the correct district
                                    vill_lst = vil[2]
                                    tmp = vil[1] #dummy variable for village id
                                    
                                    vil = vil[0]
                                    
                                    for v in vill_lst:
                                        if v == vill:
                                            min = 0
                                            haryana_id = tmp
                                            min_str = vil + "," + block + "," + dis
                                    vill_dis = lev_dis(vil.replace(" ", ""), vill.replace(" ", ""))
                                    if vill_dis < min:
                                        haryana_id = tmp
                                        min_str = vil + "," + block + "," + dis
                                    
                                if district.lower() == "gurugram" or district.lower() == "nuh" or district.lower() == "hansi":
                                    potential = []
                                    if district.lower() == "gurugram":
                                        potential = ["gurgaon", "gurugram"]#list of potential districts
                                    if district.lower() == "nuh":
                                        potential = ["mewat", "nuh"]
                                    if district.lower() == "hansi":
                                        potential == ["hisar"]
                                    if dis in potential:
                                        vill_lst = vil[2]
                                        tmp = vil[1] #dummy variable for village id
                                        vil = vil[0]
                                        #vill_dis = nltk.edit_distance(vil.strip().split(" ")[0], vill.strip().split(" ")[0])
                                        vill_dis = lev_dis(vil.strip().split(" ")[0], vill.strip().split(" ")[0])
                                        if " " in vill and "" not in vil:
                                            vill_dis = vill_dis - 1
                                        if double(vill) and not double(vil):
                                            vill_dis = vill_dis - 1
                                        for v in vill_lst:
                                            if v == vill:
                                                min = 0
                                                haryana_id = tmp
                                                min_str = vil + "," + block + "," + district
                                            #vill_dis = nltk.edit_distance(vil.replace(" ", ""), vill.replace(" ", ""))

                                        vill_dis = lev_dis(vil.replace(" ", ""), vill.replace(" ", ""))
                                        if vill_dis < min:
                                            haryana_id = tmp
                                            min_str = vil + "," + block + "," + dis
                                        
                                    
                                    
                    #print(min_str, "  ", min)
                    #print(use)
                    if min != 100:   

                        write = str(id) + "," + str(perm.replace(",", "|")) + "," + str(haryana_id) + "," +  str(min_str.replace(",", "|")) + "\n"
                        f.write(write)


            data = pd.read_csv("haryana_vill_town_coordinates.csv")

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

place = data_haryana["village_name"]
blocks = data_haryana["subdistrict"]
districts = data_haryana["district"]
state_name = data_haryana["StateNameInEnglish"]
ids = data_haryana["haryana_id"]


new_vill = []
for enum, vil in enumerate(place):
    #sep = vil.split("(")
    #item = sep[0].strip()
    #item = item.split("-")[0].strip().lower()
    item = vil.lower()
    new_vill.append(item)


dict = {}
for enum, vil in enumerate(new_vill):
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
            dict[dis][block].append((vil, id, vill_lst))
        else:
            elem = [(vil, id, vill_lst)]
            dict[dis][block] = elem
    else:
        elem = {block: [(vil, id, vill_lst)]}
        dict[dis] = elem


#df1 = pd.read_csv("HARYANA_FIR_EI.csv")
#pres_addresses = df1["english_address_1"]
#perm_addresses = df1["english_address_2"]
df1 = pd.read_csv("FIR_ArcGIS_permanent_withGP.csv")
pres_addresses = df1["present_address_clean"]
perm_addresses = df1["permanent_address_clean"]
fir_id = df1["fir_id"]
f = open("pres_shrug_test.csv", "w", encoding = "utf-8")

#nuh is mewat, gurgaon is gurugram
for enum, x in enumerate(pres_addresses):
    perm = x
    
    #perm = perm.lower().split("[")[-1]
# exclude "Block" "ps " "police" "cia" "near", "house", "pp", "khedi" exclude anything with numbers, not alphabetical
#exclude anything with the word "road", "near", "office", "post", "CIA", "nagar" in the first elem, shop, first elem has two words
    #print(enum)
    #89208
    #89828
    id = fir_id[enum]
    if type(perm) == str:
        if perm != "":
            perm = convert_alpha(perm) 
            perm = perm.lower()
            if perm[0] != ",":
                elems = perm.split(",")
                if len(elems) > 4:
                    
                    country = elems[-1]
                    state = elems[-2]
                    district = elems[-3]
                    vill = elems[0]
                    if vill[0:3] == "pp ":
                        vill = vill[3:]
                    if vill[0:3] == "ps ":
                        vill = vill[3:]
                    if isvillage(elems):
                        print("true")
                        
                        blocks = perm.split(vill)[1].split(district + ",haryana")[0].lower()
                        blocks = blocks[1:-1].strip()
                        blocks = blocks.split(",")
                        blocks.append("")                
                        penalty = 2
                        if len(blocks) == 1:
                            penalty = 0
                        if state == "haryana":
                            vill = vill.lower()
                            vill = vill.replace("blb", "").replace("fbd", "").replace("flb", "").replace("fdb", "")
                            vill = extract_village(vill)
                            if isvillage2(perm, vill, dict, district):
                                print("ok")
                                if len(vill) > 0:
                                    if " ps " in vill:
                                        vill = vill.split("ps")[0].strip()
                                    if " police station " in vill:
                                        vill = vill.split("police station")[0].strip()
                                    if "distt" in vill.lower():
                                        tmp = vill.lower().strip()
                                        vill = tmp.split("distt")[0]
                                        district_tmp = tmp.split("distt")[-1] 
                                        if district_tmp in dict:
                                            district = district_tmp
                                    if "disst" in vill.lower():
                                        tmp = vill.lower().strip()
                                        vill = tmp.split("disst")[0]
                                        district_tmp = tmp.split("disst")[-1] 
                                        if district_tmp in dict:
                                            district = district_tmp
                                    if "district" in vill.lower():
                                        tmp = vill.lower().strip()
                                        vill = tmp.split("district")[0]
                                        district_tmp = tmp.split("district")[-1] 
                                        if district_tmp in dict:
                                            district = district_tmp
                                    
                                    if " teh " in vill:
                                        vill = vill.split(" teh ")[0]
                                    
                                    print(vill)
                                    min = 100
                                    min_str = ""
                                    use = ""
                                    haryana_id = "" #id of village name
                                    
                                    for dis in dict:
                                        for block in dict[dis]:
                                            for vil in sorted(dict[dis][block]):
                                                if district.lower().replace(" ", "") == dis.replace(" ", ""): #restrict to the correct district
                                                    vill_lst = vil[2]
                                                    #print(vill_lst, "is village")
                                                    tmp = vil[1] #dummy variable for village id
                                                    vil = vil[0]
                                                    
                                                    
                                                    for v in vill_lst:
                                                        if v == vill:
                                                            if block in blocks:
                                                                min = 2
                                                            else:
                                                                min = 0
                                                            haryana_id = tmp
                                                            min_str = vil + "," + block + "," + dis  
                                                    vill_dis = lev_dis(vil.replace(" ", ""), vill.replace(" ", ""))
                                                    if " " in vill and "" not in vil:
                                                        vill_dis = vill_dis - 1
                                                    if double(vill) and not double(vil):
                                                        vill_dis = vill_dis - 1
                                                    if vill_dis < 4:
                                                        if len(vill.strip()) > 0 and len(vil.strip()) > 0:
                                                            if vill.strip().lower()[0] == vil.strip()[0]:
                                                                for b in blocks:
                                                                    b = b.lower()
                                                                    if "sadar" in b:
                                                                        b= b.replace("sadar", "")
                                                                    if "city" in b:
                                                                        b = b.replace("city", "")
                                                                    b = b.strip()
                                                                    distance =100
                                                                    if len(b) == 0:
                                                                        s1 = vil 
                                                                        s2 = vill.lower().strip()
                                                                        #distance = nltk.edit_distance(s1, s2) + penalty
                                                                        distance = lev_dis(s1, s2) + penalty
                                                                        if " " in vill and "" not in vil:
                                                                            distance = distance - 1
                                                                        
                                                                    else:
                                                                        s1 = vil + "," + block #we are trying to match with this string
                                                                        s2 = vill.lower().strip() +"," + b 
                                                                        #distance = nltk.edit_distance(s1, s2)
                                                                        distance = lev_dis(s1, s2)
                                                                        if " " in vill and "" not in vil:
                                                                            distance = distance - 1
                                                                    

                                                                        
                                                                        
                                                                        
                                                                    if distance < min:
                                                                        min = distance
                                                                        min_str = vil + "," + block + "," + dis
                                                                        use = s2
                                                                        haryana_id = tmp
                                                if district.lower() == "gurugram" or district.lower() == "nuh" or district.lower() == "hansi":
                                                    potential = []
                                                    if district.lower() == "gurugram":
                                                        potential = ["gurgaon", "gurugram"]#list of potential districts
                                                    if district.lower() == "nuh":
                                                        potential = ["mewat", "nuh"]
                                                    if district.lower() == "hansi":
                                                        potential == ["hisar"]
                                                    if dis in potential:
                                                        vill_lst = vil[2]
                                                        tmp = vil[1] #dummy variable for village id
                                                        vil = vil[0]
                                                        for v in vill_lst:
                                                            if v == vill:
                                                                if block in blocks:
                                                                    min = 2
                                                                else:
                                                                    min = 0
                                                                haryana_id = tmp
                                                                min_str = vil + "," + block + "," + dis  
                                                                #vill_dis = nltk.edit_distance(vil.replace(" ", ""), vill.replace(" ", ""))
                                                        vill_dis = lev_dis(vil.strip().split(" ")[0], vill.strip().split(" ")[0])
                                                        if " " in vill and "" not in vil:
                                                            vill_dis = vill_dis - 1
                                                        if double(vill) and not double(vil):
                                                            vill_dis = vill_dis - 1
                                                        if vill_dis < 3:
                                                            if len(vill.strip()) > 0 and len(vil.strip()) > 0:
                                                                if vill.strip().lower()[0] == vil.strip()[0]:
                                                                    for b in blocks:
                                                                        b = b.lower()
                                                                        if "sadar" in b:
                                                                            b= b.replace("sadar", "")
                                                                        if "city" in b:
                                                                            b = b.replace("city", "")
                                                                        b = b.strip()
                                                                        distance =100
                                                                        if len(b) == 0:
                                                                            s1 = vil  + "," + dis
                                                                            s2 = vill.lower().strip() 
                                                                            #distance = nltk.edit_distance(s1, s2) + penalty
                                                                            distance = lev_dis(s1, s2) + penalty
                                                                            if " " in vill and "" not in vil:
                                                                                distance = distance - 1
                                                                            
                                                                        else:
                                                                            s1 = vil + "," + block + "," + dis #we are trying to match with this string
                                                                            s2 = vill.lower().strip() +"," + b 
                                                                            #distance = nltk.edit_distance(s1, s2)
                                                                            distance = lev_dis(s1, s2)
                                                                            if " " in vill and "" not in vil:
                                                                                distance = distance - 1
                                                                                
                                                                                
                                                                                
                                                                            if distance < min:
                                                                                min = distance
                                                                                min_str = vil + "," + block + "," + dis
                                                                                use = s2
                                                                                haryana_id = tmp
                                    print(min_str, "  ", min)
                                    print(use)
                                    if min != 100:   


                                        write = str(id) + "," + str(perm.replace(",", "|")) + "," + str(haryana_id) + "," +  str(min_str.replace(",", "|")) + "\n"
                                        f.write(write)
                    if len(elems) == 4:
                        four_elem(elems, perm, dict, f, id)
                
                    