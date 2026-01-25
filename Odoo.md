##### **Pycharm**

❖ You Can't Install Pycharm Through Brew You Must Install It From the Website, and Don't Forget to Download the Community (Free) Version Not the Professional One. 

> https://www.jetbrains.com/pycharm/

:: `VS Code Keymap Plugin` ::

In PyCharm, a keymap refers to the mapping of keyboard shortcuts to specific actions or commands within the IDE. It allows you to customize and define your own preferred keyboard shortcuts for various tasks, such as running code, debugging, navigating the IDE, and more. Keymaps are useful for increasing productivity and efficiency during development by providing quick access to frequently used features.

<kbd>Command ⌘</kbd> + <kbd>K</kbd> Then Hold The <kbd>Command ⌘</kbd> Key and Then Press <kbd>T</kbd> to trigger the quick switch, You Can Change the Theme From There

:: `How to Remove the Annoying Vertical Line?` ::

Settings => Code Style => General 

Set `Hard Wrap` value to 0 instead of 120

:: `Change the Font and Terminal Font` ::

Settings => Editor => Font

:: `Install Postgres` ::

You Can Install Postgres Using Homebrew with This Command


```python
brew install postgresql@16
```

Add It to Path Variable in ZSH


```python
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
```

To Start Postgresql@16 Now and Restart at Login:


```python
brew services start postgresql@16
```

❖ By default, the only user is postgres. As Odoo forbids connecting as postgres, create a new PostgreSQL user.


```python
psql -d postgres
sudo -u postgres createuser -d -R -S $USER
createdb $USER
```

→ we also need to create a user named `odoo` using the following commands: 


```python
psql -d postgres
CREATE ROLE odoo WITH SUPERUSER LOGIN PASSWORD 'odoo';
```

:: `Install Odoo` ::

❖ the full odoo repository is big (about 9GB approx) so we will target a specific branch (odoo 17 for example) and only the latest commits using the following command: 


```python
git clone --branch 17.0 --single-branch --depth 1 git@github.com:odoo/odoo.git
```

Or if You're Using HTTP Use the Following Command: 


```python
git clone --branch 17.0 --single-branch --depth 1 https://github.com/odoo/odoo.git
```

❖ This Command Uses Branch 17 and Depth 1 (Means the Latest Commits Snapshot and Not All History) and Also Uses SSH Connection Instead of HTTPS

❖ If you'd like to download the entire branches and full history type the following command: 


```python
git clone git@github.com:odoo/odoo.git
```

❖ This will download everything, and you can switch between different branches (versions of odoo) using the following commnad: 

❖ This Command Uses Branch 17 and Depth 1 (Means the Latest Commits Snapshot and Not All History) and Also Uses SSH Connection Instead of HTTPS

❖ If you'd like to download the entire branches and full history type the following command: 


```python
git checkout 17.0
```

❖ this `checkout` command can work offline cuz Once you’ve switched to a branch and Git has its data locally, switching back and forth (e.g., git checkout main and git checkout 17.0) can be done offline because everything is managed within the .git folder.

❖ To see all branches available in your local repository use the following command:


```python
git branch -a
```

❖ odoo 17 on MacOS is compatible with python 3.11

❖ it's alwyas a best practice to create a seperate virtual environment for odoo

❖ Navigate to the path of the Odoo Community installation (CommunityPath) and run pip on the requirements file:


```python
cd /CommunityPath
pip3 install setuptools wheel
pip3 install -r requirements.txt
```

❖ Non-Python dependencies must be installed with a package manager (homebrew)

❖ Download and install the Command Line Tools:


```python
xcode-select --install
```

❖ `wkhtmltopdf` is not installed through pip and must be installed manually in version `0.12.6` for it to support headers and footers. you can install it via homebrew through the following command: 


```python
brew install wkhtmltopdf
```

❖ For languages using a right-to-left interface (such as Arabic or Hebrew), the rtlcss package is required. you can install it using the following `nodeJS` command:


```python
sudo npm install -g rtlcss
```

:: `Pycharm Configuration` ::

→ From the bottom right corner of pycharm select `add new interpeter` and choose `python` file from the `.env/bin` directory.

→ Create a new configuration from top right corner of pycharm next to the play button click the drop down arrow and choose edit configurations to create a new configuration. 

→ Create a name for the config (e.g) `odoo-17` and select the interpeter we created in the first step and in the script choose `odoo-bin` and in the script parameter add this: `-c /Users/ahmed/Documents/odoo-17/debian/odoo.conf -d learning-odoo`. later we will add the `-u` option to auto-upgrade our module. 

→ Select the working directory and `leave the path too .env files empty` 


### **postgres**

:: __`postgres Commands`__ ::

`psql -d postgres` => connect to postgres cli commands

`\du` => show roles and users

`CREATE ROLE openpg WITH LOGIN PASSWORD 'openpgpwd';` => creates new user [openpg] with password [openpgpwd]

`ALTER ROLE openpg CREATEDB;` => adds role to the user openpg so it can create a database

`\q `=> exit postgres cli 

`\l `=> list all database 

`q` => exit list database mode 

`\du` => list all users

`psql -U postgres` => set the user to postgres

`CREATE DATABASE mynewdatabase OWNER openpg;` => creates new database with owner `openpg`

`CREATE ROLE postgres WITH SUPERUSER LOGIN PASSWORD 'odoo';` => creates new **super user** [postgres] with password [odoo]

`brew services restart postgresql@16` => this will restart the postgres service

`brew services stop postgresql@16` => this will stop the postgres service

`ALTER ROLE postgres WITH SUPERUSER LOGIN PASSWORD 'odoo';` => Changes the Password for the User [postgres] to be [odoo]

### **Odoo**

:: __`Odoo ERP System`__ ::

❖ **ERP** System Stands for Enterprise Resource Planning

❖ Integrate ALL Departments In Your Company Starting From Recruitments To Interviews And Contract, Employees And HR Operation And TimeSheet, TimeOff, Custody, Loans, Payslip 

❖ With Accounting Application And All Transactions In Accounting Such AS Journals And Payments And Journal Entries To Management Of Assets And Sales And purchase Operations And Inventory To CRM Customer Relationship Managements To Provide Reports helping Managers in Decision Making

❖ **CRM** Stands for Customer Relationship Management

❖ **Odoo Handles the Following**: 

↪ CRM

↪ Sales

↪ Purchase 

↪ Stocks/Inventory

↪ Accounting

↪ Human Resources

❖ The main objective of implementing an erp system is to analyze and to help its users to make real time decision of its business processes.

❖ Some of the Core Open Source Technologies Used in OpenERP System Are :

↪ Scripting/Programming language - Python

↪ Database Server - PostgreSQL

↪ Framework - Model View Controller (MVC)


❖ Odoo Provides Different Budgets for Different Company Sizes: 

↪ Small **`=>`** Community Version

↪ Medium **`=>`** Odoo Cloud with User Subscription

↪ Large **`=>`** odoo.sh

❖ **demo.odoo.com** `=>` Provides Fast Demo and Overview or Big Picture for Clients to Explain Basic Modules

❖ odoo.sh Requires Your Github Linked to It And Provides Three Environments: 

↪ **Development**: where you test and develop your code. 

↪ **Staging[QC and Testing]**: where you prep your code to production. 

↪ **Production[Live]**: where you deploy your new code

❖ So First You Work in the Development Env and After Your Finish Developing You Do Pull Request to the Staging Branch; Now the Implementor Go in and Test the Life Cycle of the Code You Developed and if All Is Ok You Do Another Bull Request to the Production Live Server. 

❖ There's Also Backup Section in the odoo.sh Production Env Where Regular Backups Are Stored on odoo.sh 

❖ In the Production Settings There's a Custom Domain Section Where odoo.sh Provides You with a Custom Domain for Your Client

❖ https://apps.odoo.com/apps => Odoo Apps Is Like an App Store for Odoo Where You Can Install Apps that Increase Your Client Functionality and Productivity

❖ In odoo.sh when You Push a Module Through the Remote Main Github Linked to Odoo, Odoo Automatically Build an Instance for You with that Module; you can also find this instance in the build tab in odoo.sh 

❖ in odoo.sh There's a Shell Option[terminal] Where You Can Install Custom Python Libraries You Need in You Project

❖ There's Something Called "Odoo Runbot" Which Let You Demo Various Versions of Odoo Community and Enterprise. 

:: __`General Terms`__ ::


**Field**:

❖ A field in Odoo represents a single piece of data in a model. It defines the type of data (e.g., integer, string, date) and various attributes that dictate how the data should be handled and displayed.

**Model**:

❖ A model in Odoo is a class that defines the structure and behavior of data. It represents a database table and includes fields, methods, and constraints. Models are the foundation for business logic in Odoo.

**Module**:

❖ A module in Odoo is a package that groups together models, views, controllers, data files, and other resources. It extends the functionality of Odoo and can be installed or removed as needed.

**Record**:

❖ A record in Odoo is an instance of a model. It represents a single row in the database table, containing data in the fields defined by the model.

**Action**:

❖ An action in Odoo defines what happens when a user interacts with the system. Common types of actions include opening a view, executing a server action, or triggering a workflow. Actions are used to link menu items to specific functionalities.

**`What Is the Difference Between Headers in General and Odoo Headers?`**

**General Headers**:

❖ HTTP headers: Used for web communication protocols.

❖ HTML header tags: Define headings in a document.

❖ `<header></header>` tag: Defines the header section of a webpage.


**Odoo Headers**:

❖ HTTP headers: Similar to general HTTP headers but used specifically in the context of Odoo’s API and web interactions.

❖ XML headers in views: Define actions, buttons, and status elements within Odoo views.


:: __`Practical`__ ::

Basic Launch Command:


```python
python odoo-bin
```


```python
python odoo-bin -d test 
```

❖ This Command Will Create Database Test if It Doesn't Exist and Launch Odoo Server


```python
python odoo-bin -d test -i web_widget_image_cam
```

❖ This Command Will Create Database Test if It Doesn't Exist and Launch Odoo Server With Loading the Module Web_widget_cam only


```python
python odoo-bin -d test -i base
```

❖ This Command Will Load the Base Module only and It's Good for Debugging


```python
python odoo-bin --addons-path=addons,custom-addons -d mydb
```

❖ This Command Will Launch Odoo Server with the Database Mydb

❖ the Flag `--addons-path=` Sets the Path for Addons; Here We Have the Noraml Odoo Addons and Custom-Addons Folder Which Is Located Next to the Normal Addons Folder 


**`Note`**: you can add the custom addons path in the odoo.conf file like this: 


```python
addons_path = /Users/Ahmed/Documents/odoo-17.0/addons,/Users/Ahmed/Documents/odoo-17.0/custom-addons
```

❖ Now We Won't Have to Use Addons Path Flag when We Launch the Server, instead we will use `-c flag` in pycharm config with the absolute path to the `odoo.conf` file; it will be like this:


```python
-c /Users/ahmed/Documents/odoo-17/debian/odoo.conf -d learning-odoo
```



:: **`GUI Database Manager In the Browser`** ::

❖ By Default Odoo Will Generate a Master Password for You Like This: hg8c-uptq-wmv8 And Give You the Option to Change It.

❖ **But What if We Forgot that Master Password How Can We Reset It?** To Do This We Need to Load a Different Config than the Default One, but **Where that Default Config that Odoo Uses?**

❖ The default configuration file is `$HOME/.odoorc` which can be overridden using `--config` flag or `-c`. Now if We Opened This `odoorc` File with vs Code We Will See Something Like This:




:: **`GUI Database Manager In the Browser`** ::

❖ By Default Odoo Will Generate a Master Password for You Like This: hg8c-uptq-wmv8 And Give You the Option to Change It.

❖ **But What if We Forgot that Master Password How Can We Reset It?** To Do This We Need to Load a Different Config than the Default One, but **Where that Default Config that Odoo Uses?**

❖ The default configuration file is `$HOME/.odoorc` which can be overridden using `--config` flag or `-c`. Now if We Opened This `odoorc` File with vs Code We Will See Something Like This:



```python
[options]
admin_passwd = $pbkdf2-sha512$600000$ojTG.L/X2tvbu5fS.j9n7A$ggxM013okEij/wdRq3tqa8ULMrebkCqZjh9x9spRw6htgYAMaFW83u1fXeRGmBoLJKPWIyWaQevnWe4lfGHY/A
```

And the Default `odoo.conf` File Which Is Located In `/Users/Ahmed/Documents/odoo-17.0/debian/odoo.conf` Looks Like This:


```python
[options]
; This is the password that allows database operations:
; admin_passwd = admin
db_host = False
db_port = False
db_user = odoo
db_password = False
addons_path = /Users/Ahmed/Documents/odoo-17.0/addons,/Users/Ahmed/Documents/odoo-17.0/custom-addons
default_productivity_apps = True
```

Now We Need to Remove the Hashing From `admin_passwd` By Removing The `;` And the Space After It and Set a New Password We Can Leave It `admin` for Example, Now if We Relaunched the Server After Editing the Line `admin_passwd` and refreshed the localhost we will see a message like this: 

`Warning, your Odoo database manager is not protected.` And Creates a New Default Master Password for You and Give You the Option to Change It

❖ **`Note:`** If You Used `-d` Flag when Launching the Server and Didn't See the Warning You Can Use the Password in the Config as the Master Password

:: __`My Postgres Setup`__ ::


```python
 Role name |                         Attributes                         
-----------+------------------------------------------------------------
 Ahmed     | Superuser, Create role, Create DB, Replication, Bypass RLS
 odoo      | Create DB
 openpg    | Superuser, Create role, Create DB, Replication, Bypass RLS
 postgres  | Superuser
 root      | Create DB
```

:: __`Logging`__ ::

❖ The Logging Is by Default in the Terminal (the Loading when You Run the Server) but You Can Set a Custom Log File with Two Different Ways:

⟶ `First Method [Using --logfile Flag]` => launching the server command will be like this: 


```python
python odoo-bin --logfile /Users/Ahmed/Documents/odoo-17.0/odoo-server.log
```

**`PS`**: Don't Use Quotation Marks in the Path

⟶ `Second Method [Adding the Log in the Config]` => The odoo.config Will Be Like This: 


```python
[options]
; This is the password that allows database operations:
; admin_passwd = admin
db_host = False
db_port = False
db_user = odoo
db_password = False
addons_path = /Users/Ahmed/Documents/odoo-17.0/addons,/Users/Ahmed/Documents/odoo-17.0/custom-addons
default_productivity_apps = True
logfile = /Users/Ahmed/Documents/odoo-17.0/odoo-server.log
log_level = debug
```

And You Will Launch the Server with This Command: 


```python
python odoo-bin --config /Users/Ahmed/Documents/odoo-17.0/debian/odoo.conf
```

**`Note`**: No Loading Will Happen in the Terminal the Loading Will Be in the Log File 

**`VIP NOTE`**: You Can Also for Debugging Purposes only Duplicate The `odoo.conf` File and Remove Everything but The `admin_passwd` Line if the Normal `odoo.config` Didn't Load for some Reason

:: __`Activating Developer Mode and Debugger Icon`__ ::

❖ to Activate the Developer Mode Simply Go to the Home Menu >> Settings >> Scroll Untill You Reach `Developer Tools` >> Activate the Developer Mode

❖ to activate the debugger icon go to the url after word `web` add the following: `?debug=1` so the url should look something like this: 

`http://localhost:8069/web?debug=1#action=311&model=sale.order&view_type=list&cids=1&menu_id=186`

❖ There is a nice extnsion on the chrome web store called `odoo debug` when clicked it activates the developer mode for you.

:: __`Adding Custom Path for Modules`__ ::

❖ You Can Add the Path to Custom Modules in the odoo.config and Use Comma for Separating the Paths Like This: 


```python
addons_path = /Users/Ahmed/Documents/odoo-17.0/addons,/Users/Ahmed/Documents/odoo-17.0/custom-addons
```

❖ You Can Also Use the Following Flag when You Run the Server: 


```python
python odoo-bin --addons-path=addons,custom-addons
```

❖ This Assumes that the Folder `custom-addons` Is Next to The `addons` Default Folder

❖ Don't Forget to Update App List when You Login to See Your Custom Modules

:: __`Database Selector / Database Manager Url`__ ::

❖ To Choose Between Multiple Databases, Use the Following Url:
localhost:8069/web/database/manager
:: __`Create a Module From Scratch and Scaffolding`__ ::

❖ Scaffolding is the automated creation of a skeleton structure to simplify bootstrapping (of new modules, in the case of Odoo). 

❖ Scaffolding is available via the odoo-bin scaffold subcommand


```python
source /Users/ahmed/Documents/odoo-17/.venv/bin/activate # source the venv first
python odoo-bin scaffold my_module /addons/
```

Or Put It in the Custom-Addons Folder We Have:


```python
source .venv/bin/activate # source the venv first
python odoo-bin scaffold my_module custom-addons
```

❖ Assuming of Course that We Are in the Odoo17 Folder

❖ Now Let's Open the Manifest File and Add some Info to Our Module


```python
# -*- coding: utf-8 -*-
{
    'name': "my_module",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Ahmed Hesham",
    'website': "https://wa.me/qr/JQIDUJQE2B7OM1",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


```

❖ Here We Changed the Summary, Description, Author and Website

❖ You Can Find These Info in the Module Info in the Apps [The Three Dots]

❖ The `depends` Line Sets Any Modules Necessary for Our Module to Work Correctly

Note: If You Renamed the Module Folder to `First Module` without the Underscore when You Relaunch the Server You Will Get This Error Message: `The Operation Cannot Be Completed: External IDs Cannot Contain Spaces`

❖ **`Notice`** In Odoo UI There's Two Types of Names in Our Module when You Search a Module There's a Big Name in **Black** and Small Name in **Red** 

⟶ the Big Name in Black => Is the Name of the Module Which Is in the Manifest File **[You Can Add Spaces in This Name]**

⟶ the Small Name in Red => Is the Name of Folder of Your Module **[You Can Not Add Spaces in This Name]**

:: __`Menu Items and Actions`__ ::

❖ If You Installed the Sales Module for Example and Opened the `orders` Sub-Menu Item From `orders` Main-Menu Item You Will Find the Localhost Link Like This: 

`http://localhost:8069/web#action=311&model=sale.order&view_type=list&cids=1&menu_id=186`

❖ See in the Url There's a Certain Action [311] that Is Linked to a Certain Model [sale.order] and There's the View Types Like List View and Maneu Id [186]

↪ If You Clicked the Home Icon in the Top Left Corner and Choosed `Settings` and From There You Clicked the Menu Itme `Technical` and There Under `Data Structure` You Choosed Models; You Will See All the Models of Odoo Which Also Contains [sale.order] and if You Clicked on It You Will See Inside: 

