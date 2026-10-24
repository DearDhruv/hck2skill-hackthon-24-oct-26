# 10-Minute Problem Assessment Worksheet (Hack2Skill Track 01)

Completed for Track 01: Civic Complaint Agent · Ahmedabad Municipal Corporation (AMC).

---

## 1. Problem Statement Intake
- **Given Track / Theme**: Track 01 · Agents: Civic Complaint Agent (The AI reasons, uses tools, and takes action)
- **Official Problem Statement**:
  > Reporting a pothole, garbage, a broken streetlight or water logging means finding the right ward and department, filing the complaint, and chasing it for weeks. Most people give up before filing.
- **Expected Demo Output**:
  > A photo goes in. The agent identifies the issue, picks the ward and department, and files a complaint with a tracking ID. The user then asks "what's the status?" and gets an answer.

---

## 2. Problem Deconstruction (The 3 Whys)
1. **Who is the suffering user?**
   - *Target Persona*: Frustrated urban citizens, daily commuters, and civic activists in Ahmedabad who encounter potholes, overflowing garbage dumps, unlit roads, or waterlogged streets.
2. **What is their acute friction point today?**
   - *Friction*: Citizen apathy caused by administrative bureaucracy — citizens do not know whether a pothole belongs to West Zone Ward W12 (Navrangpura) or South Zone Ward W27 (Maninagar), nor which department handles stormwater vs roads. Chasing tickets requires endless manual follow-ups with zero transparency.
3. **Why do existing apps/solutions fail them?**
   - *Failure point*: Rigid 15-field bureaucratic municipal forms require manual zone selection, ward dropdowns, department classification, and account logins before filing. If the internet is spotty or servers are down, everything fails. No conversational agent exists to triage photos or answer "what's the status?" in plain English.

---

## 3. The 4-Hour Solution Scope (The 1-Killer Flow)
- **Proposed Project Name**: **NagrikAMC · CivicPulse AI**
- **One-Sentence Value Prop**:
  > *"An autonomous, offline-resilient civic complaint agent that turns raw street photos into verified municipal tickets and real-time status updates without municipal bureaucracy."*
- **The Killer Flow (The 3 Steps to Demo)**:
  1. *Input / Ingestion*: Citizen snaps a photo (or picks a 1-tap pre-packaged photo: Pothole at CG Road, Garbage at Kankaria, Streetlight at Vastrapur, Waterlogging at Stadium).
  2. *Processing / Intelligence*: Autonomous ReAct agent executes a visible 4-step tool pipeline:
     - `analyze_image`: Computer vision feature & severity diagnostics.
     - `lookup_ward_and_department`: Resolves AMC GIS ward jurisdiction & municipal department.
     - `create_complaint_ticket`: Generates official tracking ID (`AMC-2026-XXXXXX`) and SLA timer.
     - `draft_social_media_post`: Formats public escalation post for X (Twitter) tagging `@AhmedabadAMC`.
  3. *Actionable Output & Inquiry*: Citizen receives tracking ID and SLA guarantee, then asks *"what's the status?"* to receive real-time lifecycle progress with an interactive audit timeline.
- **Stretch Goal Delivered**: Continuous Road Video Scanner that samples dashcam footage every 3 seconds, detects potholes, pins GPS telemetry, and automates bulk ticket generation.

---

## 4. Multi-Device Persona Matrix
- **Mobile (Phone)**: Quick on-the-go photo capture, 1-tap samples, responsive card view.
- **Tablet / Foldable**: Side-by-side split-pane: Image preview & live ReAct reasoning stream on the left, ticket audit timeline on the right.
- **Desktop / Web**: Executive municipal ledger, video corridor hazard inspector, and live lifecycle simulator.

---

## 5. Architectural Verification & Zero-Flake Guarantee
- **Local AMC Mock Database**: Full JSON persistence (`app/data/amc_seed_database.json`) with `resetToSeedData()` for repeated judge presentations (`INV-MOCK-01`).
- **Zero Third-Party Dependency**: No WhatsApp Business API or municipal portal credentials needed.
- **Offline Resilience**: Runs 100% locally on `http://localhost:8000`.
