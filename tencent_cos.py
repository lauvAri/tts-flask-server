# 使用 pip 安装sdk：pip install -U cos-python-sdk-v5

# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import os
import logging
import time
import json

# # 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)

with open("config/tencent.json") as tencent_json_file:
    tencent = json.load(tencent_json_file)

secret_id = tencent["cos"]["secret_id"]
secret_key = tencent["cos"]["secret_key"]
region = 'ap-guangzhou'  # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
# COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
token = None  # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
client = CosS3Client(config)

#### 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
# 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
def putToTencentCOS(file):
    with open(file, 'rb') as fp:
        millisec_timestamp = int(time.time() * 1000)  # 获取毫秒级时间戳（整数）
        key = str(millisec_timestamp) + os.path.basename(file) 
        print("key is: " + key)

        try:
            response = client.put_object(
                Bucket='tts-1326430649',
                Body=fp,
                Key=key,
                EnableMD5=False
            )
            return {
                "status":"success",
                "key": key    
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }