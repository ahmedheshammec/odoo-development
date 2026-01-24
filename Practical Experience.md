## psql Basics

**Create postgres role**

```shell
psql postgres
CREATE ROLE postgres WITH SUPERUSER LOGIN PASSWORD 'postgres';
ALTER USER odoo18 WITH SUPERUSER; # command to alter user
---------
GRANT ALL PRIVILEGES ON DATABASE eqnaa TO odoo18;
ALTER DATABASE <Your DB Name> OWNER TO odoo18;
---------
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO odoo18;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO odoo18;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO odoo18;

```

→ Type \q to exit psql.

→ Now Try:

```shell
psql -U postgres
psql -U postgres -c "\du"
psql -U postgres -c "\l"
```

**Restore SQL DUMP**

```bash
createdb mydb
cd /tmp # in linux
sudo su - postgres (press enter) # in Linux
psql # in Linux
--------------
sudo -u postgres psql # in linux
CREATE DATABASE <db_name>; # in Linux
psql mydb < dump.sql
sudo -u postgres psql mydb < dump.sql # in Linux

--------------
sudo -u postgres createdb -O <user> <database> # in Linux
psql sheffield_live # in MacOS
sudo -u postgres psql <database> < dump.sql # in Linux
```

✅ You should not use the Odoo UI to create the database first, unless you’re trying to create a template db with specific modules preinstalled. For simple dump restoration, just use the CLI.

To open the **current working directory (cwd)** in the default **Linux file manager (folder viewer)**, you can use one of the following command

```bash
xdg-open .
```

→ Change The Owner to Match The Original DB

```bash
psql -U postgres
ALTER DATABASE <Your DB Name> OWNER TO odoo13;
\q
```

**How to Know the Right Version of Odoo for the dump.sql File?**

→ After the restore connect to postgres: 

```bash
psql -U postgres
```

→ Then connect the the db: 

```bash
\c mydb
```

→ You'll see something like: `You are now connected to database <db_name>`

→ Next run this command:

```sql
SELECT latest_version FROM ir_module_module WHERE name = 'base';
```

→ You'll See Something like This:

```
 latest_version
----------------
 16.0.1.3
(1 row)
```

→ Query to print db name: 

```sql
SELECT current_database();
```

#### Reset / Change DB Password

```bash
psql -U postgres
\c db_name
-------
psql -U postgres -d db_name
-------
psql -U postgres db_name
```

→ Now we need to change the password of the Admin user. If you don’t remember the user’s email value (which is used as the login), execute the following command to get a list of all user logins.

```bash
select login from res_users;
```

→ Finally, change the password value of the Admin user to the newly generated one:

```bash
update res_users set password = 'admin' where login = 'admin';
```

→ Refresh the page and enter the email & pass as `admin`

**List All Databases and Users, and Redirect the Output Into a Text File**

```bash
# Show all databases and save to databases_and_users.txt
psql -U postgres -c "\l" > databases_and_users.txt

# Append the list of users to the same file
psql -U postgres -c "\du" >> databases_and_users.txt
```

**Database Duplication Best Practices 💾**

For a **production-ready migration**, I strongly recommend the **dump/restore approach**:

```bash
# Create dump
pg_dump -h localhost -U odoo_user -d current_db_name > backup_before_confirmation.sql

# Create new database
createdb -h localhost -U odoo_user new_db_name

# Restore
psql -h localhost -U odoo_user -d new_db_name < backup_before_confirmation.sql
```

**Using Odoo Shell to Create Backup**

→ First connect to the db

```bash
./odoo-bin shell -d <db_name>
```

```py
import odoo
from odoo.service import db
db.dump_db('<db_name>', '/path/to/file.zip')
exit()
```

→ chang `<db_name>` & `file` with the actual names. 

```shell
curl -X POST \
  -F 'master_pwd=admin123' \
  -F 'name=test' \
  -F 'backup_format=zip' \
  -o italk.zip \
  http://38.114.122.29:8069/web/database/backup
```

**Filestore Location On MacOS**

```
~/Library/Application Support/Odoo/filestore/<db_name>
```

**Find Filestore on Your System**

```shell
sudo find / -type d -iname "ollama" 2>/dev/null # Mac OS
sudo find / -type d -iname "ollama" # Linux
```

**Useful Commands**

| Command                                                      | Function                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| \du                                                          | show roles and users                                         |
| \q                                                           | exit psql                                                    |
| \l                                                           | list all database                                            |
| q                                                            | exit list database mode                                      |
| createdb -U <db_user> <db_name>                              | Create DB with a Specific User                               |
| dropdb -U <db_user> <db_name>                                | Delete DB                                                    |
| ALTER ROLE postgres WITH SUPERUSER LOGIN PASSWORD 'postgres'; | Changes the Password for the User [postgres] to be [postgres] |
| brew services stop postgresql@16                             | This Will Stop the Postgres Service                          |
| brew services restart postgresql@16                          | This Will Restart the Postgres Service                       |

---

## How To Run SQL Queries Inside Odoo Shell? 

```py
cr = env.cr
cr.execute("DELETE FROM ir_attachment WHERE name LIKE 'web.assets_%';")
env.cr.commit()
```

## Local Server Commands

```bash
sudo chmod 644 /opt/odoo/odoo.conf
sudo chown odoo:odoo /opt/odoo/odoo.conf

tail -n 20 /var/log/odoo.log
# or
tail -20 /var/log/odoo.log
sudo tail -f /var/log/odoo/odoo18.log # realtime updates

sudo systemctl status odoo
sudo systemctl daemon-reload
sudo systemctl restart odoo
sudo systemctl stop odoo
sudo systemctl start odoo
```

---

### Usin Odoo Shell & SQL to Get the Right Module Dependency Technical Name

**Shell Method**

```py
print(env['res.partner'].__class__._original_module)
```

→ Replace 'res.partner' with any module.

**SQL Method**

```sql
SELECT imd.module
FROM ir_model_data imd
JOIN ir_model im ON im.id = imd.res_id
WHERE im.model = 'product.category'
    AND imd.model = 'ir.model'
LIMIT 1;
```

---

## How to Uninstall a module through Odoo Shell?

use the following snippet: 

```python
module = env['ir.module.module'].search([('name', '=', 'module_technical_name')], limit=1)
module.button_immediate_uninstall()
```

→ If you want to uninstall multiple modules

```python
modules = env['ir.module.module'].search([
    ('name', 'in', ['module_one', 'module_two'])
])
modules.button_immediate_uninstall()
```

---

## Install Venv for Any Odoo The Right Way (Odoo 16 or Lower)

1- start by creating a virtual environment then activate it using a recommended python version for the odoo server you want to run 

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip list

grep -vE '^\s*#|^\s*$' requirements.txt | while read req; do pkg=$(echo "$req" | cut -d'=' -f1 | cut -d'<' -f1 | cut -d'>' -f1); pip show "$pkg" >/dev/null || echo "$req"; done > remaining_requirements.txt

pip install -r remaining_requirements.txt

grep -ri lxml requirements.txt
grep -ri werkzeug requirements.txt
pip install "werkzeug==xxxx"

./odoo-bin -c odoo.conf -i base
```

2- If You Encountered a Problem Like This: `ValueError: current limit exceeds maximum limit`  Add the Following Lines in the Config:

```
limit_memory_hard = 0
limit_memory_soft = 0
```

:: __`Fixing AttributeError: module 'werkzeug' has no attribute '__version__' Error `__ ::

```bash
source .venv/bin/activate
pip uninstall werkzeug -y
pip install werkzeug==xx.xx.xx
```

→ See the compatible version from the requirements.txt file.

:: __`Fixing X509_V_FLAG_NOTIFY_POLICY Error `__ ::
The problem is with cryptography and pyopenssl libraries.change requirements.txt as:
go to terminal and:

```bash
pip uninstall pyopenssl -y
pip install pyopenssl==22.0.0
pip uninstall cryptography -y
pip install cryptography==37.0.0
```

:: __`Fixing DeprecationWarning: invalid escape sequence '\ ' Error `__ ::

→ This error happens when you put the odoo enterprise addons location in the config; we need to edit some manifest files

→ Run the Following Python Code: 

```python
#!/usr/bin/env python3
import os
import re

def find_invalid_escapes(directory):
    """Find manifest files with invalid escape sequences in the given directory"""
    results = []
    
    for root, dirs, files in os.walk(directory):
        if "__manifest__.py" in files:
            manifest_path = os.path.join(root, "__manifest__.py")
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for strings containing backslash+space
            if re.search(r'["\'][^"\']*\\\\?\s[^"\']*["\']', content):
                results.append(manifest_path)
                print(f"Found potentially problematic file: {manifest_path}")
                
    return results

