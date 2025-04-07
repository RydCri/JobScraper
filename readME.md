## JobScraper & Analyzer

This repo provides a toolset for scraping job listings from various job boards, analyzing their content, and extracting valuable insights for jobseekers. 
The repo is setup to extract job data like skills, accessibility, sentiment, popular interview using tools and more.

### Setup
         python -m venv <your_environment_name>
         pip install -r requirements.txt

### Features:
Scraping: Collect job listings from sites like LinkedIn, Indeed and Greenhouse and save as .csv files.
(Located in ./scraper.py)

Analysis: Process job descriptions using spaCy to extract key skills, accessibility keywords, interview prep indicators, sentiment, and named entities.
(Located in ./spacy_nre_analyzer.py)

Demo Notebook: A Jupyter notebook showcasing an example dataframe obtained from scraping, followed by dataframe processing using the analysis functions.
(Located in ./juypter_notebooks/dataframe_notes.ipynb)

### What You Can Do:
Scrape Job Listings: Use scraper.py to gather data from popular job boards based on keywords, locations and job titles.
You can modify these query links however the job board will allow you to.

Analyze Job Data: Use spacy_nre_analyzer.py to process the scraped job data and extract useful insights like sentiment, skills, and job accessibility.

<h3 style="color:orange;">Add your own keywords: in spacey_nre_analyzer.py there are variables containing lists of desired keywords</h3> 

      skills_keywords = [
       # Web Development
       'react', 'angular', 'vue.js', 'svelte', 'ember.js', 'backbone.js', 'litElement',
       'node.js', 'express', 'django', 'flask', 'ruby on rails', 'spring', 'laravel', 'asp.net', 'fastapi',
       'javascript', 'typescript', 'html', 'css', 'python', 'ruby', 'php', 'java', 'c#', 'go', 'kotlin', 'swift', 'rust',
       'bootstrap', 'tailwind css', 'bulma', 'material ui', 'foundation', 'sass', 'less',
       'jquery', 'webpack', 'babel', 'gulp', 'grunt', 'nginx', 'apache', 'varnish', '...' ]

Modify these however you want for your job queries


Explore Example: Open dataframe_notes.ipynb to see an end-to-end example of scraping and analysis, including data preprocessing and output generation.

This project is ideal for jobseekers who'd like more tools to explore job market trends and for aspiring devs interested in data analysis applications.


                

                search_url = "https://www.linkedin.com/jobs/search/?keywords=Web%20Developer&location=United%20States"
                
                df = scrape_linkedin_jobs(
                driver,
                url=search_url,
                scrolls=10,
                max_jobs=5,
                csv_path="./csvs/linkedin_ds_jobs.csv"
                )




## Job Listings Scraper - Features Overview

1. ### Title
    Description: The job title extracted from the listing (e.g., Data Scientist, Software Engineer).

    Purpose: Helps identify the role being advertised.

2. ### Company
    Description: The company name offering the job (e.g., Netflix, Google).

    Purpose: Allows job seekers to filter by their preferred companies.

3. ### Location
    Description: The location of the job (e.g., New York, Remote).

    Purpose: Helps job seekers target specific geographic regions.

4. ### URL
    Description: The direct URL link to the job listing on LinkedIn.

    Purpose: Direct access for more details and to apply.

5. ### Job Description
    Description: A summary of the job's responsibilities and requirements.

    Purpose: Provides the key information about the role, tasks, and expectations.

6. ### Skills
    Description: Extracted skills and technologies mentioned in the job description (e.g., Python, SQL).

    Purpose: Helps job seekers match their skill set to job requirements.

7. ### Accessibility
    Description: Keywords indicating job accessibility for diverse jobseekers (e.g., "No degree required", "Senior role").

    Purpose: Identifies roles suitable for early-career professionals or those with non-traditional qualifications.

8. ### Interview
   Description: Mentions related to the interview process (e.g., "Leetcode", "Hackerrank", "Portfolio projects").

    Purpose: Provides insight into the type of preparation needed for the interview.

9. ### Subjectivity
    Description: Language analysis of the job description, a score that represents subjective ambiguity. (Subjective, Neutral, Objective)   
    
    Purpose: Often an indicator of weighted emphasis on 'soft skills' used in the job description section. While it is the habit of most job postings to employ this type of language, it may prove helpful to check for postings that clearly outline the job's needs clearly and succinctly.
      
10. ### Sentiment
    Description: Sentiment analysis of the job description, showing its overall positivity or negativity (e.g., Positive, Neutral).

    Purpose: Helps job seekers gauge the tone of the company’s work environment.

11. ### NER (Named Entity Recognition)
    Description: Extracted entities such as company names, locations, technologies, and more.

    Purpose: Highlights important information such as specific tools, locations, and organizations in the job post.


## Example of dataframe output

