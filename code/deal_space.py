f1=open("/分词/基于CRF的事件要素提取/特征提取/train.data", "r", encoding="utf-8")
f2=open("/分词/基于CRF的事件要素提取/特征提取/train1.data", 'w', encoding="utf-8")
try:
    for line in f1.readlines():
        if line.split():
            f2.write(line)
finally:
    f1.close()
    f2.close()


