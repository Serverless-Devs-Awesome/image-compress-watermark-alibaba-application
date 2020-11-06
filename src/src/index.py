# -*- coding: utf-8 -*-

import os
import oss2
import json
from PIL import Image, ImageFont, ImageDraw

# 基本配置信息
AccessKey = {
    "id": os.environ.get('AccessKeyId'),
    "secret": os.environ.get('AccessKeySecret')
}

OSSSourceConf = {
    'endPoint': os.environ.get('OSSConfEndPoint'),
    'bucketName': os.environ.get('OSSConfBucketSourceName'),
    'objectSignUrlTimeOut': int(os.environ.get('OSSConfObjectSignUrlTimeOut'))
}

OSSTargetConf = {
    'endPoint': os.environ.get('OSSConfEndPoint'),
    'bucketName': os.environ.get('OSSConfBucketTargetName'),
    'objectSignUrlTimeOut': int(os.environ.get('OSSConfObjectSignUrlTimeOut'))
}

# 获取获取/上传文件到OSS的临时地址
auth = oss2.Auth(AccessKey['id'], AccessKey['secret'])
sourceBucket = oss2.Bucket(auth, OSSSourceConf['endPoint'], OSSSourceConf['bucketName'])
targetBucket = oss2.Bucket(auth, OSSTargetConf['endPoint'], OSSTargetConf['bucketName'])


# 图片水印
def watermarImage(image, watermarkStr):
    font = ImageFont.truetype("Brimborion.ttf", 40)
    drawImage = ImageDraw.Draw(image)
    height = []
    width = []
    for eveStr in watermarkStr:
        thisWidth, thisHeight = drawImage.textsize(eveStr, font)
        height.append(thisHeight)
        width.append(thisWidth)
    drawImage.text((image.size[0] - sum(width) - 10, image.size[1] - max(height) - 10),
                   watermarkStr, font=font,
                   fill=(255, 255, 255, 255))

    return image


# 图片压缩
def compressImage(image, width):
    height = image.size[1] / (image.size[0] / width)
    return image.resize((int(width), int(height)))


def handler(event, context):

    event = json.loads(event.decode("utf-8"))

    for eveEvent in event["events"]:
        # 获取object
        print("获取object")
        image = eveEvent["oss"]["object"]["key"]
        localFileName = "/tmp/" + event["events"][0]["oss"]["object"]["eTag"]
        localReadyName = localFileName + "-result.png"

        # 下载图片
        print("下载图片")
        print("image: ", image)
        print("localFileName: ", localFileName)
        sourceBucket.get_object_to_file(image, localFileName)

        # 图像压缩
        print("图像压缩")
        imageObj = Image.open(localFileName)
        imageObj = compressImage(imageObj, width=500)
        imageObj = watermarImage(imageObj, "Hello Serverless Devs")
        imageObj.save(localReadyName)

        # 数据回传
        print("数据回传")
        with open(localReadyName, 'rb') as fileobj:
            targetBucket.put_object(image, fileobj.read())
        print("Url: ", "http://" + OSSTargetConf['bucketName'] + "." + OSSTargetConf['endPoint'] + "/" + image)

    return 'oss trigger'
