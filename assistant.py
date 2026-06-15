#!/usr/bin/env python3
"""
grant-writing-assistant
=======================
An AI-powered tool that helps nonprofits do two things they never have
enough time for:

    1. GRANT MATCHING  — Describe your organization and the tool identifies
                         which grants from a curated database you're most
                         likely to qualify for, with reasoning.

    2. PROPOSAL DRAFTING — Answer a few questions about your program and
                           the tool generates a full, structured grant
                           proposal draft ready for human review and editing.

This tool does not replace a grant writer. It gives small nonprofits —
especially those with no dedicated development staff — a strong first draft
and a clearer picture of where to apply, so they can spend their limited
time on relationship-building and refinement rather than starting from scratch.

Powered by Anthropic's Claude API.

Usage:
    python3 assistant.py

Author: Sumalee Simmonds
GitHub: https://github.com/maleechanel/grant-writing-assistant
"""

import anthropic
import textwrap

# ─── Setup ────────────────────────────────────────────────────────────────────
client = anthropic.Anthropic()
MODEL  = "claude-sonnet-4-6"

# ─── Grant Database ───────────────────────────────────────────────────────────
# A curated list of real, active grant programs across major nonprofit
# focus areas. Used by the grant-matching feature to recommend the best
# funding opportunities for a given organization.
#
# Each entry includes:
#   - Funder name and grant program
#   - Focus areas (what they fund)
#   - Who is eligible
#   - Typical grant size
#   - Deadline pattern
#   - Website

