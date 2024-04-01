def main():
    
    # Import
    import tools as tool
    import os
    from dbhandler import DbHandler
    

    # get keys & database handler
    tool.configure()
    key_ninjas = os.getenv("key_ninjas")
    
    dbhandler = DbHandler("database.db")

    
    # create database basics
    dbhandler.create_base()

    
    # get capitals & countries
    capitals_json = tool.send_request("https://restcountries.com/v2/all")


    # clean/fix the result
    indexes = tool.check_key_exists(capitals_json, "capital")

    for i in indexes:
        capitals_json[i]["capital"] = capitals_json[i]["name"]
        if capitals_json[i]["name"] == "Heard Island and McDonald Islands":
            capitals_json[i]["capital"] = "McDonald Islands"
            

    # ask user -> clean the old data from DB or no
    user_input = input("\033[93mIf you want to clean the database enter 'y' or enter anything to continue.\033[0m\n")
    if user_input == "y":
        dbhandler.clean_db()
        print("Database cleaned")

    # find the last inserted data
    qry = "SELECT max(cc_id) FROM capital_cities;"
    last_record = dbhandler.execute(qry, mode="table")
    last_record = last_record[0][0]
    
    if last_record == None:
        last_record = 0
        
    remaining_records = len(capitals_json)-last_record
    
    # start/resume inserting new data from api
    for i in range(remaining_records):
        i += last_record

        country = capitals_json[i]["name"]
        capital = capitals_json[i]["capital"]
        
        # get lat & lon
        url= "https://api.api-ninjas.com/v1/geocoding"
        parameters = {"city":capital}
        headers= {'X-Api-Key': key_ninjas}
        
        print(i+1)
        ll_json = tool.send_request(base_url=url, parameters=parameters, headers=headers)

        try:
            
            lat = ll_json[0]["latitude"]
            lon = ll_json[0]["longitude"]

            # save data in DB
            qry_insert = """
                INSERT INTO capital_cities (name, country, lat, lon) 
                VALUES(?, ?, ?, ?);
            """
            parameters = (capital, country, lat, lon)

            dbhandler.execute(query=qry_insert, parameters=parameters)

        except IndexError:
            tool.error_msg(f"couldent find lat and lon for: {capital}")
            continue
        # pause
        tool.sleep_timer(0.5, 1.5)
    
    tool.error_msg("Opration Finnished.")
        
main()