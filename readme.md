# 图像压缩&图像水印

项目获取之后，可直接进行部署操作: `s deploy`

部署完成，可以打开日志：`s ServerlessBookImageDemo logs -t`

触发上传图片的操作： `s SourceBucket deploy object --verbose`

即可在日志中看到预期结果：

```
FC Invoke Start RequestId: 5FA509AD224F963135BBC489
获取object
下载图片
image:  source.png
localFileName:  /tmp/D869D95CBBDADA47EE670B5ED2A06D39
图像压缩
数据回传
Url:  http://serverlessbook-image-target.oss-cn-beijing.aliyuncs.com/source.png
FC Invoke End RequestId: 5FA509AD224F963135BBC489

```

如果对代码修改，可以单独进行代码上传：

```
s ServerlessBookImageDemo deploy function --code
```

> 额外说明， 需要在`template.yaml`中填写自己的密钥信息，也可以将密钥信息放在环境变量，自动获取。