import re

number_pattern = r'^\d+$'
text_pattern = r'^[A-Za-z]+$'

def validate_name(name):  
    return bool(re.match(text_pattern, name))   

def validate_input(id, name, team, number, weight):
    if re.match(number_pattern, id) and re.match(text_pattern, name) and re.match(text_pattern, team) and re.match(number_pattern, number) and re.match(number_pattern, weight):
        return True
    else:
        return False