# -*- coding: utf-8 -*-
"""
Created on Sun May 30 07:32:27 2021

@author: Harivyas
"""

server={"large":1,"xlarge":2,"2xlarge":4,"4xlarge":8,"8xlarge":16,"10xlarge":32}
#print(server)

output_list=[]
def get_costs(hours, cpus, price):
    if(price == None):
        get_price(hours,cpus)
    if(cpus == None):
        get_cpus(hours,price)
def print_output(region,cost,servers):
    output={}
    output["region"]=region
    output["total_cost"] = '$'+str(cost)
    output["servers"]=servers[::-1]
    output_list.append(output)
#Alice would like to request for servers with minimum 135 CPUs for 24 hours.
def get_price(hours,cpus):
    instances={'us-east': {'large': 0.12,'xlarge': 0.23,'2xlarge': 0.45,'4xlarge': 0.774,'8xlarge': 1.4,'10xlarge': 2.82},
            'us-west': {'large': 0.14,'2xlarge': 0.413,'4xlarge': 0.89,'8xlarge': 1.3,'10xlarge': 2.97}}
    temp_cpu=cpus
    for region,servers in instances.items():
        cpus=temp_cpu
        total=0
        l1=list(server.keys())
        l2=list(server.values())
        server_list=[]
        for i in range(len(l1)-1,-1,-1):
            if(cpus<=0):
                break
            nos_cpus = (cpus//server[l1[i]])
            if(nos_cpus!=0):
                server_list.append((l1[i],nos_cpus))
            total+=(nos_cpus*l2[i])
            cpus%=server[l1[i]]
        
        print_output(region,total*hours,server_list)
#Bob would like to request as many possible servers for $38 for 10 hours.        
def get_cpus(hours,price):
    instances={'us-east': {'large': 0.12,'xlarge': 0.23,'2xlarge': 0.45,'4xlarge': 0.774,'8xlarge': 1.4,'10xlarge': 2.82},
            'us-west': {'large': 0.14,'2xlarge': 0.413,'4xlarge': 0.89,'8xlarge': 1.3,'10xlarge': 2.97}}
    for region,servers in instances.items():
        priceperhour=price/hours
        total=0
        l1=list(server.keys())
        l2=list(server.values())
        server_list=[]
        for i in range(len(l1)-1,-1,-1):
            if(priceperhour<=0):
                break
            final_price = (int)(priceperhour//l2[i])
            if(final_price!=0):
                server_list.append((l1[i],final_price))
            total+=(final_price*l2[i])
            priceperhour%=l2[i]
        
        print_output(region,total*hours,server_list)        

#Example1
#get_costs(24,135,None)
#Example2
#get_costs(10,None,38)

print(output_list)             
