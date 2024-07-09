from flask import Flask, request, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load the data and the cosine similarity matrix
books_combined = pd.read_csv('combined_books.csv')
with open('cosine_sim.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

# Function to get book recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = books_combined[books_combined['Title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    book_indices = [i[0] for i in sim_scores]
    return books_combined['Title'].iloc[book_indices]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form['title']
    recommendations = get_recommendations(title)
    return render_template('recommend.html', title=title, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
