def cleanNutrition(nutritional_info):
    nutrition = {}
    try:
        calories = nutritional_info['nutrition']['nutrients'][0]
        nutrition['calories'] = calories
    except:
        nutrition['calories'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }
    try:
        fat = nutritional_info['nutrition']['nutrients'][1]
        nutrition['fat'] = fat
    except:
        nutrition['fat'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }

    try:
        saturated_fat = nutritional_info['nutrition']['nutrients'][2]
        nutrition['saturated_fat'] = saturated_fat
    except:
        nutrition['saturated_fat'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }

    try:
        carbohydrates = nutritional_info['nutrition']['nutrients'][3]
        nutrition['carbohydrates'] = carbohydrates
    except:
        nutrition['carbohydrates'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }

    try:
        sugar = nutritional_info['nutrition']['nutrients'][5]
        nutrition['sugar'] = sugar
    except:
        nutrition['sugar'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }

    try:
        cholesterol = nutritional_info['nutrition']['nutrients'][6]
        nutrition['cholesterol'] = cholesterol
    except:
        nutrition['cholesterol'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }
    try:   
        sodium = nutritional_info['nutrition']['nutrients'][7]
        nutrition['sodium'] = sodium
    except:
        nutrition['sodium'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }
    try:
        protein = nutritional_info['nutrition']['nutrients'][8]
        nutrition['protein'] = protein
    except:
        nutrition['protein'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }
    try:       
        vitaminC = nutritional_info['nutrition']['nutrients'][9]
        nutrition['vitaminC'] = vitaminC
    except:
        nutrition['vitaminC'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }
    try:   
        fiber = nutritional_info['nutrition']['nutrients'][11]
        nutrition['fiber'] = fiber
    except:
        nutrition['fiber'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }

    try:
        iron = nutritional_info['nutrition']['nutrients'][21]
        nutrition['iron'] = iron
    except:
        nutrition['iron'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }

    try:
        calcium = nutritional_info['nutrition']['nutrients'][22]
        nutrition['calcium'] = calcium
    except:
        nutrition['calcium'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }

    try:
        vitaminA = nutritional_info['nutrition']['nutrients'][23]
        nutrition['vitaminA'] = vitaminA
    
    except:
        nutrition['vitaminA'] =  {
                "title": "-",
                "amount": "-",
                "unit": "-",
                "percentOfDailyNeeds": '-'
            }   
    
    return nutrition


symptoms = ['acid reflux', 'diarrhea', 'constipation', 'heart burn', 'bloating', 'naseau', 'gas', 'upset stomach', 'abdominal pain', 'cramps', 'vomitting']