if __name__ == "__main__":
    # Replace these paths with your actual Odoo paths
    paths_to_check = [
        "/Volumes/Samsung T5/Odoo/Development & Study/odoo-17/custom-addons",
        "/Volumes/Samsung T5/Odoo/Development & Study/odoo-17/enterprise-17.0-main"
    ]
    
    all_results = []
    for path in paths_to_check:
        if os.path.exists(path):
            print(f"Checking {path}...")
            results = find_invalid_escapes(path)
            all_results.extend(results)
        else:
            print(f"Path doesn't exist: {path}")
    
    if all_results:
        print("\nPotentially problematic manifest files found:")
        for file_path in all_results:
            print(f"- {file_path}")
        
        print("\nTo fix these files, open each one and:")
        print("1. Replace '\\' followed by space with just a space, or")
        print("2. Use raw strings (prefix with 'r') for paths containing backslashes, or")
        print("3. Use double backslashes '\\\\' instead of single ones")
    else:
        print("\nNo manifest files with obvious invalid escape sequences found.")
        print("You may need to manually check files with complex string patterns.")

```

→ Don't forget to change the paths to the odoo enterprise path you have problem with

→ so i run the script `Find Invalid Escapes` in this directory (Made by Claude Ai) and it returned some resutls like this: 

```

Potentially problematic manifest files found:
- /Volumes/Samsung T5/Odoo/Development & Study/odoo-17/enterprise-17.0-main/account_bank_statement_import_qif/__manifest__.py
- /Volumes/Samsung T5/Odoo/Development & Study/odoo-17/enterprise-17.0-main/account_bank_statement_import_csv/__manifest__.py
- /Volumes/Samsung T5/Odoo/Development & Study/odoo-17/enterprise-17.0-main/account_bank_statement_import_ofx/__manifest__.py
- /Volumes/Samsung T5/Odoo/Development & Study/odoo-17/enterprise-17.0-main/delivery_ups/__manifest__.py

To fix these files, open each one and:
1. Replace '\' followed by space with just a space, or
2. Use raw strings (prefix with 'r') for paths containing backslashes, or
3. Use double backslashes '\\' instead of single ones
```

→ so i opened the manifest files the script suggested and added the raw string before the tripple quotes like this: 

![image](imgs/add_raw_string_fix.png)

**UI Database Manager Link**

http://localhost:8069/web/database/manager

**Connect Directly to a Specific DB from the UI**

http://localhost:8069/web/?db=mydb

#### Change Password for a DB

```bash
psql postgres
\c db_name
```

→ Now we need to change the password of the Admin user. If you don’t remember the user’s email value (which is used as the login), execute the following command to get a list of all user logins.

```bash
select login from res_users;
```

→ Finally, change the password value of the Admin user to the newly generated one:

```bash
update res_users set password = 'admin' where login = 'admin';
```

→ Refresh the page and enter the email & pass as `admin`

---

### How to Run Odoo Server with a Different Port than the One Written in the Config? 

This is useful for multiple odoo instance running without changing anything in the config file

→ example

```bash
./odoo-bin -c odoo.conf --http-port=8069
```

---

# Github

### Odoo Github Links

→ Community

> https://github.com/odoo/odoo

→ Enterprise 

> https://github.com/odoo/enterprise

### How to Link Github to Odoo Enterprise Private Branch? 

1- Go to odoo.com and sign in with your account. 

2- Scroll Down until you see `Useful Links` section. and click on `Partner Dashboard`

3- Under Develop & Deplopy You'll see `Enterprise Github Access` where you can Github Usernames. 

4- After you add the user name make sure there's `read` next to it. and wait for 15 Min until odoo sends an invitation. then you can view the enterprise link mentioned above.

### Command to Clone Odoo

→ Community

```bash
git clone \
  --branch 15.0 \
  --single-branch \
  --depth 1 \
  git@github.com:odoo/odoo.git odoo15.0
```

→ Enterprise

```bash
git clone \
  --branch 15.0 \
  --single-branch \
  --depth 1 \
  git@github.com:odoo/enterprise.git enterprise
```



## Show All Git Branches After Cloning a Github Project

**List remote branches**

```bash
git branch -r | cat
```

**List all branches (local + remote)**

```bash
git branch -a | cat
```

**Fetch all branches**

```bash
git fetch --all
```

**Checkout and track a remote branch**

```
git checkout <branch>
```

**or (modern)**

```bash
git switch <branch>
```

**Manually set upstream if needed**

```bash
git branch --set-upstream-to=origin/<branch> <branch>
```

---

### How to add .DS_Store to Git Ignore File? 

```bash
# 1️⃣ Create or update .gitignore to exclude .DS_Store files
echo ".DS_Store" >> .gitignore

# 2️⃣ Untrack all .DS_Store files currently tracked by Git
git ls-files | grep .DS_Store | xargs git rm --cached

# 3️⃣ Add and commit the changes
git add .gitignore
git commit -m "Remove .DS_Store files and update .gitignore"

# 4️⃣ Push to your branch (replace <branch> if not 'main')
git push origin <branch>
```

### Untrack .DS_Store File from Git

```bash
git rm --cached .DS_Store
```

If .DS_Store exists in multiple folders use this: 

```bash
find . -name ".DS_Store" -print

find . -name ".DS_Store" -exec git rm --cached {} +

git commit -m "chore: remove all .DS_Store files and ignore them"

git push origin Test
```

### How to Remove .DS_Store from all previous commits like it didn't exist?

**1. Go back to your latest work:**

```bash
git checkout -f main
```

**2. Use a "Rebase" to scrub the file from the beginning:** We are going to tell Git to go back to the start and act as if that file was never added.

```bash
git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch .DS_Store" \
--prune-empty --tag-name-filter cat -- --all
```

*(This command looks scary, but it just tells Git: "Go through every commit in my history and remove `.DS_Store` from the records.")*

**3. Cleanup the backup Git made:**

```bash
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now
```

**Why this works**

By doing this, you aren't just ignoring the file; you are **deleting it from the timeline.** * When you `git checkout e74cf98`now, `.DS_Store` won't be there as a "tracked" file.

- Git won't care if macOS creates a new one, because your Global Ignore will finally kick in for an untracked file.

**A much simpler "Workaround"**

If you don't want to mess with history, you can just get into the habit of using the **"Discard and Switch"** command whenever you move between commits:

```bash
git checkout -f main
```

The `-f` (force) is your "I don't care about .DS_Store" button. It tells Git to overwrite any local changes with the version of the files in the branch you are moving to.

### How to remove and untrack `__pycache__` files from git? 

→ First We'll Add the Following to `.gitignore`

```bash 
printf "\n# Python cache\n**/__pycache__/\n" >> .gitignore
```

→ Check

```bash
tail -n 5 .gitignore
git ls-files | grep __pycache__
```

→ Untrack 

```bash
git rm -r --cached sale_edits/**/__pycache__/
```

`PS` the `sale_edit` is an example of a module and it showed in the previous `git ls-files | grep __pycache__` command so we're untracking it from this folder. 

→ Add

```bash
git add .gitignore
git commit -m "chore: remove tracked python cache files and ignore __pycache__"
```

→ Check Again

```bash
git ls-files | grep __pycache__
```

Nothing should be printed in this command and you can push safely.

**Better Approach for using the git rm -r --cached command**

→ instead of using this command: 

```bash
git rm -r --cached sale_edits/**/__pycache__/
```

which works only for sale_edits module we can do the following 

```bash
git rm -r --cached .
git add .
```

🧪 Verification (always do this)

```bash
git ls-files | grep -E "__pycache__|\.pyc"
```

→ should output **nothing**

---

### How to View All the Git Log, Print it in Terminal and Copy it to the Clipboard?

use this command: 

```bash
git log --all | tee /dev/tty | pbcopy
```

or if you want to limit to the last 5 commits only type: 

```bash
git log -5 --all | tee /dev/tty | pbcopy
```



---

**Odoo Shell Command to Install Bulk Modules through Odoo Shell**

```py
# In Odoo shell
env = self.env

modules_to_install = [
    'add_fields_attendence',
    'attendance_treatment',
    'custom_contracts',
    'custom_hr_employee',
    'custom_hr_recruitment_custom',
    'custom_pin_and_iden',
    'custom_portal',
    'custom_portal_enhancment',
    'dynamic_trial_balance',
    'edit_employee',
    'edit_in_hr_employe',
    'employee_analytic_report',
    'hr_attendance_management',
    'hr_leave_customs',
    'hr_payroll_customs',
    'hr_zk_integration',
    'loans_and_addvance',
    'resignation_request',
    'rm_hr_attendance_sheet',
    'warning_employee',
]

# --- Step 1: Disable all crons ---
print("⏸️ Disabling all scheduled actions...")
env.cr.execute("UPDATE ir_cron SET active = false")
env.cr.commit()

# --- Step 2: Install modules one by one ---
for module_name in modules_to_install:
    module = env['ir.module.module'].search([('name', '=', module_name)], limit=1)
    if not module:
        print(f"⚠️ Module {module_name} not found.")
        continue
    if module.state in ('installed', 'to install'):
        print(f"✅ {module_name} already installed or queued.")
        continue
    try:
        module.button_immediate_install()
        env.cr.commit()
        print(f"✅ Successfully installed {module_name}")
    except Exception as e:
        env.cr.rollback()
        print(f"❌ Failed to install {module_name}: {e}")