↪ Fields 

↪ Access Rights

↪ Record Rules

↪ Notes

↪ Views

❖ You Can See Which Actions Was Used when You Click the Sub-Menu Orders for Example by Clicking on the **Debugger Icon** and Click on `Edit Actions` 

⟶ You Will See in the External Id the Action Used when You Click the Sub-Menu Orders

:: __`Refactor Module Nmae in Pycharm`__ ::

❖ From Pycharm Right Click on Your Module Name `>>` Refactor `>>` Rename; Set the New Name and Click Refactor; Now Click `Do Refactor` Button in the Buttom Corner of Pycharm

❖ Now From the Top Right Corner Click on Return Odoo Button to Relaunch the Server. 

:: __`Change the Module Icon`__ ::

❖ Right Click on Your Module Name and From New Select Directory and Type: `static/description` This Will Create Static Folder and Create Description Folder Also Inside of the Static Folder

❖ Copy the `icon.png` File You Want to Set and You Can From Pycharm Select the Description Folder and Command ⌘ + V to Paste the Icon Inside the Folder

❖ The icon file must be a png file otherwise it won't display correctly.

:: __`Create Your First Class`__ ::

❖ in `models.py` file:


```python
from odoo import models, fields, api, _

class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    name = fields.Char()
    age = fields.Integer()
    birthday = fields.Date()
```

❖ the Name Field Will Take Input Characters; the Age Will Take Integers [Numbers]; the Birthday Will Take Date

❖ `models.Model` => Is the Constructor that I Use to Make the Students Class

❖ Restart the Server, Activate the Module and Go to Settings `>>` Technical `>>` Models; and Search `students` Class We Created.

❖ Now if You Clicked the Students You Will Find in the Fields the Name and Age and Birthday Data We Entered 

❖ The Other Fields Came From `models.Model` Constructor

❖ In Odoo, a model is an object that represents data or functionality. There are three main types of models in Odoo:

→ `models.Model` The most basic type of model in Odoo. This type of model does not inherit any attributes from another model. The main characteristics of `models.Model` are:

    ❖ The class must be defined in a Python file.
    ❖ The class can have any number of methods and fields.
    ❖ It does not inherit attributes from another model.

→ `models.TransientModel` The models.TransientModel type is used to create temporary data that will be stored in the session context, but not persisted to the database.The main characteristics of models.TransientModel are:

    ❖ The class must be defined in a Python file.
    ❖ It can have any number of methods and fields.
    ❖ It does not inherit attributes from another model, but it's used to create temporary data.

→ `models.AbstractModel` The models.AbstractModel type is used to define an abstract base class that cannot be instantiated directly.The main characteristics of models.AbstractModel are:

    ❖ The class must be defined in a Python file.
    ❖ It can have any number of methods and fields.
    ❖ It cannot be instantiated directly, but it's used as a base class for other models.


:: __`Creating the Proper Views and Access Rights for Our Module `__ ::

❖ Now Think of This Simple Class as the Backend We Want to Create a Front End for It and for that We Will Go to the Views Folder and Open `views.xml` File and we will Create `3` Menu Items

⟶ **Root Menu Item** `=>` the MenuItem We See in the Apps Grid Icon when clicked and Next to the Home Icon

⟶ **Main Menu Item** `=>` the first menu-item next to the root module name which will have sub-menus

⟶ **Sub-Menu Item** `=>` a Child of the Main Menu Item Which Will Trigger an Action when Clicked [This Action Should Be Defined]

❖ Those 3 Will Be the Basic Structure to Our Module

❖ Every Menu Item Should Have a Unique Id

❖ We Also Need to Make the Access Rights for Our Module Otherwise It Won't Show up Unless You Became a Superuser

❖ First in views.xml Do the Following:


```python
<record model="ir.actions.act_window" id="my_module_students_action_window">
      <field name="name">students_action</field>
      <field name="res_model">students</field>
      <field name="view_mode">tree,form</field>
    </record>

    <menuitem
    id="my_module_topLevel_menuItem"
    name="My Module"
    web_icon="my_module/static/description/icon.png"
    />

    <menuitem
    id="my_module_mainLevel_menuItem"
    name="Students Operation"
    parent="my_module_topLevel_menuItem"
    />

    <menuitem
    id="my_module_subLevel_menuItem"
    name="Students"
    parent="my_module_mainLevel_menuItem"
    action="my_module_students_action_window"
    />
```

❖ The First Record to Define Tha Action that Will Be Triggered when the Sub-Level Mneu Item `students` Is Triggered

❖ The Last Line of the Action Definition Sets the Views for Our Module [Tree,form]

❖ After that Comes the Three Menu Items We Mentioned Earlier [Each with a Unique Id]

❖ The Menu Items Follows Parent Child Relation: Students Sub-Menu Item Is a Child of the Main Level Menu Item "Studnets Operation" And so on ...

❖ The Last Menu Item Must Have an Action Which We Defined in the Record Above

❖ Now Let's Handle the Access Rights: In the Security Folder You Will Find a Csv File with a Basic Two Lines Like This: 
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_first_module_first_module,first_module.first_module,model_first_module_first_module,base.group_user,1,1,1,1
❖ The First Line Shows the Basic Structure of Adding the Security and the Second Line Shows an Example that We Need to Change with Our Real Data

❖ as you can see from the structure the required data is seperated by a comma `,` 

❖ The `1.1.1.1` Are Permissions Shown Above in the First Line [Read, Write, Create, Unlink]

❖ unlink `=>` delete

❖ perm [In the First Lin] `=>` Permission

❖ id [in the First Line] `=>` Is the Id We Will Set for Our Access Right and It Must Be Unique [Name of Our Choice]

❖ name [in the First Line] `=>` This Is a Human-Readable Name for the Access Control Rule. It Helps in Identifying the Purpose or Target of the Rule

❖ The `model_id:id` => This Field Specifies the Model to Which the Access Rule Applies.
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
students_access,students,model_students,base.group_user,1,1,1,1
❖ Now the Last Step Is to Go to the `__manifest__.py` and Under the Data Section Remove the Hashing From the Sequrity Line or Add It if It's Not There.


```python
'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
```

❖ Now Relaunch the Server and Upgrade Your Module and Try to Create a Student Name Using the New Button. 

:: __`PRO TIP`__ ::

Sometimes when You Paste the Code the Formatting of that Code Goes All over the Place, Instead of Fixing It Manually There's a Nice Option in Pycharm Under the Code Menu Called `Reformat Code` Which Fix the Formaating for Us

:: __`Defining Views`__ ::

❖ If You Notice Now only the Name Shows We Can't See the Date or Birthday Unless We Clicked on the Data Filed, We Want Now to Show Other Fields [Age, Birthday] and for that We Need to Define the Tree View


```python
<record model="ir.ui.view" id="my_module_students_treeView">
    <field name="name">my_module students Tree View</field>
    <field name="model">students</field>
    <field name="arch" type="xml">
        <tree>
            <field name="name" width="50%"/>
            <field name="age" width="25%"/>
            <field name="birthday" width="25%"/>
        </tree>
    </field>
</record>
```

❖ We Added This Record to Our `views.xml` File, Now Relaunch the Server and Upgrade the Module and You Should See the Name, Age Properly

❖ Now Let's Define the Form View [the View We See when We Click on the Student Name]


```python
<record model="ir.ui.view" id="my_module_students_formView">
    <field name="name">my_module students form View</field>
    <field name="model">students</field>
    <field name="arch" type="xml">
        <form string="Students">
            <sheet>
                <group>
                    <group>
                        <field name="name"/>
                        <field name="age"/>
                    </group>
                    <group>
                        <field name="birthday"/>
                    </group>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

❖ Here We Created a Main Group and Put Two Groups Inside of It the First Group Is for Namd and Age and the Other Group Is for the Birthday

❖ Now After Relaunching the Server You Will Notice the Change when You Click on a Student Name

❖ Now Let's Add Another Field [Note] to Our Module; In Our Class: 


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    name = fields.Char()
    age = fields.Integer()
    birthday = fields.Date()
    note = fields.Text(string="Note")
```

And in `views.xml` File:


```python
<record model="ir.ui.view" id="my_module_students_formView">
      <field name="name">my_module students form View</field>
      <field name="model">students</field>
      <field name="arch" type="xml">
        <form string="Students">
          <sheet>
            <group>
              <group>
                <field name="name"/>
                <field name="age"/>
              </group>
              <group>
                <field name="birthday"/>
                <field name="note"/>
              </group>
            </group>
          </sheet>
        </form>
      </field>
    </record>

    <record model="ir.ui.view" id="my_module_students_treeView">
      <field name="name">my_module students Tree View</field>
      <field name="model">students</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name"/>
          <field name="age"/>
          <field name="birthday"/>
          <field name="note"/>
        </tree>
      </field>
    </record>
```

❖ Now Relaunch the Server and Verify the Note Exists

❖ Now We Want to Review This Note in Other Way `Notebook` Which Is Better than Just a Field with Text Input And This Notebook Will Be Inside the Form View when We Click on the Student Name


```python
<record model="ir.ui.view" id="my_module_students_formView">
    <field name="name">my_module students form View</field>
    <field name="model">students</field>
    <field name="arch" type="xml">
        <form string="Students">
            <sheet>
                <group>
                    <group>
                        <field name="name"/>
                        <field name="age"/>
                    </group>
                    <group>
                        <field name="birthday"/>
                    </group>
                </group>
                <notebook>
                    <page string="Extra Info">
                        <field name="note" placeholder="Type Your Note About This Student"/>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

❖ Now We Want to Add the Status of the Student [Draft(still Not Enrolled), Done(enrolled), Cancel(cacelled)] and Since These Are Multiple Data We Define in It Odoo as Selection

❖ We Add the Following in Our Class: 


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    name = fields.Char()
    age = fields.Integer()
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
    )
```

❖ The Title Case Words Are the Words that Is Shown to the User, Where the Lower Case Words Are in the System

❖ Now We Need to Go to Our Form View and Add a `Header` Before Our `Sheet Tag` Inside the Form View


```python
<header>
    <field name="status" widget="statusbar"/>
</header>
```

❖ Here's the full xml code with the header tag


```python
<odoo>
    <data>
        <record model="ir.actions.act_window" id="my_module_students_action_window">
            <field name="name">students_action</field>
            <field name="res_model">students</field>
            <field name="view_mode">tree,form</field>
        </record>

        <menuitem
                id="my_module_topLevel_menuItem"
                name="My Module"
                web_icon="my_module/static/description/icon.png"
        />

        <menuitem
                id="my_module_mainLevel_menuItem"
                name="Students Operation"
                parent="my_module_topLevel_menuItem"
        />

        <menuitem
                id="my_module_subLevel_menuItem"
                name="Students"
                parent="my_module_mainLevel_menuItem"
                action="my_module_students_action_window"
        />

        <record model="ir.ui.view" id="my_module_students_treeView">
            <field name="name">my_module students Tree View</field>
            <field name="model">students</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="age"/>
                    <field name="birthday"/>
                    <field name="note"/>
                </tree>
            </field>
        </record>

        <record model="ir.ui.view" id="my_module_students_formView">
            <field name="name">my_module students form View</field>
            <field name="model">students</field>
            <field name="arch" type="xml">
                <form string="Students">
                    <header>
                        <field name="status" widget="statusbar"/>
                    </header>
                    <sheet>
                        <group>
                            <group>
                                <field name="name"/>
                                <field name="age"/>
                            </group>
                            <group>
                                <field name="birthday"/>
                            </group>
                        </group>
                        <notebook>
                            <page string="Extra Info">
                                <field name="note" placeholder="Type Your Note About This Student"/>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>

    </data>
</odoo>

```



❖ Now Relaunch the Server and Click on Any Student Name You Will See in the Top Right Corner the 3 Status

❖ Now We Want to Create a Default Value Once We Create a Student to Be Draft How Can We Do that? In Our Class Add the Following:


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    name = fields.Char()
    age = fields.Integer()
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
```

❖ Now when You Relaunch the Server and Create a New Student and Click on It; It's Status Will Be Draft

❖ Now Let's Add the Gender


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    name = fields.Char()
    age = fields.Integer()
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
```

❖ And in `views.xml` File We Will Add the Gender in the Group with Birthday


```python
<record model="ir.ui.view" id="my_module_students_formView">
    <field name="name">my_module students form View</field>
    <field name="model">students</field>
    <field name="arch" type="xml">
    <form string="Students">
        <header>
        <field name="status" widget="statusbar"/>
        </header>
        <sheet>
        <group>
            <group>
            <field name="name"/>
            <field name="age"/>
            </group>
            <group>
            <field name="birthday"/>
            <field name="gender"/>
            </group>
        </group>
        <notebook>
            <page string="Extra Info">
            <field name="note" placeholder="Type Your Note About This Student"/>
            </page>
        </notebook>
        </sheet>
    </form>
    </field>
</record>

<record model="ir.ui.view" id="my_module_students_treeView">
    <field name="name">my_module students Tree View</field>
    <field name="model">students</field>
    <field name="arch" type="xml">
    <tree>
        <field name="name"/>
        <field name="age"/>
        <field name="birthday"/>
        <field name="gender"/>
    </tree>
    </field>
</record>
```

❖ Notice Here in the Tree View I Didn't Show the Note and Made It only Accessible when You Click on the Student Name

❖ Now Relaunch the Server and Create a New Student

❖ There some attributes [like the default attribute] that is included in fields such as required = true or false Also read only

❖ Now Let's Make the Name Required in Our Class


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    name = fields.Char(required = True)
    age = fields.Integer()
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
```

❖ Now when You Upgrade Your Module and Make a New Student if You Tried to Save without Filling the Name You Won't Be Able To. 

❖ Now We Want when We Duplicate the Student the Age Does't Get Duplicated and to Do that We Will Use the Copy Attribute


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    name = fields.Char(required = True)
    age = fields.Integer(copy = False)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
```

❖ Now You Can Duplicate the Name After You Click on It and It Won't Copy the Age

❖ We Didn't Use the Copy Attribute with the Name Cuz the Name Is a Required Field so It Will Result an Error.

❖ Now Let's Add `Chatter` to Our Modeul [Chatter Is: Sending Messages, Logging Notes, and Activities]

❖ To Add the Chatter We Will Make Our Class Inherit From A Bunch of Models and in the Views We Will Add It After the Sheet Tag `<sheet>`

❖ First in `models.py` File: 


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy = False)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
```

❖ `Mixins` are essentially classes that can be reused across multiple modules. They contain reusable code that you can inherit in your module.

❖ By inheriting from these mixins, the current module gains access to their functionality without having to duplicate code or create similar methods and fields itself.

❖ And Since We Inherited From 3 Modules [Portal, Mail, Utm] We Need to Reference Those 3 in Our `__manifest__.py` File


```python
# -*- coding: utf-8 -*-
{
    'name': "my_module",

    'summary': "This Is My First Module in Odoo",

    'description': """
This Is a Test Module Made for Learning Purposes
    """,

    'author': "Ahmed Hesham",
    'website': "https://wa.me/qr/JQIDUJQE2B7OM1",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal', 'mail', 'utm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

```

❖ Now Let's Go to Our `views.xml` File and Add the Following Div After the Sheet Tag


```python
<div class="oe_chatter">
    <field name="message_follower_ids"/>
    <field name="activity_ids"/>
    <field name="message_ids"/>
</div>
```

Here's Our Full Xml File Now 


```python
<odoo>
  <data>

    <record model="ir.ui.view" id="my_module_students_formView">
      <field name="name">my_module students form View</field>
      <field name="model">students</field>
      <field name="arch" type="xml">
        <form string="Students">
          <header>
            <field name="status" widget="statusbar"/>
          </header>
          <sheet>
            <group>
              <group>
                <field name="name"/>
                <field name="age"/>
              </group>
              <group>
                <field name="birthday"/>
                <field name="gender"/>
              </group>
            </group>
            <notebook>
              <page string="Extra Info">
                <field name="note" placeholder="Type Your Note About This Student"/>
              </page>
            </notebook>
          </sheet>
          <div class="oe_chatter">
            <field name="message_follower_ids"/>
            <field name="activity_ids"/>
            <field name="message_ids"/>
          </div>
        </form>
      </field>
    </record>

    <record model="ir.ui.view" id="my_module_students_treeView">
      <field name="name">my_module students Tree View</field>
      <field name="model">students</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name"/>
          <field name="age"/>
          <field name="birthday"/>
          <field name="gender"/>
        </tree>
      </field>
    </record>

    <record model="ir.actions.act_window" id="my_module_students_action_window">
      <field name="name">students_action</field>
      <field name="res_model">students</field>
      <field name="view_mode">tree,form</field>
    </record>

    <menuitem
    id="my_module_topLevel_menuItem"
    name="My Module"
    web_icon="my_module/static/description/icon.png"
    />

    <menuitem
    id="my_module_mainLevel_menuItem"
    name="Students Operation"
    parent="my_module_topLevel_menuItem"
    />

    <menuitem
    id="my_module_subLevel_menuItem"
    name="Students"
    parent="my_module_mainLevel_menuItem"
    action="my_module_students_action_window"
    />


  </data>
</odoo>

```

❖ Now After the Relaunch When You Click on a Student Name You Can See the Three Buttons [Send Message, Log Note, Activity] And You Can Also Upload an Attachment. 

❖ Now Since We Has Now a Log Note Let's Make that if the Age Was Changed It's Loggend in the Log Note We Created and for that We Will Use an Attribute to the Age in Our Class


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy = False, tracking = True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
```

❖ You Can Add This Tracking to Any Field You Want

❖ Now We Want to Add a Feature to `Archive / Unarchive` the Student, Now in the Tree Form when You First Click Students Sub-Menu and Select a Student and Click on the Action Button You Won't See  `Archive / Unarchive` Option. To Add Them We Will Add a Boolean Value to Our Class with Default Value 


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy = False, tracking = True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    active = fields.Boolean(default = True)
```

❖ Now when You Upgrade the Module and Select a Student You Will See Archive / Unarchive Options

❖ When You Archive a Student It Will Disappear From the Tree View, to Unarchive Go the Search Bar and Click on the Arrow Next to the Search Field and Select Custom Search by and Instead of Id Choose Active and Choose Not Set [This Student Is Not Active in Our Tree View]; by Doing so You Will See the Student We Archived and You Can Select It Again and Unarchive It and It Will Show Normal in the Tree View

❖ Next We Will Control the Status of the Document, Right Now We Can't Convert It From Draft to Done for Example and We Will Do This Using the Button Object on the Form View 

❖ Let's Go the Header Tag We Added Earlier and We Will Add a Button to It




```python
<header>
  <button name="action_done" string="Done" type="object" class="oe_highlight" />
  <field name="status" widget="statusbar" />
</header>
```

❖ Now We Need to Define Tha Action `action_done` in Our `models.py` File


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy = False, tracking = True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    active = fields.Boolean(default = True)

    def action_done(self):
        self.status = 'done'
```

❖ Now This Button Will Set the Status to Done

❖ Now Let's Make Two More Buttons the First One Will Convert the Done State to Cancel State and the Other Button Will Reset the Cacelled State Back to Draft 


```python
<header>
  <button name="action_done" string="Done" type="object" class="oe_highlight" />
  <button name="action_cancel" string="Cancel" type="object" class="oe_highlight" />
  <button name="action_draft" string="Reset" type="object" class="oe_highlight" />
  <field name="status" widget="statusbar" />
</header>
```


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy = False, tracking = True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    active = fields.Boolean(default = True)

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'
```

❖ Now We Want to Make that These 3 Buttons Are only Accessible to a Specific Group that We Will Create, to Create a New Group of Users We Will Go to the Security Folder and Create a New File Called `security.xml` And Paste the Following Code Into It


```python
<?xml version="1.0" encoding="utf-8" ?>
<odoo>
    <data noupdate="0">
        <record id="group_school_manager" model="res.groups">
            <field name="name">School Manager</field>
            <field name="category_id" ref="base.module_category_hidden"/>
        </record>
        <record id="group_school_user" model="res.groups">
            <field name="name">School User</field>
            <field name="category_id" ref="base.module_category_hidden"/>
        </record>
    </data>
</odoo>
```

❖ We Created Two Groups of Users the Normal User Group and the Manager Group

❖ Now We Need to Reference that `security.xml` File in Our `__manifest__.py` File


```python
'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/templates.xml',
],
```

❖ Now if You Go to the Settings >> Users & Companies >> Users [Sub-Menu] >> Michell Admin [The Current User] >> Scroll Down to the Technical Section and You Will File the `School Manager` and `School User` 

❖ Now We Want to View the Two Groups in a Separate View and to Do that We Will Add a New Record


```python
<?xml version="1.0" encoding="utf-8" ?>
<odoo>
    <data>
        <record id="module_school_category" model="ir.module.category">
            <field name="name">School</field>
            <field name="visible" eval="0"/>
        </record>
        <record id="group_school_manager" model="res.groups">
            <field name="name">School Manager</field>
            <field name="category_id" ref="module_school_category"/>
        </record>
        <record id="group_school_user" model="res.groups">
            <field name="name">School User</field>
            <field name="category_id" ref="module_school_category"/>
        </record>
    </data>
