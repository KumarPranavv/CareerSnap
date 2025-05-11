import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume(text: str) -> str:
    prompt = f"""
You are an expert career coach. Below is a candidate’s resume or LinkedIn profile:
---
{text}
---
1. Propose a punchy LinkedIn headline.
2. List 10 high-impact keywords to boost discoverability.
3. Recommend top skills in demand for their profile.
4. Generate a personalized Gen AI–powered cover letter for a tech role.

Respond in markdown with clear headings.
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800,
    )
    return resp.choices[0].message.content

def get_ats_score(text: str) -> str:
    prompt = f"""
You are an ATS specialist. Given the resume text below, do the following:
1. Analyse the Resume text, Provide an accurate integer ATS score from 0 to 100.
2. Under "ATS Improvement Tips:", list actionable bullet points.
Respond in markdown in this format:

ATS Score: <number>
**ATS Improvement Tips:
- tip 1
- tip 2
- tip 3

---
{text}
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=400,
    )
    return resp.choices[0].message.content

def get_skill_gap(text: str, role: str) -> str:
    prompt = f"""
You are a career strategist. Given the resume text below and the target role "{role}", do:
1. Identify the top 3 skills required for this role that are missing from the resume.
2. For each missing skill, suggest 1–2 leading online courses or resources.
3. Recommend one industry-recognized certification per skill (e.g., AWS Certified Data Analytics Specialty, PMP, CISSP).
Respond in markdown under "## Skill Gap Analysis".
---
Role: {role}

Resume Text:
{text}
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        # bumped up from 400 to 600
        max_tokens=700,
    )
    return resp.choices[0].message.content

def analyze_linkedin_profile(text: str) -> str:
    prompt = f"""
You are an expert LinkedIn coach. Below is a user’s LinkedIn export:
---
{text}
---
1. Suggest an optimized LinkedIn headline.
2. Propose improvements to the “About” / summary section.
3. List 10 SEO keywords to add to their profile.
4. Recommend 3 networking actions (e.g., types of posts, groups to join).
Respond in markdown with clear headings.
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7,
        max_tokens=600,
    )
    return resp.choices[0].message.content

def generate_resume_templates(text: str, role: str) -> dict:
    prompt = f"""
You are a resume template expert. Generate **two distinct ATS-friendly resume templates** in markdown, using headings:
## Template 1
...markdown...
## Template 2
...markdown...

Include placeholders for:
- Name
- Contact
- Summary
- Experience
- Education
- Skills
- Projects

Do **not** return JSON—just the markdown with those two sections.
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000,
    )
    content = resp.choices[0].message.content
    parts = content.split("## Template 2")
    if len(parts) == 2:
        return {
            "Template 1": parts[0].strip(),
            "Template 2": "## Template 2" + parts[1].strip()
        }
    return {"Template 1": content.strip()}

def get_career_projection(text: str, role: str) -> str:
    prompt = f"""
You are a forward‐looking career advisor. Given the candidate’s resume or LinkedIn text below:
---
Role: {role}
{text}
---
1. Analyze their current career trajectory.
2. Suggest future-focused skills they should develop over the next 3–5 years.
3. Recommend strategic career moves based on market trends.
4. Identify emerging skills in their field to watch and learn.
Respond in markdown under "## Temporal Career Projection".
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )
    return resp.choices[0].message.content