# --- Step 3: Re-enable all crons ---
print("▶️ Re-enabling scheduled actions...")
env.cr.execute("UPDATE ir_cron SET active = true")
env.cr.commit()

print("🎉 All done!")
```

**Pro Tip**: use the following zsh function: 

```bash
modules() {
    printf "modules_to_install = [\n%s\n]" "$(ls -d */ | sed "s#/##" | awk '{printf "    \047%s\047,\n", $0}' | sed '$s/,$//')"| pbcopy
}
```

→ You can now type `modules` in the directory to get the `modules_to_install` section of the command. 

---

**Odoo Shell Command to Show all installed modules that's not odoo's stock modules (Author != Odoo S.A.)**

```py
env = self.env
[(m.name, m.author) for m in env['ir.module.module'].search([
    ('state', '=', 'installed'),
    ('author', '!=', 'Odoo S.A.')
], order='name')]
```

**Note**: some modules may be installed but doesn't appear here because they don't have author in the manifest, you can check those individually using the following command: 

```python
modules_to_check = ['iet_custom_crm', 'iet_sales_custom', 'purchase_request']
[(m.name, m.state) for m in env['ir.module.module'].search([('name', 'in', modules_to_check)])]
```

---

### How to Close Shell on Odoo.sh The Right Way?

use the following command after closing the shell:

```python
reset
exit
import sys; sys.exit() # This Didn't work
```

→ Then close the browser tab and log in again to the shell from odoo.sh shell tab you will be back at the welcome odoo.sh screen.

---

## Odoo.sh

**How to Add SSH Key to Odoo.sh**

First use this command to show your ssh-key and copy it to the clipboard 

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

 → Next add it in the sh like this: 

![image](imgs/sh_profile.png)

![image](imgs/sh_ssh_keys.png)

## How to Pull Custom Addons from Odoo.sh Using SSH?

→ Example

```shell
rsync -avz \
4020511@al-hassan-and-hussien.odoo.com:/home/odoo/src/user/ \
"/Users/ahmed/Desktop/hassan/"
```



---

### Using _logger / logging the right way

→ to get white logging data instead of the normal ones odoo uses we can use something like this: 

```py
import logging

_logger = logging.getLogger(__name__)

# ANSI escape codes
WHITE = "\033[97m"   # Bright White
RESET = "\033[0m"

# Usage
_logger.info(f"{WHITE}This is my custom log in white!{RESET}")
```

---

### Fixing PyCharm Python Interpreter

→ When you try to add an existing interpreter PyCharm sometimes act as you didn't do anything and refuses to add the interpreter

→ To fix this choose the python interpreter from the system page as follows: 

![image](imgs/choosing_system_interpreter.png)

→ From the Right side click the three dots and choose python file in your `.venv` folder

---

### How to Open Two instances of Odoo at the same time?

Let's say we want to open odoo 13 and odoo 17 at the same time, to do this we need to set a different port at the config file like this: 

```
[options]
xmlrpc_port = 8071
```

→ We used port 8071 with odoo 17 and the normal 8069 with odoo 13 

---

### How to Remove PyCharm Yellow Warnings Lines

→ Step 1 👇

![image](imgs/remove_pycharm_warnings_lines.png)

→ Step 2 👇

![image](imgs/remove_effects.png)

---



### How to Create a Fresh DB for a Specific Version of Odoo without Demo Data?

→ Let's say we want to create a db that fits odoo 17 schema; to do this we will create the db using this command:

```
createdb -U odoo bay17-clean
```

→ Next we wil use the following command to install the modules: 

```shell 
./odoo-bin -c bahy_clean.conf -i base,contacts,account_accountant,sale_management,stock,purchase,point_of_sale --without-demo=all 
```

→ In the config we set the `db_name = bahy17-clean`

---

### How to Open Odoo in Shell Mode

→ This is useful for debugging; first you need to `cd` into odoo directory, then:

```shell
source .venv/bin/activate
./odoo-bin shell -c <your_config_file> --limit-memory-hard=0 --limit-memory-soft=0
```

→ Use the `limit-memory` flags if you get errors like this: 

`ValueError: current limit exceeds maximum limit`

→ Test Command to Check You're Connected to the Right DB

```python
print(env.cr.dbname)
```

→ Make sure to commit what you do via this command: 

```python
env.cr.commit()
```

→ Clear the Screen

```python
import os
os.system('clear')
```

→ To quite the shell mode type: 

```python
quit()
```

→ How to make a separator in Odoo Shell 

```python
print("\n" + "="*60)
```

or: 

```python
print("\n" + "#"*60)
```

or: 

```python
print("\n" + "█"*60)
```



---

### How to fix Filestore Issues when restoring db from a client?

→ The best practice is to get the filestore folder from the client; on ubuntu i found it in this location:

```
/opt/odoo/.local/share/Odoo/filestore
```

​	↪ but on my mac it can be found here:

``` 
/Users/ahmed/Library/Application Support/Odoo/filestore/
```

→ The Best practice is to make the local db name the same name the client named his db

→ You add the filestore before creating your local db you'll be testing 

→ Sometimes you'll face errors like this: 

`FileNotFoundError: [Errno 2] No such file or directory: '/Users/ahmed/Library/Application Support/Odoo/filestore/live/c5/c53002b461caaec7f03ca5ca63a171cbca200de4'`

​	↪ in this case we try to find that file on the client server using `sudo find` command

​	↪ if the file can't be found even on the client server then we will create a dummy version

​	     using the following command: 

```
echo "dummy file" > "/Users/ahmed/Library/Application Support/Odoo/filestore/live/c5/c53002b461caaec7f03ca5ca63a171cbca200de4"
```

​	↪ then restart odoo server

---

### How to Connect Your Database Through PyCharm and Run SQL Queries?

First thing click on the database icon on the right corner of PyCharm then click on the add (plus) and then type `Postgres` to choose the type of databse

![image](imgs/connect_db.png)

Next we need to set the database name and the user who created the db (odoo)

​	↪ you can check which user created the db from the `psql` cli

![image](imgs/connect_db_config.png)

→ **Note** that we left the password in the config empty cuz in the config file the `db_password = False`

→ Now select the db console from here:

![image](imgs/running_db_console.png)

→ let's run some simple queries to test if it's working: 

```sql
SELECT version();
```

​	↪ This will return the PostgreSQL server version and confirm that your SQL console is working.

```sql
SELECT name FROM res_partner LIMIT 5;
```

​	↪ This should give you a few contact names from the res.partner table
​	     which is the contact model in Odoo.

---

## Module Depends & Inherit

When declaring a dependency in the __manifest__.py file of your custom Odoo module, **you must use the technical name of the module**, **not the model name** or the label from the UI.

![image](imgs/technical_name.png)

but when you inherit in the python file to extend the view you use the model name: 

```python
_inherit = 'hr.employee'
```

→ The Name that Appears in the UI

### Update More than One Module in PyCahrm Config

→ example:

```
-u web,web_enterprise
```



## View Inheritance (Tree & Form)

**Xpath Tricks**

→ To append your field in the last place at the group that has a specific field use expression like this: 

```xml
<xpath expr="//field[@name='parent_id']/parent::group" position="inside">
```

→ where `parent_id` is the field that is original (not from inherited view) 

→ `parent::group` walks one step up the tree to the enclosing `<group>` element, and `position="inside"` drops your field as the last child of that group, no matter how many other fields were added there by the original view or by other inherited views.

**Xpath and res.config.settings**

→ when you put a new field or block in the res.config.settings first you need to add depends based on the section you want to add to. 

```py
'depends': ['purchase'],
```

→ To target the right external id of the section you want to add to click on the bug icon > edit view form > Inherited views.

![image](imgs/config_right_external_id.png)

→ you'll see each section has a specific external id for example the purchase app will have this external id: 

```xml
purchase.res_config_settings_view_form_purchase
```

→ Now how to put the new block in the last place at the form? 

❖ we use something like this: 

```xml
<xpath expr="//app[@name='purchase']" position="inside">
```

→ sometimes when we put our new block in the last place of the purchase app section (there's some block that's inheriting and not original that takes the last place) how can we insure our block is in the last place? 

❖ The Answer is simple: we use a higher priority number before the `inherit_id`: 

```xml
<field name="priority" eval="40"/>
```

→ Full Example: 

```xml
<record id="res_config_inter_company_settings" model="ir.ui.view">
    <field name="name">res.config.inter.company.settings</field>
    <field name="model">res.config.settings</field>
    <field name="priority" eval="40"/>
    <field name="inherit_id" ref="purchase.res_config_settings_view_form_purchase"/>
    <field name="arch" type="xml">
        <xpath expr="//app[@name='purchase']" position="inside">
            <block title="Inter Company Linking" name="inter_company_linking_container">
                <setting id="inter_company_linking" string="Inter Company Linking"
                         help="Inter Company Linking Between Two Companies.">
                    <div class="row">
                        <label for="source_company_id" class="col-lg-3 o_light_label"/>
                        <div class="col-lg-9">
                            <field name="source_company_id"/>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <label for="target_company_id" class="col-lg-3 o_light_label"/>
                        <div class="col-lg-9">
                            <field name="target_company_id"/>
                        </div>
                    </div>
                </setting>
            </block>
        </xpath>
    </field>
