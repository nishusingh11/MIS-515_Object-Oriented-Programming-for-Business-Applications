"""
Homework 5: In this assignment we are creating a tool that trains Decision tree, K nearest neighbors and neural network
machine learning models to perform the task of classifying online reviews.
"""

# Importing libraries

import joblib
import json
import math
import nltk
import requests
from sklearn import model_selection, metrics
from sklearn import tree, neighbors, neural_network
import textblob
import time
import warnings

warnings.filterwarnings("ignore")
nltk.download("punkt")

# Below code is responsible for loading data, preparing and transforming input and output data.
# Performing splitting and training 3 models
# Printing the accuracy scores
# Saving the best performing classifier (in this case it is "Neural Network") in file.

response = requests.get("https://dgoldberg.sdsu.edu/515/appliance_reviews.json")
if response:

    print("\nLoading data...")

    # Using time module to print time taken in execution process
    start_time = time.time()
    data = json.loads(response.text)
    end_time = time.time()
    time_elapsed = end_time - start_time
    print("Completed in", time_elapsed, "seconds.")

    print("\nIdentifying unique words...")
    start_time = time.time()

    # "review_text" will store all the reviews in string.
    # Using textblob module to store words in lower case.
    review_text = ''

    for line in data:
        review_text += line['Review']
        
    blob = textblob.TextBlob(review_text)
    words = blob.words.lower()

    # Using set() and list(), to store unique words in list.
    unique_words = list(set(words))
    end_time = time.time()
    time_elapsed = end_time - start_time
    print("Completed in", time_elapsed, "seconds.")

    print("\nGenerating relevance scores...")
    start_time = time.time()

    # calculating the relevance score using given formula and storing a pair of word, score in dictionary.
    rel_score = {}
    for word in unique_words:
        # if word == "dangerous":
        score = 0
        A, B, C, D = 0, 0, 0, 0
        for line in data:
            if word in line["Review"]:
                if line["Safety hazard"]:
                    A += 1
                else:
                    B += 1
            if word not in line["Review"]:
                if line["Safety hazard"]:
                    C += 1
                else:
                    D += 1

        # To handle zero division error exception using try-except
        try:
            val = (math.sqrt((A + B) * (C + D)))
            score = ((math.sqrt(A + B + C + D)) * ((A * D) - (C * B))) / val

        except ZeroDivisionError:
            score = 0

        # Filtering the score vy given threshold (4000)
        if score >= 4000:

            # adding word and score in dictionary
            rel_score[word] = score

    for key, val in rel_score.items():
        print(key,"\t",val)

    end_time = time.time()
    time_elapsed = end_time - start_time
    print("Completed in", time_elapsed, "seconds.")

    print("\nFormatting 2D list...")
    start_time = time.time()

    # Preparing input and output variable
    # Preparing 2D input and 1D output
    x, y = [], []

    for line in data:
        review = line["Review"]
        hazard = line["Safety hazard"]
        temp = []
        for word, score in rel_score.items():
            if word in review:
                temp.append(1)
            else:
                temp.append(0)
        x.append(temp)

        y.append(hazard)

    end_time = time.time()
    time_elapsed = end_time - start_time
    print("Completed in", time_elapsed, "seconds.")

    print("\nTraining machine learning models...")
    start_time = time.time()

    # Splitting the input and output data in train data set and test data set
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y)

    # Training Decision Tree Classifier and calculating the accuracy score
    clf_dt = tree.DecisionTreeClassifier()
    clf_dt = clf_dt.fit(x_train, y_train)
    prediction_dt = clf_dt.predict(x_test)
    accuracy_dt = metrics.accuracy_score(y_test, prediction_dt)

    # Training 7 Nearest Neighbor Classifier and calculating the accuracy score
    clf_knn = neighbors.KNeighborsClassifier(7)
    clf_knn = clf_knn.fit(x_train, y_train)
    prediction_knn = clf_knn.predict(x_test)
    accuracy_knn = metrics.accuracy_score(y_test, prediction_knn)

    # Training Multi Layer perceptron Classifier and calculating the accuracy score
    clf_nn = neural_network.MLPClassifier()
    clf_nn = clf_nn.fit(x_train, y_train)
    prediction_nn = clf_nn.predict(x_test)
    accuracy_nn = metrics.accuracy_score(y_test, prediction_nn)

    end_time = time.time()
    time_elapsed = end_time - start_time
    print("Completed in", time_elapsed, "seconds.\n")

    # Printing the accuracy score of Decision Tree, KNN and Neural Network.
    print(accuracy_dt)
    print(accuracy_knn)
    print(accuracy_nn)

    # Saving the trained MLP classifier in file for future use.
    joblib.dump(clf_nn, "neural_classifier.joblib")

else:
    print("Connection Error")

print("\n\nThank you for using Online Review Classification tool..")
