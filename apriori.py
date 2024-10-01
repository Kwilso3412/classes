import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules

class apriori_algo:
    def create_excel_file( self, combined_dataframe, excel_file):
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # Iterate through the dictionary and write each DataFrame to a sheet
            for sheet_name, df in combined_dataframe.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Excel file '{excel_file}' has been created with multiple sheets.")
    
    def find_association_single(self, dataframe):
        frequent_itemsets_list = []
        association_rules_list = []
        frequent_itemsets_raw = apriori(dataframe, min_support=0.3, use_colnames=True)
        # Set display options to show all rows and columns
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
            for index, row in frequent_itemsets_raw.iterrows():
                frequent_itemsets_list.append({"items" : f"{row['itemsets']}",
                                    "support" : f"{row['support']:.4f}"})
        frequent_itemsets_df = pd.DataFrame(frequent_itemsets_list)
        rules = association_rules(frequent_itemsets_raw, metric="confidence",min_threshold=0.7)
        sorted_rules = rules.sort_values('lift', ascending=False).head()
        for _, rule in sorted_rules.iterrows():
            antecedents = ', '.join(rule['antecedents'])
            consequents = ', '.join(rule['consequents'])
            with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
                association_rules_list.append({"top_associatoin" : f"If a student has {antecedents}, then they are likely to also have {consequents}",
                                                "confidence": f"{rule['confidence']:.2f}",
                                                "lift": f"{rule['lift']:.2f}"})
        association_rules_df = pd.DataFrame(association_rules_list)
        explination_list = []
        explination_list.append({"Term" : "Frequent Itemsets",
            "Explanation": "Combinations of factors or characteristics that often appear together in successful students. For example, a combination might be 'high school GPA above 3.5, participation in extracurricular activities, and advanced math courses.'"})
        explination_list.append({"Term" : "Support",
        "Explanation": "How common a particular factor or combination of factors is among all students. For instance, 'What percentage of all admitted students have both a high SAT score and leadership experience?'"})
        explination_list.append({"Term" :"Association Rules",
        "Explanation" : "Patterns expressed as 'If-Then' statements about student characteristics and outcomes. For example, 'If a student participates in a summer bridge program, then they're likely to achieve a GPA above 3.0 in their first year.' These rules come with statistics (support, confidence, and lift) that indicate how strong and reliable the pattern is."})
        explination_list.append({"Term" : "Lift",
        "Explanation" : "A measure of how much more likely a student is to succeed compared to the average, given certain factors. It helps identify unexpected predictors of success. For instance, it might reveal that students who took a gap year are disproportionately likely to maintain a high GPA in college."})
        explination_list.append({"Term" :"Confidence", 
        "Explanation": "The likelihood of student success given certain admission factors. For example, 'If a student has a high GPA and participated in community service, how likely are they to graduate within 4 years?'"})
        explination_df = pd.DataFrame(explination_list)
        combinded_dataframe_dict = {
            'Frequent Itemsets' : frequent_itemsets_df,
            'Top Association Rules' : association_rules_df,
            'epxlaination of terms' : explination_df
        }
        return combinded_dataframe_dict
    
    def explination_for_apriori(self, empty_dataframe):
        explination_list = []
        explination_list.append({"Term" : "Frequent Itemsets",
            "Explanation": "Combinations of factors or characteristics that often appear together in successful students. For example, a combination might be 'high school GPA above 3.5, participation in extracurricular activities, and advanced math courses.'"})
        explination_list.append({"Term" : "Support",
        "Explanation": "How common a particular factor or combination of factors is among all students. For instance, 'What percentage of all admitted students have both a high SAT score and leadership experience?'"})
        explination_list.append({"Term" :"Association Rules",
        "Explanation" : "Patterns expressed as 'If-Then' statements about student characteristics and outcomes. For example, 'If a student participates in a summer bridge program, then they're likely to achieve a GPA above 3.0 in their first year.' These rules come with statistics (support, confidence, and lift) that indicate how strong and reliable the pattern is."})
        explination_list.append({"Term" : "Lift",
        "Explanation" : "A measure of how much more likely a student is to succeed compared to the average, given certain factors. It helps identify unexpected predictors of success. For instance, it might reveal that students who took a gap year are disproportionately likely to maintain a high GPA in college."})
        explination_list.append({"Term" :"Confidence", 
        "Explanation": "The likelihood of student success given certain admission factors. For example, 'If a student has a high GPA and participated in community service, how likely are they to graduate within 4 years?'"})
        explination_df = pd.DataFrame(explination_list)
        empty_dataframe = explination_df.copy()
        return empty_dataframe
    
