import requests
import re


class ArtistRecommendation:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://api.spotify.com/v1'
        self.access_token = self.get_access_token()

    def get_access_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        response = requests.post(token_url, {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        })
        if response.status_code != 200:
            raise Exception('Could not authenticate with Spotify')
        return response.json().get('access_token')

    def autocomplete(self, artist_name):
        search_url = f'{self.base_url}/search'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'q': artist_name, 'type': 'artist', 'limit': 10}
        response = requests.get(search_url, headers=headers, params=params)
        search_results = response.json()

        artists_list = []
        if search_results['artists']['items']:
            for artist in search_results['artists']['items']:
                artists_list.append(artist['name'])
        return artists_list

    def recommend(self, artist_name):
        search_url = f'{self.base_url}/search'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'q': artist_name, 'type': 'artist', 'limit': 1}
        response = requests.get(search_url, headers=headers, params=params)
        search_results = response.json()

        artist_id = search_results['artists']['items'][0]['id']
        related_url = f'{self.base_url}/artists/{artist_id}/related-artists'
        response = requests.get(related_url, headers=headers)
        related_artists = response.json()

        related_artist_names = [artist['name']
                                for artist in related_artists['artists']]
        genres = [artist['genres'][0] for artist in related_artists['artists']]
        images = [artist['images'][0]['url']
                  for artist in related_artists['artists']]
        spotify_profiles = [artist['external_urls']['spotify']
                            for artist in related_artists['artists']]
        return related_artist_names, genres, images, spotify_profiles

    @staticmethod
    def to_sentence_case(text):
        pattern = re.compile(r'(?<!\w)([a-zA-Z])')

        def capitalize(match):
            return match.group().upper()
        lower_case_text = text.lower()
        sentence_case_text = pattern.sub(capitalize, lower_case_text)
        return sentence_case_text
