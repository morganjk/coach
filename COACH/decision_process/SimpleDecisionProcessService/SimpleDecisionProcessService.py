"""
An example of a decision process service. It implements a simple decision process in three steps:
1. Select an estimation method to be used to rank the value of alternatives.
2. For each alternative, estimate the value of each alternative.
3. Review the resulting ranking.
"""

# Set python import path to include COACH top directory
import os
import sys
sys.path.append(os.path.join(os.curdir, os.pardir, os.pardir, os.pardir))

# Coach framework
from COACH.framework import coach
from COACH.framework.coach import endpoint

# Standard libraries
import json

# Web server framework
from flask import request
from flask.templating import render_template


class SimpleDecisionProcessService(coach.DecisionProcessService):

    @endpoint("/process_menu", ["GET"], "text/html")
    def process_menu(self):
        return render_template("process_menu.html")


    @endpoint("/select_estimation_method_dialogue", ["GET"], "text/html")
    def select_estimation_method_dialogue_transition(self, directories):
        """
        Endpoint which lets the user select which estimation method to use for this decision process.
        """
        # Fetch the available services from the directories available in the case_db.
        services = []
        for d in [self.create_proxy(sd) for sd in json.loads(directories)]:
            services += d.get_services(service_type="estimation_method")

        # Create the alternatives for a dropdown menu
        # TODO: It should show the current estimation method as preselected.
        
        options = ["<OPTION value=\"%s\"> %s </A>" % (s[2], s[1]) for s in services]

        # Render the dialogue
        return render_template("select_estimation_method_dialogue.html", estimation_methods = options)


    @endpoint("/perform_ranking_dialogue", ["GET"], "text/html")
    def perform_ranking_dialogue_transition(self, user_id, delegate_token, case_db, case_id, knowledge_repository):
        """
        Endpoint which lets the user rank each of the alternatives using the selected estimation method dialogue.
        """
        case_db_proxy = self.create_proxy(case_db)

        estimation_method = case_db_proxy.get_case_property(user_id = user_id, token = delegate_token, case_id = case_id, name = "estimation_method")

        if estimation_method:
            # Get the alternatives from case_db and build a list to be fitted into a dropdown menu
            decision_alternatives = case_db_proxy.get_decision_alternatives(user_id = user_id, token = delegate_token, case_id = case_id)
            options = ["<OPTION value=\"%s\"> %s </A>" % (a[1], a[0]) for a in decision_alternatives]
        
            # Get the estimation method's dialogue
            estimation_method_proxy = self.create_proxy(estimation_method)
            estimation_dialogue = estimation_method_proxy.dialogue(knowledge_repository = knowledge_repository)
        
            return render_template("perform_ranking_dialogue.html", options = options, estimation_dialogue = estimation_dialogue, 
                                   estimation_method = estimation_method)
        else:
            return "You need to select an estimation method before you can rank alternatives!"
        

    @endpoint("/show_ranking_dialogue", ["GET"], "text/html")
    def show_ranking_dialogue_transition(self, user_id, delegate_token, case_db, case_id):
        """
        Endpoint which shows the alternatives in rank order. Unranked alternatives are at the bottom.
        """
        # Get the alternatives for the case.
        case_db_proxy = self.create_proxy(case_db)

        decision_alternatives = case_db_proxy.get_decision_alternatives(user_id = user_id, token = delegate_token, case_id = case_id)
        
        # Get the estimate for each alternative.
        estimates = [(a[0], case_db_proxy.get_alternative_property(user_id = user_id, token = delegate_token, case_id = case_id,
                                                                   alternative = a[1], name = "estimate")) for a in decision_alternatives]

        # Sort the ranked alternatives.
        ranked_alternatives = sorted([(a, e) for (a, e) in estimates if e], key = lambda p: float(p[1]), reverse = True)
        unranked_alternatives = [a for (a, e) in estimates if not e]
        
        # Render the dialogue
        ranked_alternatives = [a + ": estimation = " + e for (a, e) in ranked_alternatives]
        unranked_alternatives = [a + ": no estimation" for a in unranked_alternatives]
        return render_template("show_ranking_dialogue.html", ranked = ranked_alternatives, unranked = unranked_alternatives)


    @endpoint("/select_estimation_method", ["POST"], "text/html")
    def select_estimation_method(self, user_id, delegate_token, case_db, method, case_id):
        """
        This method is called using POST when the user presses the select button in the select_estimation_method_dialogue.
        It gets to form parameters: case_db, which is the url of the case database server, and method, which is the url of the selected estimation method.
        It changes the selection in the case database, and then returns a status message to be shown in the main dialogue window.
        """
        # Write the selection to the database.
        case_db_proxy = self.create_proxy(case_db)

        case_db_proxy.change_case_property(user_id = user_id, token = delegate_token, case_id = case_id, name = "estimation_method", value = method)
        return "Estimation method changed to " + method
    
    
    @endpoint("/perform_ranking", ["POST"], "text/html")
    def perform_ranking(self, user_id, delegate_token, case_id, case_db, alternative, estimation_method, knowledge_repository):
        """
        This method is called using POST when the user presses the button in the estimation method dialogue as part of the ranking dialogue.
        It calculates the estimate and writes it to the database and then returns a status message showing the updated estimate value in the main dialogue window.
        """
        # Calculate estimate. This is done by removing the values "case_db", "case_id", "estimation_method" and "alternative" from the dictionary of values. 
        # The rest should be estimation method arguments, and are passed to the evaluate endpoint of the estimation method.
        params = {"knowledge_repository" : knowledge_repository}
        for p in set(request.values.keys()) - {"case_db", "case_id", "estimation_method", "alternative", "directories", "endpoint"}:
            params[p] = request.values[p]
        
        estimation_method_proxy = self.create_proxy(estimation_method)
        value = estimation_method_proxy.evaluate(**params)
            
        # Write estimate to the database
        # TODO: For now, just set it as an attribute of the alternative node. This needs to be improved!
        case_db_proxy = self.create_proxy(case_db)
        case_db_proxy.change_alternative_property(user_id = user_id, token = delegate_token, case_id = case_id,
                                                  alternative = str(alternative), name = "estimate", value = value)
        return "Estimate of has been changed to " + str(value)
    
    
if __name__ == '__main__':
    SimpleDecisionProcessService(sys.argv[1]).run()
