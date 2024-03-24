import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # Load data from CSV file
    with open:
        reader = csv.reader(filename)
        next(reader)
        for row in reader:
            evidence = []
            labels = []

            # Values
            Administrative = int(row[0])
            Administrative_Duration = float(row[1])
            Informational = int(row[2])
            Informational_Duration = float(row[3])
            ProductRelated = int(row[4])
            ProductRelated_Duration = float(row[5])
            BounceRates = float(row[6])
            ExitRates = float(row[7])
            PageValues = float(row[8])
            SpecialDay = float(row[9])
            Months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            Month = int(Months.index(row[10]))
            OperatingSystems = int(row[11])
            Browser = int(row[12])
            Region = int(row[13])
            TrafficType = int(row[14])
            VisitorType = 1 if row[15] == "Returning_Visitor" else 0
            Weekend = 1 if row[16] == "TRUE" else 0
            Revenue = 1 if row[17] == "TRUE" else 0

            # Append values to evidence
            evidence.append(
                Administrative, Administrative_Duration, Informational, Informational_Duration,
                ProductRelated, ProductRelated_Duration, BounceRates, ExitRates, PageValues,
                SpecialDay, Month, OperatingSystems, Browser, Region, TrafficType, VisitorType, Weekend)
            
            # Append values to labels
            labels.append(Revenue)
            
    return evidence, labels

    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # Create K-Nearest Neighbor model
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # Initialize variables
    sensitivity = 0
    specificity = 0

    # Calculate sensitivity
    true_positives = 0
    true_negatives = 0

    for label, prediction in zip(labels, predictions):
        if label == 1 and prediction == 1:
            true_positives += 1
        elif label == 0 and prediction == 0:
            true_negatives += 1
    
    sensitivity = true_positives / sum(labels)
    specificity = true_negatives / (len(labels) - sum(labels))

    return (sensitivity, specificity)

    raise NotImplementedError


if __name__ == "__main__":
    main()
