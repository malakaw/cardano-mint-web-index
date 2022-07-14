#-*- coding: utf-8 -*-

import os
import os.path
import json
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from_address = {"1_addr" : "addr_test1vrfkq33rrsczulhumfssfa4cqadwzp0clh85nyjvhl0eysglfdkvs",
                "2_addr" : "serverADDRESS_sssss_2" }

#查询出address最多的order数量
max_order_query_return = 20

template_json_order = {
    "from_address"    :  "",
    "to_address"      :  "",
    "has_paid"        :  False,
    "paid_ada_amount" :  0,
    "paid_date"       :  "",
    'nfts' : [
        {
            'name'     : '',
            'count'    : 1,
            'describe' : '',
            "nft_name" : "",
            "ipfs"     : ""
        }
    ],
    "create_date"      : "",
    "modify_date"      : ""

}



def get_current_month():
    today = datetime.datetime.today()
    return  "%d_%d" % (today.year, today.month)

def get_current_date():
    now = int(round(time.time()*1000))
    return time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(now/1000))
    
        

base_path = "/Users/franco/work/all_nft/python_service/order_jsons"

def  build_dir_if_not_exist(dir_str):
    if not os.path.exists(dir_str):
        print( "创建目录：" + dir_str)
        os.makedirs(dir_str)
        
def  build_order_json_file(path,data):
    #file_name 通过当前时间戳来创建,
    now = int(round(time.time()*1000))
    file_name = time.strftime('%Y_%m_%d_%H_%M_%S.json',time.localtime(now/1000))
    n_file_name = path + "/" + file_name
    with open( n_file_name, 'w') as outfile:
        outfile.write(data)
    print "write json file over"
    return  file_name   

def build_order(name,to_address,describe,ipfs,count,nft_name):
    d_path = base_path + "/" + get_current_month() + "/" + to_address + "/" + get_current_date()
    now = int(round(time.time()*1000))
    print "in build 1.1"
    
    build_dir_if_not_exist(d_path)
    temp_order = template_json_order
    temp_order["from_address"]            = from_address["1_addr"]
    temp_order["create_date"]             = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(now/1000))
    temp_order["nfts"][0]["name"]         = name
    temp_order["nfts"][0]["count"]        = count
    temp_order["nfts"][0]["describe"]     = describe
    temp_order["nfts"][0]["ipfs"]         = ipfs
    temp_order["nfts"][0]["nft_name"]     = nft_name
    
    json_string = json.dumps(temp_order)
    print(json.dumps(temp_order, indent=4, sort_keys=True))
    return build_order_json_file(d_path ,json_string)
 


def sort_month_dir_list(s2,s1):
    s1_list = s1.split("_")
    s2_list = s2.split("_")
    if s1_list[0] < s2_list[0] :
        return -1
    else:
        if s1_list[1] < s2_list[1]:
            return -1
        else:
            return 1
    return 0


def new_sort_json_file(s2,s1):
    ls1 = long("".join(s1.split("/")[-1:][0].split(".")[0].split("_"))[3:])
    ls2 = long("".join(s2.split("/")[-1:][0].split(".")[0].split("_"))[3:])
    #print("%s >%s :%s" %(ls1, ls2, (ls1 > ls2)))
    if ls1 < ls2:
        return -1
    else :
        return 1
    return 0

 

def count_files_under_some_dir (dir_):
    now = int(round(time.time()*1000))
    today_str = time.strftime('%Y-%m-%d',time.localtime(now/1000))
    
    g             = os.walk(dir_)
    all_count_f   = 0
    today_count_f = 0
    
    for path,dir_list,file_list in g:
        for file_name in file_list:  
            #print(os.path.join(path, file_name) )
            all_count_f += 1
            filemt= time.localtime(os.stat(os.path.join(path, file_name)).st_mtime)
            if today_str == time.strftime("%Y-%m-%d",filemt):
                today_count_f += 1
            print time.strftime("%Y-%m-%d",filemt)
            
    print ("all count files:%s" % all_count_f)        
    print ("today  count files:%s" % today_count_f)        
    print( "today:%s" % today_str   )


def new_query_order(to_address):
    this_addr_files = []
    list_jsons = []

    today_file_count = count_files_under_some_dir(base_path)

    #当日文件数量控制在100个，并且要有正确的address
    if len(to_address) >= 63 and today_file_count < 101:
         g = os.walk(base_path)  
         for path,dir_list,file_list in g:  
             for file_name in file_list:  
                 #print(os.path.join(path, file_name) )
                 if to_address in os.path.join(path, file_name) :
                     this_addr_files.append(os.path.join(path, file_name))
                     
                     
         s_json_list = sorted(this_addr_files , new_sort_json_file)[:max_order_query_return]
         
         for json_f in  s_json_list:
             #print json_f
             with open(json_f) as f:
                 list_jsons.append( json.load(f))

    return list_jsons
    


if __name__ == "__main__":
    #build_dir_if_not_exist("tom")
    #print get_current_month()
    input_param = {"name"       : "nft_name_1_test",
                   "to_address" : "add_xXXX",
                   "describe"   : "describe_2222",
                   "count"      :  5,
                   "ipfs"       :  "ACSDCASD",
                   "nft_name"   :  "nft_name_in"}

    #count_files_under_some_dir("/Users/franco/work/all_nft/python_service/order_jsons/2022_3")

    #build_order(input_param["name"],
    #            input_param["to_address"],
    #            input_param["describe"],
    #            input_param["ipfs"],
    #            input_param["count"],
    #            input_param["nft_name"]
#   #             input_param[],
#   #             input_param[]
    #)
    new_query_order("add_xXXX444")
    
