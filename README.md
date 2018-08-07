# p2p-securities-trading

* Proof-of-Concept peer-to-peer securities trading platform. 
* Developed on Corda and Django.
* Built with Corda example application. 
* [Example App Documentation](https://docs.corda.net/tutorial-cordapp.html)

## Getting Started

clone repository - provides copy of Corda application (Cordapp) and Django project.
```
git clone https://github.com/MalvinLo/p2p-securities-trading.git
```
## Prerequisites

* java
* python

## Installing

### Build Borda Nodes

Change to cordapp-example directory

Linux
```
./gradlew deployNodes
```
Windows
```
gradlew.bat deployNodes
```

### Launch Corda Nodes

Make sure you are still in the cordapp-example directory

Linux
```
kotlin-source/build/nodes/runnodes
```
Windows
```
call kotlin-source\build\nodes\runnodes.bat
```

### Run Django dev server

Navigate to tradingInterface directory
```
python manage.py runserver
```


## Built With

* [Django](https://docs.djangoproject.com/en/2.0/) - Web Framework
* [Corda](https://docs.corda.net/) - Distributed Ledger Network