</odoo>
```

❖ This Creates a New Category Named School and Notice that We Are Referencing the Category Id in the `Category_id` of Each Group; Now when You Relaunch the Server You Will See the a New Category Called School with Our Two Options [School Manager & School User]

❖ In Odoo, when creating a field and setting the 'eval' number to 1, this number typically represents the field's sequence or order in the user interface. For example, in a form view, fields are displayed in the order of their 'eval' values, with lower numbers appearing first. This helps in organizing the layout and ensuring a logical flow of information for users.

❖ Now We Want to Give Certain Permissions to These Groups: 

⟶ **The School Manager** `=>` Can Read, Create, Update, Delete

⟶ **The School User** `=>` Can Read, Create, Update, Can't Delete

❖ We Will Go to Our Csv File in the Security Folder and Add Two New Lines as Follows:
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
students_access,students,model_students,base.group_user,1,1,1,1
manager_group_access,students,model_students,my_module.group_school_manager,1,1,1,1
users_group_access,students,model_students,my_module.group_school_user,1,1,1,0
❖ But to Test This We Must Remove the Line that Gives Access to the Base Group User [the Second Line] and Make Michell Admin [the Current Admin] a School Manager and Create a New User, Set It to School User and Try to Remove a Student with that School User Account, You Can't. 

❖ When you create a new user you will see the `Email Address` and the `Name` but you won't see the `Password`. to make a passworkd click on the small cog icon next to the user name and choose `Change Password`. select the user you created and add a password to it. finally log out of the user `Michell Admin` and log in with the new user we created.
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
manager_group_access,students,model_students,my_module.group_school_manager,1,1,1,1
users_group_access,students,model_students,my_module.group_school_user,1,1,1,0
❖ Now We Want to Make the Three Buttons [Done, Cancel, Reset to Draft] Available only to the School Manager Users and to do that We Will Go to Our `views.xml` File


```python
<header>
    <button name="action_done" groups="my_module.group_school_manager" string="Done" type="object"
            class="oe_highlight"/>
    <button name="action_cancel" groups="my_module.group_school_manager" string="Cancel" type="object"
            class="oe_highlight"/>
    <button name="action_draft" groups="my_module.group_school_manager" string="Reset" type="object"
            class="oe_highlight"/>
    <field name="status" widget="statusbar"/>
</header>
```

❖ When We Use `groups="...."` to Correctly Reference the Group You Need to Mention Your Module First and in This Case the Module Name Is `my_module` and Then the Dot and Then the Group Id

❖ Also Make Sure in Your `__manifest__.py` You Load the `security.xml` First


```python
'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/templates.xml',
],
```

❖ Now We Want to Make some Buttons Inactive in some Senarios (Like if the Student State Is Done the Done Button Becomes Incactive and so On) And We Will Do This Using the `modifiers` Attribute


```python
<header>
    <button name="action_done" class="oe_highlight" groups="my_module.group_school_manager" string="Done"
            type="object"
            invisible="status not in ['draft', 'cancel']"/>
    <button name="action_cancel" invisible="status not in ['draft', 'done']"
            groups="my_module.group_school_manager" string="Cancel" type="object" class="oe_highlight"/>
    <button name="action_draft" invisible="status not in ['cancel', 'done']"
            groups="my_module.group_school_manager" string="Reset" type="object" class="oe_highlight"/>
    <field name="status" widget="statusbar"/>
</header>
```

❖ Now Based on the Status of the Student only Two Buttons Will Appear if the Status = Done the Draft and Cancel Button Will Show and so on ..

❖ in odoo 16 we should use the `attrs` attribute like this: 


```python
<header>
    <button name="action_done" class="oe_highlight" groups="my_module.group_school_manager" string="Done"
            type="object"
            attrs="{'invisible': [('status', 'not in', ['draft', 'cancel'])]}"/>
    <button name="action_cancel" string="Cancel" groups="my_module.group_school_manager"
            type="object" class="oe_highlight"
            attrs="{'invisible': [('status', 'not in', ['draft', 'done'])]}"/>
    <button name="action_draft" string="Reset" groups="my_module.group_school_manager"
            type="object" class="oe_highlight"
            attrs="{'invisible': [('status', 'not in', ['cancel', 'done'])]}"/>
    <field name="status" widget="statusbar"/>
</header>
```



❖ Now We Want to Create a New Field Under the Age Group to Show Which User Created the Student? 


```python
<group>
    <field name="name"/>
    <field name="age"/>
    <field name="create_uid"/>
</group>
```

❖ Note: The `create_uid` Is a Field Automatically Created when We Create Our Module We're Just Showing It in a Field Now, but if You Activate the Debug Mode and Clicked the Bug Icon and Clicked on `view fields` You Will Find the `create_uid` Field

❖ Now This Filed `create_uid` Will Be Shown to All Users, if You Logged Out From Michell Admin [the Current User Admin] and Logged Using Ahmed [the School User We Created] You Will See that Ahmed Can See the Students Created by Michell Admin and We Want to Make The `group school user` See only the Students they Created While `group school manager` Can See Every Student and to Do that We Will Add a New Record  in Our `security.xml` File


```python
<record id="school_user_see_limit" model="ir.rule">
    <field name="name">Group School User and Create UID</field>
    <field name="model_id" ref="my_module.model_students"/>
    <field name="groups" eval="[(4, ref('my_module.group_school_user'))]"/>
    <field name="perm_read" eval="1"/>
    <field name="perm_write" eval="0"/>
    <field name="perm_create" eval="0"/>
    <field name="perm_unlink" eval="1"/>
    <field name="domain_force">[('create_uid','=',user.id)]</field>
</record>
```

:: __`Very Important Notes`__ ::

❖ When Referencing the `model_id` and `groups` We Should Correctly Reference Both of Them by Using `my_model` Which Is the Name of the Module and Then the Dot[`.`] and After that the Model/Group Name

❖ when We Set the `prem_read` and `perm_unlink` to `1` This Means We Tell Odoo Don't Give Permission to Read or Delete a Student Unless [`domain_force`] the One Who Created the Student [`create_uid`] = The Current User [`user.id`] In Other Words if the Current User Isn't the User Who Created the Student Don't Show the Student

❖ The `user.id` Can Be a Number Like 5 or 7; as You See Every User Has Id We Can Find It if We Logged Out of Ahmed [School User] and Logged in with Admin [School Manager] and Go to **Settings >> Users & Groups >> Users** and Clicked on a User You Will See The Id in the Url Which Corresponds to the User Itself I Found that Ahmed [School User] Id = `9` From the Admin Login and I Re-Logged with Ahmed and Changed the Code to This `<field name="domain_force">[('create_uid','=',9)]</field>` and the Rule Was Applied Susccessfuly and only the Students Created by Ahmed Were Shown in the Fields. 

❖ In This Example The `user_id` Must Be without Quotes `''` Where the `'create_uid'` Must Be in Quotes `=>` This Is What Worked in My Case 

❖ When constructing domain expressions in Odoo, it’s important to remember that the left-hand side (LHS) and right-hand side (RHS) of the comparison are treated differently:

⟶ **`Field Names (LHS):`** These are always strings and represent the fields of the model.

⟶ **`Values (RHS)`**: These can be literals (strings, integers, etc.) or dynamic expressions. In the case of dynamic expressions like user.id, they should not be quoted as strings.

❖ When I First Copied the Rule Record Structure From Odoo Documentation It Used in the (RHS) a Quoted Value Here's What's From Odoo Documentation And the Example Odoo Uses: 

"A record rule restricts the access rights to a subset of records of the given model. A rule is a record of the model ir.rule, and is associated to a model, a number of groups (many2many field), permissions to which the restriction applies, and a domain. The domain specifies to which records the access rights are limited.

Here is an example of a rule that prevents the deletion of leads that are not in state cancel. Notice that the value of the field groups must follow the same convention as the method write() of the ORM."

And Here's the Code Odoo Uses: 



```python
<record id="delete_cancelled_only" model="ir.rule">
    <field name="name">Only cancelled leads may be deleted</field>
    <field name="model_id" ref="crm.model_crm_lead"/>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_manager'))]"/>
    <field name="perm_read" eval="0"/>
    <field name="perm_write" eval="0"/>
    <field name="perm_create" eval="0"/>
    <field name="perm_unlink" eval="1" />
    <field name="domain_force">[('state','=','cancel')]</field>
</record>
```

:: __`Now the Big Question?`__ ::

❖ **How the Example of Odoo Documentation Is Different From My Example or in Other Words How the `user.id` Is Different From the `cancel` State Odoo Used in It's Example. Why Odoo Uses Quotes in It's Example when I Can't Use Quotes?**

❖ To Understand This We Need to Learn the Difference Between: **Static Values** vs. **Dynamic Values**

**Static Values**:

⟶ In the Odoo documentation example, 'cancel' is a `static value`. It's a constant string that directly corresponds to a specific state in the state field of the model.

⟶ Static values are always quoted because they are literals that Odoo needs to match exactly in the database

**Dynamic Values**:

⟶ `user.id` is a dynamic value. It represents the ID of the currently logged-in user, which can change based on who is using the system.

⟶ When you use dynamic values, Odoo needs to evaluate them at runtime, so they should not be quoted. If you quote them, they will be treated as static string values rather than expressions to be evaluated.

**Summary**

❖ The difference in quoting is crucial because it distinguishes between values that are static and constant (like `'cancel'`) versus values that are dynamic and need to be computed at runtime (like `user.id`). The former are quoted to indicate their static nature, while the latter are left unquoted so they can be evaluated correctly.

:: __`Creating a Simple Div and Using jQuery to Print a Message to the Console`__ ::

First We Will Add the Following Line to Our Class in `models.py` File


```python
div_field = fields.Char(string="Div Field")
```

So Now Our Class Looks Like This:


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy = False, tracking = True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    active = fields.Boolean(default = True)

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'

    div_field = fields.Char(string="Div Field")
```

Next We Will Add the Div and Our Js Code in `views.xml` File


```python
<div class="custom_div">
    <field name="div_field" style="width:500px;"/>
    <script type="text/javascript">
        $(document).ready(function() {
        console.log('Hello from the custom_div using jQuery!');
        });
    </script>
</div>
```

**Notice** that We Added a Class to the Div This Class Is Linked to Our Css File in the Following Directory `odoo-17.0/custom-addons/my_module/static/src/css/main.css`, Here's the Css Styling We Used on This Div. 

.custom_div .o_field_char {
    font-size: x-large;
    width: 500px;  /* or a specific width like 500px */
    box-sizing: border-box;  /* Ensure padding and border are included in the element's total width and height */
}
❖ Also Notice in the Xml that We Used `Style` Attribute to Set the the Width of the Field

:: __`Create Button and Link It to Javascript Function`__ ::

**We Will Demonstrate Two Ways to Achieve This:**

The First Method Using the Script Tag: 


```python
<button id="calling_js_button" name="calling_js" class="oe_highlight" string="Calling Javascript"
        type="object"/>
<script type="text/javascript">
$(document).ready(function() {
$('#calling_js_button').click(function() {
console.log('Hello From Calling JS Button Using jQuery');
});
});
</script>
```

❖ We Defined The `calling_js` Function in Our Class to Return True Just so Odoo Doesn't Give Us Error

❖ The Second Method Using Custom Javascript File in the Static Folder `odoo-17.0/custom-addons/my_module/static/src/js/main.js`

❖ Adding the File in The `__manifest__.py` File


```python
'assets': {
    'web.assets_backend': [
        'my_module/static/src/css/main.css',
        'my_module/static/src/js/main.js'
    ],
},
```

Adding the Button in Our XML:


```python
<button style="margin-left: 10px;" id="callingMainJSFile" name="calling_mainJS" string="Calling Custom Javascript File" type="object" class="oe_highlight custom-button-spacing"/>
```

❖ We Set a Style with Margin 10Px Just so This Button Is a Little Far Apart From the Previous Button

❖ The Id Will Be Used in Our Javascript to Execute a Function

❖ we defined `calling_mainJS` Function in Our Class to Return True Just so Odoo Doesn't Give Us Error

❖ We Also Add Another Class `custom-button-spacing` To Use in Our Css, Here's the Css Code:
.custom-button-spacing {
    margin-left: 10px;
}
Now Let's Add the Following jQuery Code in Our Javascript File:


```python
$(document).ready(function() {
    console.log('Custom script loaded');

    var buttonSelector = '#callingMainJSFile';
    checkButtonAndBindClickEvent();

    function checkButtonAndBindClickEvent() {
        if ($(buttonSelector).length > 0) {
            console.log('Button found in DOM');
            bindClickEvent();
        } else {
            console.log('Button NOT found in DOM');
            setTimeout(checkButtonAndBindClickEvent, 500); // Check again after 500ms
        }
    }

    function bindClickEvent() {
        $(buttonSelector).on('click', function() {
            console.log('Hello From Main.js File!');
        });
    }
});
```

**Here's an Explanation From `claude.ai` to This jQuery Code:**

The approach I used in the updated code is a bit different from the previous attempts, and it's worth understanding how it works and why it was successful.

**Here's a breakdown of what's happening:**

1. **Defining the button selector**: We start by defining a variable `buttonSelector` that holds the selector for the button element (`'#callingMainJSFile'`). This allows us to easily change the selector if needed without modifying the rest of the code.

2. **Calling the initial function**: We call the `checkButtonAndBindClickEvent` function on document ready. This function is responsible for checking if the button element exists and binding the click event handler.

3. **The `checkButtonAndBindClickEvent` function**: This function uses jQuery's `$(buttonSelector).length` to check if the button element exists in the DOM. If it does, it calls the `bindClickEvent` function to bind the click event handler. If the button element is not found, it logs a message to the console and sets a timeout to call itself again after 500ms (you can adjust this delay as needed).

4. **Recursively checking for the button**: By calling `setTimeout(checkButtonAndBindClickEvent, 500)`, we're creating a recursive loop that continuously checks for the existence of the button element. This approach is useful when dealing with dynamically rendered content or elements that might not be available immediately when the script loads.

5. **Binding the click event handler**: The `bindClickEvent` function uses jQuery's `$(buttonSelector).on('click', function() { ... })` to bind the click event handler directly to the button element. This ensures that the event handler is attached to the correct element and will fire when the button is clicked.

**The key advantages of this approach are:**

1. **Simplicity**: The code is relatively straightforward and easy to understand.

2. **Robustness**: By continuously checking for the button element, we ensure that the click event handler is bound as soon as the element becomes available, regardless of when or how it's rendered in the DOM.

3. **Flexibility**: If the button selector needs to change for any reason, we only need to update the `buttonSelector` variable, and the rest of the code will work seamlessly.

❖ The recursive nature of the `checkButtonAndBindClickEvent` function might seem a bit unconventional, but it's a common pattern used when dealing with dynamically rendered content or elements that might not be available immediately. By continuously checking for the element's existence and binding the event handler as soon as it's found, we can ensure that our code works correctly, even in scenarios where the DOM is updated or modified after the initial page load.

❖ This approach worked because it allowed the code to wait for the button element to be rendered and available in the DOM before binding the click event handler.

:: __`Back to Odoo - Adding A Search Record`__ ::

❖ Right Now if You Go to the Students and Typed `m` You Will See that You Can only Search the Name for the Letter `m` but What if I Want to Search only Male Students? Also if You Typed Any Number Ou Will See that You Can only Search the Name but What if I Want to Search Students Age; Students Who Are 22 Years Old for Example? You Can't, to Fix that We Will Add a Search Record in Our `views.xml` File


```python
<record id="view_student_filter" model="ir.ui.view">
<field name="name">students.search</field>
<field name="model">students</field>
<field name="arch" type="xml">
    <search string="students">
        <field name="name" string="Student Name"/>
        <field name="age" string="Age"/>
        <field name="gender" string="Gender"/>
    </search>
</field>
</record>
```

