"""
Example estimation method which captures expert opinion, i.e. it takes one parameter which is also the result of the estimation.
"""

# Set python import path to include COACH top directory
import os
import sys
sys.path.append(os.path.join(os.curdir, os.pardir, os.pardir, os.pardir))

import json

from flask import Response

from COACH.framework.coach import endpoint, EstimationMethodService


class ExpertOpinion(EstimationMethodService):
    """
    This is a simple example of an estimation method.
    It takes one parameter, and just returns it.
    """
    
    def parameter_names(self):
        return ["x"]
    
    
    @endpoint("/info", ["GET", "POST"])
    def info(self):
        return Response("This is an estimation method which takes one parameters (X), and returns it.")
    
    
    @endpoint("/evaluate", ["GET", "POST"])
    def evaluate(self, x):
        result = float(x)
        return Response(json.dumps(result))


if __name__ == '__main__':
    ExpertOpinion(sys.argv[1]).run()
