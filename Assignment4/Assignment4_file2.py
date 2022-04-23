""""
In this assignment file, we are using the already trained classification model to predict the output for
new input value.
"""

import joblib

# We are executing below code according to user's choice whether user wants to continue or not.
# taking input variable values from user for prediction.
choice = 'yes'
while choice == 'yes':
    file = input("Enter the name of the decision tree file to load:")
    length = int(input("Enter the length of the post to predict: "))
    num_of_pic = int(input("Enter the number of pictures in the post: "))
    loan_amount = int(input("Enter the loan amount requested: "))
    eligibility = input("Enter the bonus credit eligibility (yes/no)")
    if eligibility.lower() == 'yes':
        eligibility = 1
    else:
        eligibility = 0

    post = input("Enter whether the post was a user favorite post (yes/no):")
    if post.lower() == 'yes':
        post = 1
    else:
        post = 0

    # Storing in 2 D list.
    x_new = [[length, num_of_pic, loan_amount, eligibility, post]]

    # Using joblib module to load the classification model for further prediction.
    clf = joblib.load(file)

    # Predicting output according to new values and accordingly printing the result to user.
    predictions = clf.predict(x_new)
    if predictions == 0:
        print("\n\n Based on the decision tree, the loan will not be funded.")
    else:
        print("Based on the decision tree, the loan will be funded.")
    choice = input("\n\n Do you want to continue the prediction (yes/no)").lower()

print("\nThank you for using this prediction tool")
