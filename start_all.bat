@echo off
echo Starting Zookeeper...
start cmd /k "cd /d C:\kafka\bin\windows && zookeeper-server-start.bat ..\..\config\zookeeper.properties"

timeout /t 10

echo Starting Kafka Broker...
start cmd /k "cd /d C:\kafka\bin\windows && kafka-server-start.bat ..\..\config\server.properties"
