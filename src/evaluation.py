def accuracy(labels, predictions):
    correct = 0
    for i in range(len(labels)):
        if labels[i] == predictions[i]:
            correct += 1
    accuracy = correct / len(labels)
    return accuracy

def precision(labels, predictions):
    true_positive = 0
    false_positive = 0

    for i in range(len(labels)):
        if labels[i] == 1 and predictions[i] == 1:
            true_positive += 1
        elif labels[i] == 0 and predictions[i] == 1:
            false_positive += 1

    precision = true_positive / (true_positive + false_positive)
    return precision

def recall(labels, predictions):
    true_positive = 0
    false_negative = 0

    for i in range(len(labels)):
        if labels[i] == 1 and predictions[i] == 1:
            true_positive += 1
        elif labels[i] == 1 and predictions[i] == 0:
            false_negative += 1

    recall = true_positive / (true_positive + false_negative)
    return recall

def print_result(label, prediction):
    print("Hasil Uji KNN: ")
    accuracy_p = accuracy(label, prediction)
    precision_p = precision(label, prediction)
    recall_p = recall(label, prediction)
    print(f"Akurasi: {accuracy_p * 100:.2f}%")
    print(f"Precision: {precision_p * 100:.2f}%")
    print(f"Recall: {recall_p * 100:.2f}%")
