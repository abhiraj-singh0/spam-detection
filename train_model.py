import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle # The library used to save the model

print("Loading data and training model... please wait.")

data = pd.read_csv('spam.csv', encoding="latin1")
data.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
data.rename(columns={'v1': 'label', 'v2': 'message'}, inplace=True)
data.drop_duplicates(inplace=True)

data['label'] = data['label'].map({'ham': 'non-spam', 'spam': 'spam'})

mess = data['message']
label = data['label']

# 2. Split the data
(mess_train, mess_test, label_train, label_test) = train_test_split(mess, label, test_size=0.2)

# 3. Train the Vectorizer (converts text to numbers)
cv = CountVectorizer(stop_words='english')
features = cv.fit_transform(mess_train)

# 4. Train the Model
model = MultinomialNB()
model.fit(features, label_train)

# 5. SAVE THE TRAINED MODEL AND VECTORIZER
# 'wb' means "write binary" (saving the file to your hard drive)
pickle.dump(cv, open('vectorizer.pkl', 'wb'))
pickle.dump(model, open('spam_model.pkl', 'wb'))

with open('spam_model.pkl', 'wb') as model_file:
    pickle.dump(model , model_file)

with open('vectorizer.pkl', 'wb') as vocab_file:
    pickle.dump(cv, vocab_file)



print("Success! vectorizer.pkl and spam_model.pkl have been saved.")