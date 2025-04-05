import pandas as pd
import re
import spacy
from textblob import TextBlob


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


# Function to extract skills and proficiencies
def extract_skills(description):
    found_skills = []
    for skill in skills_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', description.lower()):
            found_skills.append(skill)
    return found_skills

# Function to check job accessibility (e.g., entry-level, degree required)
def extract_job_accessibility(description):
    accessibility = []
    for keyword in entry_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', description.lower()):
            accessibility.append(keyword)
    return accessibility

# Function to perform sentiment analysis and extract sentiment
def analyze_sentiment(description):
    sentiment = TextBlob(description).sentiment
    return sentiment.polarity, sentiment.subjectivity

# Function to extract NER (e.g., location, company names, job titles)
def extract_ner(description):
    doc = nlp(description)
    entities = {}
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'GPE', 'LOC', 'PRODUCT']:
            entities[ent.label_] = entities.get(ent.label_, []) + [ent.text]
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

    return df



def extract_interview_prep_keywords(df, interview_prep_keywords):
    """
    This function scans job descriptions for keywords related to interview preparation
    like coding challenges, interview prep books, or portfolio project terms.
    """
    def find_keywords(description, keywords):
        found_keywords = []
        for keyword in keywords:
            if keyword.lower() in description.lower():
                found_keywords.append(keyword)
        return found_keywords

    df['Interview Prep Keywords'] = df['Job Description'].apply(lambda x: find_keywords(x, interview_prep_keywords))
    return df

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
    output_file = file_path.split(".")[0] + "_processed.csv"
    df_processed.to_csv(output_file, index=False)

    print(f"Processed data saved to {output_file}")
    return df_processed

# Use the function to process a CSV file


# Replace 'your_file.csv' with the actual CSV file path
# processed_df = process_csv_file("your_file.csv")
processed_df = process_csv_file("./csvs/sentiment_analysis/spacy.csv")

# Display the processed DataFrame
print(processed_df)
