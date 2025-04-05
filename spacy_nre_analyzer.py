import os
import pandas as pd
import re
import spacy
from textblob import TextBlob

"""
    This file is for extracting from the keyword lists in the main text content block of a job posting. 
    Your dataframe must contain the Job Description column to run the main method that processes all the other functions.
    At the bottom of this script is the variable processed_df = process_csv_file("csvs/example_linkedin_jobs.csv")
    Replace the path with your .csv file to use the model.
    it will output a new .csv in ./csvs/processed/<your-file-name>_processed.csv
    You can then use that file in ./juypter_notebooks/spacy.ipynb
    
"""



# Load pre-trained spaCy model for Named Entity Recognition (NER)

nlp = spacy.load('en_core_web_sm')

# Sample DataFrame with a 'Job Description' column
data = {
    'Job Title': ['Software Developer', 'Junior Data Analyst', 'Entry-Level Marketing Specialist'],
    'Job Description': [
        'We are looking for a senior developer with 5+ years of experience. Bachelor degree required. Expertise in Python, JavaScript, and SQL is a must.',
        'This is a Junior Role with on the job training. No degree required. Experience with Python, SQL, and data analysis tools preferred.',
        'Looking for an entry level marketing role with a bachelor degree required. On the job training provided. Familiarity with SEO, social media marketing, and content creation required.'
    ]
}

# Predefined lists of skills, languages, and experience levels
skills_keywords = [
    # Web Development
    'react', 'angular', 'vue.js', 'svelte', 'ember.js', 'backbone.js', 'litElement',
    'node.js', 'express', 'django', 'flask', 'ruby on rails', 'spring', 'laravel', 'asp.net', 'fastapi',
    'javascript', 'typescript', 'html', 'css', 'python', 'ruby', 'php', 'java', 'c#', 'go', 'kotlin', 'swift', 'rust',
    'bootstrap', 'tailwind css', 'bulma', 'material ui', 'foundation', 'sass', 'less',
    'jquery', 'webpack', 'babel', 'gulp', 'grunt', 'nginx', 'apache', 'varnish',
    'rest', 'graphql', 'websockets', 'soap', 'grpc', 'firebase', 'amazon api gateway', 'postman',
    'mongodb', 'postgresql', 'mysql', 'mariadb', 'sqlite', 'oracle db', 'redis', 'firebase realtime db', 'couchdb',
    'git', 'github', 'gitlab', 'bitbucket', 'subversion', 'mercurial',
    'mocha', 'jest', 'jasmine', 'selenium', 'cypress', 'puppeteer', 'playwright', 'karma',
    'jenkins', 'circleci', 'travis ci', 'github actions', 'gitlab ci', 'bamboo', 'teamcity',

    # DevOps & Cloud
    'jenkins', 'circleci', 'travis ci', 'github actions', 'bamboo', 'teamcity', 'bitrise', 'buildkite',
    'aws', 'microsoft azure', 'google cloud platform', 'ibm cloud', 'digitalocean', 'alibaba cloud',
    'docker', 'kubernetes', 'openshift', 'helm', 'docker compose',
    'ansible', 'puppet', 'chef', 'saltstack', 'terraform', 'cloudformation',
    'prometheus', 'grafana', 'nagios', 'zabbix', 'elk stack', 'splunk', 'datadog', 'new relic',
    'vmware', 'hyper-v', 'openstack', 'proxmox', 'vagrant', 'apache cloudstack',
    'terraform', 'pulumi', 'cloudformation', 'ansible',

    # Data Science & Engineering
    'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'bokeh', 'tableau', 'power bi', 'd3.js',
    'apache spark', 'hadoop', 'kafka', 'airflow', 'nifi', 'dask', 'beam', 'luigi', 'celery',
    'tensorflow', 'keras', 'pytorch', 'scikit-learn', 'xgboost', 'lightgbm', 'theano', 'caffe', 'mxnet',
    'hadoop', 'hive', 'pig', 'apache flink', 'apache storm', 'databricks', 'redshift', 'google bigquery',
    'snowflake', 'google bigquery', 'amazon redshift', 'teradata', 'vertica',
    'mongodb', 'cassandra', 'dynamodb', 'couchbase', 'redis', 'apache hbase',
    'talend', 'apache nifi', 'informatica', 'matillion', 'alteryx', 'mulesoft', 'pentaho',
    'power bi', 'tableau', 'look', 'qlikview', 'domo', 'sisense',
    'apache airflow', 'prefect', 'dagster', 'luigi', 'streamlit',

    # Networking
    'tcp/ip', 'dns', 'dhcp', 'http', 'https', 'ftp', 'snmp', 'ssh', 'telnet', 'sip', 'smtp', 'imap',
    'routers', 'switches', 'firewalls', 'load balancers', 'vpns', 'sd-wan', 'proxies', 'ids', 'ips', 'network monitoring',
    'wireshark', 'nmap', 'metasploit', 'kali linux', 'burp suite', 'snort', 'nagios', 'palo alto networks', 'cisco asa', 'fortinet',
    'aws vpc', 'azure virtual network', 'google cloud vpc', 'cloudflare', 'nginx plus', 'f5 networks', 'akamai',

    # Security & Ethical Hacking
    'kali linux', 'metasploit', 'burp suite', 'nmap', 'wireshark', 'aircrack-ng', 'hydra', 'john the ripper',
    'splunk', 'snort', 'nessus', 'openvas', 'qualys', 'nexpose', 'crowdstrike', 'darktrace', 'palo alto networks', 'fortinet', 'check point',
    'owasp', 'cis', 'nist', 'iso/iec 27001', 'soc 2', 'gdpr', 'pci-dss',
    'openssl', 'pgp', 'aes', 'rsa', 'ssl/tls', 'gpg', 'hashing algorithms', 'sha', 'md5', 'hmac'
]