❖ Now We Added Search Fields for the Name, Age, and Gender, if You Typed the Letter `m` Now You Will See that You Can Search Name, Gender and if You Typed a Number You Can Search the Age

❖ Now We Want to Add a Filter to Filter Students Age [Small, Medium, Large] Where Small Is Lesser than 12 Years Old and Medium Is Between 12 and 17 Years Old and Large Is More than 17 Years Old, to Do that We Will Add a Separator after the gender and before the closing search tag in Our Search View Like the Following: 


```python
<separator/>
<filter name="Small" string="Small Student" domain="[('age', '&lt;', 12)]"/>
<filter name="Medium" string="Medium Student" domain="[('age', '&gt;=', 12), ('age', '&lt;', 17)]"/>
<filter name="Large" string="Large Student" domain="[('age', '&gt;=', 17)]"/>
```

:: __`What Is Domain in Odoo`__ ::

In Odoo, **Domains** are used to filter records in relational fields like Many2one, One2many, and Many2many. Domains can be applied in two main ways:

❖ **Dynamically in Python Code**: Using the @api.onchange decorator to modify the domain based on the current state of the record.

❖ **Statically in XML**: Directly specifying the domain in the view definition, which applies a static filter on the field.

**Interaction Between Python and XML Domains**:

❖ **When you specify a domain in the XML**, it acts as a static filter that is always applied when the form is loaded or refreshed. This means that the field will always be pre-filtered according to the domain specified in the XML.

❖ **When you use the @api.onchange method in Python**, you're dynamically modifying the domain of the field based on the value of another field. This modification only happens when the specified field (grade in this case) changes.

So Now Our Record Will Be Like This: 


```python
<record id="view_student_filter" model="ir.ui.view">
<field name="name">students.search</field>
<field name="model">students</field>
<field name="arch" type="xml">
    <search string="students">
        <field name="name" string="Student Name"/>
        <field name="age" string="Age"/>
        <field name="gender" string="Gender"/>
        <separator/>
        <filter name="Small" string="Small Student" domain="[('age', '&lt;', 12)]"/>
        <filter name="Medium" string="Medium Student" domain="[('age', '&gt;=', 12), ('age', '&lt;', 17)]"/>
        <filter name="Large" string="Large Student" domain="[('age', '&gt;=', 17)]"/>
    </search>
</field>
</record>
```

❖ Now if You Click on the Small Arrow Next to the Search Bar You Will See in the Filter the Small, Medium, and Large 

❖ Now if You See the Group by Section You Will Notice that It's Empty, We Want to Group the Students by Age or Gender, to Do This We Will Add Another Separator and the Group Filter as Follows:


```python
<separator/>
<group expand="0" string="Group By">
<filter string="Gender" name="Gender" domain="[]" context="{'group_by': 'gender'}"/>
<filter string="Age" name="Age" domain="[]" context="{'group_by': 'age'}"/>
</group>
```

❖ So Our Record Now Should Look Like This: 


```python
<record id="view_student_filter" model="ir.ui.view">
<field name="name">students.search</field>
<field name="model">students</field>
<field name="arch" type="xml">
    <search string="students">
        <field name="name" string="Student Name"/>
        <field name="age" string="Age"/>
        <field name="gender" string="Gender"/>
        <separator/>
        <filter name="Small" string="Small Student" domain="[('age', '&lt;', 12)]"/>
        <filter name="Medium" string="Medium Student" domain="[('age', '&gt;=', 12), ('age', '&lt;', 17)]"/>
        <filter name="Large" string="Large Student" domain="[('age', '&gt;=', 17)]"/>
        <separator/>
        <group expand="0" string="Group By">
            <filter string="Gender" name="Gender" domain="[]" context="{'group_by': 'gender'}"/>
            <filter string="Age" name="Age" domain="[]" context="{'group_by': 'age'}"/>
        </group>
    </search>
</field>
</record>
```

❖ Now You Can Group by Age or Gender

:: __`Model Constraints`__ ::

❖ We Want to Constrain Students Age to Be Between 7 and 15 Years; so the System Can't Save Student with Age Less than 7 or Greater than 16 Years Old.

❖ To Achieve that We Need to Import the Validation Error and Access Error Libraries From Odoo


```python
from odoo.exceptions import ValidationError, AccessError
```

And We Need to Add the Following Decorator in our Code:


```python
@api.constrains('age')
def _check_student_age(self):
    for record in self:
        if record.age < 7 or record.age > 16:
            raise ValidationError(
                _("The Age Of Student Must Be equal or Greater Than 7 And Equal Or Less Than 16 Years."))
```

❖ So Now Our `models.py` File Should Look Like This


```python
# -*- coding: utf-8 -*-

# from odoo import models, fields, api
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError



class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy = False, tracking = True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    active = fields.Boolean(default = True)

    @api.constrains('age')
    def _check_student_age(self):
        for record in self:
            if record.age < 7 or record.age > 16:
                raise ValidationError(
                    _("The Age Of Student Must Be equal or Greater Than 7 And Equal Or Less Than 16 Years."))

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'

    div_field = fields.Char(string="Div Field")

    def calling_js(self):
        return True

    def calling_mainJS(self):
        return True

```

❖ Now if You Tried to Create a New Student Who's Age Is More than 16 or Less than 7 You Will Get the Validation Error with Our Message

❖ Now We Want to Make Our Name Unique so No Duplicated Student Names, Let's Use Another Type of Constraints `sql constraints`


```python
_sql_constraints = [
    ('name_unique', 'unique (name)',
     'The Name must be unique!'),
]
```

Now Our `models.py` File Should Look Like This:


```python
# -*- coding: utf-8 -*-

# from odoo import models, fields, api
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError



class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy = False, tracking = True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    active = fields.Boolean(default = True)

    @api.constrains('age')
    def _check_student_age(self):
        for record in self:
            if record.age < 7 or record.age > 16:
                raise ValidationError(
                    _("The Age Of Student Must Be equal or Greater Than 7 And Equal Or Less Than 16 Years."))

    _sql_constraints = [
        ('name_unique', 'unique (name)',
         'The Name must be unique!'),
    ]

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'

    div_field = fields.Char(string="Div Field")

    def calling_js(self):
        return True

    def calling_mainJS(self):
        return True

```

❖ Now if You Tried to Create a Student with a Name Was Already Registered You Will Get the Error Message

:: __`Adding Computed Field  - Age Field Computed From Date Field`__ ::

❖ Now We Want to Make the Age Field Calculated Automatically when We Set the Birthday Field; To Do This We Will Add Attribute `compute` to the Age Field in Our Python Calss and and This Attribute Will Pass a Function that We Need to Define as Follows:

↪ First We Need to Import some Modules Like `datetime`


```python
from datetime import *
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
```

❖ Next We Add the Compute Attribute to Our Age


```python
age = fields.Integer(copy=False, tracking=True, compute='_compute_age', store=True)
```

❖ We Also Added the `store` Attribute Which Will Make the Age Field Searchable and This Is Necessary if We're Adding Filters in Our Search View Record

❖ Next We Difine the `_compute_age` Function:


```python
@api.depends('birthday')
def _compute_age(self):
    for record in self:
        if record.birthday:
            d1 = datetime.strptime(str(record.birthday), "%Y-%m-%d").date()
            d2 = date.today()
            record.age = relativedelta(d2, d1).years
        else:
            record.age = 0
```

❖ The `_compute_age` method is a computed method that calculates the age of a student based on their birthday. The `@api.depends('birthday')` decorator tells Odoo that this method depends on the `birthday` field, so whenever the `birthday` field is updated, this method will be automatically recomputed.

❖ The method loops through each record in `self` (which is a recordset of `students` objects) and checks if the `birthday` field is set. If it is, the method calculates the age of the student using the `relativedelta` function from the `dateutil` library.

❖ **Here's a breakdown of the code inside the `if` statement:**

↪ `d1 = datetime.strptime(str(record.birthday), "%Y-%m-%d").date()`: This line converts the `birthday` field (which is a `date` object) to a `datetime` object, and then extracts the `date` component from it. The `strptime` method is used to parse the `birthday` string into a `datetime` object, using the format `"%Y-%m-%d"` (which corresponds to the format of the `date` object).

↪ `d2 = date.today()`: This line gets the current date using the `date.today()` method from the `datetime` library.

↪ `record.age = relativedelta(d2, d1).years`: This line calculates the age of the student by subtracting their birthday from the current date using the `relativedelta` function. The `relativedelta` function returns a `relativedelta` object that represents the difference between two dates. The `years` attribute of this object returns the number of full years between the two dates. This value is then assigned to the `age` field of the current record.

❖ If the `birthday` field is not set, the method sets the `age` field to 0.

❖ So Our models.py File Should Look Like This:


```python
# -*- coding: utf-8 -*-

# from odoo import models, fields, api
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

from datetime import *
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta



class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy = False, tracking = True, compute = '_compute_age')
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    active = fields.Boolean(default = True)

    @api.constrains('age')
    def _check_student_age(self):
        for record in self:
            if record.age < 7 or record.age > 16:
                raise ValidationError(
                    _("The Age Of Student Must Be equal or Greater Than 7 And Equal Or Less Than 16 Years."))

    _sql_constraints = [
        ('name_unique', 'unique (name)',
         'The Name must be unique!'),
    ]

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                d1 = datetime.strptime(str(record.birthday), "%Y-%m-%d").date()
                d2 = date.today()
                record.age = relativedelta(d2, d1).years
            else:
                record.age =0


    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'

    div_field = fields.Char(string="Div Field")

    def calling_js(self):
        return True

    def calling_mainJS(self):
        return True

```

❖ Now when You Set the Birthday the Age Will Be Automatically Calculated.

:: __`Onchange Decorator`__ ::

❖ We Want to Create Two New Fields `Grade` and `Teacher` and We Want to Make that when Grade 1 Is Selected only the Teachers of that Grad Appear in the Teacher Field

❖ First We Need to Create a New Teacher Class Which Will Have Most of the  Properties as the Students Class; So Under the Student Class We Will Put the Following Teacher Class:


```python
class teachers(models.Model):
    _name = 'teachers'
    _description = 'This Model Represents the Teachers Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required=True)
    age = fields.Integer(copy=False, tracking=True, compute='_compute_age', store=True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default='draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    active = fields.Boolean(default=True)

    @api.constrains('age')
    def _check_teacher_age(self):
        for record in self:
            if record.age < 22:
                raise ValidationError(
                    _("The Age Of the Teacher Must Be Greater than 22."))

    _sql_constraints = [
        ('name_unique', 'unique (name)',
         'The Name must be unique!'),
    ]

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                d1 = datetime.strptime(str(record.birthday), "%Y-%m-%d").date()
                d2 = date.today()
                record.age = relativedelta(d2, d1).years
            else:
                record.age = 0

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'
```

❖ As You Can See We Changed the Age Constraints Along with some Basic Info

❖ Next We Will Add some Code in Our `views.xml` File Under the Students Code


```python
<!--Teacher Code Here-->
<record id="view_teacher_filter" model="ir.ui.view">
    <field name="name">teachers.search</field>
    <field name="model">teachers</field>
    <field name="arch" type="xml">
        <search string="Teachers">
            <field name="name" string="Teacher Name"/>
            <field name="age" string="Age"/>
            <field name="gender" string="Gender"/>
            <separator/>
            <filter name="Small" string="Small Teacher" domain="[('age', '&lt;', 30)]"/>
            <filter name="Medium" string="Medium Teacher" domain="[('age', '&gt;=', 30), ('age', '&lt;', 50)]"/>
            <filter name="Large" string="Large Teacher" domain="[('age', '&gt;=', 50)]"/>
            <separator/>
            <group expand="0" string="Group By">
                <filter string="Gender" name="Gender" domain="[]" context="{'group_by': 'gender'}"/>
                <filter string="Age" name="Age" domain="[]" context="{'group_by': 'age'}"/>
            </group>
        </search>
    </field>
</record>

<record model="ir.ui.view" id="my_module_teachers_formView">
<field name="name">my_module teachers form View</field>
<field name="model">teachers</field>
<field name="arch" type="xml">
    <form string="Teachers">
        <header>
            <button name="action_done" class="oe_highlight" groups="my_module.group_school_manager"
                    string="Done"
                    type="object"
                    invisible="status not in ['draft', 'cancel']"/>
            <button name="action_cancel" invisible="status not in ['draft', 'done']"
                    groups="my_module.group_school_manager" string="Cancel" type="object"
                    class="oe_highlight"/>
            <button name="action_draft" invisible="status not in ['cancel', 'done']"
                    groups="my_module.group_school_manager" string="Reset" type="object"
                    class="oe_highlight"/>
            <field name="status" widget="statusbar"/>
        </header>
        <sheet>
            <group>
                <group>
                    <field name="name"/>
                    <field name="age"/>
                    <field name="create_uid"/>
                </group>
                <group>
                    <field name="birthday"/>
                    <field name="gender"/>
                </group>
            </group>
            <notebook>
                <page string="Extra Info">
                    <field name="note" placeholder="Type Your Note About This Teacher"/>
                </page>
            </notebook>
        </sheet>
        <div class="oe_chatter">
            <field name="message_follower_ids"/>
            <field name="activity_ids"/>
            <field name="message_ids"/>
        </div>
    </form>
</field>
</record>

<record model="ir.ui.view" id="my_module_teachers_treeView">
<field name="name">my_module teachers Tree View</field>
<field name="model">teachers</field>
<field name="arch" type="xml">
    <tree>
        <field name="name"/>
        <field name="age"/>
        <field name="birthday"/>
        <field name="gender"/>
    </tree>
</field>
</record>

<record model="ir.actions.act_window" id="my_module_teachers_action_window">
<field name="name">teachers_action</field>
<field name="res_model">teachers</field>
<field name="view_mode">tree,form</field>
</record>

<menuitem
id="my_module_teacher_mainLevel_menuItem"
name="Teachers Operation"
parent="my_module_topLevel_menuItem"
/>

<menuitem
id="my_module_teacher_subLevel_menuItem"
name="Teachers"
parent="my_module_teacher_mainLevel_menuItem"
action="my_module_teachers_action_window"
/>

```

❖ Next We Will Add the Security for the Teachers in `ir.model.access.csv` File
teacher_manager_group_access,teachers,model_teachers,my_module.group_school_manager,1,1,1,1
teacher_users_group_access,teachers,model_teachers,my_module.group_school_user,1,1,1,0
Now Our File Should Look Like This:
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
manager_group_access,students,model_students,my_module.group_school_manager,1,1,1,1
users_group_access,students,model_students,my_module.group_school_user,1,1,1,0

teacher_manager_group_access,teachers,model_teachers,my_module.group_school_manager,1,1,1,1
teacher_users_group_access,teachers,model_teachers,my_module.group_school_user,1,1,1,0
❖ Now We've Successfuly Made the Teacher Structure in Our Module

❖ Next Let's Add the Teacher Field in Our Students Class:


```python
grade_teacher = fields.Many2one('teachers',string="Grade Teacher")
```

So Now Our Students Class Should Look Like This:


```python
class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required=True)
    age = fields.Integer(copy=False, tracking=True, compute='_compute_age', store=True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default='draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )

    grade_teacher = fields.Many2one('teachers', string="Grade Teacher")
    active = fields.Boolean(default=True)

    @api.constrains('age')
    def _check_student_age(self):
        for record in self:
            if record.age < 7 or record.age > 16:
                raise ValidationError(
                    _("The Age Of Student Must Be equal or Greater Than 7 And Equal Or Less Than 16 Years."))

    _sql_constraints = [
        ('name_unique', 'unique (name)',
         'The Name must be unique!'),
    ]

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                d1 = datetime.strptime(str(record.birthday), "%Y-%m-%d").date()
                d2 = date.today()
                record.age = relativedelta(d2, d1).years
            else:
                record.age = 0

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'

    div_field = fields.Char(string="Div Field")

    def calling_js(self):
        return True

    def calling_mainJS(self):
        return True

```

❖ Next We Will Go to Our views.xml File and Add the Grade Teacher Field in the Student Code as Follows:


```python
<group>
    <field name="name"/>
    <field name="age"/>
    <field name="create_uid"/>
    <field name="grade_teacher"/>
</group>
```

❖ Next We Will Add a New Selection Field in Our Python File [In the Students Class] Which Represents the Grade1, Grade2, and Grade3


```python
grade_teacher = fields.Many2one('teachers', string="Grade Teacher")
grade = fields.Selection(
    [('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3')], string="Grade"
)
```

❖ Next We Will Add This Same Grade Field in the Teacher Class as Well

❖ Next in Our views.xml File We Will Add the `Grade Field` in Both the Teacher and Student Code


```python
<group>
    <field name="grade"/>
    <field name="birthday"/>
    <field name="gender"/>
</group>
```

❖ Next We Will Add a Domain to the `grade_teacher` Field in Our `views.xml` File in the Students Form View only To Bind [Link] It with Grade Field


```python
<field name="grade_teacher" domain="[('grade', '=', grade)]"/>
```

So Now Our `models.py` File Should Look Like This:


```python
# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

from datetime import *
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta



class students(models.Model):
    _name = 'students'
    _description = 'This Model Represents the Students Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required = True)
    age = fields.Integer(copy=False, tracking=True, compute='_compute_age', store=True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default = 'draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )

    grade_teacher = fields.Many2one('teachers',string="Grade Teacher")
    grade = fields.Selection(
        [('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3')], string="Grade"
    )
    active = fields.Boolean(default = True)

    @api.constrains('age')
    def _check_student_age(self):
        for record in self:
            if record.age < 7 or record.age > 16:
                raise ValidationError(
                    _("The Age Of Student Must Be equal or Greater Than 7 And Equal Or Less Than 16 Years."))

    _sql_constraints = [
        ('name_unique', 'unique (name)',
         'The Name must be unique!'),
    ]

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                d1 = datetime.strptime(str(record.birthday), "%Y-%m-%d").date()
                d2 = date.today()
                record.age = relativedelta(d2, d1).years
            else:
                record.age =0


    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'

    div_field = fields.Char(string="Div Field")

    def calling_js(self):
        return True

    def calling_mainJS(self):
        return True


class teachers(models.Model):
    _name = 'teachers'
    _description = 'This Model Represents the Teachers Object'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(required=True)
    age = fields.Integer(copy=False, tracking=True, compute='_compute_age', store=True)
    birthday = fields.Date()
    note = fields.Text(string="Note")
    status = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Canceled')]
        , default='draft'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
    )
    grade = fields.Selection(
        [('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3')], string="Grade"
    )
    active = fields.Boolean(default=True)

    @api.constrains('age')
    def _check_teacher_age(self):
        for record in self:
            if record.age < 22:
                raise ValidationError(
                    _("The Age Of the Teacher Must Be Greater than 22."))

    _sql_constraints = [
        ('name_unique', 'unique (name)',
         'The Name must be unique!'),
    ]

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                d1 = datetime.strptime(str(record.birthday), "%Y-%m-%d").date()
                d2 = date.today()
                record.age = relativedelta(d2, d1).years
            else:
                record.age = 0

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_draft(self):
        self.status = 'draft'



```

