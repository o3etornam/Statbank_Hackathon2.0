import features

warehouse = {
    'Economic Activity': {'All Economic Activity':{'extension':'Economic Activity/econact_table.px','query_path':'Econact.json', 'age':features.age_group_1},
                         },
    'ICT': {'Ownership of Laptops':{'extension': 'ICT/ownict_table_4.px','query_path':'Own_laptop.json', 'age':features.age_group_2},
           'Ownership of Functional Mobile':{'extension':'ICT/ownmobile_table.px','query_path':'Own_functional_mobile.json','age':features.age_group_2},
           },
    'Water and Sanitation': {'Ownership of Laptops':{'extension': 'ICT/ownict_table_4.px','query_path':'Own_laptop.json'},
           'Ownership of Functional Mobile':{'extension':'ICT/ownmobile_table.px','query_path':'Own_functional_mobile.json'},
           },
    

}

categories = warehouse.keys()