entry_keywords = [
    # General Entry-level Keywords
    'entry level', 'junior role', 'beginner', 'fresh graduate', 'recent graduate',
    'new grad', 'no experience required', 'zero experience', 'trainee', 'apprentice', 'internship',
    'intern', 'apprenticeship', 'novice', 'starter', 'first job', 'new to the industry', 'new to the field',
    'entry-level position', 'entry-level job', 'junior developer', 'junior data analyst', 'junior designer',
    'junior engineer', 'junior software engineer', 'junior data scientist', 'entry-level analyst', 'entry-level software developer',

    # Keywords Related to Degree Requirements
    'no degree required', 'no degree necessary', 'degree not required', 'bachelor degree required', 'masters degree required', 'degree preferred',
    'high school diploma', 'equivalent experience', 'degree or equivalent experience','studying', 'will-earn', "towards a bachelor's deggre", 'education or experience', 'experience in lieu of degree',

    # Keywords Related to Training or Learning
    'on-the-job training', 'train', 'training provided', 'learn as you go', 'training included', 'learn on the job',
    'no formal training required', 'training and development', 'mentorship', 'coaching', 'learning opportunity', 'growth opportunity',
    'professional development', 'skill development', 'veteran', 'mentorship available', 'trainable', 'job training', 'development program',

    # Keywords for More Accessible Roles
    'no certification required', 'no specialized knowledge required', 'basic knowledge required', 'basic skills required', 'fundamental skills required',
    'willing to train', 'eager to learn', 'pair programming', 'willing to learn', 'self-starter','apprentice', 'shadow', 'quick learner', 'enthusiastic learner', 'motivated individual', 'open to learning',

    # Soft Skills and Attitudes
    'team player', 'good communication skills', 'problem solver', 'collaborative', 'adaptable', 'eager to grow', 'enthusiastic',
    'passionate about learning', 'curious', 'proactive', 'hardworking', 'positive attitude', 'self-motivated', 'goal-oriented', 'ambitious',

    # Entry-level Specific Roles/Industries
    'junior developer', 'junior analyst', 'junior engineer', 'junior designer', 'junior consultant', 'entry-level sales', 'entry-level marketing',
    'entry-level accounting', 'entry-level project management', 'junior product manager', 'junior data scientist', 'junior web developer',
    'entry-level software engineer', 'junior system administrator', 'entry-level IT', 'junior software tester', 'junior QA tester', 'entry-level business analyst',

    # Keywords for Remote
    'remote work', 'work from home', 'telecommute', 'remote position', 'flexible work hours', 'work from anywhere', 'virtual position', 'remote job',
    'remote opportunities', 'home-based position', 'telework',

    # Entry-Level Tools (for those that don't require extensive expertise)
    'microsoft office', 'google workspace', 'excel', 'word', 'powerpoint', 'outlook', 'zoom', 'slack', 'trello', 'jira', 'monday.com', 'notion',
    'basic programming', 'html', 'css', 'sql', 'python', 'excel', 'basic javascript', 'wordpress', 'google analytics', 'mailchimp'
]

interview_prep_keywords = [
    # Coding Challenge Platforms
    'leetcode', 'hackerrank', 'codewars', 'exercism', 'coderbyte', 'topcoder', 'codeforces', 'project euler',
    'codesignal', 'edx', 'freecodecamp', 'hackerearth', 'kaggle', 'interviewbit', 'spoj', 'pramp',

    # Portfolio & GitHub-related Keywords
    'portfolio', 'github', 'gitlab', 'bitbucket', 'personal website', 'personal portfolio', 'portfolio projects', 'github repositories', 'github profile',
    'github pages', 'portfolio website', 'projects on github', 'project showcase', 'developer portfolio',

    # Soft Skills Related to Interviews
    'communication skills', 'problem solving', 'critical thinking', 'collaboration', 'teamwork', 'leadership skills', 'project management', 'time management',
    'attention to detail', 'adaptability', 'learning mindset', 'creativity', 'curiosity', 'strong work ethic', 'growth mindset', 'self-motivated', 'conflict resolution',

    # Behavioral Interview Prep
    'STAR method', 'behavioral interview', 'situational interview', 'tell me about a time', 'give me an example', 'tell me about yourself', 'why do you want to work here',
    'strengths and weaknesses', 'why should we hire you', 'what is your greatest accomplishment', 'how do you handle stress', 'what motivates you',

    # Technical Interview Prep
    'technical interview', 'systems design interview', 'data structures and algorithms', 'object-oriented design', 'dynamic programming', 'recursion', 'algorithms',
    'binary search', 'graph algorithms', 'sorting algorithms', 'big o notation', 'time complexity', 'space complexity', 'circular linked list', 'hash table', 'binary tree',
    'object-oriented programming', 'mock interviews', 'data structures', 'algorithms challenges', 'technical whiteboarding', 'debugging', 'coding tests',
]


