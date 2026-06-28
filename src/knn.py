import math

def euclidian_distance(a, b):
    total = 0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    return math.sqrt(total)

def bubble_sort(distances_list):
    temp = 0
    for j in range(len(distances_list)):
        for i in range(len(distances_list) - 1 - j):
            if distances_list[i][0] > distances_list[i+1][0]:
                temp = distances_list[i]
                distances_list[i] = distances_list[i+1]
                distances_list[i+1] = temp
    return distances_list

def knn_predict(train_features, train_labels, test_features, K=5):
    predictions = []

    for test_data in test_features:
        distances_list = []
        for i in range(len(train_features)):
            distance = euclidian_distance(test_data, train_features[i])
            distances_list.append((distance, train_labels[i]))

        sorted_distance = bubble_sort(distances_list)

        k_nearest = sorted_distance[:K]

        upvote = 0
        downvote = 0
        for i in range(K):
            if k_nearest[i][1] == 1:
                upvote += 1
            else:
                downvote += 1
        if upvote > downvote:
            predict = 1
        else:
            predict = 0

        predictions.append(predict)

    return predictions
