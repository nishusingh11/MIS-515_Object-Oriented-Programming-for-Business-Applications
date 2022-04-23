"""
Assignment4_file1: Creating the tool that trains a decision model tree machine learning model to perform
the task of classifying crowdfunding posts. Dataset of crowdfunding post is taken from kiva.com, which
allows user to loan small amounts of money to small business ventures in developing countries.
Some posts meet their funding goals and receive the loans, whereas
others expire before doing so. The goal of your tool is to predict the success or failure of these
posts as accurately as possible.
The dataset contains data on 6,300 posts. Your decision tree model will make predictions based
on five factors:
• Length: the number of characters in the post.
• Number of pictures: the number pictures in the post.
• Loan amount: the amount of money requested by the post.
• Bonus credit eligibility: whether the post was eligible for any bonus or promotional
opportunity on Kiva.com (yes/no).
• User favorite post: whether the post received many page views on Kiva.com (yes/no).
Decision tree model will predict the loan status (funded/expired).
The dataset is available at https://dgoldberg.sdsu.edu/515/kiva_data_full.json.
"""

import json
import joblib
import matplotlib.pyplot as plt
import requests
import sklearn.metrics
import sklearn.model_selection
import sklearn.tree

# Below code is responsible for storing, preparing the input and output variable data, transforming
# the non-numeric data to numeric data and finally appending the data in x(Input variable) and y (Output variable).
response = requests.get("https://dgoldberg.sdsu.edu/515/kiva_data_full.json")

# Checking for connection
if response:
    data = json.loads(response.text)
    x, y = [], []

    for line in data:
        length = line['length']
        num_of_pic = line['number_of_pictures']
        loan_amount = line['loan_amount']

        if line['bonus_credit_eligibility'] == 'yes':
            eligibility = 1
        else:
            eligibility = 0
        if line['user_favorite_post'] == 'yes':
            post = 1
        else:
            post = 0
        loan_status = line['loan_status']
        if line['loan_status'] == 'funded':
            loan_status = 1
        else:
            loan_status = 0
        x.append([length, num_of_pic, loan_amount, eligibility, post])
        y.append(loan_status)

    # splitting the x & y data in train and test data
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, random_state=0)

    # Using decision tree classifier for modelling
    clf = sklearn.tree.DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)

    # Predicting the test data using above trained model and calculating the accuracy.
    predictions = clf.predict(x_test)
    accuracy = sklearn.metrics.accuracy_score(y_test, predictions)
    print("Accuracy:", accuracy)

    # Show a visual of decision tree, saving the image in the directory with "tree.png".
    sklearn.tree.plot_tree(clf, max_depth=3,
                           feature_names=["length", "num_of_pic", "loan_amount", "eligibility", "post"],
                           class_names=["funded", "expired"])
    plt.savefig("tree.png")

    # Show a visual of confusion matrix, saving the image in the directory with the name of "cm.png".
    cm = sklearn.metrics.confusion_matrix(y_test, predictions)
    disp = sklearn.metrics.ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.show()
    plt.savefig("cm.png")

    # Export decision tree model using joblib for further use.
    joblib.dump(clf, "kiva_decision_tree.joblib")

else:
    print("Connection Error")