# Function to extract skills and proficiencies
def extract_skills(description):
    found_skills = set()

    # Ensure description is a string before processing
    if isinstance(description, str):
        description = description.lower()
    else:
        description = ""  # Set to empty string if it's not a string (e.g., NaN or float)

    for skill in skills_keywords:
        # Search for skill keywords in the description
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', description):
            found_skills.add(skill)

    print("Extracting Skill Keywords.")
    return list(found_skills)


# Function to check job accessibility (e.g., entry-level, degree required)
def extract_job_accessibility(description):
    accessibility = []

    # Ensure description is a string before processing
    if isinstance(description, str):
        description = description.lower()
    else:
        description = ""  # Set to empty string if it's not a string (e.g., NaN or float)

    for keyword in entry_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', description.lower()):
            accessibility.append(keyword)
    print("Extracting Accessibility Keywords.")
    return accessibility


# Function to perform sentiment analysis and extract sentiment
def analyze_sentiment(description):
    print("Analyzing Sentiment.")

    # Ensure description is a string before processing
    if isinstance(description, str):
        description = description.lower()
    else:
        description = ""  # Set to empty string if it's not a string (e.g., NaN or float)

    sentiment = TextBlob(description).sentiment

    return sentiment.polarity, sentiment.subjectivity


def interpret_sentiment(polarity, subjectivity):
    sentiment = "Neutral"
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"

    subjectivity_label = "Objective" if subjectivity < 0.5 else "Subjective"

    return sentiment, subjectivity_label

# Interpret sentiment example:
# polarity, subjectivity = 0.24166666666666664, 0.44375000000000003
# interpretation = interpret_sentiment(polarity, subjectivity)
# print(interpretation)

# Function to extract NER (e.g., location, company names, job titles)


def extract_ner(description):

    # Ensure description is a string before processing
    if isinstance(description, str):
        description = description.lower()
    else:
        description = ""  # Set to empty string if it's not a string (e.g., NaN or float)
    doc = nlp(description)
    entities = {}

    for ent in doc.ents:
        if ent.label_ in ['ORG', 'GPE', 'LOC', 'PRODUCT']:
            entities = {label: list(set(values)) for label, values in entities.items()}
    print("NER extracted.")
    return entities


# Main function to process the job descriptions
# If you make a custom function for a new column, include it in here
def process_job_descriptions(df):

    skill_data = []
    accessibility_data = []
    interview_data = []
    sentiment_data = []
    ner_data = []

    for description in df['Job Description']:
        skills = extract_skills(description)
        accessibility = extract_job_accessibility(description)
        interview = extract_interview_prep_keywords(description)
        sentiment = analyze_sentiment(description)
        ner = extract_ner(description)
        sentiment = interpret_sentiment(sentiment[0], sentiment[1])

        skill_data.append(skills)
        accessibility_data.append(accessibility)
        interview_data.append(interview)
        sentiment_data.append(sentiment)
        ner_data.append(ner)

    # Add the extracted data as new columns in the DataFrame
    df['Skills'] = skill_data
    df['Accessibility'] = accessibility_data
    df['Interview'] = interview_data
    df['Sentiment'] = sentiment_data
    df['NER'] = ner_data

    print("spaCy and NER functions completed.")
    return df


def extract_interview_prep_keywords(description):

    #     This function scans job descriptions for keywords related to interview preparation
    #     like coding challenges, interview prep books, or portfolio project terms.

    interview_keywords = []

    # Ensure description is a string before processing
    if isinstance(description, str):
        description = description.lower()
    else:
        description = ""  # Set to empty string if it's not a string (e.g., NaN or float)

    for keyword in interview_prep_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', description.lower()):
            interview_keywords.append(keyword)
            print("Extracting Accessibility Keywords.")
    return interview_keywords

# Full processing function for a CSV
def process_csv_file(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Ensure the 'Job Description' column exists
    if 'Job Description' not in df.columns:
        raise ValueError("CSV file must contain a 'Job Description' column.")

    # Apply the processing function for the job descriptions
    df_processed = process_job_descriptions(df)

    # Save the processed DataFrame to a new CSV file
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = os.path.join(os.path.dirname("./csvs/processed/"), base_name + "_processed.csv")

    df_processed.to_csv(output_file, index=False)

    print(f"Processed data saved to {output_file}")
    return df_processed


# Replace 'your_file.csv' with the actual CSV file path
# processed_df = process_csv_file("your_file.csv")


processed_df = process_csv_file("csvs/example_linkedin_ds_jobs.csv")

# Display the processed DataFrame
print(processed_df)
