"""
Populate MongoDB with legal knowledge base for Michigan legal topics.
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

print("Starting population script...")

load_dotenv()

try:
    client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=30000, connectTimeoutMS=30000)
    print("✓ MongoDB connection successful")
    
    db = client["hackathonDB"]
    legal_knowledge = db["legal_knowledge"]
    
    # Clear existing data
    legal_knowledge.delete_many({})
    
    # Legal knowledge base
    legal_data = [
        {
            "category": "renters_rights",
            "title": "Renter's Rights",
            "description": "Know your rights as a tenant in Michigan",
            "quick_facts": [
                "Security deposit cannot exceed 1.5x monthly rent",
                "Deposits must be returned within 30 days of move-out",
                "Landlord must provide itemized list of deductions"
            ],
            "subtopics": [
                {"name": "Security Deposits", "plain_english": "Your landlord can hold money from when you move in to cover damages. By law, they can ask for no more than 1.5 times your monthly rent. They have 30 days to give it back after you move out.", "legal_details": "MCL 554.601 requires landlords to return deposits within 30 days or provide itemized deductions.", "icon": "🏠"},
                {"name": "Eviction Process", "plain_english": "Your landlord must follow specific steps to evict you. They cannot lock you out or remove your belongings.", "legal_details": "Michigan requires 30-day notice for no-cause eviction.", "icon": "⚔️"},
                {"name": "Lease Disputes", "plain_english": "Disagreements about what's in your lease agreement. Make sure to read before signing and understand all terms.", "legal_details": "Leases must comply with Michigan Residential Tenancy Act.", "icon": "📋"},
                {"name": "Repairs & Habitability", "plain_english": "Your landlord must keep the place safe and livable. They must fix major problems like broken heat, plumbing, or structural issues.", "legal_details": "Landlord has duty to maintain premises in habitable condition.", "icon": "🔧"},
                {"name": "Tenant Screening & Discrimination", "plain_english": "Landlords cannot discriminate based on protected characteristics. Fair Housing Act protects against housing discrimination.", "legal_details": "Fair Housing Act prohibits discrimination based on race, color, religion, sex, national origin, disability, familial status.", "icon": "⚖️"}
            ]
        },
        {
            "category": "small_claims",
            "title": "Small Claims Court",
            "description": "Resolve disputes over money without hiring a lawyer",
            "quick_facts": [
                "Maximum claim: $7,500",
                "No lawyers allowed",
                "Fast process (usually 2-4 months)"
            ],
            "subtopics": [
                {"name": "When You Can Sue", "plain_english": "Small claims court is for disagreements about money amounts up to $7,500.", "legal_details": "MCL 600.8401 governs small claims. District Court handles cases.", "icon": "⚖️"},
                {"name": "Filing Your Claim", "plain_english": "You file paperwork at the District Court where the dispute happened.", "legal_details": "File complaint with District Court. Include defendant's name, address, and detailed claim description.", "icon": "📝"},
                {"name": "Small Claims Process", "plain_english": "After filing, the other person is notified. You both go to court, present your case, and the judge decides.", "legal_details": "Trial usually 30-60 days later. Informal proceeding with judge or magistrate.", "icon": "🏛️"},
                {"name": "Evidence & Documentation", "plain_english": "Bring receipts, contracts, emails, photos, and any proof of the money dispute.", "legal_details": "Rules of evidence are simplified in small claims. Documents, witness testimony, and photographs admissible.", "icon": "📸"},
                {"name": "After the Judgment", "plain_english": "If you win, you get a judgment. Then you need to collect the money.", "legal_details": "Judgment is enforceable for 10 years. Can use wage garnishment or property execution.", "icon": "💰"}
            ]
        },
        {
            "category": "personal_injury",
            "title": "Personal Injury Law",
            "description": "Get compensation for accidents or injuries caused by someone else",
            "quick_facts": [
                "Standard statute of limitations: 3 years",
                "Medical malpractice: 2 years",
                "Mini-tort limit for property damage: $3,000"
            ],
            "subtopics": [
                {"name": "Accident Claims", "plain_english": "If you're injured in an accident due to someone else's carelessness, you may be able to sue for compensation.", "legal_details": "Michigan is a no-fault auto insurance state. Can still sue for non-economic damages if threshold met.", "icon": "🚗"},
                {"name": "Medical Malpractice", "plain_english": "When a doctor or hospital causes injury through negligence or failure to follow proper care standards.", "legal_details": "Requires expert testimony. Statute of limitations 2 years, or 1 year of discovery.", "icon": "🏥"},
                {"name": "Insurance & Recovery", "plain_english": "Understanding your insurance options and what compensation you can receive for your injuries.", "legal_details": "No-fault benefits cover medical, rehabilitation, and lost wages up to policy limits.", "icon": "🛡️"},
                {"name": "Property Damage", "plain_english": "Recovering money for damage to your car, home, or other property caused by someone else.", "legal_details": "Mini-tort threshold allows small claims up to $3,000 without lawsuit.", "icon": "🏠"},
                {"name": "Liability & Negligence", "plain_english": "Understanding when someone is legally responsible for your injuries and how courts calculate fault.", "legal_details": "Pure comparative negligence: your recovery reduced by your percentage of fault.", "icon": "⚖️"}
            ]
        },
        {
            "category": "small_business",
            "title": "Small Business Law",
            "description": "Legal guidance for starting and running a business in Michigan",
            "quick_facts": [
                "Business registration required with state",
                "Sales tax collection required (6%)",
                "Employment law compliance mandatory"
            ],
            "subtopics": [
                {"name": "Business Registration & Licensing", "plain_english": "You need to register your business name with the state before operating.", "legal_details": "DBA registration required if using name other than legal name.", "icon": "📋"},
                {"name": "Business Structure (LLC, Corp, Sole Prop)", "plain_english": "Choose how your business is organized legally. Options include sole proprietorship, LLC, corporation, and partnership.", "legal_details": "Each structure has different tax and liability implications.", "icon": "🏢"},
                {"name": "Employment & Labor Law", "plain_english": "Rules you must follow when hiring employees: minimum wage, overtime, taxes, and anti-discrimination laws.", "legal_details": "Michigan minimum wage currently $10.33/hr. Must pay overtime, withhold taxes.", "icon": "👥"},
                {"name": "Contracts & Agreements", "plain_english": "Putting agreements in writing protects you and your business partners, customers, and suppliers.", "legal_details": "Contracts must have offer, acceptance, consideration, and legal purpose.", "icon": "✍️"},
                {"name": "Taxes & Financial Compliance", "plain_english": "Track income and expenses, collect sales tax, pay quarterly taxes, and maintain business records for 7 years.", "legal_details": "6% Michigan sales tax, federal income tax, self-employment tax if sole prop/partnership.", "icon": "💼"}
            ]
        }
    ]

    # Insert data
    legal_knowledge.insert_many(legal_data)
    print(f"✓ Successfully populated {len(legal_data)} categories")
    
    client.close()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
