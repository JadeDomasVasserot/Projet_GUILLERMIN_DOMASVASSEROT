import requests
import streamlit as st
BASE_URL = "https://api-cloud-g4-0bc391d2f0c3.herokuapp.com"

POST = "POST"
GET = "GET"

class AbstractService:
    
    def __init__(self, domain):
        self.url = BASE_URL + domain
        
    def request(self, methods, route, params = {}, files= {}):
        try:
            response = AbstractService.call(methods, self.url + route, params=params, files=files)
            if response.status_code == 200:
                return response.json()
            else :
                st.json(response)
                raise Exception(response.status_code)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur : {e}")    
    
    def call(methods, route, params, files):
        if methods == POST:
            return requests.post(route, params=params, files=files)
        if methods == GET:
            return requests.get(route, params=params, files=files)
        else:
            raise  Exception("Methode non implementée.")