</record>
```

**How to Make The Many2One field in Settings Save it's Value through Getter and Setter Methods?**

→ Here's the corresponding python code: 

```py
class ResCompany(models.Model):
    _inherit = 'res.company'

    source_company_id = fields.Many2one(
        'res.company', string='Source company (SO)')
    target_company_id = fields.Many2one(
        'res.company', string='Target company (PO)')

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    source_company_id = fields.Many2one(
        'res.company', string='Source company (SO)', related='company_id.source_company_id', readonly=False)
    target_company_id = fields.Many2one(
        'res.company', string='Target company (PO)', related='company_id.target_company_id', readonly=False)

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['res.company'].search([]).write({
            'source_company_id': self.source_company_id.id if self.source_company_id else False,
            'target_company_id': self.target_company_id.id if self.target_company_id else False,
        })
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        company = self.env.company
        res.update(
            source_company_id=company.source_company_id.id if company.source_company_id else False,
            target_company_id=company.target_company_id.id if company.target_company_id else False,
        )
        return res
```

      1. We've added the actual fields to the res.company model, which is where the data will
      be permanently stored
      2. We've properly linked the res.config.settings fields to the company fields using the
      related attribute
      3. We've implemented the set_values method to write the values to the company records
      when settings are saved
      4. We've implemented the get_values method to retrieve the values from the company
      records when the settings form is loaded

**Detailed Exlpanation**

  1. Why we put set_values() before get_values(), does the order matter?

  The order doesn't matter for functionality. You can put them in any order. In Python
  classes, method definitions can be in any order. We could have put get_values() first
  and set_values() second - it would work exactly the same.

  2. What is the use for the res variable in both methods?

  The res variable is used to:
   - In `set_values()`: Store the result of calling the parent method, then return it at
     the end
   - In `get_values()`: Store the dictionary of values from the parent method that we'll
     add our custom values to

  Think of it as "don't break what the parent class was already doing, just add our stuff
  to it."

  3. Line-by-line explanation:

```py
def set_values(self):
  			# Call the parent class's set_values method to preserve existing functionality
    		# This ensures we don't break any other settings that Odoo handles
        res = super(ResConfigSettings, self).set_values()
        
        # Write our custom field values to the company records
        # self.env['res.company'].search([]) finds all companies
        # .write({}) updates them with our field values
        self.env['res.company'].search([]).write({
            'source_company_id': self.source_company_id.id if self.source_company_id else False,
            'target_company_id': self.target_company_id.id if self.target_company_id else False,
        })
        # Return the result from the parent method (usually None, but good practice)
        return res
```

```py
@api.model
    def get_values(self):
    		# Call the parent class's get_values method to get existing configuration values
      	# This returns a dictionary of all the settings Odoo already handles
        res = super(ResConfigSettings, self).get_values()
        
        # Get the current company (the one the user is configuring)
        company = self.env.company

        # Add our custom field values to the dictionary
        # update() adds new key-value pairs to an existing dictionary
        res.update(
            source_company_id=company.source_company_id.id if company.source_company_id else False,
            target_company_id=company.target_company_id.id if company.target_company_id else False,
        )
        # Return the complete dictionary with both Odoo's values and our custom values
        return res
```

**Why this pattern?**

 This is a standard Odoo pattern for extending configuration settings:

   1. Always call the parent method first - Don't break existing functionality
   2. In `set_values()`: Save your custom data to the database
   3. In `get_values()`: Load your custom data from the database
   4. Use `super()` - This calls the same method in the parent class
   5. Return what the parent returns - Maintain the expected behavior

  Think of it as:
   - `set_values()` = "When user saves settings, also save my custom fields"
   - `get_values()` = "When showing settings form, also load my custom fields"

**Why we Used `@api.model` in the get method and not in the set method?**

Think of it like this:

  **Without `@api.model`:**

```py
# This method NEEDS a specific record to work
def set_values(self):
	# self = a specific config settings record (like record #5)
	print(self.id)  # This works! We have a real record
	# Odoo calls: config_record_5.set_values()

  # With @api.model:

# This method can work WITHOUT a specific record
@api.model
def get_values(self):
	# self = the model itself, not a specific record
	print(self)  # This is the model class, not a record
	# Odoo calls: ResConfigSettings.get_values() - no specific record!
```

**Why does this matter?**

Because when Odoo loads the settings form, it doesn't start with a specific record - it needs to create the form with default values. That's why `get_values()` needs to work at the model level, not the record level.

The `@api.model` decorator tells Python: "This method doesn't need a specific record to work - it can work on the model itself."

Think of it like:
   - Without `@api.model` = "I need a specific car to drive"
   - With `@api.model` = "I can talk about cars in general without needing a specific car"

**Tree Example**

```xml
<record id="view_sale_order_tree_legacy_date" model="ir.ui.view">
    <field name="name">sale.order.tree.legacy.date</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_quotation_tree_with_onboarding"/>
    <field name="arch" type="xml">
        <xpath expr="//tree" position="inside">
            <field name="legacy_create_date" optional="show"/>
        </xpath>
    </field>
</record>
```

**Another Tree Example**

```xml
<record id="view_employee_arabic_name" model="ir.ui.view">
    <field name="name">hr.employee.tree.arabic.name</field>
    <field name="model">hr.employee</field>
    <field name="inherit_id" ref="hr.view_employee_tree"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='name']" position="after">
            <field name="arabic_name_field_employee" optional="show"/>
        </xpath>
    </field>
</record>
```

**Form Example**

```xml
<!-- Inherit the purchase order form view -->
<record id="view_purchase_order_form_inherited" model="ir.ui.view">
    <field name="name">purchase.order.form.custom</field>
    <field name="model">purchase.order</field>
    <field name="inherit_id" ref="purchase.purchase_order_form"/>
    <field name="arch" type="xml">
        <!-- Make date_planned invisible -->
        <xpath expr="//field[@name='date_planned']" position="attributes">
            <attribute name="invisible">1</attribute>
        </xpath>

        <!-- Make date_approve invisible -->
        <xpath expr="//field[@name='date_approve']" position="attributes">
            <attribute name="invisible">1</attribute>
        </xpath>

        <!-- Add date_approve field after date_order -->
        <xpath expr="//field[@name='date_order']" position="after">
            <field name="legacy_date_approve" readonly="0"/>
        </xpath>
    </field>
</record>
```

**Another Form Example**

```xml
<record id="view_employee_arabic_name_form" model="ir.ui.view">
    <field name="name">hr.employee.form.arabic.name</field>
    <field name="model">hr.employee</field>
    <field name="inherit_id" ref="hr.view_employee_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='job_title']" position="before">
            <group col="1">
                <field name="arabic_name_field_employee" placeholder="Arabic Name"/>
            </group>
        </xpath>
    </field>
</record>
```

**Another Example**

```xml
<xpath expr="//div[@name='wage']" position="after">
    <label for="percentage" string="Percentage"/>
    <div class="o_row mw-50" name="percentage_row">
        <field name="percentage" class="oe_inline o_hr_narrow_field" nolabel="1"/>
        <div class="mb-3">%</div>
    </div>
</xpath>
```

**Another example in Settings**

```xml
<odoo>
    <record id="view_purchase_config_settings" model="ir.ui.view">
        <field name="name">res.config.settings.view.form.inherit.purchase.discount</field>
        <field name="model">res.config.settings</field>
        <field name="inherit_id" ref="purchase.res_config_settings_view_form_purchase"/>
        <field name="arch" type="xml">
           <xpath expr="//form//block[@name='purchase_setting_container']" position="inside">
                <div class="d-flex align-items-center mt16" style="gap: 8px;">
                    <field name="purchase_discount_enabled"/>
                    <div class="border-start ps-2">
                        <label for="purchase_discount_enabled" class="o_light_label"/>
                    </div>
                </div>
            </xpath>
        </field>
    </record>
</odoo>
```

**another example in settings**

```xml
<xpath expr="//div[hasclass('settings')]" position="inside">
    <div class="app_settings_block" data-string="My Module" string="My Module" data-key="my_module">
        <h2>My Module Settings</h2>
        <div class="row mt16 o_settings_container">
            <div class="col-12 col-lg-6 o_setting_box">
                <div class="o_setting_right_pane">
                    <label for="birthday"/>
                    <div class="row">
                        <div class="text-muted col-md-8">
                            Set Here the Default Birthday
                        </div>
                        <div class="content-group mt16">
                            <field name="birthday"/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</xpath>