GRANT_DATABASE = """
=== GRANT DATABASE: GENERAL NONPROFIT FUNDING OPPORTUNITIES ===

--- HUMANITARIAN & REFUGEE SERVICES ---

1. Robert Wood Johnson Foundation — Health Equity Grants
   Focus: Health equity, social determinants of health, vulnerable populations
   Eligible: 501(c)(3) nonprofits, community orgs, research institutions
   Amount: $50,000 – $500,000
   Deadlines: Rolling (Letter of Inquiry first)
   Website: https://www.rwjf.org/en/grants.html

2. MacArthur Foundation — Safety and Justice Challenge
   Focus: Criminal justice reform, immigration, refugee resettlement, human rights
   Eligible: Nonprofits with demonstrated community impact
   Amount: $100,000 – $1,000,000
   Deadlines: By invitation / competitive RFP cycles
   Website: https://www.macfound.org/programs/safety-and-justice/

3. United Nations Voluntary Fund for Victims of Torture
   Focus: Rehabilitation of torture survivors, trauma services, refugee support
   Eligible: NGOs providing direct services to torture survivors
   Amount: $50,000 – $300,000
   Deadlines: Annual (typically March)
   Website: https://www.ohchr.org/en/special-procedures/sr-torture/united-nations-voluntary-fund-victims-torture

4. Open Society Foundations — Human Rights Initiative
   Focus: Refugee rights, immigration, civil liberties, racial justice
   Eligible: NGOs and nonprofits globally
   Amount: $50,000 – $500,000
   Deadlines: Rolling
   Website: https://www.opensocietyfoundations.org/grants

--- EDUCATION & YOUTH DEVELOPMENT ---

5. W.K. Kellogg Foundation — Education and Learning
   Focus: Early childhood education, K-12 equity, literacy, youth development
   Eligible: Nonprofits serving vulnerable children and families
   Amount: $100,000 – $1,000,000
   Deadlines: Rolling (pre-proposal required)
   Website: https://www.wkkf.org/grants

6. Bill & Melinda Gates Foundation — U.S. Education
   Focus: College readiness, K-12 learning, educational equity
   Eligible: Nonprofits, schools, educational institutions
   Amount: $100,000 – $5,000,000
   Deadlines: By invitation; unsolicited LOIs accepted in some programs
   Website: https://www.gatesfoundation.org/about/how-we-work/grant-seekers

7. Lumina Foundation — Talent Strong America
   Focus: Postsecondary education, workforce credentials, adult learners
   Eligible: Nonprofits, colleges, advocacy organizations
   Amount: $50,000 – $500,000
   Deadlines: Rolling
   Website: https://www.luminafoundation.org/grants/

8. Dollar General Literacy Foundation
   Focus: Adult literacy, GED/HiSET prep, English language learning (ESL)
   Eligible: Nonprofits providing literacy services in Dollar General market areas
   Amount: Up to $15,000
   Deadlines: Annual (typically March)
   Website: https://www.dgliteracy.org/grant-programs/

--- FOOD SECURITY & BASIC NEEDS ---

9. Feeding America — Member Food Bank Grants
   Focus: Food distribution, hunger relief, nutrition programs
   Eligible: Nonprofits affiliated with or partnering with Feeding America network
   Amount: $10,000 – $100,000
   Deadlines: Varies by program
   Website: https://www.feedingamerica.org/our-work/our-approach/engage-government

10. USDA Community Food Projects Competitive Grant Program
    Focus: Community food systems, food access, food banks, urban agriculture
    Eligible: Private nonprofits, tribal organizations, public food banks
    Amount: Up to $400,000 (over 4 years)
    Deadlines: Annual (typically May)
    Website: https://www.nifa.usda.gov/grants/programs/community-food-projects-competitive-grant-program

11. Walmart Foundation — Community Grants
    Focus: Hunger relief, workforce development, sustainability, community resilience
    Eligible: 501(c)(3) nonprofits in Walmart store communities
    Amount: $250 – $5,000 (local); larger through regional/national programs
    Deadlines: Rolling
    Website: https://walmart.org/how-we-give/local-community-grants

--- HEALTH & MENTAL HEALTH ---

12. Substance Abuse and Mental Health Services Administration (SAMHSA)
    Focus: Mental health services, substance use treatment, crisis intervention
    Eligible: State and local governments, nonprofits, tribal organizations
    Amount: $100,000 – $2,000,000
    Deadlines: Varies by grant program (grants.gov listings)
    Website: https://www.samhsa.gov/grants

13. CVS Health Foundation — Behavioral Health Grants
    Focus: Mental health, substance use disorder, health equity
    Eligible: Nonprofits with demonstrated health programming
    Amount: $10,000 – $100,000
    Deadlines: Annual
    Website: https://cvshealth.com/social-responsibility/our-giving

14. The JPB Foundation — Poverty Program
    Focus: Healthcare access for low-income populations, medical services
    Eligible: Nonprofits serving people in poverty
    Amount: $200,000 – $1,000,000
    Deadlines: By invitation
    Website: https://www.jpbfoundation.org/programs/poverty/

--- WORKFORCE DEVELOPMENT & ECONOMIC EMPOWERMENT ---

15. JPMorgan Chase — Workforce Initiative
    Focus: Job training, skills development, economic mobility, small business
    Eligible: Nonprofits, community colleges, workforce boards
    Amount: $100,000 – $1,000,000
    Deadlines: Rolling (RFP-based cycles)
    Website: https://www.jpmorganchase.com/impact/economic-opportunity

16. Google.org — Economic Opportunity Grants
    Focus: Workforce skills, digital literacy, economic mobility
    Eligible: Nonprofits globally; US focus includes underserved communities
    Amount: $100,000 – $1,000,000
    Deadlines: Rolling; also Google Ad Grants (separate program)
    Website: https://www.google.org/our-work/

17. Walmart Foundation — Workforce Development
    Focus: Skilled job training, workforce readiness, economic self-sufficiency
    Eligible: Nonprofits focused on workforce and job placement
    Amount: $250,000 – $1,000,000
    Deadlines: Annual RFP cycle
    Website: https://walmart.org

--- IMMIGRANT & MINORITY COMMUNITIES ---

18. Marguerite Casey Foundation — Equal Voice
    Focus: Low-income families, immigrant communities, racial equity, advocacy
    Eligible: Community-based nonprofits led by and serving communities of color
    Amount: $100,000 – $500,000
    Deadlines: By invitation (but accepts introductory emails)
    Website: https://caseygrants.org

19. Asian Americans/Pacific Islanders in Philanthropy (AAPIP)
    Focus: AAPI communities, immigrant rights, civic engagement
    Eligible: AAPI-led nonprofits and organizations
    Amount: $5,000 – $50,000
    Deadlines: Annual
    Website: https://www.aapip.org/

20. Hispanic Federation — Community Grants
    Focus: Latino/Hispanic communities, immigration, education, health, civic engagement
    Eligible: Latino nonprofits in the Northeast US
    Amount: $5,000 – $30,000
    Deadlines: Annual
    Website: https://hispanicfederation.org/grants/

--- ARTS, CULTURE & COMMUNITY ---

21. National Endowment for the Arts — Grants for Organizations
    Focus: Arts programming, cultural access, community arts
    Eligible: Nonprofits, schools, government agencies with arts programs
    Amount: $10,000 – $100,000
    Deadlines: Annual (February and July cycles)
    Website: https://www.arts.gov/grants/grants-organizations

22. Bloomberg Philanthropies — Arts Program
    Focus: Arts and cultural organizations, community engagement through arts
    Eligible: Arts nonprofits in Bloomberg-priority cities
    Amount: $100,000 – $1,000,000
    Deadlines: By invitation
    Website: https://www.bloomberg.org/public-affairs/arts/

--- ENVIRONMENT & SUSTAINABILITY ---

23. EPA Environmental Justice Collaborative Problem-Solving Grant
    Focus: Environmental justice, underserved community sustainability
    Eligible: Nonprofits in communities overburdened by pollution
    Amount: Up to $1,000,000
    Deadlines: Annual
    Website: https://www.epa.gov/environmentaljustice/environmental-justice-collaborative-problem-solving-cooperative-agreement

24. 11th Hour Project
    Focus: Food systems, environment, marine conservation
    Eligible: Nonprofits working on sustainable food and environment
    Amount: $50,000 – $500,000
    Deadlines: Rolling
    Website: https://www.11thhourproject.org/grants/
"""