And Our `views.xml` Should Look Like This:


```python
<odoo>
    <data>

        <record id="view_student_filter" model="ir.ui.view">
            <field name="name">students.search</field>
            <field name="model">students</field>
            <field name="arch" type="xml">
                <search string="students">
                    <field name="name" string="Student Name"/>
                    <field name="age" string="Age"/>
                    <field name="gender" string="Gender"/>
                    <separator/>
                    <filter name="Small" string="Small Student" domain="[('age', '&lt;', 12)]"/>
                    <filter name="Medium" string="Medium Student" domain="[('age', '&gt;=', 12), ('age', '&lt;', 17)]"/>
                    <filter name="Large" string="Large Student" domain="[('age', '&gt;=', 17)]"/>
                    <separator/>
                    <group expand="0" string="Group By">
                        <filter string="Gender" name="Gender" domain="[]" context="{'group_by': 'gender'}"/>
                        <filter string="Age" name="Age" domain="[]" context="{'group_by': 'age'}"/>
                    </group>
                </search>
            </field>
        </record>


        <record model="ir.ui.view" id="my_module_students_formView">
            <field name="name">my_module students form View</field>
            <field name="model">students</field>
            <field name="arch" type="xml">
                <form string="Students" js_class="students_js_form">
                    <header>
                        <button name="action_done" class="oe_highlight" groups="my_module.group_school_manager"
                                string="Done"
                                type="object"
                                invisible="status not in ['draft', 'cancel']"/>
                        <button name="action_cancel" invisible="status not in ['draft', 'done']"
                                groups="my_module.group_school_manager" string="Cancel" type="object"
                                class="oe_highlight"/>
                        <button name="action_draft" invisible="status not in ['cancel', 'done']"
                                groups="my_module.group_school_manager" string="Reset" type="object"
                                class="oe_highlight"/>
                        <field name="status" widget="statusbar"/>
                    </header>
                    <button id="calling_js_button" name="calling_js" class="oe_highlight" string="Calling Javascript"
                            type="object"/>
                    <script type="text/javascript">
                        $(document).ready(function() {
                        $('#calling_js_button').click(function() {
                        console.log('Hello From Calling JS Button Using jQuery');
                        });
                        });
                    </script>
                    <button style="margin-left: 10px;" id="callingMainJSFile" name="calling_mainJS"
                            string="Calling Custom Javascript File" type="object"
                            class="oe_highlight custom-button-spacing"/>
                    <sheet>
                        <group>
                            <group>
                                <field name="name"/>
                                <field name="age"/>
                                <field name="create_uid"/>
                                <field name="grade"/>
                                <field name="grade_teacher" domain="[('grade', '=', grade)]"/>
                            </group>
                            <group>
                                <field name="birthday"/>
                                <field name="gender"/>
                                <div class="custom_div">
                                    <field name="div_field" style="width:500px;"/>
                                    <script type="text/javascript">
                                        $(document).ready(function() {
                                        console.log('Hello from the custom_div using jQuery!');
                                        });
                                    </script>
                                </div>
                            </group>
                        </group>
                        <notebook>
                            <page string="Extra Info">
                                <field name="note" placeholder="Type Your Note About This Student"/>
                            </page>
                        </notebook>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>


        <record model="ir.ui.view" id="my_module_students_treeView">
            <field name="name">my_module students Tree View</field>
            <field name="model">students</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="age"/>
                    <field name="birthday"/>
                    <field name="gender"/>
                </tree>
            </field>
        </record>

        <record model="ir.actions.act_window" id="my_module_students_action_window">
            <field name="name">students_action</field>
            <field name="res_model">students</field>
            <field name="view_mode">tree,form</field>
        </record>

        <menuitem
                id="my_module_topLevel_menuItem"
                name="My Module"
                web_icon="my_module/static/description/icon.png"
        />

        <menuitem
                id="my_module_mainLevel_menuItem"
                name="Students Operation"
                parent="my_module_topLevel_menuItem"
        />

        <menuitem
                id="my_module_subLevel_menuItem"
                name="Students"
                parent="my_module_mainLevel_menuItem"
                action="my_module_students_action_window"
        />

        <!--Teacher Code Here-->
        <record id="view_teacher_filter" model="ir.ui.view">
            <field name="name">teachers.search</field>
            <field name="model">teachers</field>
            <field name="arch" type="xml">
                <search string="Teachers">
                    <field name="name" string="Teacher Name"/>
                    <field name="age" string="Age"/>
                    <field name="gender" string="Gender"/>
                    <separator/>
                    <filter name="Small" string="Small Teacher" domain="[('age', '&lt;', 30)]"/>
                    <filter name="Medium" string="Medium Teacher" domain="[('age', '&gt;=', 30), ('age', '&lt;', 50)]"/>
                    <filter name="Large" string="Large Teacher" domain="[('age', '&gt;=', 50)]"/>
                    <separator/>
                    <group expand="0" string="Group By">
                        <filter string="Gender" name="Gender" domain="[]" context="{'group_by': 'gender'}"/>
                        <filter string="Age" name="Age" domain="[]" context="{'group_by': 'age'}"/>
                    </group>
                </search>
            </field>
        </record>

        <record model="ir.ui.view" id="my_module_teachers_formView">
            <field name="name">my_module teachers form View</field>
            <field name="model">teachers</field>
            <field name="arch" type="xml">
                <form string="Teachers">
                    <header>
                        <button name="action_done" class="oe_highlight" groups="my_module.group_school_manager"
                                string="Done"
                                type="object"
                                invisible="status not in ['draft', 'cancel']"/>
                        <button name="action_cancel" invisible="status not in ['draft', 'done']"
                                groups="my_module.group_school_manager" string="Cancel" type="object"
                                class="oe_highlight"/>
                        <button name="action_draft" invisible="status not in ['cancel', 'done']"
                                groups="my_module.group_school_manager" string="Reset" type="object"
                                class="oe_highlight"/>
                        <field name="status" widget="statusbar"/>
                    </header>
                    <sheet>
                        <group>
                            <group>
                                <field name="name"/>
                                <field name="age"/>
                                <field name="create_uid"/>
                                <field name="grade"/>
                            </group>
                            <group>
                                <field name="birthday"/>
                                <field name="gender"/>
                            </group>
                        </group>
                        <notebook>
                            <page string="Extra Info">
                                <field name="note" placeholder="Type Your Note About This Student"/>
                            </page>
                        </notebook>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <record model="ir.ui.view" id="my_module_teachers_treeView">
            <field name="name">my_module teachers Tree View</field>
            <field name="model">teachers</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="age"/>
                    <field name="birthday"/>
                    <field name="gender"/>
                </tree>
            </field>
        </record>

        <record model="ir.actions.act_window" id="my_module_teachers_action_window">
            <field name="name">teachers_action</field>
            <field name="res_model">teachers</field>
            <field name="view_mode">tree,form</field>
        </record>

        <menuitem
                id="my_module_teacher_mainLevel_menuItem"
                name="Teachers Operation"
                parent="my_module_topLevel_menuItem"
        />

        <menuitem
                id="my_module_teacher_subLevel_menuItem"
                name="Teachers"
                parent="my_module_teacher_mainLevel_menuItem"
                action="my_module_teachers_action_window"
        />

    </data>
</odoo>


```

❖ Next Let's Add the Grade Field in Our Tree View [in Both the Teacher and Student Code] for Convenience so We See Grade of Both the Teachers and Students From Tree:


```python
<tree>
    <field name="name"/>
    <field name="age"/>
    <field name="birthday"/>
    <field name="gender"/>
    <field name="grade"/>
</tree>
```

❖ Create some Teachers with Different Grades so We Can Test This.

❖ Next We Want to Apply a constraint to the `grade_teacher` and `grade` fields so that if the user tried to change the student grade and the teacher assigned grade is not corresponding to the student grade which the user selected; there will be a validation error telling the user: "Change Grade Teacher to Match the New Grade"

❖ in our `models.py` file we will add the following


```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

@api.constrains('grade', 'grade_teacher')
def _check_grade_before_save(self):
    for rec in self:
        if rec.grade != rec.grade_teacher.grade:
            raise ValidationError(_("Change Grade Teacher to Match the New Grade"))
```

**`Very Important Note`**: If the Domain in the Xml `<field name="grade_teacher" domain="[('grade', '=', grade)]"/>` Was Not Added This Whole thing Won't Work. 

❖ **by adding the domain we're effectively telling Odoo to:**

↪ Look at the grade field in the teachers model.

↪ Compare it to the current value of the grade field in the students model.

↪ Only show teachers records where the grade matches the current grade of the student.

❖ **if the domain was not set in the xml here's what will happen:**

↪ Form loads, and `grade_teacher` shows all teachers (no initial filter was linking it to the student grade).

↪ User selects a grade, and onchange method triggers and sets the domain, but the initial load might still show all teachers because the form didn't have a predefined filter.

❖ **if the domain was set this will work cuz the following senario happens:**

↪ Form loads, and `grade_teacher` is filtered based on the grade value due to the XML domain.

↪ User selects a grade, and onchange method triggers and updates the domain, ensuring the grade_teacher field continues to show the correct teachers based on the selected grade.

:: __`Relation Between Models in Odoo`__ ::

❖ We Demonstrated `many2one` Relation when We Created the Teacher Grade and Grade Example, but There's Also `one2many` and `many2many` Relationship. 

1. **Many2one (Many to One):** This relationship is used when many records in one model are related to a single record in another model. For example, imagine you have two models: "Student" and "Classroom". Many students can belong to one classroom, so the "Student" model would have a Many2one field for the "Classroom" model. This means that each student is associated with one specific classroom.

2. **One2many (One to Many):** This is the inverse of Many2one. It's used when a single record in one model is related to many records in another model. In our previous example, the "Classroom" model would have a One2many field for the "Student" model. This means that each classroom can have multiple students.

3. **Many2many (Many to Many):** This relationship is used when multiple records in one model can be related to multiple records in another model. For example, consider two models: "Student" and "Subject". A student can study multiple subjects, and a subject can be studied by multiple students. So, both the "Student" and "Subject" models would have a Many2many field for each other.

❖ Many2one and One2many are like two sides of the same coin, but they are used from different perspectives.

❖ In the context of our previous example, Many2one and One2many represent the same relationship between "Student" and "Classroom", but they are used differently based on which model you're looking at

❖ To Demonstrate Those We Will Create Two Objects: Level and Material But Will Create a Brand New Python File Instead of Putting It in the `models.py` File And We Will Create a New `level.xml` File as Well Under the Views Directory

❖ Crate a New `level.py` File in the Models Directory and in the `__init__.py` in the Models Folder We Will Add the Following Line: 


```python
from . import level
```

❖ Next, in Our level.py File We Will Add the Following Modules:


```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

from datetime import *
from datetime import date
```

❖ Next We Will Add Our Classes And Set the Proper Views and Access Rights:


```python
class level(models.Model):
    _name = 'level'
    _description = 'This Class Represents the Students Level'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(string='Level')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    students_ids = fields.Many2many('students', string='Students')
    material_lines = fields.One2many('material', 'level_id', string='Materials')

class material(models.Model):
    _name = 'material'
    _description = 'This Class Represents the Materials'
    name = fields.Char(string='Material Name')
    grade_teacher = fields.Many2one('teachers')
    level_id = fields.Many2one('level')
```

→ and in our `level.xml` file add the following: 


```python
<odoo>
    <data>

        <record model="ir.ui.view" id="my_module_level_formView">
            <field name="name">my_module level form View</field>
            <field name="model">level</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <group>
                            <group>
                                <field name="name"/>
                            </group>
                            <group>
                                <field name="start_date"/>
                                <field name="end_date"/>
                            </group>
                            <notebook>
                                <page string="Materials">
                                    <group>
                                        <field name="material_lines" string="Materials">
                                            <tree string="Materials" editable="bottom">
                                                <field name="name"/>
                                                <field name="grade_teacher"/>
                                            </tree>
                                        </field>

                                    </group>
                                </page>
                                <page string="Students">
                                    <group>
                                        <field name="students_ids"/>
                                        <tree>
                                            <field name="name"/>
                                        </tree>
                                    </group>
                                </page>
                            </notebook>
                        </group>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <record model="ir.ui.view" id="my_module_level_treeView">
            <field name="name">my_module level Tree View</field>
            <field name="model">level</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="start_date"/>
                    <field name="end_date"/>
                </tree>
            </field>
        </record>

        <record model="ir.actions.act_window" id="my_module_level_action">
          <field name="name">level_action</field>
          <field name="res_model">level</field>
          <field name="view_mode">tree,form</field>
      </record>

        <menuitem
                id="my_module_levelView_mainLevel_menuItem"
                name="Level Operation"
                parent="my_module_topLevel_menuItem"
        />

        <menuitem
                id="my_module_levelView_subLevel_menuItem"
                name="Level"
                parent="my_module_levelView_mainLevel_menuItem"
                action="my_module_level_action"
        />
    </data>
</odoo>
```

and in our `ir.model.access.csv` file we will add: 
level_manager_group_access,level,model_level,my_module.group_school_manager,1,1,1,1
level_users_group_access,level,model_level,my_module.group_school_user,1,1,1,0

material_manager_group_access,material,model_material,my_module.group_school_manager,1,1,1,1
material_users_group_access,material,model_material,my_module.group_school_user,1,1,1,0
❖ Next We Need to Reference the `level.xml` File in Our Manifest File


```python
'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/level.xml',
    'views/templates.xml',
],

```

**`Explanation`:**

❖ **First Let's Understand the Relationship Between the Models in Odoo:** 

★ First of All the Relationships in Odoo **[Many2many, One2many, Many2one]** Have Two Sides Separated by the Number 2, the First Side Before the Number Points to the Current Class [the active class where we're typing the relationship code]  and the Other Side After the Number Points to Another Class We Will Specify After the Relationship Type/Keyword

**Types of Relationship**

↪ **`Many2many`**: This is a bi-directional relationship [رايح جاي] where one record in a model can be related to many records in another model and vice versa. For example, a student can be enrolled in multiple levels, and a level can have multiple students.

↪ **`One2many`**: This is a uni-directional [طريق واحد] relationship where one record in a model can be related to many records in another model, but not vice versa. For example, a level can have multiple materials, but a material can only be associated with one level.

↪ **Many2one**: This is a uni-directional relationship [طريق واحد] where many records in a model can be related to one record in another model, but not vice versa. For example, multiple materials can be associated with one teacher, but a teacher can only be associated with one material at a time

**`In the Level Class:`** 

❖ The **`student_ids`** Is an Object that Sets the Relation Between the Level and the Students `=>` Many Students Can Be in Different Levels and Multiple Levels Can Be Assigned to Multiple Students. **[Many to Many Relationship]**

❖ The **`material_lines`** Is an Object that Sets the Relation Between the Level and the Material `=>` The Level Has Multiple Materials While the Material Can Be Assigned to One Level  **[One to Many Relationship]**

**`But What the Fuck Does that Even Mean?`** 

❖ If You Created Two Levels and Tried to Add the Same Material in Both Levels It Will Be Added without a Problem, Then What Do You Mean by Saying `The Level Has Multiple Materials While the Material Can Be Assigned to One Level?`

❖ Well to Answer This We Need to Understand First that One2many or Many2one Relation Doesn't Enforce Uniquness to the Fields, What Enforces Uniqueness Is `Api Constraint` and `Sql Constraint`; Ok but Now the Big Question Remains: If the Relation Doesn't Enforce Uniquness, **Then What's the Point?** **What Makes It Different than Many2many?** Ok, Let's Explain This: 

↪ **To Truely Understand This** Create a Material to Level 1 and Then Create a Different Material in Level 2 Then Get Back to Level 1 and Create Another Material. 

↪ Next, Change the Relation in `level.py` File From One2many to Many2many and Restart the Server and Go to Level One and Try to Create a New Material, You Will Notice a Popup Suggesting the Material We Created From Level 2 

↪ Reset the Relation in the Python File Back to One2many and Restart the Server and Get Back to Level 1 and Create a Material, You Will Notice that the Popup Is Gone and It Doesn't Suggest Adding the Material From Level 2 to Level 1 

↪ This Means that Many2many Binds [Link] the Materials Across Level 1 and 2 and That's Why We Saw the Popup and Suggestion, While One2many Is only Bound to This Level Even if the Material Name Is the Same Across the Levels [Cuz the Relationship Doesn't Enforce Uniquness to the Field]

↪ So, The Relationship Between Records and the Uniqueness of Those Records Are Two Separate Concepts in Odoo. The Relationship Defines How Records Are Related to Each Other, While Uniqueness Defines Whether Certain Records Are Allowed to Have the Same Properties or Not.

-------------------------------------------------------------

❖ **`Question`**: **Why We Referenced `level_id` in The `material_lines` And Didn't Reference Anything when We Set the Relationship Between Level and Students?**

↪ **`students_ids`**: In the level class, the students_ids field is a Many2many field, which means that a level can have multiple students and a student can be associated with multiple levels. In this case, Odoo automatically creates a join table to manage the many-to-many relationship between level and students. The join table will have two columns: one for the level_id and one for the student_id.

↪ **`material_lines`**: When We Define a One2many Relationship They're Like Two Sides of the Same Coin and the Difference Is the Prespective Where You View the Coin From? So in the Level Class [Prespective] We Tell Odoo: Look at the Material Class [the Other Side of the Coin] but It Can't Look to the Other Side without Knowing Where to Look [Where to Put the Linking Data]. So We Tell Odoo Set the Linking Data in the Level_id Field.

Now After We Flipped the Coin and We're at the Material  Class [Prespective] It's the Opposite Now so Instead of One2many It's Many2one Now and It's Many2one with the Level Object. 

↪ So, You Can Think of the Level_id Field in the Material Model as the "Link" Between the Level and Material Models. It Allows Odoo to Know Which Materials Are Associated with Which Levels, and Vice Versa.

**Ok, but This Raises a New Question, Why when We Set the Grade_teacher Relation to Many2one in the Teachers and Students Class We Didn't Specify the Field Which the Data Will Be Stored At?**

↪ when defining a Many2one field, you don't need to specify the field that will store the linking data because Odoo automatically creates it for you in the related model. 

