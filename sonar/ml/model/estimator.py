from sonar.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os
class TargetValueMapping:
    def __init__(self):
        self.R: int = 0
        self.M: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))