| <br/>Title                                                   | Company<br/>  | Location<br/>  | URL<br/>                                          | Job Description<br/> | Skills<br/> | Accessibility<br/> | Interview<br/> | Sentiment<br/> | NER<br/> |
|:---|:---|:-------|:---| :--- | :--- | :--- | :--- | :--- | :--- |
| Full Stack - Software Engineer \(L5\) - Platform Engineering | Netflix       | Los Gatos, CA  | https://www.linkedin.com/jobs/view/full-stack-... | Netflix is one of the world's leading entertai... | \['aws'\] | \[\] | \[\] |  Positive \| Objective | {} |
| Frontend Engineer                                            | Porter        | New York, NY   | https://www.linkedin.com/jobs/view/frontend-en... | The Role\\n\\nWe're looking for an experienced f... | \['https', 'github'\] | \[\] | \['github'\] |  Positive \| Subjective | {} |
| Frontend Developer                                           | Adapty.io     | United States  | https://www.linkedin.com/jobs/view/frontend-de... | Adapty is a revenue management platform for mo... | \[\] | \[\] | \[\] |  Positive \| Objective | {} |
| Front-End / Full-Stack Developer                             | Corsair       | Milpitas, CA   | https://www.linkedin.com/jobs/view/front-end-f... | Job Description\\n\\nWe are a fast-growing eComm... | \['css', 'typescript', 'tailwind css', 'react'\] | \['css'\] | \[\] |  Neutral \| Objective | {} |
| Junior Web Developer                                         | IntelliBridge | Washington, DC | https://www.linkedin.com/jobs/view/junior-web-... | Overview\\n\\nIntelliBridge is an award-winning ... | \[\] | \['collaborative', 'junior web developer'\] | \['collaboration'\] |  Positive \| Objective | {} |


<h3>Why Measure Subjectivity and Sentiment?</h3>

<p>Subjectivity reflects the presence of opinions or biases in the language, while sentiment analysis gauges the overall tone (positive, negative, or neutral).</p>

<h4 style="color:lawngreen;">Subjectivity in Job Postings:</h4>
<ul>
    <li>What it is: Subjectivity includes language that’s open to interpretation, not based on objective facts.</li>
    <li>Examples: 
        <ul>
            <li>"Highly motivated and passionate individual" (subjective)</li>
            <li>"Fast-paced and dynamic team" (subjective)</li>
            <li>"Must be a team player" (subjective)</li>
        </ul>
    </li>
    <li><span style="color:lawngreen;">Subjectivity</span> can make a job description unclear, potentially leading to misinterpretations or attracting candidates who don't truly fit the role.</li>
<li>This model reflects <span style="color:red">high</span> levels of Subjectivity with a <span style="color:red;">Positive rating</span> and <span style="color:#00acc1;">Objectivity</span> with a <span style="color:#00acc1;">Negative rating.</span>
Hope that's not confusing!</li>
</ul>

<h4 style="color:lawngreen;">Sentiment Analysis in Job Postings:</h4>
<ul>
    <li>What it is: Sentiment analysis identifies the emotional tone of the job description.</li>
    <li>What it reveals:
        <ul>
            <li>Tone: Positive, negative, or neutral.</li>
            <li>Emotional Valence: Specific feelings associated with the job.</li>
            <li>Company Culture: Insight into the org's temperament/values.</li>
        </ul>
    </li>
    <li>Uses:
        <ul>
            <li><strong>Candidate Matching</strong>: Aligns candidates with job postings based on tone.</li>
        </ul>
</ul>


### Named Entity Recognition (NER)

This model collects the following labels from scraped job listings: 
<br><br>
['ORG', 'GPE', 'PRODUCT', 'MONEY']

<br>
<ul>
<li>ORG - Organizations: Business, Government, Agencies</li>
<li>GPE - Geopolitical Entities: Countries, States, Provinces</li>
<li>PRODUCT - Objects, vehicles, foods, etc. (Not services.)</li>
<li>MONEY - Quantifiable currency amounts ($1,000,000 - 773 300 GBP)</li>
</ul>
Additional labels can be easily added in the extract_ner function in ./spacy_nre_analyzer.py
<br>
More NERs:
<ul>
<li>PERSON:      People, including fictional.</li>
<li>NORP:        Nationalities or religious or political groups.</li>
<li>FAC:         Buildings, airports, highways, bridges, etc.</li>
<li>ORG:         Companies, agencies, institutions, etc.</li>
<li>GPE:         Countries, cities, states.</li>
<li>LOC:         Non-GPE locations, mountain ranges, bodies of water.</li>
<li>PRODUCT:     Objects, vehicles, foods, etc. (Not services.)</li>
<li>EVENT:       Named hurricanes, battles, wars, sports events, etc.</li>
<li>WORK_OF_ART: Titles of books, songs, etc.</li>
<li>LAW:         Named documents made into laws.</li>
<li>LANGUAGE:    Any named language.</li>
<li>DATE:        Absolute or relative dates or periods.</li>
<li>TIME:        Times smaller than a day.</li>
<li>PERCENT:     Percentage, including ”%“.</li>
<li>MONEY:       Monetary values, including unit.</li>
<li>QUANTITY:    Measurements, as of weight or distance.</li>
<li>ORDINAL:     “first”, “second”, etc.</li>
<li>CARDINAL:    Numerals that do not fall under another type.</li>
</ul>

If you just want a live demo:
### Check out the notebook
[Interactive Data Analysis on GitHub Pages](https://placeholder-link.com)
