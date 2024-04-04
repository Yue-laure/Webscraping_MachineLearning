import json

import pandas as pd
import requests
# Proxycurl API is a LinkedIn Profile Scraping API Use Cases:
#
# Building Data Driven Applications. (Lead Generation, Prospecting etc)
#
# Eg. Leveraging NLP like GPT-3 to Write Personalize Email , Message, LinkedIn Invitation based on their profile info like Occuption, Experince, Summary etc
#
# https://nubela.co/proxycurl/linkedin
#
# API Documentation : https://nubela.co/proxycurl/docs#people-api-person-profile-endpoint

df = pd.read_csv('./dataDownloadSelenium/cvUrlIT.csv')

with open('api_key.txt', 'r') as f:
    api_key = f.readline().strip()
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
headers = {'Authorization': 'Bearer ' + api_key}

response = {}
profile_data = {}
# Interroger chaque lien dans le CSV et appeler l'API pour obtenir les données de LinkedIn.
for index, row in df.iterrows():
    linkedin_profile_url = row['CVurl']  # Obtenir un lien vers la ligne en cours

    # Envoyer la demande
    response[index] = requests.get(api_endpoint,
                                   params={'url': linkedin_profile_url, 'skills': 'include'},
                                   headers=headers)

    # Réponse au traitement
    if response[index].status_code == 200:
        profile_data[index] = response[index].json()
        # print(profile_data[index])
        with open(f'./dataDownloadSelenium/cv_profiles_linkedin_{index}.json', 'w') as json_file:
            json.dump(profile_data[index], json_file)
    else:
        print(f"Failed to fetch data for {linkedin_profile_url}, status code: {response[index].status_code}")


