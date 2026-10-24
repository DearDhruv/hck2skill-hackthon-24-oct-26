# 2-Minute Demo Video & Presentation Script
## NagrikAMC · Autonomous Civic Complaint Agent (Track 01)

**Duration**: 120 seconds  
**Presenter**: Dhruv Patel  
**Target Audience**: Hack2Skill Judges & Municipal Evaluators  

---

### [00:00 - 00:20] The Hook: The Civic Friction
*(Screen opens on NagrikAMC Web Dashboard at `http://localhost:8000`. The green 'Mock AMC Engine Active' badge pulses.)*

**Spoken**:  
"Good afternoon, judges. In cities like Ahmedabad, reporting a road pothole, overflowing garbage, or a broken streetlight takes 15 minutes of frustrating form-filling. You have to figure out which of the 48 municipal wards you're standing in, which department handles it, and chase tracking numbers for weeks. Most citizens give up before filing.  
Today, we present **NagrikAMC** — an autonomous AI agent that reasons, uses municipal tools, and takes action."

---

### [00:20 - 00:50] The Core Flow: Photo In, Verified Ticket Out
*(Dhruv clicks the 1-Tap sample button 'Pothole at CG Road'. The preview loads instantly. He clicks 'Execute Autonomous AI Filing'.)*

**Spoken**:  
"Watch the agent's live ReAct reasoning stream in the terminal.  
First, the agent calls `analyze_image` to classify the hazard. It detects a critical asphalt cavity with 96% confidence and extracts surface failure characteristics.  
Next, it calls `lookup_ward_and_department`. It maps CG Road directly to **Ward W12 (Navrangpura, West Zone)** and routes it to **Roads & Buildings**.  
Then, it calls `create_complaint_ticket`, generating official tracking ID **AMC-2026-000126**, binding a 24-hour SLA guarantee, and assigning Sub-Divisional Engineer Er. Rajesh Dave.  
Notice the **Municipal Authority Escalation Desk**: with 1 click, the citizen can directly call Ward Officer Shri Arvind Trivedi, dial the AMC 24x7 helpline `155303`, or open Google Maps directions to the local ward office!"

---

### [00:50 - 01:10] The Status Query & Stage Advance
*(Dhruv clicks 'Track Status' or switches to the 'Status Check' tab. He clicks the quick chip 'what\'s the status?'.)*

**Spoken**:  
"Now, the citizen asks plain conversational English: *'What's the status?'*  
The agent parses the intent, invokes `fetch_complaint_status`, and pulls the real-time record from the municipal ledger.  
Notice the visual lifecycle pipeline: Submitted, Assigned, In Progress, Work Verified, and Resolved.  
If I click 'Advance to Next Stage', we simulate the field repair crew in action on stage. The status immediately updates to 'In Progress', timestamped with repair notes."

---

### [01:10 - 01:30] Chaos Engineering: Zero-Flake Resilience & Self-Healing
*(Dhruv toggles 'Chaos Mode: ON' with '500 DB Crash', clicks 'Execute Autonomous AI Filing', shows the ErrorStateCard, and clicks 'Turn Off Chaos & Recover'.)*

**Spoken**:  
"Judges love to ask: *'What happens if the backend crashes or the network drops during demo?'*  
We engineered built-in Fault Injection. I flip Chaos Mode on to simulate a 500 database pool deadlock. The UI catches it gracefully with zero form data loss, displays the subsystem diagnostic, and with one tap on 'Turn Off Chaos & Recover', the system self-heals and commits the verified ticket in 300ms!"

---

### [01:20 - 01:45] The Stretch Goal: Continuous Road Video Scanner
*(Dhruv switches to the 'Road Scanner' tab and clicks 'Execute Road Video Inspection'.)*

**Spoken**:  
"We didn't stop there. Here is our stretch goal: continuous road video surveillance.  
Imagine dashcams on municipal garbage trucks or BRTS buses. The system samples 1 frame every 3 seconds along the CG Road corridor, detects road craters with vision heuristics, plots GPS coordinates, and automatically files AMC tickets with zero human intervention. In 5 frames, it identified 2 critical road craters and auto-filed official tickets."

---

### [01:45 - 02:00] Architecture & Closing
*(Dhruv clicks the 'AMC Ledger' tab to show all tickets safely stored in the database.)*

**Spoken**:  
"NagrikAMC runs with Clean Architecture, an offline-resilient AMC mock engine with 1-click seed reset for venue reliability, and 100% automated test coverage.  
NagrikAMC turns civic frustration into immediate municipal action. Thank you!"
