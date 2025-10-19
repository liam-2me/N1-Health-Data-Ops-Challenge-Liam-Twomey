import sqlite3 as sql


dbfile = 'n1_data_ops_challenge.db'



try:
    with sql.connect(dbfile) as conn:
        print(f"Successfully connected to {dbfile}")
        cursor = conn.cursor()

        cursor.execute("SELECT distinct count(member_id) from std_member_info WHERE eligibility_start_date <= '2025-04-01' AND eligibility_end_date >= '2025-04-31'")
        results = cursor.fetchall()
        print("the number of distinct members who had eligibility during April 2025 is: "+ str(results))

        cursor.execute("SELECT member_id, COUNT(*) from std_member_info group by member_id having count(*)>1")
        results = cursor.fetchall()
        print("the number of members included more than once is: " + str(results))

        cursor.execute("select distinct payer, count(*) from std_member_info group by payer")
        results = cursor.fetchall()
        print("The breakdown of members by payer are as follows: " + str(results))

        cursor.execute("SELECT count(*) from std_member_info a Inner join model_scores_by_zip b on a.zip_code = b.zcta WHERE b.food_access_score < 2.0")
        results = cursor.fetchall()
        print("The number of members who live in a zip code with a food access score less than 2 is: " + str(results))

        cursor.execute("SELECT avg(b.social_isolation_score) from std_member_info a inner join model_scores_by_zip b on a.zip_code = b.zcta")
        results = cursor.fetchall()
        print("The average social isolation score across all members is: "+ str(results))

        cursor.execute("Select member_id, member_first_name, member_last_name from std_member_info a inner join(SELECT zcta, max(algorex_sdoh_composite_score) from model_scores_by_zip) b on " \
        "a.zip_code = b.zcta")
        results = cursor.fetchall()
        print("The members who live in the zip code with the highest Algorex SDOH composite score are: " + str(results) )
    
      
 
       
except sql.Error as e:
    print(f"Error connecting to database: {e}")

print("Connection closed")
