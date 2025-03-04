from services.abstractService import AbstractService, POST, GET
import streamlit as st
MODELS_DOMAIN = "/models"

class ModelsService(AbstractService):
    
    def __init__(self):
        super().__init__(MODELS_DOMAIN)

    def model_change(self, name, version):
        return self.request(POST, "/change", params = {"name": name, "version": version}, files={})
    
    def search_all(self):
        return self.request(GET, "/search/all")
    
    def get_current(self):
        return self.request(GET, "/current")
    
modelsService = ModelsService()
