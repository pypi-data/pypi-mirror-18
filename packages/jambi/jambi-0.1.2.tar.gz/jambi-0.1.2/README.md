# jambi
A peewee database migration manager (in development)

### Disclaimer
This is in development, so some of the things you see might not be fully working. I will be sure to update this project and remove this disclaimer once things are in a stable state, but for right now, **use this tool at your own risk**. I claim no responsibility for bugs or other misuse of this tool resulting in loss of data or any other unintended side-effect.

### Getting Started
1. clone this repo
    * `git clone https://github.com/kruchone/jambi.git`
    * `cd jambi/`
2. create a python virtual environment
    * `virtualenv --python=python3 env`
    * `source env/bin/activate`
3.  upgrade pip and wheel
    * `pip install --upgrade pip`
    * `pip install --upgrade wheel`
4. install jambi's requirements
    * `pip install -r requirements.txt`
5. run jambi!
    * `./jambi.py --help`

### Supported Operations
* **inspect** -- return the database's current version.
* **upgrade _&lt;revision&gt;_** -- upgrade your database to the supplied revision
* **downgrade _&lt;revision&gt;_** -- downgrade your database to the supplied revision
* **makemigration** -- generate a new migration version from template

### Configuration
Jambi needs to know how to connect to your database, and where your migrations are stored, which can be conveyed though the `jambi.conf` configuration file. Currently `jambi.conf` needs to be in the same directory as jambi itself, however soon you will be able to check `jambi.conf` in to your source code.

Here is an example `jambi.conf`, set up to connect to a vanilla postgres database:
```
[database]
database=test
schema=public
host=localhost
user=postgres
password=

[migrate]
location=./migrations/
```

### Contributing
I would like to get things to a decently-stable state before I start accepting contributions, but stay tuned!
