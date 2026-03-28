from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["hackathonDB"]

# Clear existing data
db.legal_topics.delete_many({})

# Insert legal information for our 4 sections
legal_data = [
    {
        "id": "small_business",
        "title": "Small Business",
        "description": "Legal requirements for operating a business in Michigan",
        "content": "Starting and operating a small business in Michigan requires understanding state and federal laws. This section covers the essential legal information you need to know.",
        "subtopics": [
            {
                "title": "Business Licenses & Registration",
                "content": "In Michigan, you need to register your business name with the state. If using a name other than your own, file it as a DBA (Doing Business As) with your county clerk. Depending on your business type, you may need specific licenses from the state or local health departments."
            },
            {
                "title": "Employment Law",
                "content": "Michigan employers must follow federal and state employment laws. You must pay at least Michigan's minimum wage, keep records of hours worked, and follow tax withholding requirements. You also cannot discriminate based on race, gender, age, disability, or religion."
            },
            {
                "title": "Contracts & Agreements",
                "content": "Contracts protect both you and your customers or suppliers. A good contract should clearly state the services or products being provided, payment terms, delivery dates, and what happens if someone doesn't fulfill their obligations. Get contracts in writing when possible."
            },
            {
                "title": "Taxes & Record Keeping",
                "content": "Businesses must keep records of income and expenses for tax purposes. Michigan has a sales tax (6%) and businesses must collect it from customers. You'll also need an EIN (Employer Identification Number) from the IRS if you have employees or operate as an LLC or corporation."
            },
            {
                "title": "Insurance & Liability",
                "content": "Most small businesses need liability insurance to protect against lawsuits. If you have employees, you need workers' compensation insurance. Depending on your business type, you may also need property insurance, professional liability insurance, or vehicle insurance."
            }
        ]
    },
    {
        "id": "small_claims",
        "title": "Small Claims",
        "description": "How to file a small claims case and recover money owed to you",
        "content": "Small claims court is designed to help people resolve disputes over money without expensive lawyers. In Michigan, you can sue for amounts up to $6,500 (or $7,500 if both people agree).",
        "subtopics": [
            {
                "title": "When You Can File Small Claims",
                "content": "You can use small claims court when someone owes you money and won't pay. This includes unpaid debts, broken contracts where money is owed, security deposits not returned, or property damage. You must file in the county where the person being sued lives or where the problem happened."
            },
            {
                "title": "How to File Your Case",
                "content": "Go to your district court and explain your case to a clerk. They'll help you fill out the paperwork. You'll need the other person's name and address. There's a filing fee (usually $50-100) and you must serve them with papers telling them about the lawsuit. You have several ways to serve them, including by mail or having a sheriff do it."
            },
            {
                "title": "Preparing Your Evidence",
                "content": "Bring proof of what happened and what you're owed. This could be written contracts, texts, emails, photos of damage, receipts, or invoices. Write down the dates and amounts clearly. If people saw what happened, they can come testify (tell the judge what they saw). Organize everything before court so it's easy to explain."
            },
            {
                "title": "The Court Hearing",
                "content": "Tell the judge your side of the story clearly and calmly. Show your evidence. The other person gets to tell their side too. After hearing both sides, the judge decides who wins. The whole process usually takes 5-10 minutes per person. You don't need a lawyer, but you can bring one if you want."
            },
            {
                "title": "After the Judge Decides",
                "content": "If you win, the judge orders the other person to pay you (called a judgment). You then have to collect the money. If they don't pay, you can place a lien on their property or ask the court to help you collect. If you lose, you have limited options to appeal."
            }
        ]
    },
    {
        "id": "renters_rights",
        "title": "Renter's Rights",
        "description": "Know your rights as a tenant in Michigan",
        "content": "Michigan law protects tenants' rights and sets duties for both tenants and landlords. Understanding these laws helps protect you from unfair treatment.",
        "subtopics": [
            {
                "title": "Security Deposits",
                "content": "Landlords can ask for a security deposit (usually 1 month's rent). The landlord must put it in a separate account and return it within 30 days after you move out, minus deductions for damages beyond normal wear and tear. The landlord must give you an itemized list of any deductions. If they don't return your deposit, you can sue them."
            },
            {
                "title": "Repairs & Maintenance",
                "content": "Your landlord must keep the rental in good condition and fix major problems like broken heating, plumbing, electrical, or roof leaks. Tell your landlord about problems in writing (email or letter works). If they don't fix serious problems in a reasonable time, you may have the right to withhold rent or fix it yourself and deduct the cost."
            },
            {
                "title": "Your Right to Privacy",
                "content": "Your landlord cannot enter your home without permission except in emergencies (fire, gas leak). For non-emergencies, they must give you written notice to enter, usually 24 hours ahead of time. They can only enter during reasonable hours and for legitimate reasons like repairs or showing the apartment to new renters."
            },
            {
                "title": "Eviction & Your Lease",
                "content": "A landlord cannot evict you without a reason and a court order. Valid reasons include not paying rent, breaking the lease terms, or the lease ending. They must give you written notice and file in court. The eviction process takes at least 2-4 weeks. You have the right to appear in court and tell your side."
            },
            {
                "title": "Discrimination",
                "content": "Landlords cannot discriminate against you because of race, color, religion, national origin, gender, disability, or familial status. This includes refusing to rent, charging more rent, or treating you unfairly. If you believe you've been discriminated against, you can file a complaint with the Michigan Department of Civil Rights."
            }
        ]
    },
    {
        "id": "personal_injury",
        "title": "Personal Injury",
        "description": "Get guidance on accidents and injury claims",
        "content": "If you're injured in an accident caused by someone else's carelessness, you may have the right to recover money for your injuries and losses. Here's what you need to know.",
        "subtopics": [
            {
                "title": "Car Accidents",
                "content": "After a car accident, get emergency help if needed. Exchange information with the other driver (name, phone, insurance, license plate). Take photos of the damage and get witness contact information. Report it to your insurance company and the police if there's significant damage. Keep records of medical visits and car repair bills."
            },
            {
                "title": "Proving Fault & Negligence",
                "content": "To win an injury case, you must prove the other person was careless (negligent) and that carelessness caused your injury. Negligence means they breached a duty they owed you (like driving safely), causing damage. Evidence can include police reports, witness statements, photos, medical records, and expert opinions about how the accident happened."
            },
            {
                "title": "Medical Treatment & Documentation",
                "content": "Seek medical treatment right away, even for small injuries, because some injuries show up later. Keep detailed records of all doctor visits, medications, medical tests, and treatment. Save all medical bills. These records prove your injury and how serious it was. Take photos of visible injuries as they heal."
            },
            {
                "title": "Slip & Fall Injuries",
                "content": "Property owners must keep their property safe for visitors. If you slip and fall because of a hazard (wet floor, broken stairs, poor lighting), you may have a claim. You must prove the owner knew (or should have known) about the danger and didn't fix it. This is harder to prove than car accidents, so documentation is critical."
            },
            {
                "title": "Workplace Injuries & Workers' Compensation",
                "content": "If injured at work, you may be entitled to workers' compensation benefits to cover medical care and lost wages. Report the injury to your employer immediately. You don't need to prove fault - but you do need to show the injury happened at work. If your employer denies the claim, you can appeal or contact a workers' comp attorney."
            }
        ]
    }
]

db.legal_topics.insert_many(legal_data)
print(f"Database populated with {len(legal_data)} topics!")
