# This file was automatically generated by the C:/Users/Jakob Axelsson/Documents/Arbetsdokument/Eclipse workspace/COACH/COACH/build_coach_deployments.py script on <module 'datetime' from 'C:\\Users\\Jakob Axelsson\\AppData\\Local\\Programs\\Python\\Python36\\lib\\datetime.py'>.

import os
import sys

sys.path.append(os.path.join(os.curdir, os.pardir))

from COACH.framework import coach
from COACH.framework.DirectoryService import DirectoryService
from COACH.context_model import ContextModelService
from COACH.property_model import PropertyModelService
from COACH.knowledge_repository import KnowledgeRepositoryService
from COACH.decision_process.SimpleDecisionProcessService import SimpleDecisionProcessService
from COACH.decision_process.PughService import PughService
from COACH.estimation_method.AverageOfTwo import AverageOfTwo
from COACH.estimation_method.ExpertOpinion import ExpertOpinion
from COACH.framework.casedb import CaseDatabase
from COACH.framework.AuthenticationService import AuthenticationService
from COACH.framework.KnowledgeInferenceService import KnowledgeInferenceService
from COACH.estimation_method.expert_estimate_text import ExpertEstimateText
from COACH.estimation_method.expert_estimate_float import ExpertEstimateFloat
from COACH.estimation_method.expert_estimate_integer import ExpertEstimateInteger
from COACH.estimation_method.basic_cocomo import BasicCOCOMO
from COACH.estimation_method.intermediate_cocomo import IntermediateCOCOMO
from COACH.estimation_method.cost_estimation import CostEstimation
from COACH.framework.InteractionService import InteractionService

def run_all():
    # Start all the services
    
    DirectoryService().run()
    
    ContextModelService.ContextModelService().run()
    
    PropertyModelService.PropertyModelService().run()
    
    KnowledgeRepositoryService.KnowledgeRepositoryService().run()
    
    SimpleDecisionProcessService.SimpleDecisionProcessService().run()
    
    PughService.PughService().run()
    
    AverageOfTwo.AverageOfTwo().run()
    
    ExpertOpinion.ExpertOpinion().run()

    CaseDatabase().run()

    AuthenticationService().run()
    
    KnowledgeInferenceService().run()
    
    ExpertEstimateText.ExpertEstimateText().run()
    
    ExpertEstimateFloat.ExpertEstimateFloat().run()
    
    ExpertEstimateInteger.ExpertEstimateInteger().run()
    
    BasicCOCOMO.BasicCOCOMO().run()
    
    IntermediateCOCOMO.IntermediateCOCOMO().run()
    
    CostEstimation.CostEstimation().run()

    InteractionService().run()

if __name__ == '__main__':
    run_all()
