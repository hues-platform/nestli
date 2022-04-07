import os


def modify_idf_start_date(folder, day, month):
    idf_file = folder + "/UMAR.idf"
    if(os.path.exists(idf_file)):
        with open(idf_file, "r") as f:
            idf_text = f.read()
            idf_text = idf_text.replace("1,                       !- Begin Month", f"{month},                       !- Begin Month")
            idf_text = idf_text.replace("1,                       !- Begin Day of Month", f"{day},                       !- Begin Day of Month")
        with open(idf_file, "w") as f:
            f.write(idf_text)
    
