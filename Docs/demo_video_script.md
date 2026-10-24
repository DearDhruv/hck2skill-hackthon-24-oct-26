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
Finally, it calls `draft_social_media_post`, creating an instant, 1-click X (Twitter) post tagging `@AhmedabadAMC` for public civic escalation."

---

### [00:50 - 01:20] The Status Query: "What's the status?"
*(Dhruv clicks 'Track Status' or switches to the 'Status Check' tab. He clicks the quick chip 'what\'s the status?'.)*

**Spoken**:  
"Now, the citizen asks plain conversational English: *'What's the status?'*  
The agent parses the intent, invokes `fetch_complaint_status`, and pulls the real-time record from the municipal ledger.  
Notice the visual lifecycle pipeline: Submitted, Assigned, In Progress, Work Verified, and Resolved.  
If I click 'Advance to Next Stage', we simulate the field repair crew in action on stage. The status immediately updates to 'In Progress', timestamped with repair notes."

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
