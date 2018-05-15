#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import paho.mqtt.client as mqtt
import datetime
#使得系统支持汉字输入输出
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

trust = "/Users/mimin/Documents/EMQTT/root_cert.pem" #开启TLS时的认证文件目录
user = "gds/gdl_python"
pwd = "LWjf8IryApYTdDLSXgK71UUZJH2DEDPjYU32MAjWMQ4="
endpoint = "htgyy.mqtt.iot.gz.baidubce.com"
port = 1884
in_topic = "gdsp/dglp/#"#订阅的主题
out_topic = "gds/dgl/python"#发布的主题，这里做自身ID使用


# 连接后返回0为成功
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(in_topic,qos=0)  # qos订阅消息

#成功发布消息的操作
def on_publish(msgo,  rc):
    if rc == 0:
        print("发出主题："+ out_topic + "  内容： " + msgo)

#接收订阅的消息
def on_message(client, userdata, msg):
    print("收到主题: " + msg.topic + " 内容： " + str(msg.payload))#打印接收内容

    msgo = str(datetime.datetime.now())#加载消息内容
    rc, mid= client.publish(out_topic, msgo,qos=0)  #发布消息
    on_publish(msgo, rc)#验证发布消息


client = mqtt.Client(
    client_id="4b600f1d44cd4bd389e18e50df8c0cd5",
    protocol=mqtt.MQTTv311
)



client.tls_set(trust)  # 设置认证文
client.username_pw_set(user, pwd)  # 设置用户名，密码
client.on_connect = on_connect  # 连接后的操作
client.on_message = on_message  # 接受消息的操作
client.connect(endpoint, port, 60)  # 连接服务 keepalive=60
client.loop_forever()
