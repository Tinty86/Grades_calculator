def write_it_in_red(text: str):
    print(f"\033[91m{text}\033[00m")

def can_var_be_float(variable): 
    try:
        float(variable)
        return True
    except:
        return False