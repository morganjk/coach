# This file was automatically generated by the C:\Users\Jakob Axelsson\Documents\Arbetsdokument\Eclipse workspace\COACH\COACH\build_coach_deployments.py script on <module 'datetime' from 'C:\\Python34\\lib\\datetime.py'>.

import os
import sys

sys.path.append(os.path.join(os.curdir, os.pardir))

from COACH.framework import coach
from COACH.framework.InteractionService import InteractionService
from COACH.estimation_method.AverageOfTwo import AverageOfTwo
from COACH.context_model import ContextModelService
from COACH.framework.DirectoryService import DirectoryService
from COACH.decision_process.SimpleDecisionProcessService import SimpleDecisionProcessService
from COACH.estimation_method.ExpertOpinion import ExpertOpinion
from COACH.decision_process.PughService import PughService
from COACH.framework.casedb import CaseDatabase
from COACH.knowledge_repository import KnowledgeRepositoryService
from COACH.framework.AuthenticationService import AuthenticationService

if __name__ == '__main__':
    try:
        # This will work if running script from command line (Windows or Linux)
        # For some reason, it does not work if starting from within Eclipse
        topdir = os.path.abspath(os.curdir)
        
        # Start root service and directory service from the framework module
        wdir = os.path.join(topdir, "framework")
        os.chdir(wdir)
    except:
        # Workaround for starting in Eclipse
        topdir = os.path.join(os.path.abspath(os.curdir), "COACH")

        # Start root service and directory service from the framework module
        wdir = os.path.join(topdir, "framework")
        os.chdir(wdir)
        
        # Start all the services

    wdir = os.path.join(topdir, os.path.normpath("framework"))
    os.chdir(wdir)
    InteractionService(os.path.join(topdir, os.path.normpath("local_settings.json")), 
                       os.path.normpath("settings/root_secret_data.json"),
                       working_directory = wdir).run()
    
    wdir = os.path.join(topdir, os.path.normpath("estimation_method/AverageOfTwo"))
    os.chdir(wdir)
    coach.EstimationMethodService(os.path.join(topdir, os.path.normpath("local_settings.json")), 
                              handling_class = AverageOfTwo.AverageOfTwo,
                              working_directory = wdir).run()
    
    wdir = os.path.join(topdir, os.path.normpath("context_model"))
    os.chdir(wdir)
    ContextModelService.ContextModelService(os.path.join(topdir, os.path.normpath("local_settings.json")), 
                                                              working_directory = wdir).run()
    
    wdir = os.path.join(topdir, os.path.normpath("framework"))
    os.chdir(wdir)
    DirectoryService(os.path.join(topdir, os.path.normpath("local_settings.json")), 
                    working_directory = os.path.join(topdir, "framework")).run()
    
    wdir = os.path.join(topdir, os.path.normpath("decision_process/SimpleDecisionProcessService"))
    os.chdir(wdir)
    SimpleDecisionProcessService.SimpleDecisionProcessService(os.path.join(topdir, os.path.normpath("local_settings.json")), working_directory = wdir).run()
    
    wdir = os.path.join(topdir, os.path.normpath("estimation_method/ExpertOpinion"))
    os.chdir(wdir)
    coach.EstimationMethodService(os.path.join(topdir, os.path.normpath("local_settings.json")), 
                              handling_class = ExpertOpinion.ExpertOpinion,
                              working_directory = wdir).run()
    
    wdir = os.path.join(topdir, os.path.normpath("decision_process/PughService"))
    os.chdir(wdir)
    PughService.PughService(os.path.join(topdir, os.path.normpath("local_settings.json")), working_directory = wdir).run()

    wdir = os.path.join(topdir, os.path.normpath("framework"))
    os.chdir(wdir)
    CaseDatabase(os.path.join(topdir, os.path.normpath("local_settings.json")), 
                 os.path.normpath("settings/root_secret_data.json"),
                 "CaseDB",
                 working_directory = wdir).run()
    
    wdir = os.path.join(topdir, "framework")
    os.chdir(wdir)
    KnowledgeRepositoryService.KnowledgeRepositoryService(os.path.join(topdir, os.path.normpath("local_settings.json")), 
                                                    os.path.normpath("settings/root_secret_data.json"),
                                                    working_directory = wdir).run()

    wdir = os.path.join(topdir, os.path.normpath("framework"))
    os.chdir(wdir)
    AuthenticationService(os.path.join(topdir, os.path.normpath("local_settings.json")), 
                            os.path.normpath("settings/root_secret_data.json"),
                            working_directory = wdir).run()
