# Docker: add credentials through environment variables
import re
import sys
import logging
from time import sleep, time
from pymongo import MongoClient
from pprint import pprint
from utils import create_dict, float_int_check, query_to_csv, get_filenames


# Table names
main_doc_name = "main_public"
main_table_name = "znoexam"
helper_table_name = "status_tracker"

# Logger init
logging.basicConfig(level=logging.DEBUG, filename='mongo_db_log.log', format='%(asctime)s %(levelname)s:%(message)s')


def create_connection(reconn_num = 10, **conn_params):
    client = None
    
    for idx in range(reconn_num + 1):
        try:
            client = MongoClient(
                                host=conn_params.get('host'),
                                port=conn_params.get('port')
                                )
            print("Connection created.")
            logging.info("Connection created.")
            break
        except:
            #print(f"Connection errors: {e}", end = '\r')
            if idx != reconn_num:
                logging.error(f"Connection error. Try to reconnect. Try {idx + 1}")
                print(f"Connection error. Try to reconnect. Try {idx + 1}")
                sleep(2)
    
    return client

def insert_data_mongo(client, zno_table, tracker, filenames, batch_size = 1000, **conn_params):
    idx = 0
    helper_row = 0
    if tracker.find_one() is None:
        tracker.insert_one({"batch_index": 0})
    else:
        helper_row = tracker.find_one().get("batch_index")

    start_time = time()
    for filename in filenames:
        exam_year = re.findall(r'\d+', filename)[0]
        with open(filename, 'r', encoding="cp1251") as csv_data:
            csv_line = csv_data.readline()
            col_name = csv_line.strip().replace('"', '').replace(',', '.').split(";")
            col_name.append("examyear")
            col_name = [elem.lower() for elem in col_name]
            while csv_line != "":
                batch_dict_arr = []
                for i in range(batch_size):
                    csv_line = csv_data.readline()
                    if csv_line is None or csv_line == "":
                        logging.debug("End of file reached")
                        break

                    if helper_row > idx:
                        idx += 1
                        continue

                    line_to_insert = csv_line.strip().replace('"', '').replace(',', '.').split(";")
                    line_to_insert.append(exam_year)
                    line_to_insert = [None if elem == "null" else float_int_check(elem) for elem in line_to_insert]

                    batch_dict_arr.append(create_dict(col_name, line_to_insert))

                try:
                    zno_table.insert_many(batch_dict_arr)
                    logging.debug("Batch inserted")
                    
                    # update tracker table
                    tracker.update_one({ "batch_index": idx }, {"$set": { "batch_index": idx + 1 }})
                    
                    idx += 1
                except:
                    return client, False

    end_time = time()
    print(f"INSERTION TIME: {end_time - start_time}")
    logging.info(f"INSERTION TIME: {end_time - start_time}")
    tracker.drop()

    return client, True

def db_query(collection):
    query_mongo = list(
        collection.aggregate([
        {
            "$match": {
                "engteststatus": "Зараховано"
            },
        },
        {
            "$group": {
                "_id" : {
                    "Region": "$regname",
                    "Year": "$examyear"
                },
                "Min_Result": {
                    "$min": "$engball100"
                }
            }
        }
    ])
    )

    print("Data queried.")
    logging.info("Data queried.")

    query_to_csv(query_mongo)

    print("Data added to .csv")
    logging.info("Data added to .csv")


def main():
    # Get connection params
    python_file, host, port = sys.argv
    port = int(port)

    # Get filenames
    filenames = get_filenames("data")
    if filenames == []:
        logging.error("Directory with data is empty. Exit program.")
        print("Directory with data is empty. Exit program.")
        return

    # Start connection (else: exit script)
    client = create_connection(host=host, port=port)
    if client is None:
        logging.error("Connection failed. Exit program.")
        print("Connection failed. Exit program.")
        return

    # db instance (creating or getting)
    db = client[main_doc_name]

    # Collections instances (creating ot getting)
    main_table = db[main_table_name]
    helper_table = db[helper_table_name]

    # Insert data
    client, bool_inserted = insert_data_mongo(client, main_table, helper_table, filenames, host=host, port=port)
    if not bool_inserted:
        if client is not None:
            client.close()
        logging.error("Data insertion error. Exit Program.")
        print("Data insertion error. Exit Program.")
        return

    # Query data and add to .csv
    db_query(main_table)

    # Drop collection
    main_table.drop()

    # End connection
    client.close()

if __name__ == "__main__":
    main()
