###
### This script checks for uppercase table names during creation
###
### Notes:
### 1. Only basic CREATE statements are supported

###
### Helpers come from Liquibase
###
import sys
import liquibase_utilities


### Read GGTables.txt
with open("GGTables.txt", "r", encoding="utf-8") as file:
    GGTables = file.read()

###
### Retrieve log handler
### Ex. liquibase_logger.info(message)
###
liquibase_logger = liquibase_utilities.get_logger()

###
### Retrieve status handler
###
liquibase_status = liquibase_utilities.get_status()

###
### Retrieve all changes in changeset
###
changes = liquibase_utilities.get_changeset().getChanges()

###
### Loop through all changes
###
for change in changes:
    ### Split sql into a list of strings to remove whitespace
    ###
    sql_list = liquibase_utilities.generate_sql(change).split()
    ###
    ### Locate "alter table" in list
    ### This handles most ALTER TABLE statements including ADD COLUMN, DROP COLUMN, MODIFY COLUMN, PRIMARY KEY, FOREIGN KEY
    ###
    if "alter" in map(str.casefold, sql_list) and "table" in map(str.casefold, sql_list):
        index_table = [token.lower() for token in sql_list].index("table")
        if index_table + 1 < len(sql_list):
            table_name = sql_list[index_table + 1]
            # print(f"ALTER: Table name: {table_name}")
            if table_name.upper() in GGTables.upper():
                liquibase_status.fired = True
                status_message = f"ALTER TABLE: \"{table_name}\" appears in GGTables.txt - This is a GoldenGate-replicated table."
                liquibase_status.message = status_message
                sys.exit(1)

    ###
    ### Locate "drop table" in list
    ###
    if "drop" in map(str.casefold, sql_list) and "table" in map(str.casefold, sql_list):
        index_table = [token.lower() for token in sql_list].index("table")
        if index_table + 1 < len(sql_list):
            table_name = sql_list[index_table + 1]
            # print(f"DROP: Table name: {table_name}")
            if table_name.upper() in GGTables.upper():
                liquibase_status.fired = True
                status_message = f"DROP TABLE: \"{table_name}\" appears in GGTables.txt - This is a GoldenGate-replicated table."
                liquibase_status.message = status_message
                sys.exit(1)

    ###
    ### Locate "create index XXX on ..." in list
    ###
    if "create" in map(str.casefold, sql_list) and "index" in map(str.casefold, sql_list):
        index_table = [token.lower() for token in sql_list].index("index")
        if index_table + 3 < len(sql_list):
            table_name = sql_list[index_table + 3].split('(')[0]
            # print(f"CREATE INDEX: Table name: {table_name}")
            if table_name.upper() in GGTables.upper():
                liquibase_status.fired = True
                status_message = f"CREATE INDEX: \"{table_name}\" appears in GGTables.txt - This is a GoldenGate-replicated table."
                liquibase_status.message = status_message
                sys.exit(1)

###
### Default return code
###
False