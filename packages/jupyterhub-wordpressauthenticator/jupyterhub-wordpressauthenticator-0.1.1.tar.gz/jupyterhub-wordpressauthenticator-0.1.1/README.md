# WordPress JupyterHub Authenticator #

Wordpress authenticator for [JupyterHub](http://github.com/jupyter/jupyterhub/) along with [WordPress](https://wordpress.org) database.

## Requirements
[PyMySQL](https://pypi.org/project/PyMySQL/)

[PassLib](https://pythonhosted.org/passlib/)

## Installation

```
pip install jupyterhub-wordpressauthenticator
```

And add the following lines to your `jupyterhub_config.py`:

```
c.JupyterHub.authenticator_class = "wordpressauthenticator.WordPressAuthenticator"
c.WordPressAuthenticator.dbuser = "yourDatabaseUserName"
c.WordPressAuthenticator.dbpassword = "yourDatabasePassword"
```

* `dbuser` : user name to access your wordpress database
* `dbpassword` : password to access your wordpress database

Next lines are optional:
```
c.WordPressAuthenticator.dbhost = "localhost"
c.WordPressAuthenticator.dbport = "3306"
c.WordPressAuthenticator.dbname = "wordpress"
c.WordPressAuthenticator.table_prefix = "wp_"
```
* `dbhost` : URL or IP address of the database server (Default : `localhost`)
* `dbport` : port of the database server (Default : `3306`)
* `dbname` : database name that your wordpress uses (Default : `wordpress`)
* `table_prefix` : table prefix for your wordpress (Default : `wp_`)

## License
MIT License