↪ when defining a One2many field, you do need to specify the field that will store the linking data in the related model

--------

❖ The `editable="bottom"` attribute in the `<tree>` view of Odoo indicates that the user can only add new records at the bottom of the list, and not in between existing records. This means that the user can only append new records to the end of the list, and cannot insert new records between existing ones.

:: __`Kanban View In Odoo`__ ::

❖ We Will Add Kanban View to the Students Class so We Will Add the Following Structure in Our `views.xml` File 


```python
<record id="students_kanban_view" model="ir.ui.view">
    <field name="name">students_kanban_view</field>
    <field name="model">students</field>
    <field name="arch" type="xml">
        <kanban>
            <templates>
                <t t-name="kanban-box">
                    <div>
                        <strong>
                            <field name="name"/>
                        </strong>
                    </div>
                    <div>
                        <strong>
                            <field name="birthday"/>
                        </strong>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

❖ Next We Will Edit the Action Record to Include Our Kanban View:


```python
<record model="ir.actions.act_window" id="my_module_students_action_window">
    <field name="name">students_action</field>
    <field name="res_model">students</field>
    <field name="view_mode">tree,form,kanban</field>
</record>
```

❖ **Note**: In This Line `<field name="view_mode">tree,form,kanban</field>` Don't Leave Spaces Otherwise You Will Get an Error.

❖ Restart the Server and You Should See the Kanban View Now.

:: __`Explanation`__ ::

❖ The `<t>` tag is a core part of Odoo's QWeb templating engine. It's used to define templates, which are reusable pieces of XML markup that can be rendered dynamically with data.

❖ The `t-name` attribute is used to give a unique name to a QWeb template. This name is used to identify the template when it's being called from other parts of the code. For example, in a kanban view, the `t-name` attribute is used to specify the name of the template that should be used to render each record in the kanban view.

❖ In summary, the `<t>` tag is used to define templates, and the `t-name` attribute is used to give a unique name to a template so that it can be called from other parts of the code.

:: __`Adding Binary Image`__ ::

❖ In the Students Class We Will Add the Following: 


```python
img = fields.Binary()
```

❖ And in Our `views.xml` File In the Form View We Will Add the Following Field: 


```python
<field name="img" widget="image" class="oe_avatar"/>
```


```python
<group>
    <field name="grade"/>
    <field name="birthday"/>
    <field name="gender"/>
    <field name="img" widget="image" class="oe_avatar"/>
</group>
```

❖ Now We've Succcessfully Added a Binary Image in Our Module. 

❖ Next Add the Img Field Also to the Kanban View. 


```python
<record id="students_kanban_view" model="ir.ui.view">
    <field name="name">students_kanban_view</field>
    <field name="model">students</field>
    <field name="arch" type="xml">
        <kanban>
            <templates>
                <t t-name="kanban-box">
                    <div>
                        <strong>
                            <field name="name"/>
                        </strong>
                    </div>
                    <div>
                        <strong>
                            <field name="birthday"/>
                        </strong>
                    </div>
                    <div>
                        <field name="img" widget="image" class="oe_avatar"/>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

:: __`Graph View`__ ::

❖ Add the Following Record in the `views.xml` File: 


```python
<record id="students_graph_view" model="ir.ui.view">
    <field name="name">students_graph_view</field>
    <field name="model">students</field>
    <field name="arch" type="xml">
        <graph string="Students Analysis" sample="2">
            <field name="name"/>
            <field name="birthday" interval="year"/>
            <field name="age" type="measure"/>
        </graph>
    </field>
</record>
```

❖ Next We Will Update the Action Windows to Include Our Graph View:


```python
<record model="ir.actions.act_window" id="my_module_students_action_window">
    <field name="name">students_action</field>
    <field name="res_model">students</field>
    <field name="view_mode">tree,form,kanban,graph</field>
</record>
```

:: __`Calendar View`__ ::

❖ Add the Following Record in `views.xml` File: 


```python
<record id="students_calendar_view" model="ir.ui.view">
    <field name="name">students_calendar_view</field>
    <field name="model">students</field>
    <field name="arch" type="xml">
        <calendar
                string="students"
                date_start="birthday"
                date_stop="birthday"
                mode="month"
                scales="month,year"
                event_open_popup="true">
            <field name="name"/>
        </calendar>
    </field>
</record>
```

❖ Next We Will Update the Action Windows to Include Our calendar View:


```python
<record model="ir.actions.act_window" id="my_module_students_action_window">
    <field name="name">students_action</field>
    <field name="res_model">students</field>
    <field name="view_mode">tree,form,kanban,graph,calendar</field>
</record>
```

:: __`Adding Ribbon in Odoo`__ ::

❖ We Want to Add a Ribbon to the Archived Student and We Want to Control the Visibility of that Ribbon Based on Condition of Active Status of the Student 

❖ Active Student = Not Archived Student & Not Active Student = Archived Student

❖ The Active Status Came From This Field in Our models.py File: `active = fields.Boolean(default = True)` Which Is True by Default. 

❖ We Will Add the Following Code in Our `views.xml` File in the `form view` record under the sheet opening tag: 


```python
<field name="active" invisible="1"/>
<widget name="web_ribbon" title="Archived" bg_color="bg-danger" invisible="active != False"/>
```

❖ Now We're Telling Odoo if the Student Active Stauts Is Not False [True] Don't Show the Ribbon Cuz the Student Will Be Unarchived; Otherwise Show the Ribbon Cuz the Student Will Be Archived

❖ The reason we created the active field (the first line before the widget) in the in xml is because we used it in the widget code (the second line) but we didn't create a proper field for it or defined first. in other words if we removed that field when the compiler reaches the `invisible` attribute of the widget and see that it depends on the active status of the student it won't be able to compile cuz the active is not defined in the xml (and only defined in the python file). we can also put it like this: we're calling the active field for the python file first and then use it in the widget.

❖ The reason we put the attribute `invisible="1"` (which makes the field invisible or hidden) in the active field is because if we set it to `invisible="0"` (which makes the field visible) and relaunched the server you will notice a little checkbox in the sheet (checked or unchecked based on the status of the student being archived or not archived). 

❖ We Will Use This Field and Widget Under the Sheet Tag, Here's the Full Sheet Tag Code From the views.xml File: 


```python
<sheet>
    <field name="active" invisible="1"/>
    <widget name="web_ribbon" title="Archived" bg_color="bg-danger" invisible="active != False"/>


    <group>
        <group>
            <field name="name"/>
            <field name="age"/>
            <field name="create_uid"/>
            <field name="grade"/>
            <field name="grade_teacher" domain="[('grade', '=', grade)]"/>
            <field name="img" widget="image" class="oe_avatar"/>
        </group>
        <group>
            <field name="birthday"/>
            <field name="gender"/>
            <div class="custom_div">
                <field name="div_field" style="width:500px;"/>
                <script type="text/javascript">
                    $(document).ready(function() {
                    console.log('Hello from the custom_div using jQuery!');
                    });
                </script>
            </div>
        </group>
    </group>
    <notebook>
        <page string="Extra Info">
            <field name="note" placeholder="Type Your Note About This Student"/>
        </page>
    </notebook>
</sheet>
```

❖ if we set the invisible attribute to 0 like this: `<widget name="web_ribbon" title="Archived" bg_color="bg-danger" invisible="0"/>` The Button Will Always Be Visible, and if You Set It to 1 the Button Will Be Always Invisible.

❖ In Odoo 16 the Command To Control the Visibility Would Use the `attrs` Attribute As Follows: 


```python
<widget name="web_ribbon" title="Archived" bg_color="bg-danger" attrs="{'invisible': [('active', '=', True)]}"/>
```

❖ But `attrs` Attribute Is Depricated in Odoo 17.

:: __`Creating Sequence in Odoo`__ ::

❖ In Odoo, a Sequence is a series of numbers automatically displayed when an invoice or sales order (or a new student in our case) is created. e.g studnet-1, or sales0001, ...etc

❖ Create a New Directory in Your Module and Name It `data` Also Inside that Directory Create `data.xml` File

❖ In the Xml We Created Add the Following Code: 


```python
<odoo>
    <data>
        <record model="ir.sequence" id="students_sequence">
        <field name="name">Students Sequence</field>
        <field name="code">sequence.student</field>
        <field name="prefix">Student-000</field>
        <field name="number_next" eval="1"/>
        <field name="number_increment" eval="1"/>
        </record>
    </data>
</odoo>
```

❖ `number_next` → the number we will start counting from

❖ `number_increment` → is the number of incrementation will happend to the `number_next` each time a new record (student, invoice, ..etc) is created. 

❖ Next in Our Students Class We Will Add the Following Code: 


```python
code = fields.Char(string="Number", required=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('sequence.student'))
```

❖ Next We Will Add the Field Code in Our views.xml File in the Form View Record


```python
<field name="code"/>
```


```python
<group>
    <field name="code"/>
    <field name="name"/>
    <field name="age"/>
    <field name="create_uid"/>
    <field name="grade"/>
    <field name="grade_teacher" domain="[('grade', '=', grade)]"/>
    <field name="img" widget="image" class="oe_avatar"/>
</group>
```

❖ Next We Will Add the Xml to the Manifest File: 


```python
'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/level.xml',
        'data/data.xml',
        'views/templates.xml',
        ]
```

❖ Now We've Successfuly Implemented the Sequence in Our Module.

❖ If You Already Have some Students Before Applying This Sequence Logic, You'll Notice that All of Them Are Taking Student-1 Sequence as They Shouldn't, to Fix This there's two solution: 

### **`My Soultion Way`**

❖ Make all old students code value = old so when we create a new student it will start from number 1

❖ We Need to Make a Button in Our Formview that Trigger a Function that Sets the Sequence to All Existing Students to the New Value; Actually I Made Two Buttons One to Control the Current Student Sequence and the Other Button Controls All Current Student Sequence.




```python
<button name="update_existing_students" string="Update Current Student Sequence" type="object" class="oe_highlight"/>
<button name="update_all_students" string="Update All Students Sequence" type="object" class="oe_highlight"/>
```

❖ Those Buttons I Included Them In the Header for Easy Access Under the widget field

❖ Now Let's Define the Functions in Our Python File.


```python
def update_existing_students(self):
    # Fetch the current student (assuming you're calling this method within a student record)
    current_student = self

    if current_student.code != _('Old'):
        # Set the value to "Old" and remove the old sequence
        current_student.write({'code': _('Old')})


def update_all_students(self):
    all_students = self.search([])
    for student in all_students:
        if student.code != _('Old'):
            student.write({'code': _('Old')})

```

❖ now restart the server and click any student to enter the form view and click on the button to update all students you will see that all students code value is now = old and when you create a new record it will start from 1 

### **`The Odoo 16 Course Way`**

First We Will Edit the Default Value to Take New Instead of the Sequence.


```python
code = fields.Char(string="Number", required=True, copy=False, default=lambda self: _('New'))
```

❖ Now if We Restarted the Server and Created a New Student You Will See that They're Taking the New Value but the Old Students Sequence Is The Same, to Fix This We Need to Overwrite The Built-in Create Function; So in Our Python File We Will Do the Following: 


```python
code = fields.Char(string="Number", required=True, copy=False, default=lambda self: _('New'))


@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('sequence.student') or _('New')
    return super().create(vals_list)

```

❖ now when you create a new student it will take the new sequence, but the old students still have the sequence; also if you created student-5 and student-6 for example and deleted them, when you create a new student it will continue from the deleted sequence and create a student-7 where it should start from student-1

❖ To Fix This First We Need to Make a Button in Our Formview that Trigger a Function that Sets the Sequence to All Existing Students to the New Value; Actually I Made Two Buttons One to Control the Current Student Sequence and the Other Button Controls All Current Student Sequence.


```python
<button name="update_existing_students" string="Update Current Student Sequence" type="object" class="oe_highlight"/>
<button name="update_all_students" string="Update All Students Sequence" type="object" class="oe_highlight"/>
```

❖ Those Buttons I Included Them In the Header for Easy Access


```python
<header>
    <button name="action_done" class="oe_highlight" groups="my_module.group_school_manager"
            string="Done"
            type="object"
            invisible="status not in ['draft', 'cancel']"/>
    <button name="action_cancel" invisible="status not in ['draft', 'done']"
            groups="my_module.group_school_manager" string="Cancel" type="object"
            class="oe_highlight"/>
    <button name="action_draft" invisible="status not in ['cancel', 'done']"
            groups="my_module.group_school_manager" string="Reset" type="object"
            class="oe_highlight"/>
    <field name="status" widget="statusbar"/>
    <button name="update_existing_students" string="Update Current Student Sequence" type="object"
            class="oe_highlight"/>
    <button name="update_all_students" string="Update All Students Sequence" type="object" class="oe_highlight"/>
</header>
```

❖ Now Let's Define the Functions in Our Python File.


```python
def update_existing_students(self):
    # Fetch the current student (assuming you're calling this method within a student record)
    current_student = self

    if current_student.code != _('New'):
        # Set the value to "New" and remove the old sequence
        current_student.write({'code': _('New')})


def update_all_students(self):
    all_students = self.search([])
    for student in all_students:
        if student.code != _('New'):
            student.write({'code': _('New')})

```

❖ Now These Two Buttons Controls the Sequence of the Current Students, Next We Want to Modify the Overwrite We Made to the Create Function to Do the Following: 

`↪` We check if any student has a non-“New” sequence.

`↪` If yes, we determine the highest existing sequence number and continue from there.

`↪` If no existing students have a sequence, we start from 1.



```python
@api.model_create_multi
def create(self, vals_list):
    # Check if any student has a non-"New" sequence
    existing_students = self.search([('code', '!=', _('New'))])

    if existing_students:
        # Get the highest existing sequence number
        existing_numbers = [int(student.code.split('-')[1]) for student in existing_students]
        next_number = max(existing_numbers) + 1
        prefix = existing_students[0].code.split('-')[0]
    else:
        # No existing students with a sequence, start from 1
        next_number = 1
        prefix = 'Student'

    for vals in vals_list:
        if vals.get('code', _('New')) == _('New'):
            # Set the new sequence value
            vals['code'] = f"{prefix}-{next_number}"
            next_number += 1

    return super().create(vals_list)

```

:: `Very Important Note` :: This solution or workflow doesn't require `data.xml` file or the data inside of it. 

→ The workflow is to create two buttons in the header tag to reset the numbering for all existing students to be `New`

→ handle the numbering with the override create function.

:: __`Adding Setting Section to our Module`__ ::

❖ We Want to Make a Default Value in the Birthday Field and This Default Value We Will Controlled in the Settings Menu

❖ If You Looked at the Sales Module, You Will See a Main-Level Menu Item Called `Configuration` and the First Sub-Level Menu Item Under the Configuration Is `Settings`, if You Clicked on It It Will Move You to the Sales Settings Section so You Can Edit the Settings You Want. 

❖ First Let's Create a New Python File in the Models Directroy, Let's Name It `my_module_settings.py` and Add the Following Code to It.


```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

from datetime import *
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    birthday = fields.Datetime(string='Birthday Date', help="Birthday Date", config_parameter='my_module.birthday')
```

❖ Next in The `__init__.py` File Under the Models Directory We Will Reference Our New Python File by Adding the Following Line: 


```python
from . import my_module_settings
```

❖ Next We Want to Create the Main-Level and Sub-Level Menu Items in Our Module, First Let's Create a New Xml File Under the Views Directroy and Call It `my_module_settings.xml` And Add the Following Code to It.

**`→ For Odoo 17`**: 


```python
<odoo>
    <data>
        <record model="ir.ui.view" id="my_module_settings_form_view">
            <field name="name">my_module.settings.form</field>
            <field name="model">res.config.settings</field>
            <field name="inherit_id" ref="base.res_config_settings_view_form"/>
            <field name="arch" type="xml">
                <xpath expr="//form[contains(@class, 'oe_form_configuration')]" position="inside">
                    <app data-string="My Module Settings" string="My Module" name="my_module"
                         logo="/my_module/static/description/icon.png">
                        <div class="row mt16 o_settings_container">
                            <div class="col-xs-12 col-md-6 o_setting_box">
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
                    </app>
                </xpath>
            </field>
        </record>

        <record model="ir.actions.act_window" id="action_my_module_settings_config">
            <field name="name">my_module_settings</field>
            <field name="type">ir.actions.act_window</field>
            <field name="res_model">res.config.settings</field>
            <field name="view_mode">form</field>
            <field name="target">inline</field>
            <field name="context">{'module' : 'my_module'}</field>
        </record>

        <menuitem
                id="my_module_settings_main_menu_item"
                name="Configuration"
                parent="my_module_topLevel_menuItem"
        />
        <menuitem
                id="my_module_settings_subLevel_menu_item"
                name="Settings"
                parent="my_module_settings_main_menu_item"
                action="action_my_module_settings_config"
        />
    </data>
</odoo>
```

**`→ for odoo 16`**: 


```python
<odoo>
    <data>
        <record model="ir.ui.view" id="my_module_settings_form_view">
            <field name="name">my_module.settings.form</field>
            <field name="model">res.config.settings</field>
            <field name="inherit_id" ref="base.res_config_settings_view_form"/>
            <field name="arch" type="xml">
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
            </field>
        </record>

        <record model="ir.actions.act_window" id="action_my_module_settings_config">
            <field name="name">my_module_settings</field>
            <field name="type">ir.actions.act_window</field>
            <field name="res_model">res.config.settings</field>
            <field name="view_mode">form</field>
            <field name="target">inline</field>
            <field name="context">{'module' : 'my_module'}</field>
        </record>

        <menuitem
                id="my_module_settings_main_menu_item"
                name="Configuration"
                parent="my_module_topLevel_menuItem"
        />
        <menuitem
                id="my_module_settings_subLevel_menu_item"
                name="Settings"
                parent="my_module_settings_main_menu_item"
                action="action_my_module_settings_config"
        />
    </data>
</odoo>
```

**`Key Difference in Code between odoo 16 and 17`**: 

`→` The difference in behavior between Odoo 16 and 17 is related to how the settings views are structured and how the <app> element is handled.

**Key changes made for Odoo 16 compatibility:**

`→` Changed the xpath expression from //form[hasclass('oe_form_configuration')] to //div[hasclass('settings')]

`→` Replaced the `<app>` tag with `<div class="app_settings_block">`

`→` Added data-key="my_module" attribute for proper module identification

`→` Updated CSS classes for better responsiveness:

`→` Changed col-xs-12 col-md-6 to col-12 col-lg-6

`→` Added proper heading with `<h2>` tag



❖ add this new file to the `__mainfest__.py` file under the data xml file.


