# FakeRealNewsClassifier
This project will not be highly modularized, but rather proof-of-concept using each library in the same project.

### Tech stack:
* Language: **Python**
* Helper libraries: **pandas**

### Prerequisites
* Download Java 17 from: https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html

### Libraries:
* Dataset source: **Kaggle**
* Preprocessing: **ApacheSpark** (or maybe just use pandas instead?)
* Baseline testing: **scikit-learn**
* Model training: **TensorFlow**
* User input testing: **Flask**
* Deployment: **Docker**

### Identifying dimensions in the data:
* Article word count
* Article word letter count average
* Title
* Subject
* Body text
* Date (7-bit data based on day of week)

### Goals
* Neural nets trained for A) single-word sentiment association and B) stochastic chunk-wise word sequence sentiment association.
    Train/test these on the title, subject, and body text as needed,
* Regression model for article word count, article word letter count average, and date.
* A meta Bayesian network model for analyzing the aforementioned models' predictive strengths with respect to one another.  For example, posting on Saturdays might be less bad if word count is high, meaning that posting on Saturdays should only be treated as a significant negative factor if word count is high, and otherwise an insignificant factor.

Then determine predictive strength of all models and dimensions, use the Bayesian network to upscale or downscale their predictive strengths, and finally put them all together to maximize their collective predictive strengths.
