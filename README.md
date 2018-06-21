# p2p-securities-trading

* A peer-to-peer platform for trading securities. 
* Developed on Corda and Django.
* Started with Corda example application.

## Getting Started

clone repository - provides copy of Corda application (Cordapp) and Django project.

### Prerequisites

* java
* python

### Installing

launch corda nodes from Cordapp home directory

```
call kotlin-source\build\nodes\runnodes
```

configure ALLOWED_HOSTS in Django settings file

run Django test server from Django project directory
```
python manage.py runserver
```

navigate to server on web browser to test application


## Built With

* [Django](https://docs.djangoproject.com/en/2.0/) - Web Framework
* [Corda](https://docs.corda.net/) - Distributed Ledger Network

