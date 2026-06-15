# Nonprofit Grant Writing Assistant

An AI-powered tool that helps nonprofits find grants they qualify for
and generate complete grant proposal drafts — in minutes, not weeks.

Built with Anthropic's Claude API.
Read the full impact statement: IMPACT.md

---

## The problem

Small nonprofits do essential work with insufficient resources. They often
cannot afford professional grant writers, so they apply to fewer grants,
win less funding, and serve fewer people — not because their mission isn't
worthy, but because they lack capacity.

This tool gives any nonprofit with a laptop access to:
  1. Personalized grant matching with reasoning
  2. Complete 10-section grant proposal drafts

---

## Features

GRANT MATCHING
  - Describe your organization in plain language
  - The tool analyzes 24 real grant programs across 8 focus areas
  - Returns your top 5 matches with fit scores and reasoning
  - Flags eligibility concerns before you invest hours applying

PROPOSAL DRAFTING
  - Answer questions about your program and the grant
  - Receive a complete structured draft covering all 10 standard sections:
      Executive Summary, Organization Background, Statement of Need,
      Program Description, Implementation Plan, Evaluation Plan,
      Organizational Capacity, Budget Narrative, Sustainability Plan,
      and Conclusion
  - Draft is saved to grant_proposal_draft.txt for editing

DO BOTH
  - Match grants first, then immediately draft a proposal
  - Full workflow in one session

---

## Grant database covers

  - Humanitarian and refugee services
  - Education and youth development
  - Food security and basic needs
  - Health and mental health
  - Workforce development and economic empowerment
  - Immigrant and minority communities
  - Arts, culture, and community
  - Environment and sustainability

---

## Setup

Requirements: Python 3.9 or higher, Anthropic API key

  git clone https://github.com/maleechanel/grant-writing-assistant.git
  cd grant-writing-assistant
  pip3 install anthropic
  export ANTHROPIC_API_KEY="sk-ant-your-key-here"
  python3 assistant.py

---

## Sample session

  NONPROFIT GRANT WRITING ASSISTANT
  Powered by Claude AI
  ============================================================
  What would you like to do?

  1. Find grants I qualify for (Grant Matching)
  2. Draft a grant proposal (Proposal Drafting)
  3. Do both — match grants, then draft a proposal

  Enter 1, 2, or 3: 3

  STEP 1: Tell us about your organization

  Organization name: Bridges Community Center
  Mission: We provide ESL classes, job training, and legal aid
  to newly arrived immigrants and refugees in Queens, NY.
  Primary focus areas: Immigration, education, workforce development
  Who do you serve: Newly arrived immigrants and refugees
  City and state: Queens, New York
  Annual budget: $180,000
  Funding sought: $45,000

  Analyzing your organization and searching for matching grants...

  TOP GRANT MATCHES:

  1. Dollar General Literacy Foundation (Fit: 9/10)
     Strong match — your ESL programming directly aligns with their
     adult literacy and English language learning focus. Your Queens
     location falls within their service area. Budget size is appropriate.

  2. JPMorgan Chase Workforce Initiative (Fit: 8/10)
     Your job training component aligns well. Chase prioritizes
     immigrant economic mobility. Recommended for your workforce program.

  ...

---

## Important notes for users

This tool generates DRAFTS for human review. Before submitting:

  - Verify all facts and statistics — AI can make errors
  - Personalize the narrative to sound like your organization
  - Check current grant deadlines directly on funder websites
  - Fill in all [INSERT: ...] placeholders with real data
  - Have a human editor review before submission

Read IMPACT.md for a full discussion of responsible use.

---

## Project structure

  grant-writing-assistant/
  |__ assistant.py              Main tool — matching and drafting
  |__ README.md                 This file
  |__ IMPACT.md                 Humanitarian impact statement
  |__ requirements.txt          Dependencies
  |__ grant_proposal_draft.txt  Generated after running the tool

---

## License

MIT — free to use and adapt. If this helps your nonprofit win funding,
that's the whole point.
