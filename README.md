# GrizzHacks8
This is the code for GrizzHacks 8

Phase 1: Project Setup 

Repo Initialization: Clone the ai-chatbot-with-memory repo. 

The "MCL Registry" (Michigan Compiled Laws): 
Create a data/michigan_rules.json file. This prevents the AI from making up dates.

Small Claims: Max $7,000; Filing fees $30–$70.

Renters: Max deposit 1.5x rent; Return deadline 30 days.

Injury: 3-year standard deadline (MCL 600.5805).

API Key: Get one free key from Google AI Studio (Gemini 1.5 Flash). 
Store it in a .env file 

Phase 2: The "Anti-Jargon" Logic (Backend)
The System Prompt: Modify the chatbot's system message.

Goal: Tell the AI: "You are a Michigan legal guide. Explain everything like I'm 12. If you say 'Statute of Limitations,' immediately follow it with '(The legal deadline to sue).'"

Context Injection: Write a small Python function that reads your michigan_rules.json and attaches it to every user message before it goes to Gemini.
to make sure the AI always "sees" the $7,000 limit before answering a small claims question.

Phase 3: User Experience & Accessibility (Frontend)
"Quick-Start" Triage Buttons: Add four big buttons above the chat input:

"Small Business Grants"

"Small Claims ($7k (legal limit under michigan legeslative laws))"

"Renter/Landlord Rights"

"Injury/Accident Help"

The "Plain English" Toggle: (Optional fun feature) Add a toggle switch that says "Explain it simpler" which changes the AI's temperature or prompt.

Phase 4: The Michigan "Action" Links
The SCAO Link Bank: Create a dictionary of links to official Michigan State Court Administrative Office (SCAO) PDFs.

Example: If the user is a renter, the bot should provide a direct link to Form DC 102a (Complaint, Nonpayment of Rent).

Detroit/Local Resources: Add a section for local help like the Detroit Neighborhood Entrepreneurs Project (DNEP) for the small business feature.

Phase 5: Final Polish & possibly Deployment
Bug Bash: Have the bot by asking it for legal advice outside of Michigan. Ensure the bot says: "I only know Michigan law!"

Connect your GitHub.
