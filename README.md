# IoT Trigger-Action Protection Prototype

A reference implementation of “Activity-Recognition Protection for IoT Trigger-Action Platforms” (EuroS&P 2024) plus a real-time dashboard.

## Features
* Simulated temperature & motion sensors  
* Rule-based activity detector that publishes `activity/detected`  
* Policy checker that decides whether requested actions are *allowed* or *blocked*  
* Enforcement layer that executes or drops the action  
* Flask dashboard (`http://localhost:5000`) showing the last activity, action, and decision  
* One-command run: `python main.py`

## Project structure
<explain tree above>

## Quick start
```bash
git clone https://github.com/<you>/IoT_TriggerAction_Protection.git
cd IoT_TriggerAction_Protection
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
