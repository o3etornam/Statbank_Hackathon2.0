import features

warehouse = {
    'Economic Activity': {'All Economic Activity':{'extension':'econact_table.px','query_path':'Econact.json', 'age':features.eco_age},
                         'Child Economic Activity':{'extension':'child_econact_table.px','query_path':'Child_Econact.json','age':features.eco_child_age},
                         'Unemployment Rate':{'extension':'Unemployment_table_2.px','query_path':'Unemployment.json','age':features.eco_age},
                         'Child in Economic Activity(Occupation)':{'extension':'occupa_table_child.px','query_path':'Child_in_Econact_Occ.json','age':features.eco_child_age},
                         'Child in Economic Activity(Industry)':{'extension':'child_industry_table.px','query_path':'Child_in_Econact_Ind.json','age':features.eco_child_age},
                         'Employed(Industry)':{'extension':'industry_table.px','query_path':'Employed_Ind.json','age':features.eco_age},
                         'Employed(Industry)':{'extension':'occupation_table.px','query_path':'Employed_Occ.json','age':features.eco_age},
                         'Employed(Sector)':{'extension':'sector_table.px','query_path':'Employed_Sec.json','age':features.eco_age},
                         'Employed(Status)':{'extension':'status_table.px','query_path':'Employed_Status.json','age':features.eco_age},
                         },


    'ICT': {'Ownership of Laptops':{'extension': 'ownict_table_4.px','query_path':'Own_laptop.json', 'age':features.ict_ages},
           'Ownership of Functional Mobile':{'extension':'ownmobile_table.px','query_path':'Own_functional_mobile.json','age':features.ict_ages},
           'Ownership of Non Smart Phone':{'extension':'ownict_table_2.px','query_path':'Own_non_smart_phone.json','age':features.ict_ages},
           'Ownership of Tablet':{'extension':'ownict_table_3.px','query_path':'Own_tablet.json','age':features.ict_ages},
           'Ownership of Smart Phone':{'extension':'ownict_table_1.px','query_path':'Own_smartphone.json','age':features.ict_ages},
           'Used internet on mobile phone in the last 3 months':{'extension':'use_internet_on_device_1.px','query_path':'used_phone.json','age':features.ict_ages},
           'Used internet on laptop in the last 3 months ':{'extension':'use_internet_on_device_3.px','query_path':'used_laptop.json','age':features.ict_ages},
           'Used internet on desktop in the last 3 months':{'extension':'use_internet_on_device_4.px','query_path':'used_desktop.json','age':features.ict_ages},
           'Used internet on any other device in the last 3 months':{'extension':'use_internet_on_device_6.px','query_path':'used_other_device.json','age':features.ict_ages},
           'Use of mobile phone for financial transaction':{'extension':'usephone_financial_table.px','query_path':'use_phone_finance.json','age':features.ict_ages},
           'Use of any ICT device in the last 3 months':{'extension':'useict_table_9.px','query_path':'use_functional_ict.json','age':features.ict_ages},
           },
    'Water and Sanitation': {'Defaecation Point':{'extension': 'defaecate_table.px','query_path':'defaecation.json'},
           'Water for Other Domestic Use':{'extension':'domesticWater_table.px','query_path':'main_water.json'},
           'Defaecation Point':{'extension': 'defaecate_table.px','query_path':'defaecation.json'},
           'Defaecation Point':{'extension': 'defaecate_table.px','query_path':'defaecation.json'},
           'Defaecation Point':{'extension': 'defaecate_table.px','query_path':'defaecation.json'},
           'Defaecation Point':{'extension': 'defaecate_table.px','query_path':'defaecation.json'},
           'Defaecation Point':{'extension': 'defaecate_table.px','query_path':'defaecation.json'},
           'Defaecation Point':{'extension': 'defaecate_table.px','query_path':'defaecation.json'},
           'Defaecation Point':{'extension': 'defaecate_table.px','query_path':'defaecation.json'},
           },
    'Difficulties in Performing Activities':{'Difficulty Status':{'extension':'disability_table.px','query_path':'Difficulty_Status.json','age':features.diff_age},
                                            'Difficulty in Seeing':{'extension':'forms_seeing_disability_table.px','query_path':'seeing.json','age':features.diff_age},
                                            'Difficulty in Hearing':{'extension':'hearing_disability_table.px','query_path':'hearing.json','age':features.diff_age},
                                            'Difficulty in Remembering or Concentrating':{'extension':'intellectual_disability_table.px','query_path':'Remeber_and_Concetrate.json','age':features.diff_age},
                                            'Physical Disability':{'extension':'physical_disability_table.px','query_path':'Physical.json','age':features.diff_age},
                                            'Difficulty in Self-Care':{'extension':'selfcare_disability_table.px','query_path':'Physical.json','age':features.diff_age},
                                            'Severity of Disability':{'extension':'severe_disability_table.px','query_path':'Severity.json','age':features.diff_age},
                                            'Difficulty in Speech':{'extension':'speech_disability_table.px','query_path':'Speech.json','age':features.diff_age},
                                          
                                          },
     'Education and Literacy':{'Highest Level of Education':{'extension':'attended_table.px', 'query_path':'highest.json','age':features.edu_age},
                            'Currently in School':{'extension':'currently_attend_table.px', 'query_path':'currently in school.json','age':features.edu_sch_age}, 
                            'Ghanaian Language of Literacy':{'extension':'GHLang_table.px', 'query_path':'Language of literacy(GH).json','age':features.edu_age},
                            'Language of Literacy':{'extension':'Lang_of_Lit_table.px', 'query_path':'Language of literacy.json','age':features.edu_age},
                            'Languages Spoken':{'extension':'Lang_of_Lit_table_2.px', 'query_path':'language spoken.json','age':features.edu_age},
                            'Literacy Status':{'extension':'literacystatus_table_v2.px', 'query_path':'lit_status.json','age':features.edu_age},
                               },
       'Structures':{'Completeness of Residential Structures':{'extension':'Levelof_completion_res_table.px', 'query_path':'completeness.json'},
                     'Completeness of Structures':{'extension':'Levelof_completion_struc_table.px', 'query_path':'completeness(all).json'},
                     'Type of Residential Structures':{'extension':'res_struc_table.px', 'query_path':'res_str.json'},
                     'Type of Structures':{'extension':'Struc_type_table.px', 'query_path':'gen_str.json'},
           
       },
       'Population': {'Population by Geographic Area':{'extension':'population_table.px', 'query_path':'population.json','age':features.ict_ages},
                     'Population by Nationality':{'extension':'nationality_table.px', 'query_path':'nationality.json','age':features.ict_ages},
                     'Type of Residential Structures':{'extension':'res_struc_table.px', 'query_path':'res_str.json'},
                     'Type of Structures':{'extension':'Struc_type_table.px', 'query_path':'gen_str.json'},
           
       },
       'Housing':{'Completeness of Residential Structures':{'extension':'Levelof_completion_res_table.px', 'query_path':'completeness.json'},
                     'Completeness of Structures':{'extension':'Levelof_completion_struc_table.px', 'query_path':'completeness(all).json'},
                     'Type of Residential Structures':{'extension':'res_struc_table.px', 'query_path':'res_str.json'},
                     'Type of Structures':{'extension':'Struc_type_table.px', 'query_path':'gen_str.json'},
           
       },
       'Fertility and Mortality':{'Number of Children Ever Born':{'extension':'fertility_table_1.px', 'query_path':'children_ever_born.json', 'age':features.eco_age},
                     'Number of Children Surviving':{'extension':'fertility_table_2.px', 'query_path':'children_surviving.json',  'age':features.eco_age},
                     'Mean Age at First Birth':{'extension':'fertility_table_3.px', 'query_path':'mean_age.json',  'age':features.eco_age},
                     'Mean Number of Children Ever Born':{'extension':'fertility_table_4.px', 'query_path':'mean_number_ever_born.json',  'age':features.eco_age},
                     'Mean Number of Children Surviving':{'extension':'fertility_table_5.px', 'query_path':'mean_number_surviving.json',  'age':features.eco_age},
           
       },
       'Mortality':{
           
       }
     

}

extras = {'ICT':"Data on ICT was taken from individuals in households and stable institutions.It was restricted to individuals age 6 and above",
          'Economic Activity':'Data on Economic Activity was taken from individuals in households and in stable instituitions',
          'Water and Sanitation':'Water and Sanitation data was taken from households in the various geographic areas',
          'Housing':'Housing data was collected from households in the various geographic areas',
          'Mortality':'Mortality data was collected from the households in the various geographic areas',
          'Fertility':'Fertility data was collected from girls 12 and above',
          }

categories = warehouse.keys()
individual_cat = ['Economic Activity', 'ICT', 'Difficulties in Performing Activities',
                  'Education and Literacy','Fertility','Population']

housing_cat = ['Mortalilty','Water and Sanitation', 'Housing']