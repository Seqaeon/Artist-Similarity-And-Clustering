from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

from artist_recommendation import ArtistRecommendation



client_id= os.getenv('CLIENT_ID') #REPLACE WITH YOUR CLIENT ID
client_secret=  os.getenv('CLIENT_SECRET') #REPLACE WITH YOUR CLIENT SECRET

print(client_id)

client = ArtistRecommendation(client_id, client_secret)
# Initialize Flask app
app = Flask(__name__)

# Load song data
artists = pd.read_csv('artists.csv', delimiter='\t')
top_20_artists = artists.nlargest(20, 'popularity')
top_20_artists['artist_type'] = top_20_artists['artist_type'].apply(
    client.to_sentence_case)
top_20_artists['main_genre'] = top_20_artists['main_genre'].apply(
    client.to_sentence_case)


# Route for home page
@app.route('/', methods=['GET'])
def homePage():
    # Select 5 random songs from the top 20 most popular
    random_artists = top_20_artists.sample(5).to_dict(orient='records')

    for artist in random_artists:
        artist['spotify_url'] = f"https://open.spotify.com/artist/{artist['artist_id']}"
    return render_template("index.html", artists=random_artists)



@app.route('/recommendation', methods=['GET'])
def recommendation():
    artist = request.args.get('artist')

    if not artist:
        return jsonify({'error': 'Artist Name required.'})

    try:
        artist_names, genres, images, spotify_profiles = client.recommend(
            artist_name=artist)

    except Exception as e:
        return jsonify({'error': f'Failed to fetch recommendation: {str(e)}. Kindly refresh.'})

    recommended = {
        'artist_names': artist_names,
        'genres': genres,
        'images': images,
        'spotify_profiles': spotify_profiles
    }
    # recommended = pd.DataFrame(recommended).to_dict(orient='records')
    return jsonify(recommended)


@app.route('/search_suggestions')
def search_suggestions():
    query = request.args.get('query', '')
    if len(query) >= 3:
        # Perform search and return suggestions (this is just an example)
        # autocomplete(query)  # Replace with actual search logic
        suggestions = client.autocomplete(query)
        return jsonify(suggestions)
    return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
