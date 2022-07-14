#-*- coding: utf-8 -*-

from flask import Flask, request, Response
from flask_cors import CORS
import json
import order as orderOper
import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    print(request.data)	
    return 'Hello, World!'

@app.route('/add', methods=['POST','GET'])
def add():
    result = {'title': "return from falsk" , "body": "bbbb"}
    print "in..."
    return Response(json.dumps(result),  mimetype='application/json')


@app.route('/queryOrder', methods=['GET'])
def queryOrder():
    result = orderOper.new_query_order(request.args.get("address"))
    addr = request.args.get("address")
    print "in...%s " % addr
    #print result
    return Response(json.dumps(result),  mimetype='application/json')


nft_price_dict = {
    1: 2,
    2: 2,
    3: 7,
    5: 8,
    10: 10,
    100: 11
}


order_return_template = {"orderbuild_result": "ok",
                         "server_ada_address": "addr_test1vrfkq33rrsczulhumfssfa4cqadwzp0clh85nyjvhl0eysglfdkvs",
                         "send_ada_mount": 5}


@app.route('/addOrder', methods=['POST'])
def addOrder():
    #result = {'build_date': "" , "orderbuild_result": "fail"}
    real_order_return_template = order_return_template

    try:
       data = request.json
       #default
       input_param = {"name"       : "nft_name_1_test",
                      "to_address" : "add_xXXX",
                      "describe"   : "describe_2222",
                      "count"      :  5,
                      "ipfs"       :  "ACSDCASD",
                      "nft_name"   :  "nft_name_in"}
       
       input_param = data
       print data
       c_time = orderOper.build_order(input_param["name"],
                   input_param["to_address"],
                   input_param["describe"],
                   input_param["ipfs"],
                   input_param["count"],
                   input_param["nft_name"]
       )

       time.sleep(3)
       real_order_return_template["send_ada_mount"] = nft_price_dict.get(int(input_param["count"]))
    except Exception as e:
        real_order_return_template["orderbuild_result"]  = "fail"
        print (e)
    return Response(json.dumps(real_order_return_template),  mimetype='application/json')
    



if __name__ =="__main__":
    app.run(debug=True,port=8080,host="0.0.0.0")
    

 #创建订单，同步的，创建成功后才能返回ok;
 # 写入json文件
 # 格式
 ##目录定义规则：周/钱包名/订单日期.json

# curl  -i -X POST  http://localhost:8080/addOrder \
# -H "Content-Type: application/json" \
# -d '{"tom":"11"}'

 
