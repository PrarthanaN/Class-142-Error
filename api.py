from storage import allMovies, likedMovies, disLikedMovies, didNotWatchedMovies
from flask import Flask, jsonify, request
from demographicFiltering import output
from contentBasedFiltering import recommendations

app = Flask(__name__)
@app.route("/get-movie")

def get_movie():
    return jsonify({ 
        "data": allMovies[0], 
        "status": "success" 
    })

@app.route("/liked-movie", methods = ["POST"])

def liked_movie():
    movie = allMovies[0]
    allMovies = allMovies[1:]
    likedMovies.append(movie)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/disLiked-movie", methods = ["POST"])

def disLiked_movie():
    movie = allMovies[0]
    allMovies = allMovies[1:]
    disLikedMovies.append(movie)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/didNotWatched-movie", methods = ["POST"])

def didNotWatched_movie():
    movie = allMovies[0]
    allMovies = allMovies[1:]
    didNotWatchedMovies.append(movie)
    return jsonify({
        "status": "success"
    }), 201
@app.route("/popular-movies") 
def popular_movies(): 
    movie_data = [] 
    for movie in output: 
        _d = { 
            "title_x": movie[0], 
            "poster_link": movie[1], 
            "release_date": movie[2] or "N/A", 
            "duration": movie[3], 
            "rating": movie[4], 
            "overview": movie[5] 
        } 
        movie_data.append(_d) 
    return jsonify({ 
        "data": movie_data, 
        "status": "success" 
    }), 200

@app.route("/recommended-movies")

def recommended_movies(): 
    all_recommended = [] 
    for liked_movie in likedMovies: 
        output = recommendations(liked_movie[19]) 
        for data in output: 
            all_recommended.append(data) 
    import itertools 
    all_recommended.sort() 
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended)) 
    movie_data = [] 
    for recommended in all_recommended: 
        _d = { 
            "title_x": recommended[0], 
            "poster_link": recommended[1], 
            "release_date": recommended[2] or 
            "N/A", "duration": recommended[3], 
            "rating": recommended[4], 
            "overview": recommended[5] 
        } 
        movie_data.append(_d) 
    return jsonify({ 
        "data": movie_data, 
        "status": "success" 
    }), 200

if __name__ == "__main__":
    app.run()