# ─── Proposal Template Structure ──────────────────────────────────────────────
# Standard sections found in most foundation and government grant proposals.
# Claude uses this structure to ensure the draft covers all expected components.

PROPOSAL_SECTIONS = [
    "Executive Summary",
    "Organization Background",
    "Statement of Need",
    "Program Description and Goals",
    "Implementation Plan and Timeline",
    "Evaluation Plan",
    "Organizational Capacity",
    "Budget Narrative",
    "Sustainability Plan",
    "Conclusion",
]


# ─── Feature 1: Grant Matching ─────────────────────────────────────────────────

def match_grants(org_info: dict) -> None:
    """
    Analyze a nonprofit's profile and recommend the best-fit grants
    from the database, with reasoning for each recommendation.

    Uses Claude to read the nonprofit's focus area, population served,
    location, and budget size, then cross-references against the grant
    database to identify the strongest matches.

    Args:
        org_info (dict): Dictionary containing:
            - name        (str): Organization name
            - mission     (str): Mission statement
            - focus_areas (str): Primary program areas
            - population  (str): Who they serve
            - location    (str): City/state
            - annual_budget (str): Approximate annual budget
            - program_budget (str): Budget for the program seeking funding
    """
    print("\n  Analyzing your organization and searching for matching grants...")
    print("  This may take 15–20 seconds...\n")

    matching_prompt = f"""You are an expert nonprofit grant consultant with 20 years of experience
matching organizations to funding opportunities.

A nonprofit has provided the following information about their organization:

Organization Name: {org_info['name']}
Mission: {org_info['mission']}
Primary Focus Areas: {org_info['focus_areas']}
Population Served: {org_info['population']}
Location: {org_info['location']}
Annual Organizational Budget: {org_info['annual_budget']}
Budget for Program Seeking Funding: {org_info['program_budget']}

Below is a database of grant opportunities. Your job is to:
1. Identify the TOP 5 best-fit grants for this organization
2. For each grant, explain specifically WHY it's a good match (2-3 sentences)
3. Flag any eligibility concerns to be aware of
4. Give each match a fit score from 1-10

Format your response clearly with each grant numbered and well-organized.
Be specific — reference actual details from both the org profile and the grant description.

GRANT DATABASE:
{GRANT_DATABASE}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": matching_prompt}],
    )

    print("=" * 60)
    print("  TOP GRANT MATCHES FOR YOUR ORGANIZATION")
    print("=" * 60)
    print(textwrap.fill(response.content[0].text, width=70,
                        subsequent_indent="  "))
    print()


# ─── Feature 2: Proposal Drafting ─────────────────────────────────────────────

def draft_proposal(org_info: dict, grant_info: dict) -> str:
    """
    Generate a complete, structured grant proposal draft tailored to
    a specific organization and grant opportunity.

    The draft follows standard grant proposal structure and is written
    in professional nonprofit development language. It is designed to be
    a strong starting point for human review, editing, and personalization
    — not a final submission.

    Args:
        org_info  (dict): Organization profile (same as match_grants).
        grant_info (dict): Dictionary containing:
            - funder_name  (str): Name of the foundation/agency
            - grant_name   (str): Name of the grant program
            - grant_amount (str): Amount being requested
            - grant_focus  (str): What this grant funds
            - deadline     (str): Submission deadline

    Returns:
        str: The full proposal draft as a formatted string.
    """
    sections_list = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(PROPOSAL_SECTIONS))

    drafting_prompt = f"""You are a professional nonprofit grant writer with expertise in