```



### Layout Examples

→ See this 👇

![image](imgs/totals_form_view.png)

here's it's code snippet: 

```xml
<group name="note_group" col="6" class="mt-2 mt-md-0">
    <group colspan="4" class="order-1 order-lg-0">
        <field colspan="2" name="description" nolabel="1"
               placeholder="Add any contract description or terms..."/>
    </group>
    <group string="Totals" class="oe_subtotal_footer d-flex order-0 order-lg-1 flex-column gap-0 gap-sm-3"
           colspan="2" name="totals_group">
        <div class="d-flex justify-content-between">
            <span>Untaxed Amount:</span>
            <field name="amount_untaxed" readonly="1" widget="monetary" nolabel="1"/>
        </div>
        <div class="d-flex justify-content-between">
            <span>Taxes:</span>
            <field name="amount_tax" readonly="1" widget="monetary" nolabel="1"/>
        </div>
        <div class="d-flex justify-content-between">
            <span>Total:</span>
            <field name="amount_total" readonly="1" widget="monetary" nolabel="1"/>
        </div>
        <field name="currency_id" invisible="1"/>
    </group>
</group>
```



---

### How to Make Page Action Loads with a Default Value for a Specific Field?

→ Use something like this: 

```py
@api.model
    def action_rfq_test2(self):
        """Dynamic action for Test 2 - material2 (خامات مساعدة)"""
        res = self._get_dynamic_rfq_action("خامات مساعدة", 'material2')
        res_context = dict(res.get('context') or {})
        res_context.update({'default_picking_type_id': 12})
        res['context'] = res_context
        return res
```

---

## Wizard Cheat Sheet

Example of action that opens a Wizard: 

```py
def action_send_to_shipper(self):
    return {
        'type': 'ir.actions.act_window',
        'name': 'Ramp Shipment',
        'res_model': 'ramp.shipment.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {'active_id': self.id},
    }

```

→ The Basic Model of the wizard would be like this: 

```py
from odoo import _, api, fields, models

class RampShipmentWizard(models.TransientModel):
    _name = 'ramp.shipment.wizard'
    _description = 'Ramp Shipment Wizard'
```

→ The Basic View will be like this: 

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="view_ramp_shipment_wizard_form" model="ir.ui.view">
            <field name="name">ramp.shipment.wizard.form</field>
            <field name="model">ramp.shipment.wizard</field>
            <field name="arch" type="xml">
                <form>
                    <separator string="PICKUP ADDRESS"/>
                </form>
            </field>
        </record>
    </data>
</odoo>
```

→ Then add the proper security like this: 

```
access_ramp_shipment_wizard,ramp.shipment.wizard,model_ramp_shipment_wizard,base.group_user,1,1,1,1
```

---

## Line IDs (Relational Fields in Odoo) Cheat Sheet

→ Python File Example: 

```py
from odoo import models, fields, api


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    ramp_delivery_line_ids = fields.One2many('ramp.delivery.line', 'carrier_id', string='Ramp Delivery Lines')


class RampDeliveryLine(models.Model):
    _name = 'ramp.delivery.line'
    _description = 'Ramp Delivery Line'

    carrier_id = fields.Many2one('delivery.carrier', string='Delivery Carrier', required=True, ondelete='cascade')
    city = fields.Char(string='City', required=True)
    price = fields.Float(string='Price', required=True)

```

→ The main field that will be added is this one: 

```
ramp_delivery_line_ids
```

→ XML Lines Definition

```xml
<!-- Ramp Delivery Line Views -->
<record id="view_ramp_delivery_line_tree" model="ir.ui.view">
    <field name="name">ramp.delivery.line.list</field>
    <field name="model">ramp.delivery.line</field>
    <field name="arch" type="xml">
        <list editable="bottom">
            <field name="city"/>
            <field name="price"/>
        </list>
    </field>
</record>

<record id="view_ramp_delivery_line_form" model="ir.ui.view">
<field name="name">ramp.delivery.line.form</field>
<field name="model">ramp.delivery.line</field>
<field name="arch" type="xml">
    <form>
        <group>
            <field name="city"/>
            <field name="price"/>
        </group>
    </form>
</field>
</record>
```

→ Security File: 

```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_ramp_delivery_line,ramp.delivery.line,model_ramp_delivery_line,base.group_user,1,1,1,1
```

**Notes**

→ In the context of relational fields in Odoo, there's a parent-child relationship where the `one2many` field is the parent and the `many2one` field is the child. 

→ The One2many field is a *reverse* relation: it doesn’t store anything in the database; it just reflects the records from the other model that point to it via Many2one.

→ The Many2one field is the one that actually holds the foreign key (i.e., stores the parent ID).

---

### What Is the Difference Between Internal User, Portal User, and Public User in Odoo? 

In Odoo, users are categorized based on their access level and intended interaction with the system. Here’s a breakdown of the three main user types:

⸻

1. **Internal User**
	• Purpose: Regular employees or staff members who work inside the company.
	• Access Level: Full access to backend applications (based on assigned roles).
	• Typical Roles:
	• Salesperson
	• Accountant
	• HR officer
	• Inventory manager
	• License Impact: Counts towards Odoo licenses (in Odoo Enterprise).
	• Example Use Case: A sales rep creating and managing quotations, or an accountant reconciling accounts.

⸻

2. **Portal User**
   • Purpose: External partners like customers or vendors who need limited access to their own records.
   • Access Level: Read-only or limited interaction with specific data (e.g., their own sales orders, invoices, helpdesk tickets).
   • Typical Roles:
   • Customer viewing their order history
   • Vendor checking RFQs or invoices
   • License Impact: Does not count towards Odoo licenses (in Enterprise).
   • How Assigned: Usually granted automatically when a contact is invited to the portal via the “Send Portal Invitation” option.
   • Example Use Case: A customer logs in to track their orders and download invoices.

⸻

3. **Public User**
   • Purpose: Website visitors who are not logged in.
   • Access Level: Minimal — only sees what’s public on the website (e.g., blog posts, product catalog).
   • Typical Roles: Anonymous visitor browsing the site.
   • License Impact: Not counted as a user.
   • Example Use Case: Someone browsing your eCommerce store without creating an account.

⸻

| **Feature**                | **Internal User** | **Portal User** | **Public User** |
| -------------------------- | ----------------- | --------------- | --------------- |
| Login Required             | ✅                 | ✅               | ❌               |
| Backend Access             | ✅                 | ❌ (Portal only) | ❌               |
| Access to Own Records      | ✅                 | ✅               | ❌               |
| Website Access             | ✅                 | ✅               | ✅               |
| License Count (Enterprise) | ✅                 | ❌               | ❌               |



---

### How to Get Rid Of Odoo's Demo Data From Existing Database?

→ First Create a New User with Full Privileges by Going to Settings >> Users & Companies >> Users and Click the New Button

→ Fill in the basic information (name, email)

​	↪ The E-mail you set is the one you will log with, and the name is the name will appear 
​	     above the db name in debug mode. 

​	↪ We Have to Create a Password for the User Through the Gear Icon (used for login)

![image](imgs/create_user.png)

→ Make the appropriate type of administrative privilege 

![image](imgs/admin_rights.png)

​	↪ This is crucial otherwise you won't be able to access the settings once you login. 

❖ Once logged in as your new admin, you can proceed to the next step which is the following 

