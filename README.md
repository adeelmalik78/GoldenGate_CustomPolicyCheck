# Python Policy Checks for detecting changes to GoldenGate-replicated tables
This repository shows Python Policy Check for detecting changes to tables (ALTER | DROP | CREATE INDEX) that are being replicated in GoldenGate. 

A sample changelog, [changelog.sql](changelog.sql), is provided to show various DDL changes applied to multiple tables in the database.

A [GGTables.txt](GGTables.txt) file contains a list of tables that are replicated in GoldenGate (one table name per line).


# ✔️ Pre-Execution Steps
1. Java 17 or higher is required. 
1. Download the latest version of [Liquibase](https://www.liquibase.com/download-secure). Beginning with version 4.31.0, the policy check jar is included. Older versions require the latest [checks jar](https://repo1.maven.org/maven2/org/liquibase/ext/liquibase-checks/) to be placed inside the liquibase/lib folder.
1. Ensure this environment variable or setting is set to enable custom policy checks.<br>
    *Environment variable*
    ```
    LIQUIBASE_COMMAND_CHECKS_RUN_CHECKS_SCRIPTS_ENABLED='true'
    ```
    *liquibase.properties*
    ```
    checks-scripts-enabled=true
    ```

# Configuring Python Policy Checks
1. To aid in debugging, it's useful to disable all other policy checks.
    ```
    % liquibase checks bulk-set --disable
    ```
1. Create a new policy check based on the Python script: 
    ```
    % liquibase checks customize --check-name=CustomCheckTemplate
    ```

|Prompt| Input |
|----------|-----------------------|
|Short name|`CheckGoldenGateTables`|
|Severity| `<0,1,2,3,4>`|
|Script Description|`This script checks for table names that appear in GGTables.txt file`|
|Script Scope|`CHANGELOG`|
|Script Message|`<blank>`|
|Script Path|`Python/Scripts/CheckGoldenGateTables.py`|
|Script Args|`<blank>`|
|Requires Snapshot|`false`|

# Running the check
In you CICD pipeline, you will run the following command:
    `liquibase checks run`

This is what policy checks will detect when it encounters SQL making changes to tables that are mentioned in `GGTables.txt`.
```
Checks-settings File:      liquibase.checks-settings.conf
=========================================================
CHANGELOG CHECKS
----------------
Checks completed validation of the changelog and found the following issues:

Check Name:         Custom Check Template (CheckGoldenGateTables)
Changeset ID:       addressses_pk
Changeset Filepath: changelog.sql
Check Severity:     MINOR (Return code: 1)
Message:            ALTER TABLE: "ADDRESSES" appears in GGTables.txt - This is a GoldenGate-replicated table.

Check Name:         Custom Check Template (CheckGoldenGateTables)
Changeset ID:       orgs_index_industry
Changeset Filepath: changelog.sql
Check Severity:     MINOR (Return code: 1)
Message:            CREATE INDEX: "ORGANIZATIONS" appears in GGTables.txt - This is a GoldenGate-replicated table.

Check Name:         Custom Check Template (CheckGoldenGateTables)
Changeset ID:       orgs_index_name
Changeset Filepath: changelog.sql
Check Severity:     MINOR (Return code: 1)
Message:            CREATE INDEX: "ORGANIZATIONS" appears in GGTables.txt - This is a GoldenGate-replicated table.

Check Name:         Custom Check Template (CheckGoldenGateTables)
Changeset ID:       orgs_rank
Changeset Filepath: changelog.sql
Check Severity:     MINOR (Return code: 1)
Message:            ALTER TABLE: "ORGANIZATIONS" appears in GGTables.txt - This is a GoldenGate-replicated table.
```

# 📒 Notes
1. Scripts are called once for each changeset (changelog scope) or once for each database object (database scope). Changesets may contain multiple SQL statements.
1. The print() function can be used to display debugging messages (instead of just liquibase_logger). This works regardless of log_level. Additionally, f strings automatically convert variables for printing and remove the need for concatenation to build a string of static and dynamic text.
    ```
    my_int = 123
    my_str = "Hello World!"
    print(f"{my_str} My variable is: {my_int}")
    ```
    f strings can also be used wherever strings are expected.
    ```
    my_int = 123
    liquibase_status.message = f"My variable is: {my_int}"
    ```
1. The latest [Liquibase provided modules](https://docs.liquibase.com/secure/user-guide-5-1/what-are-some-examples-of-custom-policy-check-scripts) can be imported into your checks to access Liquibase provided functions.
    ```
    import liquibase_utilities
    import liquibase_changesets

    print(liquibase_changesets.get_labels(liquibase_utilities.get_changeset()))
    ```
1. LoadData change types are not currently supported. 
1. Environment variables can be accessed using the os module.
    ```
    import os

    print(os.environ.get("LIQUIBASE_COMMAND_URL"))
    ```

# 🐍 Local Python Environment
⚠️ *Not required to use or develop custom policy checks*

[Setup a Virtual Python Environment for Liquibase Policy Checks](https://docs.liquibase.com/secure/deliver-changes-6-0/set-up-a-custom-python-virtual-environment-for-liquibase-policy-checks)