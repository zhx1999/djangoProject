#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import pymysql

if __name__ == "__main__":
    conn = pymysql.Connect(
        host='gz-cdb-d56gtnd7.sql.tencentcdb.com',
        port=58361,
        user='root',
        password='cmit2021',
        db='pymysql',
        charset='utf8'
    )
    cursor = conn.cursor()

    with open('./中国天气.txt','r',encoding='utf-8') as fp:
        allData = fp.readlines()
    for lineData in allData:
        data = lineData.split('\t')
        state = data[0]
        date = data[1]
        citysData = data[2:]
        for city in citysData:
            city_item = city.split('\t')[0]
            if city_item != '\n':
                item_list = city_item.split('-')
                city_name = item_list[0]
                city_msg = item_list[1]
                city_msg = city_msg.replace('\'','\"')

                city_msg_obj = json.loads(city_msg)

                min_temp = city_msg_obj['min_temp']
                max_temp = city_msg_obj['max_temp']
                weather = city_msg_obj['cloud']
                wind = city_msg_obj['wind']
                sql = "insert into dbzq_weatherdata(state,city,dt,min_temp,max_temp,weather,wind)values('%s','%s','%s','%s','%s','%s','%s')"%(state,city_name,date,min_temp,max_temp,weather,wind)
                cursor.execute(sql)
                conn.commit()
                print('正在写入一条数据......')
    cursor.close()
    conn.close()

