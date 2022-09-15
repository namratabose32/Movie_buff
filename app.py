from flask import Flask,render_template,request
import pickle
import pandas as pd
import os,smtplib


# def get_poster(movie_id):
#     request.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
#     data=response.json()
#     return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)

imageFolder = os.path.join('static','images')
app.config['UPLOAD_FOLDER']=imageFolder

@app.route('/')

def index():
    return render_template('main.html')

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_movies', methods = ['post'])
def recommend():
    user_input = request.form.get('user_input')
    movie_index = movies[movies['title'] == user_input].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies= []
    # recommended_movies_posters=[]
    for i in movies_list:
        movie_id = i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
        # get poster
        # recommended_movies_posters= get_poster(movie_id)
    return render_template('recommend.html',data=recommended_movies)
# def recommend():
#     user_input = request.form.get('user_input')
#     index = np.where(pt.index == user_input)[0][0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
#
#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
#
#         data.append(item)
#     print(data)
#     return render_template('recommend.html',data=data)
#

#cosine similarity

@app.route('/contact')
def contact_ui():
    return render_template('contact.html')

@app.route('/contact_form', methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        error_statement = "ALL FORM FIELDS ARE REQUIRED...."
        return render_template("contact.html",error_statement=error_statement,name=name,email=email)

    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)