import pandas as pd
import os
from sqlalchemy.exc import IntegrityError
from database import Session, Lead, engine, setup_database
from scraper import search_leads
from processor import verify_lead_email, categorize_lead
from notifier import send_report

def run_project():
    # --- DATABASE SETUP ---
    # Ensures the database schema is created before any operations.
    setup_database()

    session = Session()
    print("🚀 Project Started...")

    # --- CONFIGURATION ---
    report_recipient = "your_recipient_email@example.com" # Email to send the final report

    # TRY MULTIPLE COMPANIES TO ENSURE DATA FLOW
    target_companies = ["Google", "Microsoft", "Amazon"]
    target_role = "Sales Manager"

    all_found = []
    for co in target_companies:
        print(f"🔍 Searching for leads at {co}...")
        results = search_leads(target_role, co) # This now returns a list of dicts
        if results:
            print(f"    ✅ Found {len(results)} leads for {co}.")
            all_found.extend(results)
        else:
            print(f"    ⚠️ No leads found for {co}.")

    if not all_found:
        print("⚠️ NO LEADS FOUND. Check your browser/internet connection.")
        return

    print(f"📂 Found {len(all_found)} potential leads. Saving to database...")

    for item in all_found:
        # Extract a unique identifier from the LinkedIn profile URL to create mock data
        try:
            profile_slug = item['url'].split('/in/')[1].split('?')[0].strip('/')
            if not profile_slug:
                continue # Skip if slug is empty after parsing
            clean_name = profile_slug.replace('-', ' ').replace('.', ' ').title()
            # Create a unique, syntactically valid email from the slug
            test_email = f"{profile_slug.replace('-', '.')}@{item['company'].lower().replace(' ', '')}.com"
        except IndexError:
            print(f"⚠️ Could not parse profile from URL: {item['url']}. Skipping.")
            continue

        v_email = verify_lead_email(test_email)
        if not v_email:
            # This case should be rare given the email generation logic, but it's good practice
            print(f"⏩ Skipped/Error: Could not validate generated email for {clean_name}")
            continue

        category = categorize_lead(target_role)

        new_lead = Lead(
            name=clean_name, 
            job_title=target_role, 
            company=item['company'], 
            email=v_email,
            linkedin_url=item['url'], # Save the source LinkedIn URL
            status=category
        )

        try:
            session.add(new_lead)
            session.commit()
            print(f"✅ Successfully saved: {clean_name} at {item['company']}")
        except IntegrityError:
            session.rollback()
            print(f"⏩ Skipped: Lead likely already exists in database (email or URL).")
        except Exception as e:
            session.rollback()
            print(f"⏩ Skipped/Error saving {clean_name}: {e}")

    # 3. Force CSV Update
    report_dir = "reports"
    report_path = os.path.join(report_dir, "weekly_research_report.csv")
    os.makedirs(report_dir, exist_ok=True) # Ensure the 'reports' directory exists

    df = pd.read_sql("SELECT * FROM leads", engine)
    df.to_csv(report_path, index=False)
    print(f"\n📊 Report Updated! Rows in CSV: {len(df)}")

    # 4. Send Notification
    if not df.empty and report_recipient != "your_recipient_email@example.com":
        send_report(report_recipient, report_path)

if __name__ == "__main__":
    run_project()
