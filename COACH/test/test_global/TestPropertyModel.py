"""
Created on 27 juil. 2017

@author: francois
"""
import os
import sys
import unittest

sys.path.append(os.path.join(os.curdir, os.pardir, os.pardir, os.pardir))
from COACH.test.test_global.TestGlobal import TestGlobal
from COACH.test.test_global.EstimationMethodValue import EstimationMethodValue

from selenium.webdriver.support.select import Select
from selenium.common.exceptions import UnexpectedTagNameException
from selenium.common.exceptions import NoSuchElementException

class TestPropertyModel(TestGlobal):
    #Global
    COMPUTED_VALUE_FORMATTER = "{0:.4f}"
    
    #add_alternative_dialogue.html
    ADD_ALTERNATIVE__SUB_TITLE = "Add new decision alternative"
    ADD_ALTERNATIVE__TITLE_FIELD_NAME = "title"
    ADD_ALTERNATIVE__DESCRIPTION_FIELD_NAME = "description"
    ADD_ALTERNATIVE__USAGE_FIELD_NAME = "asset_usage"
    ADD_ALTERNATIVE__ORIGIN_FIELD_NAME = "asset_origin"
    ADD_ALTERNATIVE__TYPE_FIELD_NAME = "asset_type"
    ADD_ALTERNATIVE__CONFIRMATION_MESSAGE = "New alternative added!"
    
    #properties_overview_dialogue.html
    PROPERTY_OVERVIEW__SUB_TITLE = "Properties"
    
    #properties_estimation_methods_dialogue.html
    PROPERTY_ESTIMATION_METHOD__SUB_TITLE = "Estimation methods"
    PROPERTY_ESTIMATION_METHOD__ALTERNATIVE_SELECT_NAME = "alternative_name"
    PROPERTY_ESTIMATION_METHOD__PROPERTY_SELECT_NAME = "property_name"
    PROPERTY_ESTIMATION_METHOD__ESTIMATION_METHOD_SELECT_NAME = "estimation_method_name"
    PROPERTY_ESTIMATION_METHOD__SUBMIT_COMPONENT_NAME = "submit_component"
    PROPERTY_ESTIMATION_METHOD__USED_PROPERTIES_LIST_ID = "used_properties"
    PROPERTY_ESTIMATION_METHOD__PARAMETERS_LIST_ID = "used_parameters"
    PROPERTY_ESTIMATION_METHOD__USED_PROPERTIES_SELECT_SUFFIX = "_selected_estimation_method"
    PROPERTY_ESTIMATION_METHOD__USED_PROPERTIES_VALUE_SUFFIX = "_property_value"
    PROPERTY_ESTIMATION_METHOD__PARAMETER_NAME_SUFFIX = "_parameter"
    PROPERTY_ESTIMATION_METHOD__COMPUTE_BUTTON_VALUE = "Compute"
    PROPERTY_ESTIMATION_METHOD__DELETE_BUTTON_VALUE = "Delete"
    PROPERTY_ESTIMATION_METHOD__GOTO_BUTTON_SUFFIX = "_goto_button"
    PROPERTY_ESTIMATION_METHOD__NO_COMPUTE_VALUE_MESSAGE = "This estimation has not been computed yet"
    PROPERTY_ESTIMATION_METHOD__COMPUTE_VALUE_MESSAGE = "Current value is "
    PROPERTY_ESTIMATION_METHOD__NOT_COMPUTED_VALUE = "---"
    PROPERTY_ESTIMATION_METHOD__USED_PROPERTY_OUT_OF_DATE_MESSAGE = "/!\ This value is out-of-date"
    PROPERTY_ESTIMATION_METHOD__ESTIMATION_OUT_OF_DATE_MESSAGE = "/!\ The current value is out-of-date"
    
    def test_property_estimation_method(self):
        """
        This method tests macro functionalities on the property model. 
        
        It will test:
            - Creation of an alternative
            - Estimation computed for different alternatives
            - Overview page without any estimation being computed
            - Shortcut with a click on a cell of the overview page
            - Compute an estimation with parameters
            - Compute an estimation with used properties
            - Message before a value is computed
            - Up-to-date is set to False when a used property is re-computed
            - Delete a property
            - Up-to-date is set to False when a used property is deleted
            - When up-to-date is False, the overview background is yellow
            - When up-to-date is False, a warning message is displayed before the value of the current estimation
            - When up-to-date is False, a warning message is displayed before the value of the used estimation
            - Shortcut with the goto button
            - Selectable estimation method are those for the selected property
            - Selectable estimation method for a used property are those for this property
            - If a used estimation has not been computed yet, the compute button is disable
            - If all used estimations have been computed, the compute button is enable
            - If an estimation has not been computed yet, the delete button is disable
            - If an estimation has been computed, the delete button is enable
            - When up-to-date is False, it becomes True once the estimation is re computed
            - Selected estimation method for used properties is the one used for the last computation
            - Parameters's value are the ones used for the last computation
        """       
        # Creation of an alternative
        self._go_to_link(self.MAIN_MENU__ALTERNATIVES_MENU, self.MAIN_MENU__ADD_ALTERNATIVE_LINK, 600)
        self._add_alternative("Alt 1")
        self.assertIn(self.ADD_ALTERNATIVE__CONFIRMATION_MESSAGE, self.driver.page_source)
        self._go_to_link(self.MAIN_MENU__ALTERNATIVES_MENU, self.MAIN_MENU__ADD_ALTERNATIVE_LINK)
        self._add_alternative("Alt 2")
        self.assertIn(self.ADD_ALTERNATIVE__CONFIRMATION_MESSAGE, self.driver.page_source)
        
        # Overview page without any estimation being computed
        # Shortcut with a click on a cell of the overview page
        # Message before a value is computed
        # Compute an estimation with parameters
        # Selectable estimation method are those for the selected property
        # If an estimation has not been computed yet, the delete button is disable
        # If an estimation has been computed, the delete button is enable
        estimation = ("Alt 1", "Development effort", "Expert estimate float")
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK, 600)
        self._assert_property_overview_page()
        self._click_on_property_overview_shortcut(estimation)
        self._assert_property_estimation_method_page(estimation)
        self._assert_compute_value(None)
        self._compute_estimation({"estimation": 5})
        self.estimation_value_list.append((*estimation, 5.0))
        self._assert_compute_value(5)
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK, 30)
        self._assert_property_overview_page()
   
        # Compute an estimation with used properties
        # Selectable estimation method for a used property are those for this property
        # If all used estimations have been computed, the compute button is enable
        estimation = ("Alt 1", "Cost", "Cost estimation")
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_ESTIMATION_METHODS_LINK)
        self._assert_property_estimation_method_page()
        self._select_estimation(estimation)
        self._assert_compute_value(None)
        self._assert_property_estimation_method_page(estimation)
        self._compute_estimation({"Salary": 10}, {"Development effort": "Expert estimate float"})
        self.estimation_value_list.append((*estimation, 50.0))
        self._assert_compute_value(50)
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK)
        self._assert_property_overview_page()
         
        # Up-to-date is set to False when a used property is re-computed
        # When up-to-date is False, the overview background is yellow
        # When up-to-date is False, a warning message is displayed before the value of the current estimation
        # Parameters's value are the ones used for the last computation
        estimation = ("Alt 1", "Development effort", "Expert estimate float")
        self._click_on_property_overview_shortcut(estimation)
        self._assert_property_estimation_method_page(estimation, {"estimation": 5})
        self._assert_compute_value(5)
        self._compute_estimation()
        self._assert_property_estimation_method_page(estimation, {"estimation": 5})
        self._assert_compute_value(5)
        poped_estimation = self.estimation_value_list.pop(-1)
        self.estimation_value_list.append((*poped_estimation, False))
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK)
        self._assert_property_overview_page()
         
        # When up-to-date is False, it becomes True once the estimation is re computed
        # Selected estimation method for used properties is the one used for the last computation
        estimation = ("Alt 1", "Cost", "Cost estimation")
        self._click_on_property_overview_shortcut(estimation)
        self._assert_property_estimation_method_page(estimation, {"Salary": 10}, {"Development effort": ("Expert estimate float", True)}, False)
        self._assert_compute_value(50)
        self._compute_estimation()
        self._assert_compute_value(50)
        self._assert_property_estimation_method_page(estimation, {"Salary": 10}, {"Development effort": ("Expert estimate float", True)}, True)
        self.estimation_value_list.pop(-1)
        self.estimation_value_list.append((*estimation, 50.0))
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK)
        self._assert_property_overview_page()
         
        # If a used estimation has not been computed yet, the compute button is disable
        estimation = ("Alt 2", "Development effort", "Basic COCOMO")
        self._click_on_property_overview_shortcut(estimation)
        self._assert_property_estimation_method_page(estimation)
        
        # Shortcut with the goto button
        # Estimation computed for different alternatives
        estimation = ("Alt 2", "KLOC", "Expert estimate float")
        self._click_on_goto_button("KLOC", "Expert estimate float")
        self._assert_property_estimation_method_page(estimation)
        self._assert_compute_value(None)
        self._compute_estimation({"estimation": 5})
        self.estimation_value_list.append((*estimation, 5.0))
        self._assert_property_estimation_method_page(estimation, {"estimation": 5})
        self._assert_compute_value(5)
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK)
        self._assert_property_overview_page()
        
        estimation = ("Alt 2", "Development effort", "Basic COCOMO")
        self._click_on_property_overview_shortcut(estimation)
        self._assert_property_estimation_method_page(estimation)
        self._assert_compute_value(None)
        self._compute_estimation({"developmentMode": "Semi-detached"}, {"KLOC": "Expert estimate float"})
        self.estimation_value_list.append((*estimation, 18.1957))
        self._assert_property_estimation_method_page(estimation, {"developmentMode": "Semi-detached"}, {"KLOC": ("Expert estimate float", True)})
        self._assert_compute_value(18.1957)
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK)
        self._assert_property_overview_page()
        
        estimation = ("Alt 2", "KLOC", "Expert estimate float")
        self._click_on_property_overview_shortcut(estimation)
        self._assert_property_estimation_method_page(estimation, {"estimation": 5})
        self._assert_compute_value(5)
        self._compute_estimation()
        poped_estimation = self.estimation_value_list.pop(-1)
        self.estimation_value_list.append((*poped_estimation, False))
        self._assert_property_estimation_method_page(estimation, {"estimation": 5})
        self._assert_compute_value(5)
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK)
        self._assert_property_overview_page()
        
        # When up-to-date is False, a warning message is displayed before the value of the used estimation
        estimation = ("Alt 2", "Cost", "Cost estimation")
        self._click_on_property_overview_shortcut(estimation)
        self._assert_property_estimation_method_page(estimation)
        self._assert_compute_value(None)
        self._compute_estimation({"Salary": 10}, {"Development effort": "Basic COCOMO"})
        self.estimation_value_list.append((*estimation, 181.9565))
        self._assert_property_estimation_method_page(estimation, {"Salary": 10}, {"Development effort": ("Basic COCOMO", False)})
        self._assert_compute_value(181.9565)
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK)
        self._assert_property_overview_page()
        
        # Delete a property
        # Up-to-date is set to False when a used property is deleted
        estimation = ("Alt 2", "Development effort", "Basic COCOMO")
        self._click_on_property_overview_shortcut(estimation)
        self._assert_property_estimation_method_page(estimation, {"developmentMode": "Semi-detached"}, {"KLOC": ("Expert estimate float", True)}, False)
        self._assert_compute_value(18.1957)
        self._delete_estimation()
        self.estimation_value_list.pop(-2)
        # The property is still linked to the alternative in the database, so "---" will appear in the overview.
        self.estimation_value_list.append((*estimation, self.PROPERTY_ESTIMATION_METHOD__NOT_COMPUTED_VALUE))
        poped_estimation = self.estimation_value_list.pop(-2)
        self.estimation_value_list.append((*poped_estimation, False))
        self._assert_property_estimation_method_page(estimation)
        self._assert_compute_value(None)
        self._go_to_link(self.MAIN_MENU__PROPERTIES_MENU, self.MAIN_MENU__PROPERTY_OVERVIEW_LINK)
        self._assert_property_overview_page()
        
        
    def _add_alternative(self, alternative_name, alternative_description = "desc", alternative_usage="Unknown",
                         alternative_origin="Unknown", alternative_type_list=[]):
        self.alternatives_name_list.append(alternative_name)
        
        self._send_key_in_field(self.ADD_ALTERNATIVE__TITLE_FIELD_NAME, alternative_name)
        self._send_key_in_field(self.ADD_ALTERNATIVE__DESCRIPTION_FIELD_NAME, alternative_description)
        self._select_combo_box(self.ADD_ALTERNATIVE__USAGE_FIELD_NAME, alternative_usage)
        self._select_combo_box(self.ADD_ALTERNATIVE__ORIGIN_FIELD_NAME, alternative_origin)
        
        type_field = self.driver.find_element_by_name(self.ADD_ALTERNATIVE__TYPE_FIELD_NAME)
        parameter_element = Select(type_field)
        for alternative_type in alternative_type_list:
            parameter_element.select_by_visible_text(alternative_type)
        
        with self.wait_for_page_load():
            type_field.submit()
            
    
    def _click_on_property_overview_shortcut(self, estimation):
        (alternative_name, property_name, estimation_method_name) = estimation
        
        if "&" in alternative_name or "&" in property_name or "&" in estimation_method_name:
            raise NotImplementedError("Name containing '&' are not implemented yet")
        
        table_element = self.driver.find_element_by_tag_name("table")
        links_element = table_element.find_elements_by_tag_name("a")
        for link in links_element:
            link_text = link.get_attribute("href").replace("%20", " ")
            link_split_text = link_text.split("&")
            link_alternative_name = link_split_text[1].split("=")[1].strip()
            link_property_name = link_split_text[2].split("=")[1].strip()
            link_estimation_method_name = link_split_text[3].split("=")[1].strip()
            
            if (alternative_name == link_alternative_name and property_name == link_property_name and
                    estimation_method_name == link_estimation_method_name):
                with self.wait_for_page_load():
                    link.find_element_by_tag_name("div").click()
                return
            
        raise RuntimeError("The link ({0}, {1}, {2}) should have been clicked.".format(alternative_name, property_name, estimation_method_name))
        
    def _compute_estimation(self, parameters_dict = {}, used_properties_dict = {}):
        # The page is refresh each time a used property is selected: it must be done before keying in parameters 
        for used_property_name in used_properties_dict:
            self._select_combo_box(used_property_name + "_selected_estimation_method", used_properties_dict[used_property_name], True)

        for parameter_name in parameters_dict:
            try:
                self._select_combo_box(parameter_name + "_parameter", parameters_dict[parameter_name])
            except UnexpectedTagNameException: #Throw when trying to create a Select without a select element
                self._send_key_in_field(parameter_name + "_parameter", parameters_dict[parameter_name])
        
        compute_button = self._find_submit_component(self.PROPERTY_ESTIMATION_METHOD__COMPUTE_BUTTON_VALUE)
        with self.wait_for_page_load(15):
            compute_button.click()
    
    def _delete_estimation(self):
        delete_button = self._find_submit_component(self.PROPERTY_ESTIMATION_METHOD__DELETE_BUTTON_VALUE)
        with self.wait_for_page_load():
            delete_button.click()

    def _click_on_goto_button(self, property_name, estimation_method_name):
        self._select_combo_box(property_name + self.PROPERTY_ESTIMATION_METHOD__USED_PROPERTIES_SELECT_SUFFIX, estimation_method_name, True)
        goto_button = self._find_submit_component(property_name + self.PROPERTY_ESTIMATION_METHOD__GOTO_BUTTON_SUFFIX)
        with self.wait_for_page_load():
            goto_button.click()
    
    def _find_submit_component(self, component_value):
        submit_elements = self.driver.find_elements_by_name(self.PROPERTY_ESTIMATION_METHOD__SUBMIT_COMPONENT_NAME)
        for submit_element in submit_elements:
            if submit_element.get_attribute("value") == component_value:
                return submit_element
    
    def _select_estimation(self, estimation = (None, None, None)):
        (alternative_name, property_name, estimation_method_name) = estimation
        
        if alternative_name is not None:
            self._select_combo_box(self.PROPERTY_ESTIMATION_METHOD__ALTERNATIVE_SELECT_NAME, alternative_name, True)
        if property_name is not None:
            self._select_combo_box(self.PROPERTY_ESTIMATION_METHOD__PROPERTY_SELECT_NAME, property_name, True)
        if estimation_method_name is not None:
            self._select_combo_box(self.PROPERTY_ESTIMATION_METHOD__ESTIMATION_METHOD_SELECT_NAME, estimation_method_name, True)
            
    
    def _assert_property_overview_page(self):
        self._assert_page(self.PROPERTY_OVERVIEW__SUB_TITLE)
        actual_estimation_method_value = EstimationMethodValue.build_from_web_page(self.driver)
        expected_estimation_method_value = EstimationMethodValue.build_expected_result(self.alternatives_name_list, self.estimation_value_list)
        self.assertTrue(actual_estimation_method_value.__eq__(expected_estimation_method_value, "actual", "expected"))
        
    def _assert_property_estimation_method_page(self, estimation = (None, None, None), parameters_value = {}, used_properties_estimation_method = {}, 
                                                up_to_date = True):
        (alternative_name, property_name, estimation_method_name) = estimation
            
        self._assert_page(self.PROPERTY_ESTIMATION_METHOD__SUB_TITLE)
        alternative_select = Select(self.driver.find_element_by_name(self.PROPERTY_ESTIMATION_METHOD__ALTERNATIVE_SELECT_NAME))
        property_select = Select(self.driver.find_element_by_name(self.PROPERTY_ESTIMATION_METHOD__PROPERTY_SELECT_NAME))
        estimation_method_select = Select(self.driver.find_element_by_name(self.PROPERTY_ESTIMATION_METHOD__ESTIMATION_METHOD_SELECT_NAME))
        
        # Assert selected alternative, property, estimation method
        if alternative_name is not None:
            self.assertEqual(alternative_name, alternative_select.first_selected_option.text)
        if property_name is not None:
            self.assertEqual(property_name, property_select.first_selected_option.text)
        if estimation_method_name is not None:
            self.assertEqual(estimation_method_name, estimation_method_select.first_selected_option.text)
        
        # Assert list of possible alternatives, properties, estimation methods
        self.assertEqual(set(self.alternatives_name_list), {option.text for option in alternative_select.options})
        
        properties_name_list = EstimationMethodValue.get_expected_properties_name_list()
        self.assertEqual(set(properties_name_list), {option.text for option in property_select.options})
        
        estimation_methods_name_list = EstimationMethodValue.get_expected_estimation_methods_name_list(property_select.first_selected_option.text)
        self.assertEqual(set(estimation_methods_name_list), {option.text for option in estimation_method_select.options})
        
        self._assert_used_properties(used_properties_estimation_method)
        self._assert_parameters(parameters_value)
        self.assertEqual(up_to_date, self.PROPERTY_ESTIMATION_METHOD__ESTIMATION_OUT_OF_DATE_MESSAGE not in self.driver.page_source)
        
    def _assert_used_properties(self, used_properties_estimation_method):
        is_compute_button_enable = True
        try:
            used_properties_list_element = self.driver.find_element_by_id(self.PROPERTY_ESTIMATION_METHOD__USED_PROPERTIES_LIST_ID)
            used_properties_list_item_list = used_properties_list_element.find_elements_by_tag_name("li")
        except NoSuchElementException:
            used_properties_list_item_list = []
            
        for list_element in used_properties_list_item_list:
            select_used_property = list_element.find_element_by_tag_name("select")
            property_name = select_used_property.get_attribute("name")[:-len(self.PROPERTY_ESTIMATION_METHOD__USED_PROPERTIES_SELECT_SUFFIX)]
            estimation_methods_name_list = EstimationMethodValue.get_expected_estimation_methods_name_list(property_name)
            select_used_property = Select(select_used_property)
            self.assertEqual(set(estimation_methods_name_list), {option.text for option in select_used_property.options})
            
            if property_name in used_properties_estimation_method:
                selected_estimation_method = select_used_property.first_selected_option.text
                (expected_selected_estimation_method, up_to_date) = used_properties_estimation_method[property_name]
                del used_properties_estimation_method[property_name]
                self.assertEqual(selected_estimation_method, expected_selected_estimation_method)
                self.assertEqual(up_to_date, self.PROPERTY_ESTIMATION_METHOD__USED_PROPERTY_OUT_OF_DATE_MESSAGE not in list_element.text)
            
            value_element = list_element.find_element_by_name(property_name + self.PROPERTY_ESTIMATION_METHOD__USED_PROPERTIES_VALUE_SUFFIX)
            if value_element.get_attribute("value") == self.PROPERTY_ESTIMATION_METHOD__NOT_COMPUTED_VALUE:
                is_compute_button_enable = False
                
        self.assertEqual(is_compute_button_enable, self._find_submit_component(self.PROPERTY_ESTIMATION_METHOD__COMPUTE_BUTTON_VALUE).is_enabled())
        self.assertEqual(len(used_properties_estimation_method), 0)
        
    def _assert_parameters(self, parameters_value_dict):
        try:
            parameters_ul_element = self.driver.find_element_by_id(self.PROPERTY_ESTIMATION_METHOD__PARAMETERS_LIST_ID)
            parameters_input_element_list = parameters_ul_element.find_elements_by_tag_name("input")
            parameters_select_element_list = parameters_ul_element.find_elements_by_tag_name("select")
        except NoSuchElementException:
            parameters_input_element_list = []
            parameters_select_element_list = []
        
        # Check all parameters of type text, float, integer
        for parameter_element in parameters_input_element_list:
            parameter_name = parameter_element.get_attribute("name")[:-len(self.PROPERTY_ESTIMATION_METHOD__PARAMETER_NAME_SUFFIX)]
            parameter_value = parameter_element.get_attribute("value")
            if parameter_name in parameters_value_dict:
                self.assertEqual(str(parameter_value), str(parameters_value_dict[parameter_name]))
                del parameters_value_dict[parameter_name]
            
        # Check all parameters of type select
        for parameter_element in parameters_select_element_list:
            parameter_name = parameter_element.get_attribute("name")[:-len(self.PROPERTY_ESTIMATION_METHOD__PARAMETER_NAME_SUFFIX)]
            parameter_value = Select(parameter_element).first_selected_option.text
            if parameter_name in parameters_value_dict:
                self.assertEqual(str(parameter_value), str(parameters_value_dict[parameter_name]))
                del parameters_value_dict[parameter_name]
                        
        self.assertEqual(len(parameters_value_dict), 0)
        
    def _assert_compute_value(self, value):
        if value == self.PROPERTY_ESTIMATION_METHOD__NOT_COMPUTED_VALUE:
            raise RuntimeError("Tests won't make difference between this value and no computed value when checking if the delete button " +
                               "is enable. Consequently, this value must not be used in test cases.")
        if value is None:
            self.assertIn(self.PROPERTY_ESTIMATION_METHOD__NO_COMPUTE_VALUE_MESSAGE, self.driver.page_source)
            self.assertFalse(self._find_submit_component(self.PROPERTY_ESTIMATION_METHOD__DELETE_BUTTON_VALUE).is_enabled())
        else:
            value_string = self.COMPUTED_VALUE_FORMATTER.format(value)
            self.assertIn(self.PROPERTY_ESTIMATION_METHOD__COMPUTE_VALUE_MESSAGE + value_string, " ".join(self.driver.page_source.split()))
            self.assertTrue(self._find_submit_component(self.PROPERTY_ESTIMATION_METHOD__DELETE_BUTTON_VALUE).is_enabled())


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPropertyModel)
    unittest.TextTestRunner().run(suite)
    
    
    
