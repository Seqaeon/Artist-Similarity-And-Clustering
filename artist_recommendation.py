import requests
import re
import time


class ArtistRecommendation:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://api.spotify.com/v1'
        self.access_token = None
        self.token_expires = time.time() - 1

    def get_access_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        response = requests.post(token_url, {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        })

        if response.status_code != 200:
            raise Exception('Could not authenticate with Spotify')
        self.access_token = response.json().get('access_token')
        self.token_expires = time.time() + 1800

    def check_token(self):
        if time.time() >= self.token_expires:
            self.get_access_token()

    def autocomplete(self, artist_name):
        self.check_token()
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

    def norecs(self, artist_name):
        self.check_token()
        search_url = f'{self.base_url}/search'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'q': artist_name, 'type': 'artist', 'limit': 1}
        response = requests.get(search_url, headers=headers, params=params)
        search_results = response.json()
        artist_json = search_results['artists']['items']

        related_artist_names = [artist['name'] for artist in artist_json]

        genres = [artist['genres'][0] if artist['genres']
                  else "Not Available" for artist in artist_json]

        images = [artist['images'][0]['url'] if artist['images'] else "data:image/png;base64,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" for artist in artist_json]

        spotify_profiles = [artist['external_urls']['spotify']
                            if artist['external_urls'] else "Not Available" for artist in artist_json]

        return related_artist_names, genres, images, spotify_profiles

    def recommend(self, artist_name):
        self.check_token()
        search_url = f'{self.base_url}/search'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'q': artist_name, 'type': 'artist', 'limit': 1}
        response = requests.get(search_url, headers=headers, params=params)
        search_results = response.json()

        artist_id = search_results['artists']['items'][0]['id']
        related_url = f'{self.base_url}/artists/{artist_id}/related-artists'
        response = requests.get(related_url, headers=headers)
        related_artists = response.json()

        if len(related_artists['artists']) > 0:

            related_artist_names = [artist['name']
                                    for artist in related_artists['artists']]

            genres = [artist['genres'][0] if artist['genres']
                      else "Not Available" for artist in related_artists['artists']]

            images = [artist['images'][0]['url'] if artist['images'] else "data:image/png;base64,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" for artist in related_artists['artists']]

            spotify_profiles = [artist['external_urls']['spotify'] if artist['external_urls']
                                else "Not Available" for artist in related_artists['artists']]
        else:
            related_artist_names, genres, images, spotify_profiles = self.norecs(
                artist_name)

        return related_artist_names, genres, images, spotify_profiles

    @staticmethod
    def to_sentence_case(text):
        pattern = re.compile(r'(?<!\w)([a-zA-Z])')

        def capitalize(match):
            return match.group().upper()
        lower_case_text = text.lower()
        sentence_case_text = pattern.sub(capitalize, lower_case_text)
        return sentence_case_text