writing compelling, fundable proposals for foundations and government agencies.

Write a complete, professional grant proposal draft based on the following information.

ORGANIZATION PROFILE:
  Name: {org_info['name']}
  Mission: {org_info['mission']}
  Focus Areas: {org_info['focus_areas']}
  Population Served: {org_info['population']}
  Location: {org_info['location']}
  Annual Budget: {org_info['annual_budget']}

GRANT BEING APPLIED FOR:
  Funder: {grant_info['funder_name']}
  Grant Program: {grant_info['grant_name']}
  Amount Requested: {grant_info['grant_amount']}
  Grant Focus: {grant_info['grant_focus']}
  Deadline: {grant_info['deadline']}

PROGRAM DETAILS:
  Program Name: {grant_info.get('program_name', 'To be specified')}
  Program Description: {grant_info.get('program_description', 'To be specified')}
  Number of People Served: {grant_info.get('people_served', 'To be specified')}
  Key Outcomes: {grant_info.get('outcomes', 'To be specified')}

Write the full proposal covering these sections:
{sections_list}

Guidelines:
- Write in a professional but warm, human voice
- Be specific — use the organization's actual details throughout
- Where you don't have specific data, write [INSERT: specific statistic or detail here]
  so the grant writer knows exactly what to add
- Make the Statement of Need emotionally compelling and data-driven
- The Budget Narrative should reference the grant amount and explain how it will be used
- Length: approximately 1,500-2,000 words total
- This is a DRAFT for human review — write a note at the top reminding the user to
  review, personalize, and verify all facts before submission

