import pandas as pd
from database import Session, Lead, engine
from scraper import search_leads
from processor import verify_lead_email, categorize_lead

def run_project():
    session = Session()
    print("🚀 Project Started...")

    # TRY MULTIPLE COMPANIES TO ENSURE DATA FLOW
    target_companies = ["Google", "Microsoft", "Amazon"]
    target_role = "Sales Manager"

    all_found = []
    for co in target_companies:
        print(f"🔍 Searching for leads at {co}...")
        results = search_leads(target_role, co)
        all_found.extend(results)

    if not all_found:
        print("⚠️ NO LEADS FOUND. Check your browser/internet connection.")
        return

    print(f"📂 Found {len(all_found)} potential leads. Saving to database...")

    for item in all_found:
        # Create a dummy email for testing purposes
        clean_name = "Contact"
        test_email = f"info@{item['company'].lower().replace(' ', '')}.com"
        
        v_email = verify_lead_email(test_email)
        category = categorize_lead(target_role)

        new_lead = Lead(
            name=clean_name, 
            job_title=target_role, 
            company=item['company'], 
            email=test_email, # Using test_email directly for now
            status=category
        )

        try:
            session.add(new_lead)
            session.commit()
            print(f"✅ Successfully saved: {item['company']}")
        except Exception as e:
            session.rollback()
            print(f"⏩ Skipped/Error: {item['company']}")

    # 3. Force CSV Update
    df = pd.read_sql("SELECT * FROM leads", engine)
    df.to_csv("reports/weekly_research_report.csv", index=False)
    print(f"\n📊 Report Updated! Rows in CSV: {len(df)}")

if __name__ == "__main__":
    run_project()