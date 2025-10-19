import sqlite3 as sql


dbfile = 'n1_data_ops_challenge.db'
tables = ["roster_1", "roster_2", "roster_3", "roster_4", "roster_5"]

try:
    with sql.connect(dbfile) as conn:
        print(f"Successfully connected to {dbfile}")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS std_member_info")
        table_create_query = """
        CREATE TABLE std_member_info (
            member_id INT PRIMARY KEY,
            member_first_name VARCHAR(50),
            member_last_name VARCHAR(50),
            date_of_birth DATE,
            main_address VARCHAR(250),
            city VARCHAR(250),
            state VARCHAR(50),
            zip_code char(10),
            payer VARCHAR(50),
            eligibility_start_date DATE,
            eligibility_end_date DATE
    );
"""     
        cursor.execute(table_create_query)
        for table in tables:
            insert = """INSERT INTO std_member_info (member_id,member_first_name,member_last_name,date_of_birth,main_address,city,state,zip_code,payer,eligibility_start_date,eligibility_end_date)
                    SELECT a.Person_Id, a.First_Name, a.Last_Name, a.Dob, a.Street_Address, a.State, a.City, a.Zip, a.payer, a.eligibility_start_date, a.eligibility_end_date FROM """+table+""" a LEFT OUTER JOIN std_member_info t on a.person_id = t.member_id
                    WHERE t.member_id IS NULL AND strftime('%Y',a.eligibility_start_date) <= strftime('%Y',current_date) AND (strftime('%Y',a.eligibility_end_date) >= strftime('%Y',current_date) OR a.eligibility_end_date IS NULL); """#-- Eligibility ends in or after the current year, or is ongoing
            cursor.execute(insert)
            conn.commit()
            

except sql.Error as e:
    print(f"Error connecting to database: {e}")

print("Connection Closed.")