Begin the proposal now."""

    print("\n  Drafting your grant proposal...")
    print("  This may take 20–30 seconds...\n")

    response = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": drafting_prompt}],
    )

    return response.content[0].text


# ─── Input Helpers ─────────────────────────────────────────────────────────────

def get_org_info() -> dict:
    """
    Interactively collect basic information about the nonprofit
    through a series of simple prompts.

    Returns:
        dict: Organization profile with keys: name, mission, focus_areas,
              population, location, annual_budget, program_budget.
    """
    print("\n" + "=" * 60)
    print("  STEP 1: Tell us about your organization")
    print("=" * 60)
    print("  Answer each question as best you can.")
    print("  You can be brief — a sentence or two is fine.\n")

    return {
        "name":           input("  Organization name: ").strip(),
        "mission":        input("  Mission statement (what do you do and who do you serve?): ").strip(),
        "focus_areas":    input("  Primary focus areas (e.g. education, housing, food, health): ").strip(),
        "population":     input("  Who do you serve? (e.g. refugees, youth, low-income families): ").strip(),
        "location":       input("  City and state: ").strip(),
        "annual_budget":  input("  Approximate annual organizational budget (e.g. $250,000): ").strip(),
        "program_budget": input("  How much funding are you seeking for this program? (e.g. $50,000): ").strip(),
    }


def get_grant_info() -> dict:
    """
    Collect information about the specific grant being applied for
    and the program it will fund.

    Returns:
        dict: Grant and program details with keys: funder_name, grant_name,
              grant_amount, grant_focus, deadline, program_name,
              program_description, people_served, outcomes.
    """
    print("\n" + "=" * 60)
    print("  STEP 2: Tell us about the grant and your program")
    print("=" * 60)
    print("  If you used the grant matching feature, pick one of")
    print("  the recommended grants and enter its details here.\n")

    return {
        "funder_name":          input("  Funder name (e.g. W.K. Kellogg Foundation): ").strip(),
        "grant_name":           input("  Grant program name: ").strip(),
        "grant_amount":         input("  Amount you are requesting: ").strip(),
        "grant_focus":          input("  What does this grant fund? (brief description): ").strip(),
        "deadline":             input("  Submission deadline (or 'rolling'): ").strip(),
        "program_name":         input("  Name of the program you're seeking funding for: ").strip(),
        "program_description":  input("  Describe the program (2-3 sentences): ").strip(),
        "people_served":        input("  How many people will this program serve?: ").strip(),
        "outcomes":             input("  What are the 2-3 main outcomes or results you expect?: ").strip(),
    }


# ─── Main Menu ─────────────────────────────────────────────────────────────────

def main() -> None:
    """
    Display the main menu and route the user to the grant matching
    or proposal drafting features based on their selection.

    The tool can run both features in sequence — match first,
    then draft a proposal for the best match.
    """
    print("\n" + "=" * 60)
    print("  NONPROFIT GRANT WRITING ASSISTANT")
    print("  Powered by Claude AI")
    print("=" * 60)
    print("  Helping nonprofits find funding and write stronger proposals.")
    print()
    print("  What would you like to do?")
    print()
    print("  1. Find grants I qualify for (Grant Matching)")
    print("  2. Draft a grant proposal (Proposal Drafting)")
    print("  3. Do both — match grants, then draft a proposal")
    print()

    choice = input("  Enter 1, 2, or 3: ").strip()

    if choice == "1":
        org_info = get_org_info()
        match_grants(org_info)

    elif choice == "2":
        org_info  = get_org_info()
        grant_info = get_grant_info()
        proposal  = draft_proposal(org_info, grant_info)

        # Save the proposal to a file
        output_file = "grant_proposal_draft.txt"
        with open(output_file, "w") as f:
            f.write(proposal)

        print("=" * 60)
        print("  GRANT PROPOSAL DRAFT")
        print("=" * 60)
        print(proposal)
        print(f"\n  Draft saved to: {output_file}")
        print("  Review carefully before submitting. Add specific data")
        print("  and statistics where marked [INSERT: ...].\n")

    elif choice == "3":
        org_info = get_org_info()
        match_grants(org_info)

        print("\n" + "=" * 60)
        print("  Now let's draft your proposal.")
        print("  Use one of the matched grants above.")
        print("=" * 60)

        grant_info = get_grant_info()
        proposal   = draft_proposal(org_info, grant_info)

        output_file = "grant_proposal_draft.txt"
        with open(output_file, "w") as f:
            f.write(proposal)

        print("=" * 60)
        print("  GRANT PROPOSAL DRAFT")
        print("=" * 60)
        print(proposal)
        print(f"\n  Draft saved to: {output_file}")
        print("  Review carefully before submitting. Add specific data")
        print("  and statistics where marked [INSERT: ...].\n")

    else:
        print("\n  Please enter 1, 2, or 3.")
        main()


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