```python
# always loaded
'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/level.xml',
    'data/data.xml',
    'views/my_module_settings.xml',
    'views/templates.xml',
],

```

**`Continue for Odoo 17`**

❖ This Will Work Fine but You'll See the Following Warning in the Logs: `odoo.addons.base.models.ir_ui_view: Error-prone use of @class in view my_module.settings.form (my_module.my_module_settings_form_view): use the hasclass(*classes) function to filter elements by their classes` To Fix This We Will Change the Xpath Expression to the Following:


```python
<xpath expr="//form[hasclass('oe_form_configuration')]" position="inside">
```

❖ So Now Our View Should Be Like This: 


```python
<odoo>
    <data>
        <record model="ir.ui.view" id="my_module_settings_form_view">
            <field name="name">my_module.settings.form</field>
            <field name="model">res.config.settings</field>
            <field name="inherit_id" ref="base.res_config_settings_view_form"/>
            <field name="arch" type="xml">
                <xpath expr="//form[hasclass('oe_form_configuration')]" position="inside">
                    <app data-string="My Module Settings" string="My Module" name="my_module"
                         logo="/my_module/static/description/icon.png">
                        <div class="row mt16 o_settings_container">
                            <div class="col-xs-12 col-md-6 o_setting_box">
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
                    </app>
                </xpath>
            </field>
        </record>

        <record model="ir.actions.act_window" id="action_my_module_settings_config">
            <field name="name">my_module_settings</field>
            <field name="type">ir.actions.act_window</field>
            <field name="res_model">res.config.settings</field>
            <field name="view_mode">form</field>
            <field name="target">inline</field>
            <field name="context">{'module' : 'my_module'}</field>
        </record>

        <menuitem
                id="my_module_settings_main_menu_item"
                name="Configuration"
                parent="my_module_topLevel_menuItem"
        />
        <menuitem
                id="my_module_settings_subLevel_menu_item"
                name="Settings"
                parent="my_module_settings_main_menu_item"
                action="action_my_module_settings_config"
        />
    </data>
</odoo>
```

❖ By Using `hasclass()` Function You Can Avoid Such Errors.

❖ In Odoo, XPath (XML Path Language) is a query language used to navigate and select elements in XML documents, such as those found in Odoo's database models, forms, and views.

**Why use XPath in Odoo?**

XPath is used in various scenarios:

    → Form validation : To validate fields on a form using specific conditions.
    → View creation : To define the structure of a view, including fields, groups, and other elements.
    → Record manipulation : To update or delete records based on specific conditions.

**Basic XPath concepts:**

    → Element selection : // - selects all elements on the page; / - selects an element by its path; . - selects the current element.
    → Attribute selection : [attribute_name] - selects an attribute of an element.
    → Child and parent selection : child/parent - selects a child or parent element.

**Example XPath expression:**



```python
//form[@name='my_form']/field[@name='my_field']
```

→ This XPath expression selects all fields with the name "my_field" within a form named "my_form".

**Explaining our XPath Example**

First we inherit from the `res.config.settings` which is the model responsible for the settings

**XPath expression:**

`//form[hasclass('oe_form_configuration')]`

    →   `//form`: selects all `<form>` elements on the page.
    
    →   `[hasclass('oe_form_configuration')]:` applies a filter to select only those forms that have a CSS class named "oe_form_configuration".
    
    → `position="inside"` means that the XPath expression will be evaluated inside the current element (i.e., the <app> element).

In other words, this XPath expression will match only one form: the main settings form of Odoo.

**App element:**

 `<app ...>`

This is an Odoo app template element. The `data-string`, `string`, and `name` attributes are used to customize the app's appearance:

    →   `data-string="My Module Settings"`: sets a data attribute for the app.

    →   `string="My Module"`: sets the app's title (label).

    →   `name="my_module"`: sets the app's name.


**Logo:**

`<img src="/my_module/static/description/icon.png">`

This line includes an image from a static folder, used as the app's logo.

**Form layout:**

The rest of the code defines the form layout:

    →   `<div class="row mt16 o_settings_container">`: creates a row with a specific style and class.

    →   `<div class="col-xs-12 col-md-6 o_setting_box">`: creates a column that spans 12 columns on small screens and 6 columns on medium/large screens, with a specific class.

    →   `<div class="o_setting_right_pane">`: creates a container for the form fields, using a specific class.


**Form fields:**

The code includes two form fields:

    →   `label for="birthday"`: creates a label element without any visible content ( likely used as a placeholder).
    
    →   `<field name="birthday"/>`: creates a field with the name "birthday". This field will be displayed in the form, and its value can be edited by users.

In summary, this XPath code defines an XML template for Odoo's main settings form. It includes a logo, a title, and two form fields: one for setting the default birthday.


❖ Now We've Successfuly Added the Our App to the Settings, but the Date in the Settings Is Not yet Linked to the Birthday Field in Our Module.

❖ First Set the Date You Want Use as the Default Value in the Settings, Then Go to the models.py File and Add the Following Function Before the Birthday Field.


```python
def _default_birthday_date(self):
    birthday = self.env['ir.config_parameter'].sudo().get_param('my_module.birthday')
    return birthday
birthday = fields.Date(default=_default_birthday_date)
```

❖ Notice that We Defined the Function Before Accessing It in the Birthday Field Cuz Python Is Interpreted Language And We Can't Use a Function Before Defining It.

:: __`Translate the Entire Module to Another Language`__ ::

❖ First Create a New Directory Under Your Module Name and Call It `i18n`

❖ Activate the Developer/Debug Mode and Go to Settings and From the Translation Main Menu-Item Choose `Translation >> Language >> Arabic` Now You Changed the Language to Arabic, but We Want to Add the Arabic Language to Our Module and to Do This We Will Choose `Translation >> Export Translation` 

❖ Next We Will Set the Settings as Follows: 

↪ **`Language`**: New Language (Empty translation template)

↪ **`File Format`**: PO File

↪ **`Export Type`**: Module

↪ **`Apps To Export`**: my_module

❖ Download the Pot File Odoo Will Give You and Put It in Our `i18n` Directory

❖ Next We Will Export Another Translation but This Time We Will Set the Language to Arabic, Downlaod the Po File and Put It in Our Directory as Well

❖ You Will Notice the Following Structure in the Arabic File:
msgid "Access warning"
msgstr ""
❖ The Second Line Inside the Quotes You Will Put the Arabic Words that Corresponds to the First Line.

❖ You'll Need to Do This for the Rest of the File. 

:: `How to delete a module the right way` ::

→ first uninstall the module from the app list UI. 

→ if you still see the module name and icon click on the three dots next to the module name and choose module info. 

→ you'll see a small cog next to the module name under the top header click on it and choose delete. 

:: **`Smart Buttons in Odoo`** ::

❖ If you go to the sales module >> orders menu >> customers >> and select any customer you will notice three smart buttons (sales, invoiced, certificates). the sales smart button for examples shows the number of sales orders this customer has made and if you clicked on this smart buttons it will transform you to the quotation and sales of that customer

❖ We will do the same thing in our module, we will create a smart button in the levels; this button will take us to a tree view of the materials where we can upload some documents for the materials. to start first add some data in the levels >> create a level >> add some materials and choose some teachers. 

❖ There's two types of smart buttons: **`object smart buttons`** and **`aciton smart buttons`**

**`Object Smart Button`**

❖ Go to the `levels.xml` file and paste the following code right after the opening sheet tag in the levels form view


```python
<div class="oe_button_box" name="button_box">
    <button
            name="action_view_material"
            type="object"
            class="oe_stat_button"
            icon="fa-globe icon"
    >
        <div class="o_field_widget o_stat_info">
            <span class="o_stat_text">Materials</span>
        </div>
    </button>
</div>
```

So now our `levels.xml` file should look like this: 


```python
<odoo>
    <data>

        <record model="ir.ui.view" id="my_module_level_formView">
            <field name="name">my_module level form View</field>
            <field name="model">level</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <div class="oe_button_box" name="button_box">
                            <button
                                    name="action_view_material"
                                    type="object"
                                    class="oe_stat_button"
                                    icon="fa-globe icon"
                            >
                                <div class="o_field_widget o_stat_info">
                                    <span class="o_stat_text">Materials</span>
                                </div>
                            </button>
                        </div>
                        <group>
                            <group>
                                <field name="name"/>
                            </group>
                            <group>
                                <field name="start_date"/>
                                <field name="end_date"/>
                            </group>
                            <notebook>
                                <page string="Materials">
                                    <group>
                                        <field name="material_lines" string="Materials">
                                            <tree string="Materials" editable="bottom">
                                                <field name="name"/>
                                                <field name="grade_teacher"/>
                                            </tree>
                                        </field>

                                    </group>
                                </page>
                                <page string="Students">
                                    <group>
                                        <field name="students_ids"/>
                                        <tree>
                                            <field name="name"/>
                                        </tree>
                                    </group>
                                </page>
                            </notebook>
                        </group>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <record model="ir.ui.view" id="my_module_level_treeView">
            <field name="name">my_module level Tree View</field>
            <field name="model">level</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="start_date"/>
                    <field name="end_date"/>
                </tree>
            </field>
        </record>

        <record model="ir.actions.act_window" id="my_module_level_action">
            <field name="name">level_action</field>
            <field name="res_model">level</field>
            <field name="view_mode">tree,form</field>
        </record>

        <menuitem
                id="my_module_levelView_mainLevel_menuItem"
                name="Level Operation"
                parent="my_module_topLevel_menuItem"
        />

        <menuitem
                id="my_module_levelView_subLevel_menuItem"
                name="Level"
                parent="my_module_levelView_mainLevel_menuItem"
                action="my_module_level_action"
        />
    </data>
</odoo>
```

❖ Now we will create a function for the `action_view_material` this function will take us to the a tree view of the materials of the levels

❖ add the following function to `level.py` file in the level class


```python
def action_view_material(self):
    material_lines = self.mapped('material_lines')
    domain = [('id', 'in', material_lines.ids)]
    context = {'default_level_id': self.id, }
    return {
        'name': _('Materials Lines'),
        'res_model': 'material',
        'view_mode': 'tree,form',
        'domain': domain,
        'context': context,
        'type': 'ir.actions.act_window',
    }

```

❖ Now our `level.py` file should look like this: 


```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

from datetime import *
from datetime import date


class level(models.Model):
    _name = 'level'
    _description = 'This Class Represents the Students Level'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(string='Level')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    students_ids = fields.Many2many('students', string='Students')
    material_lines = fields.One2many('material', 'level_id', string='Materials')

    def action_view_material(self):
        material_lines = self.mapped('material_lines')
        domain = [('id', 'in', material_lines.ids)]
        context = {'default_level_id': self.id,}
        return {
            'name': _('Materials Lines'),
            'res_model': 'material',
            'view_mode': 'tree,form',
            'domain': domain,
            'context': context,
            'type': 'ir.actions.act_window',
        }


class material(models.Model):
    _name = 'material'
    _description = 'This Class Represents the Materials'
    name = fields.Char(string='Material Name')
    grade_teacher = fields.Many2one('teachers')
    level_id = fields.Many2one('level')

```

❖ Restart odoo server for changes to take effect. when you restart and click on the smart button you will notice a default tree view for the materials and if you clicked one of the material records it will show you a basic form view as well.
❖ We want to define the tree and form view of the materials, first we will go to the `level.py` and in the material class we will add the following: 


```python
_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
```

To add the chatter part, also add the following: 


```python
active = fields.Boolean(default=True)
```

To add the archive option to the materials

❖ So now our `level.py` file should look like this: 


```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

from datetime import *
from datetime import date


class level(models.Model):
    _name = 'level'
    _description = 'This Class Represents the Students Level'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    name = fields.Char(string='Level')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    students_ids = fields.Many2many('students', string='Students')
    material_lines = fields.One2many('material', 'level_id', string='Materials')

    def action_view_material(self):
        material_lines = self.mapped('material_lines')
        domain = [('id', 'in', material_lines.ids)]
        context = {'default_level_id': self.id,}
        return {
            'name': _('Materials Lines'),
            'res_model': 'material',
            'view_mode': 'tree,form',
            'domain': domain,
            'context': context,
            'type': 'ir.actions.act_window',
        }


class material(models.Model):
    _name = 'material'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'This Class Represents the Materials'
    name = fields.Char(string='Material Name')
    grade_teacher = fields.Many2one('teachers')
    level_id = fields.Many2one('level')
    active = fields.Boolean(default=True)

```

❖ Next we will go to our `level.xml` file and add the following records: 

**`for odoo 17`**:


```python
<record model="ir.ui.view" id="material_view_form">
    <field name="name">Material</field>
    <field name="model">material</field>
    <field name="arch" type="xml">
        <form>
            <sheet>
                <field name="active" invisible="1"/>
                <widget name="web_ribbon" title="Archived" bg_color="bg-danger" invisible="active != False"/>

                <group>
                    <group>
                        <field name="name"/>
                    </group>
                    <group>
                        <field name="grade_teacher"/>
                        <field name="level_id"/>
                    </group>
                </group>

            </sheet>
            <div class="oe_chatter">
                <field name="message_follower_ids"/>
                <field name="activity_ids"/>
                <field name="message_ids"/>
            </div>
        </form>
    </field>
</record>

<record model="ir.ui.view" id="material_view_list">
<field name="name">Materials</field>
<field name="model">material</field>
<field name="arch" type="xml">
    <tree>
        <field name="name" width="40%"/>
        <field name="grade_teacher" width="30%"/>
        <field name="level_id" readonly="1" width="30%"/>
    </tree>
</field>
</record>
```

**`for odoo 16`**:


```python
<record model="ir.ui.view" id="material_view_form">
    <field name="name">Material</field>
    <field name="model">material</field>
    <field name="arch" type="xml">
        <form>
            <sheet>
                <field name="active" invisible="1"/>
                <widget name="web_ribbon" title="Archived" bg_color="bg-danger" attrs="{'invisible': [('active', '=', True)]}"/>

                <group>
                    <group>
                        <field name="name"/>
                    </group>
                    <group>
                        <field name="grade_teacher"/>
                        <field name="level_id"/>
                    </group>
                </group>

            </sheet>
            <div class="oe_chatter">
                <field name="message_follower_ids"/>
                <field name="activity_ids"/>
                <field name="message_ids"/>
            </div>
        </form>
    </field>
</record>

<record model="ir.ui.view" id="material_view_list">
<field name="name">Materials</field>
<field name="model">material</field>
<field name="arch" type="xml">
    <tree>
        <field name="name" width="40%"/>
        <field name="grade_teacher" width="30%"/>
        <field name="level_id" readonly="1" width="30%"/>
    </tree>
</field>
</record>
```

**`Key Difference`** 

→ in odoo 17 we used the `invisible` attribute while in odoo 16 we used the `attrs` attribute

**`Now Back to Odoo 17`**

❖ So our `level.xml` file should look something like this: 


```python
<odoo>
    <data>

        <record model="ir.ui.view" id="material_view_form">
            <field name="name">Material</field>
            <field name="model">material</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <field name="active" invisible="1"/>
                        <widget name="web_ribbon" title="Archived" bg_color="bg-danger" invisible="active != False"/>

                        <group>
                            <group>
                                <field name="name"/>
                            </group>
                            <group>
                                <field name="grade_teacher"/>
                                <field name="level_id"/>
                            </group>
                        </group>

                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <record model="ir.ui.view" id="material_view_list">
            <field name="name">Materials</field>
            <field name="model">material</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name" width="40%"/>
                    <field name="grade_teacher" width="30%"/>
                    <field name="level_id" readonly="1" width="30%"/>
                </tree>
            </field>
        </record>

        <record model="ir.ui.view" id="my_module_level_formView">
            <field name="name">my_module level form View</field>
            <field name="model">level</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <div class="oe_button_box" name="button_box">
                            <button
                                    name="action_view_material"
                                    type="object"
                                    class="oe_stat_button"
                                    icon="fa-globe icon"
                            >
                                <div class="o_field_widget o_stat_info">
                                    <span class="o_stat_text">Materials</span>
                                </div>
                            </button>
                        </div>
                        <group>
                            <group>
                                <field name="name"/>
                            </group>
                            <group>
                                <field name="start_date"/>
                                <field name="end_date"/>
                            </group>
                            <notebook>
                                <page string="Materials">
                                    <group>
                                        <field name="material_lines" string="Materials">
                                            <tree string="Materials" editable="bottom">
                                                <field name="name"/>
                                                <field name="grade_teacher"/>
                                            </tree>
                                        </field>

                                    </group>
                                </page>
                                <page string="Students">
                                    <group>
                                        <field name="students_ids"/>
                                        <tree>
                                            <field name="name"/>
                                        </tree>
                                    </group>
                                </page>
                            </notebook>
                        </group>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <record model="ir.ui.view" id="my_module_level_treeView">
            <field name="name">my_module level Tree View</field>
            <field name="model">level</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="start_date"/>
                    <field name="end_date"/>
                </tree>
            </field>
        </record>

        <record model="ir.actions.act_window" id="my_module_level_action">
            <field name="name">level_action</field>
            <field name="res_model">level</field>
            <field name="view_mode">tree,form</field>
        </record>

        <menuitem
                id="my_module_levelView_mainLevel_menuItem"
                name="Level Operation"
                parent="my_module_topLevel_menuItem"
        />

        <menuitem
                id="my_module_levelView_subLevel_menuItem"
                name="Level"
                parent="my_module_levelView_mainLevel_menuItem"
                action="my_module_level_action"
        />
    </data>
</odoo>
```

❖ Now we've successfully implemented the smart button functionality in our module. 

**`Action Smart Button`**

❖ Add the following button in the `level.xml` file before or after our last smart button. 


```python
<button name="%(my_module.material_action)d" type="action" class="oe_stat_button" icon="fa-globe icon">
    <div class="o_field_widget o_stat_info">
        <span class="o_stat_text">Materials</span>
        <span class="o_stat_text">Action</span>
    </div>
</button>
```

❖ so the whole div now should look something like this: 


```python
<div class="oe_button_box" name="button_box">
    <button
            name="action_view_material"
            type="object"
            class="oe_stat_button"
            icon="fa-globe icon"
    >
        <div class="o_field_widget o_stat_info">
            <span class="o_stat_text">Materials</span>
        </div>
    </button>
    <button name="%(my_module.material_action)d" type="action" class="oe_stat_button"
            icon="fa-globe icon">
        <div class="o_field_widget o_stat_info">
            <span class="o_stat_text">Materials</span>
            <span class="o_stat_text">Action</span>
        </div>
    </button>

</div>
```

