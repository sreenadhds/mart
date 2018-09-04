import os
development={

    "db_host":os.getenv('db_host',"127.0.0.1"),
    "db_username":"",
    "db_password":"",
    "secret_key":"",
    "admin_hash":"pbkdf2:sha256:50000$Fl2wclwD$7909a58b9f43326897ea2d2a40653c3760ff2c35ea08415680fc8a3b84020968",
    "admin_username":"admin"
}


production={
    "db_host":os.getenv('db_host',"127.0.0.1"),
    "db_username":"",
    "db_password":"",
    "secret_key":"",
    "admin_hash":"pbkdf2:sha256:50000$Fl2wclwD$7909a58b9f43326897ea2d2a40653c3760ff2c35ea08415680fc8a3b84020968",
    "admin_username":"admin"
}