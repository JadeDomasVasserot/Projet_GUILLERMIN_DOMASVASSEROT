from services.abstractService import AbstractService, POST, GET

PREDICT_DOMAIN = "/models/predict"

class PredictService(AbstractService):
    
    def __init__(self):
        super().__init__(PREDICT_DOMAIN)

    def predict(self, buffer):
        return self.request(POST, "", files = {"data": buffer})
    
    def predict_best(self, buffer):
        return self.request(POST, "/best", files = {"data": buffer})
    
predictService = PredictService()