→ Stop Odoo Server from Pycharm (This is important to stop odoo's backend activities)

→ in your terminal log in to the database in shell mode 

→ Run the following code: 

```python
users_to_archive = env['res.users'].browse([1, 2])  # Adjust IDs as needed
users_to_archive.write({'active': False})
env.cr.commit()
```

​	↪ the id's in my situatiorn were 2, 6 for Mitchell Admin and Marc Demo

→ Now restart odoo server and check that the two users are not there (Archived) 

→ Go to your module e.g contacts and go to **List View** and click on the top checkbox next to the name to select all records but yours, Now archive those records. 

![image](imgs/archive_all_records.png)

→ Now you can archive any records in any module. 

---

## How to Extend DB Expiration Date

❖ Search for `System Parameters` in home, just type the text and you will will see results like this:

![image](imgs/extend_db.png)

→ Change The Expiration Date (You might need to restart the server!).

**How to Change Expiration Date from Odoo Shell**

→ **To check the current value:**

```python
env['ir.config_parameter'].sudo().get_param('database.expiration_date')
```

→ **To set a new value:**

```python
env['ir.config_parameter'].sudo().set_param('database.expiration_date', '2026-12-30')
```

→ To Commit

```python
env.cr.commit()
```

P.S : you might get False as result from the terminal, don't panic, that's the normal behaviour, just run the check code again to check that it's changed to the desired value. 

**Query That Fixed Belle Date with Enterprise Subscription Code Issue**

the error was like this: 

```
unreachable code after return statement web.assets_web.min.js:32:5
OwlError: An error occured in the owl lifecycle (see this Error's "cause" property)
    OwlError@https://capstone-solution-belleshop.odoo.com/web/assets/477dd30/web.assets_web.min.js:694:1
    handleError@https://capstone-solution-belleshop.odoo.com/web/assets/477dd30/web.assets_web.min.js:938:101
    handleError@https://capstone-solution-belleshop.odoo.com/web/assets/477dd30/web.assets_web.min.js:1585:29
    render@https://capstone-solution-belleshop.odoo.com/web/assets/477dd30/web.assetsweb.min.js:963:19
    render@https://capstone-solution-belleshop.odoo.com/web/assets/477dd30/web.assets_web.min.js:961:6
    initiateRender@https://capstone-solution-belleshop.odoo.com/web/assets/477dd30/web.assets_web.min.js:1031:47

Caused by: TypeError: can't access property "days", duration.values is undefined
```

**The Fix**

```sql
psql $DATABASE_NAME << 'EOF'
-- Update enterprise code to indicate a valid subscription
UPDATE ir_config_parameter 
SET value = 'renewal'
WHERE key = 'database.enterprise_code';

-- Or remove it entirely to disable checks
-- DELETE FROM ir_config_parameter WHERE key = 'database.enterprise_code';
EOF
```

---

### How to Fix User View After Adding Record to the Group Users?

→ if you added a record in the `security.xml` file creating users groups you will get something like this when you restart the odoo server: 

![image](imgs/user_view_change.png)

→ To fix this view we have to fix the view from the ui (not PyCahrm)

![image](imgs/user_view_fix.png)



---

### Search Directory (e.g Custom Addons) for a Specific String

use the following command: 

```bash
cd <your_directory>
grep -ri --include="*.py" --include="*.xml" "Master Data" .
```

→ change `Master Data` with the actual data you want to find. 

---

### How to Show Arabic Text in Report without getting letters scrambled

```xml
<style>
    .arabic-text {
    font-family: 'Noto Sans Arabic', 'Amiri', 'Tahoma', 'Arial Unicode MS', 'DejaVu Sans', sans-serif !important;
    direction: rtl;
    text-align: right;
    unicode-bidi: bidi-override;
    }
</style>
        </head>
<t t-foreach="docs" t-as="o">
<div class="page arabic-text" style="direction: rtl; text-align: right;">
```

→ Notice the class `arabic-text` it fixes the arabic text appearance. 

---

### Migration Codes

```bash
source .venv/bin/activate
python <(curl -s https://upgrade.odoo.com/upgrade) production -d <your db name> -t 17.0 --contract M250129203722535
```

→ After the migration is done, do a backcup dump

→ Each Time the Migration Run Can result in a Different Outcome

→ Change The Owner to Match The Original DB

```bash
psql -U postgres
ALTER DATABASE <Your DB Name> OWNER TO odoo13;
\q
```

**Fixing Filestore Permissions**

```bash
sudo chmod -R 755 "/Users/ahmed/Library/Application Support/Odoo/filestore/<Your DB Name>"
```

→ Put the File Store After Connecting The DB and Replace Files

→ Set The Right `db_user` in the Config: 

```ini
[options]
db_user = odoo13
db_password = your_password
# ... other configurations
```

→ Add Custom Addons to the Config as Well

→ Re-Creating Missing FileStore Files

```bash
DIR="" && mkdir "$DIR" && echo "Dummy" > "$DIR"
```

→ Test on localhost

```
http://localhost:8071/web/login?debug=1
```

**Blank Page Fix**

Sometimes Odoo thinks it needs to process (install/upgrade/remove) **500 modules**, so it **refuses to run ir.cron jobs** for the database until you fix it.

✅ Step-by-Step Plan to Fix It

🔍 Step 1: See What Modules Are Uninstalled

```sql
SELECT name, state FROM ir_module_module WHERE state != 'installed';
```

🧹 Step 2: Clean Uninstalled Modules (Safe)

```sql
UPDATE ir_module_module
SET state = 'uninstalled'
WHERE state = 'uninstalled';
```

🚀 Step 3: Relaunch Odoo Server

#### 500 Internal Server Error Assets Fix

```sql
DELETE FROM ir_attachment WHERE name LIKE 'web.assets_%';
```



---

### Migration SQL Command that Fixed Filestore

**Finally What Fixed The Issue**

```sql
-- Clear company logos (4 companies)
UPDATE res_company SET logo_web = NULL WHERE logo_web IS NOT NULL;

-- Clear report layout images
UPDATE report_layout SET image = NULL WHERE image IS NOT NULL;

-- Remove empty/corrupted image attachments
DELETE FROM ir_attachment 
WHERE mimetype LIKE 'image/%' 
AND (db_datas IS NULL OR file_size = 0 OR file_size < 100);
```

→ After the last query you'll find all images are broken, don't panic, do another restart with -u all and stop after init and restart. 

---

### Change DB Name

```bash
psql -U postgres
```

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = "old_db_name";
```

```sql
ALTER DATABASE "old_db_name" RENAME TO "new_db_name";
```

---

**Show Custom Module Icon in Enterprise The Right Way**

```xml
<menuitem
        id="cs_lastpoint_topLevel_menuItem"
        name="LastPoint"
        web_icon="cs_lastpoint,static/description/icon.png"
/>
```

> The comma is **essential** — it’s how Odoo resolves the file through the asset loader.

---

## Postman & API

**How to Open API Documentation in Postman?**

→ if the link on the left side has a lock icon next to it then you have to switch acount to the guest account you've been invited to. 

→ if there's no lock you can go from the left side, right click on choose export, then import on your main account.

![image](./imgs/apiIntegrationToPostman.png) 

### Where Odoo Gets Egypt's States Data From?

→  Odoo gets Egypt's states from the file:
` /Volumes/Samsung T5/Odoo/Development & Study/odoo-18.0/odoo/addons/base/data/res.country.state.csv`



## How to Generates `X-API-Key` cryptographically secure random data to use in API KEYS?

→ Use this command in Terminal

```shell
openssl rand -base64 32 | tr -d '/+=' | cut -c1-40
```

---

## Python Query to Extract Shopify Credentials

Once inside the Odoo shell, use this Python code:

```python
# Query to get Shopify instances with all credentials
instances = env['shopify.instance.ept'].search([])

print(f"\nFound {len(instances)} Shopify instance(s):\n")

for instance in instances:
    print(f"{'='*70}")
    print(f"Instance Name: {instance.name}")
    print(f"Shop URL: {instance.shopify_host}")
    print(f"API Key (shopify_api_key): {instance.shopify_api_key}")
    print(f"Shared Secret (shopify_shared_secret): {instance.shopify_shared_secret}")
    print(f"Access Token (shopify_password): {instance.shopify_password}")
    print(f"Active: {instance.active}")
    print(f"{'='*70}\n")
```

## Python Query to Extract Bosta Credentials

```python
# Query to get delivery carriers that use Bosta (only those with API key set)
carriers = env['delivery.carrier'].search([
    ('bosta_api_key', '!=', False)
])

print(f"\nFound {len(carriers)} Bosta-enabled carrier(s):\n")

for carrier in carriers:
    print(f"{'='*70}")
    print(f"Carrier Name: {carrier.name}")
    print(f"Bosta API Key: {carrier.bosta_api_key}")
    print(f"Bosta API URL: {carrier.bosta_api_url}")
    print(f"Bosta Tracking Endpoint: {carrier.bosta_tracking_endpoint}")
    print(f"Active: {carrier.active}")
    print(f"{'='*70}\n")
```

---

## How to Fix Field Is Undefined? And How to Search Missing Fields From SQL?

```sql
SELECT id, model, name, type
FROM ir_ui_view
WHERE arch_db::text LIKE '%available_peppol_eas%';
```

That will tell you **which view is trying to render it**.

**Alternative Approach via Odoo Shell**

```python
views = env['ir.ui.view'].search([('arch_db', 'like', 'available_peppol_eas')])
for v in views:
    print(v.id, v.model, v.name, v.type)
```

**How to See the XML that Is Actually Stored?**

```python
view = env['ir.ui.view'].browse(1101)
print(view.arch_db)
```

 → Next Delete the Invalid View: 

```python
# Browse the view
view = env['ir.ui.view'].browse(1101)

# Delete it
view.unlink()

```

→ In case there's a children of that view: 

```python
env.cr.rollback()
children = env['ir.ui.view'].search([('inherit_id', '=', 775)])
[(c.id, c.name, c.model) for c in children]
# [(839, 'res.partner.property.form.inherit', 'res.partner'), (919, 'res.partner.view.form.property.inherit', 'res.partner')]
env.cr.rollback()
env['ir.ui.view'].browse([839, 919]).unlink() # The Children
env['ir.ui.view'].browse(775).unlink() # The Parent
```

**Another Way to get the Descendants**

```python
def get_descendants(view_id):
    result = []
    children = env['ir.ui.view'].search([('inherit_id', '=', view_id)])
    for c in children:
        result.append(c.id)
        result += get_descendants(c.id)
    return result

print(get_descendants(219))

to_delete = get_descendants(219) + [219]
env['ir.ui.view'].browse(sorted(to_delete, reverse=True)).unlink()
```



---

### Fix JSON Response

```bash
pbpaste | iconv -f utf-8 -t utf-8 -c | tr -d '\000-\037' | perl -0777 -ne 'print $1 if /(\{.*\}|\[.*\])/s' | jq '.' > response.json
```



---

### JS POS

**Manifest**: Put the Following After the Data Section

```python
'assets': {
    'point_of_sale._assets_pos': [
        'your_module_name/static/src/**/*',
    ],
},

```

**Opening Tag and First Log**

```js
/** @odoo-module **/
console.log("File Loaded Successfully 🚀")
```

**Imports for Odoo 17**

```js
/** @odoo-module **/
console.log("File Loaded Successfully 🚀")

import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Orderline } from "@point_of_sale/app/store/models";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";

