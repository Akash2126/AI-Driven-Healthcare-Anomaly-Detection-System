@echo off
echo ==========================================
echo AI ANOMALY DETECTION SYSTEM - STARTING
echo ==========================================

start start_kafka.bat
timeout /t 20

start start_consumer.bat
timeout /t 5

start start_producer.bat
