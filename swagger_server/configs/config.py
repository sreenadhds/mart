import os
import logging
development={

    "db_host":os.getenv('db_host',"127.0.0.1"),
    "db_name": "usermgmt",
    "db_password":"root",
    "secret_key":"nfjcnfjncjfn",
    "admin_hash":"pbkdf2:sha256:50000$Fl2wclwD$7909a58b9f43326897ea2d2a40653c3760ff2c35ea08415680fc8a3b84020968",
    "admin_username":"admin",
    "log_level":logging.DEBUG,
    "log_filename":"/tmp/mart.log",
    "metrics_port":9000
}


production={
    "db_host":os.getenv('db_host',"127.0.0.1"),
    "db_name":"usermgmt",
    "db_username":"root",
    "db_password":"root",
    "secret_key":"nfjcnfjncjfn",
    "admin_hash":"pbkdf2:sha256:50000$Fl2wclwD$7909a58b9f43326897ea2d2a40653c3760ff2c35ea08415680fc8a3b84020968",
    "admin_username":"admin",
    'log_level':logging.INFO,
    "log_filename": "/tmp/mart.log",
    "metrics_port":9000

}