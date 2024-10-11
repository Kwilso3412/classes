import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules

class apriori_algo:
    def create_excel_file( self, combined_dataframe, excel_file_name):
        with pd.ExcelWriter(excel_file_name, engine='openpyxl') as writer:
        # Iterate through the dictionary and write each DataFrame to a sheet
            for sheet_name, df in combined_dataframe.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Excel file '{excel_file_name}' has been created with multiple sheets.")

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
    
    #Sample useage:
    '''
    columns_to_convert_binary_list = [
    {'column':'coulmn_name', 'threshold':3.6},
    {'column':'coulmn_name_2', 'threshold':3.6}
    ]
    columns_to_convert_binary = pd.DataFrame(columns_to_convert_binary_list)
    column_to_pop_out = 'Primary_Academic_Institution_(Name)'
    institution['Cohort_Start_(Year)'] = institution['Cohort_Start_(Year)'].astype(str)
    testing_dataset = one_hot_selective(encoding_institution, columns_to_convert_binary, column_to_pop_out)
    testing_dataset.head(1)

    '''
    def one_hot_selective(self, dataframe, columns_to_convert, column_to_pop_out):
        popped_column = dataframe.pop(column_to_pop_out)
        num_col = dataframe.copy()
        num_col_names = num_col.select_dtypes(include=[np.number]).columns
        num_col = num_col[num_col_names]
        cat_col = dataframe.copy()
        cat_col_names = cat_col.select_dtypes(exclude=[np.number]).columns
        cat_col = cat_col[cat_col_names]
        for i, row in columns_to_convert.iterrows():
            num_col[row['column']] = self.binary_converter(num_col, row['column'], row['threshold'])
            
        encoded_cat_cols = pd.get_dummies(cat_col, dtype=int)
        testing_sample = pd.concat([num_col, encoded_cat_cols], axis = 1)
        testing_sample.insert(0,column_to_pop_out,popped_column)
        return testing_sample
    
    def one_hot_encoder(self, dataframe, columns_to_convert):
        num_col = dataframe.copy()
        num_col_names = num_col.select_dtypes(include=[np.number]).columns
        num_col = num_col[num_col_names]
        cat_col = dataframe.copy()
        cat_col_names = cat_col.select_dtypes(exclude=[np.number]).columns
        cat_col = cat_col[cat_col_names]
        for i, row in columns_to_convert.iterrows():
            num_col[row['column']] = self.binary_converter(num_col, row['column'], row['threshold'])
        encoded_cat_cols = pd.get_dummies(cat_col, dtype=int)
        testing_sample = pd.concat([num_col, encoded_cat_cols], axis = 1)
        return testing_sample
    
    '''
    Example usage 

    explanation_empty_df = pd.DataFrame()
    explanation_df = explination_for_apriori(explanation_empty_df)

    category_dict = {}
    category_column = 'Primary_Academic_Institution_(Name)'
    category_dict['Explanation'] = explanation_df
    for category, group in testing_dataset_by_insta.groupby(category_column):
        category_dict[category] = find_association_by_category(group.drop(category_column, axis=1))
        print(f'{category} report complete')

    excel_file_name_inst = "apriori_by_institution.xlsx"
    create_excel_file(category_dict, excel_file_name_inst)
    '''

    def find_association_by_category(dataframe):
        association_rules_list = []
        frequent_itemsets_list = []
        frequent_itemsets_raw = apriori(dataframe, min_support=0.3, use_colnames=True)
        sorted_frequent = frequent_itemsets_raw.sort_values('support', ascending=False).head(50)
        rules = association_rules(sorted_frequent, support_only=True, metric="confidence",min_threshold=0.7)
        sorted_rules = rules.sort_values('lift', ascending=False).head()
        for index, row in sorted_frequent.iterrows():
            frequent_itemsets_list.append({"items" : f"{row['itemsets']}",
                                "support" : f"{row['support']:.4f}"})
        
        frequent_itemsets_df_raw = pd.DataFrame(frequent_itemsets_list)
        frequent_itemsets_df = frequent_itemsets_df_raw.copy()
        frequent_itemsets_df['antecedents'] = np.nan
        frequent_itemsets_df['consequents'] = np.nan
        frequent_itemsets_df['confidence'] = np.nan
        for _, rule in sorted_rules.iterrows():
            antecedents = ', '.join(rule['antecedents'])
            consequents = ', '.join(rule['consequents'])
            association_rules_list.append({"top_associatoin" : f"If a student has {antecedents}, then they are likely to also have {consequents}",
                                            "confidence": f"{rule['confidence']:.2f}",
                                            "lift": f"{rule['lift']:.2f}"})
        association_rules_df = pd.DataFrame(association_rules_list)
        full_df = pd.concat([frequent_itemsets_df, association_rules_df], axis=1)
        return full_df

    def explination_for_apriori(empty_dataframe):
        generated_list = []
        generated_list.append({"Term" : "Frequent Itemsets",
            "Explanation": "Combinations of factors or characteristics that often appear together in successful students. For example, a combination might be 'high school GPA above 3.5, participation in extracurricular activities, and advanced math courses.'"})
        generated_list.append({"Term" : "Support",
        "Explanation": "How common a particular factor or combination of factors is among all students. For instance, 'What percentage of all admitted students have both a high SAT score and leadership experience?'"})
        generated_list.append({"Term" :"Association Rules",
        "Explanation" : "Patterns expressed as 'If-Then' statements about student characteristics and outcomes. For example, 'If a student participates in a summer bridge program, then they're likely to achieve a GPA above 3.0 in their first year.' These rules come with statistics (support, confidence, and lift) that indicate how strong and reliable the pattern is."})
        generated_list.append({"Term" : "Lift",
        "Explanation" : "A measure of how much more likely a student is to succeed compared to the average, given certain factors. It helps identify unexpected predictors of success. For instance, it might reveal that students who took a gap year are disproportionately likely to maintain a high GPA in college."})
        generated_list.append({"Term" :"Confidence", 
        "Explanation": "The likelihood of student success given certain admission factors. For example, 'If a student has a high GPA and participated in community service, how likely are they to graduate within 4 years?'"})
        full_dataframe = pd.DataFrame(generated_list)
        return full_dataframe