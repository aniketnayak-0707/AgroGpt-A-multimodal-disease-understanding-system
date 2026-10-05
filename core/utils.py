def format_class_name(class_name):
    crop, disease = class_name.split("___")
    return f"{crop.capitalize()} - {disease.replace('_',' ').capitalize()}"