console.log("Multiple Imports Loaded Successfully 🚀")
```

---

**Patch OrderLine.prototype.set_quantity() and detect if quantity is decreasing.**

```js
patch(Orderline.prototype, {
    set_quantity(quantity, keep_price) {
        const prevQty = this.quantity;
        const res = super.set_quantity(quantity, keep_price);

        if (quantity < prevQty) {
            console.log(`➖ Quantity decreased for: ${this.product.display_name} (from ${prevQty} to ${quantity})`);
        }

        return res;
    },
});
```

---

## Print & PDF Reports

→ Microsoft Word Like Template with Just `Hello World`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Paper format with no margins -->
    <record id="paperformat_salary_certificate" model="report.paperformat">
        <field name="name">Salary Certificate</field>
        <field name="default" eval="False"/>
        <field name="format">A4</field>
        <field name="page_height">0</field>
        <field name="page_width">0</field>
        <field name="orientation">Portrait</field>
        <field name="margin_top">0</field>
        <field name="margin_bottom">0</field>
        <field name="margin_left">0</field>
        <field name="margin_right">0</field>
        <field name="header_line" eval="False"/>
        <field name="header_spacing">0</field>
        <field name="dpi">90</field>
    </record>

    <!-- Report template -->
    <template id="report_salary_certificate_document">
        <t t-call="web.html_container">
            <style>
                @page {
                    size: A4;
                    margin: 0mm;
                }
                body {
                    margin: 0;
                    padding: 0;
                }
                header, footer, .header, .footer, .o_background_header, .o_standard_header {
                    display: none !important;
                    height: 0 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }
            </style>
            <t t-foreach="docs" t-as="o">
                <article style="padding: 0; margin: 0;">
                    <div class="page" style="padding: 2.5cm; margin: 0; page-break-after: always;">
                        <p>hello world</p>
                    </div>
                </article>
            </t>
        </t>
    </template>

    <!-- Report action -->
    <record id="action_report_salary_certificate" model="ir.actions.report">
        <field name="name">Salary Certificate</field>
        <field name="model">hr.employee</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">hr_salary_certificate.report_salary_certificate_document</field>
        <field name="report_file">hr_salary_certificate.report_salary_certificate_document</field>
        <field name="binding_model_id" ref="hr.model_hr_employee"/>
        <field name="binding_type">report</field>
        <field name="paperformat_id" ref="paperformat_salary_certificate"/>
    </record>
</odoo>
```

→ if you're using this in another module make sure to replace `hr_salary_certificate` with the correct module name. 

→ Here's after adding the img as background just like in MS-Word: 

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Paper format with no margins -->
    <record id="paperformat_salary_certificate" model="report.paperformat">
        <field name="name">Salary Certificate</field>
        <field name="default" eval="False"/>
        <field name="format">A4</field>
        <field name="page_height">0</field>
        <field name="page_width">0</field>
        <field name="orientation">Portrait</field>
        <field name="margin_top">0</field>
        <field name="margin_bottom">0</field>
        <field name="margin_left">0</field>
        <field name="margin_right">0</field>
        <field name="header_line" eval="False"/>
        <field name="header_spacing">0</field>
        <field name="dpi">90</field>
    </record>

    <!-- Report template -->
    <template id="report_salary_certificate_document">
        <t t-call="web.html_container">
            <style>
                @page {
                    size: A4;
                    margin: 0mm;
                }
                body {
                    margin: 0;
                    padding: 0;
                }
                header, footer, .header, .footer, .o_background_header, .o_standard_header {
                    display: none !important;
                    height: 0 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }
            </style>
            <t t-foreach="docs" t-as="o">
                <t t-set="background_image" t-value="o._get_salary_certificate_background()"/>
                <div class="page" style="padding: 0; margin: 0; page-break-after: always; position: relative;">
                    <!-- Background image for full page -->
                    <t t-if="background_image">
                        <img t-att-src="'data:image/jpeg;base64,' + background_image"
                             style="
                                position: fixed;
                                top: 0;
                                left: 0;
                                width: 100%;
                                height: 100%;
                                object-fit: cover;
                                opacity: 0.1;
                                z-index: 0;
                             " alt="Background"/>
                    </t>

                    <!-- Content container with padding -->
                    <div style="padding: 2.5cm; position: relative; z-index: 1;">
                        <p>hello world</p>
                    </div>
                </div>
            </t>
        </t>
    </template>

    <!-- Report action -->
    <record id="action_report_salary_certificate" model="ir.actions.report">
        <field name="name">Salary Certificate</field>
        <field name="model">hr.employee</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">hr_salary_certificate.report_salary_certificate_document</field>
        <field name="report_file">hr_salary_certificate.report_salary_certificate_document</field>
        <field name="binding_model_id" ref="hr.model_hr_employee"/>
        <field name="binding_type">report</field>
        <field name="paperformat_id" ref="paperformat_salary_certificate"/>
    </record>
</odoo>
```

→ and here's the python part the decodes and read the img file before adding it to qweb: 

```python
# -*- coding: utf-8 -*-

import base64
import os
from odoo import models, api
from odoo.modules.module import get_module_path


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def _get_salary_certificate_background(self):
        """
        Get the background image as base64 encoded string for salary certificate
        """
        try:
            module_path = get_module_path('hr_salary_certificate')
            image_path = os.path.join(module_path, 'static', 'src', 'img', 'Picture1.jpg')

            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            # Return empty string if image not found
            return ''

```

**How to Fix Arabic Text Scrambled and Not Displayed Properly?**

→ First Add the file in this path: 

`/Volumes/Samsung T5/Odoo/Odoo/Eqnaa/18/Eqnaa-Dev/custom-eqnaa3/hr_salary_certificate/static/src/fonts/amiri-regular.ttf`

→ Now let's encode the file in our python file: 

```python
# -*- coding: utf-8 -*-

import base64
import os
from odoo import models, api
from odoo.modules.module import get_module_path


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def _get_salary_certificate_background(self):
        """
        Get the background image as base64 encoded string for salary certificate
        """
        try:
            module_path = get_module_path('hr_salary_certificate')
            image_path = os.path.join(module_path, 'static', 'src', 'img', 'Picture1.jpg')

            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            # Return empty string if image not found
            return ''


class ReportSalaryCertificate(models.AbstractModel):
    _name = 'report.hr_salary_certificate.report_salary_certificate_document'
    _description = 'Salary Certificate Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.employee'].browse(docids)

        # Path to the font inside your module
        font_path = os.path.join(
            os.path.dirname(__file__), '..', 'static', 'src', 'fonts', 'amiri-regular.ttf'
        )

        # Safely read and encode the font
        with open(font_path, 'rb') as f:
            amiri_font_b64 = base64.b64encode(f.read()).decode()

        return {
            'docs': docs,
            'amiri_font': amiri_font_b64,
        }
```

→ Add this line before the `<style>` tag: 

```xml
<meta charset="UTF-8"/>
```

→ and at the start of the template make sure it's like this: 

```xml
<?xml version="1.0" encoding="utf-8"?>
```

→ Here's the Full Template: 

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Paper format with no margins -->
    <record id="paperformat_salary_certificate" model="report.paperformat">
        <field name="name">Salary Certificate</field>
        <field name="default" eval="False"/>
        <field name="format">A4</field>
        <field name="page_height">0</field>
        <field name="page_width">0</field>
        <field name="orientation">Portrait</field>
        <field name="margin_top">0</field>
        <field name="margin_bottom">0</field>
        <field name="margin_left">0</field>
        <field name="margin_right">0</field>
        <field name="header_line" eval="False"/>
        <field name="header_spacing">0</field>
        <field name="dpi">90</field>
    </record>

    <!-- Report template -->
    <template id="report_salary_certificate_document">
        <t t-call="web.html_container">
            <!-- Note: amiri_font is provided by the report model's _get_report_values method -->
            <meta charset="UTF-8"/>
            <style>
                @page {
                    size: A4;
                    margin: 0mm;
                }
                body {
                    margin: 0;
                    padding: 0;
                }
                header, footer, .header, .footer, .o_background_header, .o_standard_header {
                    display: none !important;
                    height: 0 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }

                /* ✅ Embed font directly */
                @font-face {
                    font-family: 'Amiri';
                    src: url('data:font/truetype;charset=utf-8;base64,<t t-esc="amiri_font"/>') format('truetype');
                }

                body {
                    font-family: 'Amiri', sans-serif !important;
                }

                .content-wrapper {
                    padding: 2.5cm;
                    position: relative;
                    z-index: 1;
                }

                .date-section {
                    margin-bottom: 1cm;
                }

                .arabic-section {
                    direction: rtl;
                    text-align: right;
                }
            </style>

            <t t-foreach="docs" t-as="o">
                <t t-set="background_image" t-value="o._get_salary_certificate_background()"/>
                <div class="page" style="padding: 0; margin: 0; page-break-after: always; position: relative;">
                    <!-- Background image -->
                    <t t-if="background_image">
                        <img t-att-src="'data:image/jpeg;base64,' + background_image"
                             style="
                                position: fixed;
                                top: 0;
                                left: 0;
                                width: 100%;
                                height: 100%;
                                object-fit: cover;
                                opacity: 0.1;
                                z-index: 0;
                             " alt="Background"/>
                    </t>

                    <!-- Content -->
                    <div class="content-wrapper">
                        <div class="date-section">
                            <p>Date: 06/12/1446 H</p>
                            <p>Corr: 02/06/2025 G</p>
                        </div>

                        <div class="arabic-section">
                            <p>تحية طيبة وبعد،،</p>
                            <p>تشهد شركة طيبة المحدودة بأن الموظف المذكور أدناه يعمل لديها.</p>
                        </div>
                    </div>
                </div>
            </t>
        </t>
    </template>

    <!-- Report action -->
    <record id="action_report_salary_certificate" model="ir.actions.report">
        <field name="name">Salary Certificate</field>
        <field name="model">hr.employee</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">hr_salary_certificate.report_salary_certificate_document</field>
        <field name="report_file">hr_salary_certificate.report_salary_certificate_document</field>
        <field name="binding_model_id" ref="hr.model_hr_employee"/>
        <field name="binding_type">report</field>
        <field name="paperformat_id" ref="paperformat_salary_certificate"/>
    </record>
</odoo>

```