❖ Now we need to define `material_action` that we mentioned in our button, to do this add the following record in our `level.xml` file right after the data tag


```python
<record model="ir.actions.act_window" id="material_action">
    <field name="name">Material</field>
    <field name="res_model">material</field>
    <field name="view_mode">tree,form</field>
    <field name="domain">[('level_id', '=', active_id)]</field>
    <field name="context">{'default_level_id': active_id}</field>
</record>
```

❖ So now our `level.xml` file should look like this: 


```python
<odoo>
    <data>

        <record model="ir.ui.view" id="material_view_form">
            <field name="name">Material</field>
            <field name="model">material</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <field name="active" invisible="1"/>
                        <widget name="web_ribbon" title="Archived" bg_color="bg-danger" invisible="active != False"/>

                        <group>
                            <group>
                                <field name="name"/>
                            </group>
                            <group>
                                <field name="grade_teacher"/>
                                <field name="level_id"/>
                            </group>
                        </group>

                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <record model="ir.actions.act_window" id="material_action">
            <field name="name">Material</field>
            <field name="res_model">material</field>
            <field name="view_mode">tree,form</field>
            <field name="domain">[('level_id', '=', active_id)]</field>
            <field name="context">{'default_level_id': active_id}</field>
        </record>

        <record model="ir.ui.view" id="material_view_list">
            <field name="name">Materials</field>
            <field name="model">material</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name" width="40%"/>
                    <field name="grade_teacher" width="30%"/>
                    <field name="level_id" readonly="1" width="30%"/>
                </tree>
            </field>
        </record>

        <record model="ir.ui.view" id="my_module_level_formView">
            <field name="name">my_module level form View</field>
            <field name="model">level</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <div class="oe_button_box" name="button_box">
                            <button
                                    name="action_view_material"
                                    type="object"
                                    class="oe_stat_button"
                                    icon="fa-globe icon"
                            >
                                <div class="o_field_widget o_stat_info">
                                    <span class="o_stat_text">Materials</span>
                                </div>
                            </button>
                            <button name="%(my_module.material_action)d" type="action" class="oe_stat_button"
                                    icon="fa-globe icon">
                                <div class="o_field_widget o_stat_info">
                                    <span class="o_stat_text">Materials</span>
                                    <span class="o_stat_text">Action</span>
                                </div>
                            </button>

                        </div>
                        <group>
                            <group>
                                <field name="name"/>
                            </group>
                            <group>
                                <field name="start_date"/>
                                <field name="end_date"/>
                            </group>
                            <notebook>
                                <page string="Materials">
                                    <group>
                                        <field name="material_lines" string="Materials">
                                            <tree string="Materials" editable="bottom">
                                                <field name="name"/>
                                                <field name="grade_teacher"/>
                                            </tree>
                                        </field>

                                    </group>
                                </page>
                                <page string="Students">
                                    <group>
                                        <field name="students_ids"/>
                                        <tree>
                                            <field name="name"/>
                                        </tree>
                                    </group>
                                </page>
                            </notebook>
                        </group>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <record model="ir.ui.view" id="my_module_level_treeView">
            <field name="name">my_module level Tree View</field>
            <field name="model">level</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="start_date"/>
                    <field name="end_date"/>
                </tree>
            </field>
        </record>

        <record model="ir.actions.act_window" id="my_module_level_action">
            <field name="name">level_action</field>
            <field name="res_model">level</field>
            <field name="view_mode">tree,form</field>
        </record>

        <menuitem
                id="my_module_levelView_mainLevel_menuItem"
                name="Level Operation"
                parent="my_module_topLevel_menuItem"
        />

        <menuitem
                id="my_module_levelView_subLevel_menuItem"
                name="Level"
                parent="my_module_levelView_mainLevel_menuItem"
                action="my_module_level_action"
        />
    </data>
</odoo>
```

❖ Now we've successfully implemented a smart button it's type is action in our module

**`Reports in Odoo 16`**

→ create a new file under your module inside a new `reports` directory. or simply create a new file with this `reports/report.xml` and add the following code to it: 


```python
<odoo>
    <data>
        <record id="my_module_student_report" model="ir.actions.report">
            <field name="name">School Student</field>
            <field name="model">students</field>
            <field name="report_type">qweb-pdf</field>
            <field name="print_report_name">('Student - %s' % (object.name))</field>
            <field name="report_name">my_module.report_students</field>
            <field name="report_file">my_module.report_students</field>
            <field name="binding_model_id" ref="model_students"/>
            <field name="binding_type">report</field>
        </record>
    </data>
</odoo>
```

→ also reference it in our `manifest` file after the `templates.xml`: 


```python
# always loaded
'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/level.xml',
    'data/data.xml',
    'views/my_module_settings.xml',
    'views/templates.xml',
    'reports/report.xml',
],
```

❖ now we need to define `report_students` that we mentioned in `report_name` and `report_file` in our `templates.xml` file

❖ open `templates.xml` file and add the following code to it:


```python
<odoo>
    <data>

        <template id="report_students_document">
            <t t-call="web.external_layout">
                <t t-set="doc" t-value="doc"/>
                <div class="page">
                    <div class="oe_structure"/>
                    <h2 class="mt-4">
                        <span>Student Name #</span>
                        <span t-field="doc.name"/>
                    </h2>
                    <div class="row mt-4 mb-4" id="informations">
                        <div t-if="doc.age" class="col-auto col-3 mw-100 mb-2" name="informations_reference">
                            <strong>Age:</strong>
                            <p class="m-0" t-field="doc.age"/>
                        </div>
                        <div t-if="doc.birthday" class="col-auto col-3 mw-100 mb-2" name="information_date">
                            <strong>Birth Date:</strong>
                            <p class="m-0" t-field="doc.birthday"/>
                        </div>
                        <div t-if="doc.gender" class="col-auto col-3 mw-100 mb-2">
                            <strong>Gender:</strong>
                            <p class="m-0" t-field="doc.gender"/>
                        </div>
                    </div>

                    <div class="row mt-4 mb-4" id="informations">
                        <div t-if="doc.note" class="col-auto col-6 mw-100 mb-2" name="informations_reference">
                            <strong>note:</strong>
                            <p class="m-0" t-field="doc.note"/>
                        </div>
                    </div>
                    
                </div>
            </t>
        </template>


        <template id="report_students">
            <t t-call="web.html_container">
                <t t-foreach="docs" t-as="doc">
                    <t t-call="my_module.report_students_document"/>
                </t>
            </t>
        </template>
    </data>
</odoo>
```

❖ Now relaunch the server and upgrade the module and click on any student to view it's form view you will see a print button next to the action button. print the document and the browser should ask you to download a pdf document (the report of that student). 

**`Print PDF Report With Wizard and Transient Model In odoo 16 & 17`**

→ The idea of the wizard is that we want to create a menu item in our module that will trigger a wizard which will ask you if you want to print all students or only a certain grade of students. 

→ Create a new directory under your module name we will call it `wizard` and we will create a file under that directory called `report_student_wizard.py`. or simply right click on your module >> choose new file and type `wizard/report_student_wizard.py`

→ Add the following code to it: 


```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

class wizard_report_student(models.TransientModel):
    _name = 'wizard.report.student'
    show_all_grade = fields.Boolean(default=True)
    grade = fields.Selection(
        [('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3')], string='Grade'
    )

    def print_report_pdf(self):
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'students',
            'form': data
        }
        return self.env.ref('my_module.students_details_report').report_action([], data=datas)
```

→ also create a new `report_student_wizard.xml` file next to the python file under the `wizard` directory and add the following code to it: 


```python
<odoo>
    <data>
        <record model="ir.ui.view" id="student_report_view_form">
            <field name="name">Student Report</field>
            <field name="model">wizard.report.student</field>
            <field name="arch" type="xml">
                <form>
                    <group>
                        <group>
                            <field name="show_all_grade"/>
                            <field name="grade"/>
                        </group>
                    </group>
                    <footer>
                        <button name="print_report_pdf" string="Print" type="object" default_focus="1" class="oe_highlight" data-hotkey="q"/>
                        <button string="Cancel" class="btn btn-secondary" special="cancel" data-hotkey="z"/>
                    </footer>
                </form>
            </field>
        </record>

        <record id="action_report_wizard_student" model="ir.actions.act_window">
            <field name="name">Student Reports</field>
            <field name="res_model">wizard.report.student</field>
            <field name="view_mode">form</field>
            <field name="target">new</field>
        </record>


        <menuitem
        id="menu-reports"
        name="Reports"
        parent="my_module_topLevel_menuItem"
        sequence="10"
        />

        <menuitem
        id="menu-my_module_config"
        name="Students Report"
        parent="menu-reports"
        sequence="1"
        action="action_report_wizard_student"
        />


    </data>
</odoo>
```

→ also create `__init__.py` file under the wizard directory and add the following code to it: 


```python
from . import report_student_wizard
```

→ also in the module main `__init__.py` file add the following line: 


```python
from . import wizard
```

→ Now let's go to the module `__manifest__.py` file to reference the wizard


```python
# always loaded
'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/views.xml',
    'views/level.xml',
    'data/data.xml',
    'views/my_module_settings.xml',
    'views/templates.xml',
    'reports/report.xml',
    'wizard/report_student_wizard.xml',
],
```

→ Now let's create the access rights for what we did, in the `ir.model.access.csv` file add the following: 


```python
access_report_student_manager,access_report_student,model_wizard_report_student,my_module.group_school_manager,1,1,1,1
access_report_student_user,access_report_student,model_wizard_report_student,my_module.group_school_user,1,1,1,0
```

**`Very Important Note`**

→ in file `report_student_wizard.xml` in the action record there's a field `res_model` which is set to `wizard.report.student` which is the same name of the `_name` in the class `wizard_report_student` in the `report_student_wizard.py` file. 

❖ Untill now we can't print all students yet so we will follow on ..

❖ Next go to `report.xml` and add the following record: 


```python
<record id="students_details_report" model="ir.actions.report">
    <field name="name">Student Details</field>
    <field name="model">students</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">my_module.report_students_details</field>
</record>
```

→ As you can see the id of that record `students_details_report` is the same name of what the function (`print_report_pdf`) returns in the file `report_student_wizard.py` 

→ Next create a new python file under the report directory. we will call it `report.py` and add the following code to it: 


```python
from odoo import api, fields, models
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ReportStudentDetails(models.AbstractModel):
    _name = 'report.my_module.report_students_details'
    _description = 'Student Details'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        students = self.env['students'].search([])
        return {
            'students': students
        }
```

→ as you can see the `_name` of the class is the same name as the `report_name` field in `report.xml` file.

→ Next we need to create `__init__.py` file next to the `report.py` file and add the following to it:  


```python
from . import report
```

→ **`VIP Note`** report without s cuz the python file is called report.py while the directory is called reports with an s

→ Next in the main `__init__.py` file of the module add the following line as well:


```python
from . import reports
```

→ We added the s here cuz we want to import the directory reports.

→ Next we will go to the `templates.xml` file and define `report_students_details` so open the file and add the following template to it: 


```python
<template id="report_students_details">
    <t t-call="web.html_container">
        <t t-call="web.internal_layout">
            <div class="page">
                <div class="text-center">
                    <h2>Student Details</h2>
                </div>
                <h3>Students</h3>
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Age</th>
                            <th>Grade</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr t-foreach="students" t-as="line">
                            <td>
                                <t t-esc="line['name']"/>
                            </td>
                            <td>
                                <t t-esc="line['age']"/>
                            </td>
                            <td>
                                <t t-esc="line['grade']"/>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </t>
    </t>
</template>
```

→ Now relaunch the server and go print all the students from all the grades. 

→ Next we will learn how to print all students from a specific grade. to do this we need to edit the `_get_report_values` function that we overwrite it in our `report.py` file. instead of returning all the students we will make an if statement: 


```python
@api.model
def _get_report_values(self, docids, data=None):
    if data['form'].get('grade', False):
        students = self.env['students'].search([('grade', '=', data['form'].get('grade', False))])
        return {
            'students': students,
            'data': data['form'],
        }
    else:
        students = self.env['students'].search([])
        return {
            'students': students,
            'data': data['form'],
        }

```

→ Relaunch the server and now you can print a specific grade or if no grade is set it in the wizard it will print all the students from all the grades. 

→ Now we want to mention in our out report template which grade is being printed or if all students are printed so who ever see the report knows which grade he is reading. 

→ open `templates.xml` file, and we will add a div under the H3 Element `<h3>Students</h3>`


```python
<div>
    <br/>
    <t t-if="data['grade']" class="text-end">
        <span>
            Grade:
            <t t-esc="data['grade']"/>
        </span>
    </t>
    <t t-if="not data['grade']" class="text-end">
        <span>
            All Grades
        </span>
    </t>
</div>
```

→ So now our template should look like this: 


```python
<template id="report_students_details">
    <t t-call="web.html_container">
        <t t-call="web.internal_layout">
            <div class="page">
                <div class="text-center">
                    <h2>Student Details</h2>
                </div>
                <h3>Students</h3>

                <div>
                    <br/>
                    <t t-if="data['grade']" class="text-end">
                        <span>
                            Grade:
                            <t t-esc="data['grade']"/>
                        </span>
                    </t>
                    <t t-if="not data['grade']" class="text-end">
                        <span>
                            All Grades
                        </span>
                    </t>
                </div>

                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Age</th>
                            <th>Grade</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr t-foreach="students" t-as="line">
                            <td>
                                <t t-esc="line['name']"/>
                            </td>
                            <td>
                                <t t-esc="line['age']"/>
                            </td>
                            <td>
                                <t t-esc="line['grade']"/>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </t>
    </t>
</template>
```

→ Relaunch the server and try to print again and see the difference. 

**`Print Excel Reports with Wizard`**

→ To print excel reports we need external module on odoo apps called `base report xlsx` you can find it through this link: 

[Base Report xlsx](https://apps.odoo.com/apps/modules/16.0/report_xlsx)

→ `VIP Note`: This Module has version for odoo 16 and odoo 17 so choose the corresponding one.

→ After you download the module and extract the zip file copy the folder `report_xlsx` to your custom-addons directory.

→ Restart the server and go to the Apps list and activate the new module. 

→ next we need to edit our wizard to include a new button for print xlsx and we will edit the old print button to be print PDF 

→ open `report_student_wizard.xml` file and let's make those changes: first add the following button code: 


```python
<button name="print_report_xlsx" string="Print xlsx" type="object" default_focus="1" class="oe_highlight" data-hotkey="q"/>
```

→ The record now should look something like this: 


```python
<record model="ir.ui.view" id="student_report_view_form">
    <field name="name">Student Report</field>
    <field name="model">wizard.report.student</field>
    <field name="arch" type="xml">
        <form>
            <group>
                <group>
                    <field name="show_all_grade"/>
                    <field name="grade"/>
                </group>
            </group>
            <footer>
                <button name="print_report_pdf" string="Print PDF" type="object" default_focus="1" class="oe_highlight"
                        data-hotkey="q"/>
                <button name="print_report_xlsx" string="Print xlsx" type="object" default_focus="1"
                        class="oe_highlight" data-hotkey="q"/>
                <button string="Cancel" class="btn btn-secondary" special="cancel" data-hotkey="z"/>
            </footer>
        </form>
    </field>
</record>
```

→ We renamed the string value to be `Print PDF` 

→ Next we need to define the function `print_report_xlsx` in our `report_student_wizard.py` file. so add the following function after the print pdf report function: 


```python
def print_report_xlsx(self):
    data = {
        'form_data': self.read()[0],
    }
    return self.env.ref('my_module.students_details_xlsx').report_action(self, data=data)
```

→ Next we need to define `students_details_xlsx` in our `report.xml` so we will add the following new record at the end of the existing records: 


```python
<record id="students_details_xlsx" model="ir.actions.report">
    <field name="name">Student Details</field>
    <field name="model">wizard.report.student</field>
    <field name="report_type">xlsx</field>
    <field name="report_name">my_module.students_details_xlsx</field>
    <field name="report_file">my_module.students_details_xlsx</field>
    <field name="binding_type">report</field>
</record>
```

→ As you can see the model name is the same name from the report_student_wizard.py file (The `_name` of the class)

→ Next we need to define `students_details_xlsx` as a python code so we will go to `report.py` file and add the following class: 


```python
class PartnerXlsx(models.AbstractModel):
    _name = 'report.my_module.students_details_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            if data['form_data'].get('grade', False):
                report_name = "Grade:" + str(data['form_data'].get('grade', False))
            else:
                report_name = "All Grade"

            if data['form_data'].get('grade', False):
                students = self.env['students'].search([('grade', '=', data['form_data'].get('grade', False))])
            else:
                students = self.env['students'].search([])

            sheet = workbook.add_worksheet(report_name)
            bold = workbook.add_format({'bold': True})
            date_format = workbook.add_format({'num_format': 'dd/mm/yy'})
            align_center = workbook.add_format({'align': 'center'})
            align_center_b = workbook.add_format({'align': 'center', 'bold': True})
            row = 5
            col = 5
            sheet.write(row, col, 'Grade', bold)
            col += 1
            sheet.write(row, col, report_name)
            row += 1
            col -= 1
            col += 1
            if students:
                row += 2
                col = 1
                sheet.merge_range(row, col, row, col + 5, 'students', align_center)
                row += 1
                col = 1
                sheet.write(row, col, 'Name', bold)
                col += 1
                sheet.write(row, col, 'Age', bold)
                col += 1
                sheet.write(row, col, 'Grade', bold)
                row += 1
                col = 1
                for record in students:
                    sheet.write(row, col, record.name)
                    col += 1
                    sheet.write(row, col, record.age)
                    col += 1
                    sheet.write(row, col, record.grade)
                    col = 1
                    row += 1
        workbook.close()

```

→ Now update both `my_module` and `report_xlsx` in you PyCharm config 

`odoo.conf -u my_module -u report_xlsx -d odoo_16_learning`

→ Add the module `report_xlsx` in our manifest file


```python
# any module necessary for this one to work correctly
'depends': ['base', 'portal', 'mail', 'utm', 'report_xlsx'],
```

and try to print the excel sheet again 

**`VIP Note`** if you encounter any issues you might want to uninstall `my_module` and re-install it again. but if you do that you will find out that `all your menus are gone!` and the module will take you to the settings page and that's it. 

**`The Reason:`** when you uninstall the module there's no permission now for `Mitchell Admin` the default odoo user to view the modules menu because he is not a school manager anymore. so in order to fix this we need to go to settings >> users & companies >> users >> Mitchell Admin and make him a shcool manager again. 

→ Refersh the page go to your module. you'll find all menus are back.

