import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier



trainfile = 'E:\\流量特征csv\\train.csv'
testfile = 'E:\\流量特征csv\\test.csv'
# 读取csv文件
trainset = pd.read_csv(trainfile, engine='python')
testset = pd.read_csv(testfile, engine='python')

# 提取特征和标签
x_train = trainset.iloc[:, :-2].values
y_train = trainset.iloc[:, [-1]].values.ravel()

x_test = testset.iloc[:, :-2].values
y_test = testset.iloc[:, [-1]].values.ravel()

# 分类训练
classifier = RandomForestClassifier(n_estimators=25, criterion='entropy', max_depth=25, random_state=0)
classifier.fit(x_train, y_train)



# 预测

y_pred = classifier.predict(x_test)
print(np.mean(y_pred == y_test))

# 输出分类错误的
count = 0
for _i in range(len(y_pred)):
    if y_pred[_i] != y_test[_i]:
        count += 1
        print(_i+1)
print(count)