The snippet responsible for calling a new page break: 

```xml
<div class="page" style="padding: 0; margin: 0; page-break-after: always; position: relative;">
```

**How to Properly Display Bi-Directions En / Ar Text?**

![image](imgs/bi-directions-test.png)

use this styling on the English Text: 

```css
direction: ltr; unicode-bidi: embed;
```

→ Here's the Full Snippet: 

```xml
<h3 style="direction: rtl; text-align: right;">مقرها الرئيسي:
    <span style="direction: ltr; unicode-bidi: embed;" t-field="o.sub_contractor_id.state_id"/>
</h3>
```



## Partners Sign Section



```xml
<tr>
    <td style="width: 25%; text-align: left; vertical-align: top; padding: 0; border: 0 !important;">
        <h1 style="font-family: 'Calibri', 'CalibriBold', 'Arial', sans-serif; font-size: 20px; line-height: 22px; font-weight: 900; direction: rtl; text-align: center; text-shadow: 0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, -0.5px 0 0 currentColor; margin: 0;">
            الطرف الثاني
        </h1>

    </td>
    <td style="width: 50%; border: 0 !important;">
    </td>
    <td style="width: 25%; text-align: right; vertical-align: top; padding: 0; border: 0 !important;">

        <h1 style="font-family: 'Calibri', 'CalibriBold', 'Arial', sans-serif; font-size: 20px; line-height: 22px; font-weight: 900; direction: rtl; text-align: center; text-shadow: 0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, -0.5px 0 0 currentColor; margin: 0;">
            الطرف الأول
        </h1>
        <br/>
        <span style="font-family: 'Calibri', 'Arial', sans-serif; direction: rtl; text-align: center;"
              t-field="o.company_id.name"/>
    </td>
</tr>
```

→ Now let's make the company name centered to the h1 element above it and for that we will use `display: block,`

```xml
<table style="width: 100%; border-collapse: collapse; border: 0 !important; border-spacing: 0; margin: 0; padding: 0;">
    <tr>
        <td style="width: 25%; text-align: left; vertical-align: top; padding: 0; border: 0 !important;">
            <h1 style="font-family: 'Calibri', 'CalibriBold', 'Arial', sans-serif; font-size: 20px; line-height: 22px; font-weight: 900; direction: rtl; text-align: right; text-shadow: 0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, -0.5px 0 0 currentColor; margin: 0;">
                الطرف الثاني
            </h1>

        </td>
        <td style="width: 50%; border: 0 !important;">
        </td>
        <td style="width: 25%; text-align: right; vertical-align: top; padding: 0; border: 0 !important;">

            <h1 style="font-family: 'Calibri', 'CalibriBold', 'Arial', sans-serif; font-size: 20px; line-height: 22px; font-weight: 900; direction: rtl; text-align: center; text-shadow: 0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, -0.5px 0 0 currentColor; margin: 0;">
                الطرف الأول
            </h1>
            <br/>
            <span style="font-family: 'Calibri', 'Arial', sans-serif; direction: rtl; text-align: center; display: block;"
                  t-field="o.company_id.name"/>
        </td>
    </tr>
</table>
```

→ To make the text on the `same horizontal baseline` you can use the style `float` it's preferred with `wkhtmltopdf` 

```xml
<!-- Signature Section -->
<div style="width: 100%; margin-top: 40px; padding: 15px 0; overflow: hidden;">
    <div style="float: right; text-align: center;">
        <div style="font-weight: bold; border-bottom: 1px solid #333; display: inline-block; min-width: 150px; padding-bottom: 40px;">
            المستلم
        </div>
    </div>
    <div style="float: left; text-align: center;">
        <div style="font-weight: bold; border-bottom: 1px solid #333; display: inline-block; min-width: 150px; padding-bottom: 40px;">
            محاسب Accountant
        </div>
    </div>
</div>
```



---

## Repeat Margins in Every Page

```xml
<record id="paperformat_legal_contract" model="report.paperformat">
    <field name="name">Legal Contract</field>
    <field name="default" eval="False"/>
    <field name="format">A4</field>
    <field name="page_height">0</field>
    <field name="page_width">0</field>
    <field name="orientation">Portrait</field>
    <!-- Use wkhtmltopdf margins so they apply on every page, not just the first -->
    <field name="margin_top">60</field>
    <field name="margin_bottom">20</field>
    <field name="margin_left">20</field>
    <field name="margin_right">20</field>
    <field name="header_line" eval="False"/>
    <field name="header_spacing">0</field>
    <field name="dpi">90</field>
</record>
```

### Important Note When Using CSS Rules in a Report

→ i had a problem with cut-offs from the right side of all qweb print reports caused by global css rule in one of the custom addons. 

→ **The Fix**:Scoped the attestation report CSS to avoid leaking global @page/body margins into all reports, and wrapped the template content so the styles apply only to that report. This should stop the right‑side cutoff caused by the global margins/headers in web.report_assets_common.

### Useful Snippets

```xml
<span t-field="o.partner_id.name"/>
```

→ Load `img` from the `company_id.logo` field

```xml
<img t-if="o.company_id.logo" t-att-src="image_data_uri(o.company_id.logo)" style="max-height: 90px; margin-top: 5px;" alt="Logo"/>
```

→ Control Line Height

```css
line-height: 22px;
```

→ For custom field using `t-if` so if the module is installed it will render the field, if not it won't render the field and not breake the whole report 

instead of using: 

```xml
<td style="padding: 3px;"><span t-field="o.partner_id.gln_custom"/></td>
```

use: 

```xml
<td style="padding: 3px;"><span t-if="'gln_custom' in o.partner_id._fields" t-field="o.partner_id.gln_custom"/></td>
```

You can use this pattern for any other custom fields:

```xml
<span t-if="'field_name' in o.model._fields" t-field="o.model.field_name"/>
```



---

## Deletion

→ Delete All Products (Product.template) except the ones protected by foreign constraint. 

```python
# Product variants used in sale order lines
used_variant_ids = env['sale.order.line'].search([]).mapped('product_id').ids

# Corresponding templates
used_template_ids = env['product.product'].browse(used_variant_ids).mapped('product_tmpl_id').ids

len(used_template_ids)


# Protected default templates
protected_template_ids = env['ir.model.data'].search([
    ('model', '=', 'product.template'),
    ('noupdate', '=', True),
]).mapped('res_id')

# Templates used in sales
used_template_ids = env['sale.order.line'].search([])\
    .mapped('product_id.product_tmpl_id').ids

# Final deletable templates
deletable_templates = env['product.template'].search([
    ('id', 'not in', protected_template_ids),
    ('id', 'not in', used_template_ids),
])

print(f"Deletable templates: {len(deletable_templates)}")


deletable_templates.unlink()
```

→ Archive All Contacts

```python
# First, let's check which users are still active
active_users = self.env['res.users'].search([('active', '=', True)])
print(f"Active users: {active_users.mapped('name')}")

# Archive all users except yourself (the one you're logged in as)
users_to_archive = self.env['res.users'].search([
    ('id', '!=', self.env.uid),
    ('active', '=', True)
])
print(f"Archiving users: {users_to_archive.mapped('name')}")
users_to_archive.write({'active': False})

# Now archive all partners
self.env['res.partner'].search([]).write({'active': False})


# Reactivate admin user (usually ID 2) and their partner
self.env.cr.execute("UPDATE res_users SET active = true WHERE login = 'admin'")
self.env.cr.execute("UPDATE res_partner SET active = true WHERE id IN (SELECT partner_id FROM res_users WHERE login = 'admin')")
self.env.cr.commit()

# Restart The Server for Changes to Take Effect.
```



