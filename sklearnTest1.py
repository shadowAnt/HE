train_data = [[160, 60, 1], [155, 80, 1], [178, 53, 2], [158, 53, 2], [166, 45, 2], [170, 50, 2], [156, 56, 2],
              [166, 50, 1], [175, 55, 1], [188, 68, 1], [159, 41, 2], [166, 70, 1], [175, 85, 1], [188, 98, 1],
              [159, 61, 2]]
train_target = [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]
test_data = [[166, 45, 2], [172, 52, 1], [156, 60, 1], [150, 70, 2]]
test_target = [0, 0, 1, 1]
# from sklearn.linear_model import LogisticRegression
#
# clf = LogisticRegression().fit(train_data, train_target)
# result = clf.predict_proba(test_data)
# print(result)
# # [[ 0.95138903  0.04861097]
# #  [ 0.85670921  0.14329079]
# #  [ 0.18763392  0.81236608]
# #  [ 0.01270012  0.98729988]]

from sklearn import svm

clf = svm.SVC()
clf.fit(train_data, train_target)
print(clf)
result = clf.predict(test_data)
print(type(result))
  # <type 'numpy.ndarray'>转成list 用 result.tolist()
print(result)
# [0 1 1 1]


if __name__ == "__main__":
    print(111111111)