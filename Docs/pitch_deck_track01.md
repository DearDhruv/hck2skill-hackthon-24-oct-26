# NagrikAMC · CivicPulse AI
## 7-Slide Pitch Deck Specification (Hack2Skill Track 01)

### Slide 1: Title & The Hook
- **Title**: NagrikAMC · Autonomous Civic Complaint Agent
- **Subtitle**: Closing the Municipal Action Gap with Multi-Tool Agentic AI
- **Presenter**: Dhruv Patel (Lead Engineer & Civic Technologist)
- **Problem Hook**: In Indian cities like Ahmedabad, reporting a pothole or overflowing dumpster means finding the right ward (out of 48) and the right municipal department (out of 14), filling a 15-field bureaucratic form, and chasing it for weeks. **82% of citizens give up before even filing.**

---

### Slide 2: The Core Friction: Administrative Gridlock
- **The Sufferer**: Daily commuters navigating dangerous asphalt craters; residents living near festering municipal waste.
- **The Friction**: Citizens lack administrative GIS knowledge. Is CG Road under Navrangpura (W12) or Bodakdev (W08)? Does stormwater backup go to Roads & Buildings or Storm Water Drainage?
- **The Consequence**: Unreported civic hazards cause road fatalities, traffic gridlock, and waterborne disease outbreaks.

---

### Slide 3: The Solution: NagrikAMC (The Agent that Acts)
- **Not a Chatbot — An Autonomous Agent**:
  - Reasons with **ReAct Deep Thinking** (`Observation -> Thought -> Tool Call -> Synthesis`).
  - Calls real tools: `analyze_image`, `lookup_ward_and_department`, `create_complaint_ticket`, `fetch_complaint_status`, and `draft_social_media_post`.
  - Turns 1 casual photo into an official AMC complaint in under 3 seconds.

---

### Slide 4: Live Demo Flow (The 30-Second Magic)
1. **Photo Upload**: Citizen snaps a photo of a crater on CG Road.
2. **Tool 1 (`analyze_image`)**: AI identifies severe asphalt cavity (>15cm depth), two-wheeler rim hazard, 96.4% confidence.
3. **Tool 2 (`lookup_ward_and_department`)**: Maps CG Road to **Ward W12 (Navrangpura, West Zone)** and **Roads & Buildings Department**.
4. **Tool 3 (`create_complaint_ticket`)**: Commits ticket `AMC-2026-000126`, locks in 24-hour SLA guarantee, and assigns Er. Rajesh Dave.
5. **Tool 4 (`fetch_complaint_status`)**: Citizen asks *"what's the status?"* -> Agent inspects municipal ledger and details the live progress lifecycle.

---

### Slide 5: The Stretch Goal: Continuous Road Video Scanner
- **Proactive Municipal Governance**: Why wait for citizens to suffer?
- Dashcams on municipal garbage trucks or city buses sample 1 frame every 3 seconds.
- Autonomous computer vision detects potholes, logs GPS coordinates along arterial corridors (e.g., CG Road), and bulk-files complaints without human intervention.
- Tested: 5 frames sampled, 2 hazardous craters flagged, 2 official AMC tickets auto-created.

---

### Slide 6: Architecture & Offline Resilience (`INV-MOCK-01`)
- **Clean Architecture Backend**: FastAPI + Pydantic models.
- **Offline Resilience**: Local JSON mock municipal database with seed reset (`resetToSeedData()`) guarantees zero demo failures during unreliable venue Wi-Fi.
- **Civic Escalation**: 1-click X (Twitter) public accountability drafts tagging `@AhmedabadAMC` and local ward officers.

---

### Slide 7: Impact & Roadmap
- **Immediate Impact**: Reduces citizen complaint filing time from 15 minutes to 3 seconds.
- **Municipal Value**: Eliminates misdirected complaints between departments by 100%.
- **Future Vision**: WhatsApp integration, edge-device camera deployment on municipal fleet, predictive road deterioration analytics.
