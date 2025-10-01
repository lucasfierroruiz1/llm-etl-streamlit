# LLM ETL Project Report

## Data Collected
I collected text from the Charlotte FC news page:  
https://www.charlottefootballclub.com/news  

I chose this source because I follow the team and wanted to transform live soccer news into structured records that can be searched, summarized, and 
visualized.

## Prompt Used
The structurer step used this concise prompt:  

You will receive raw text. Return JSON list of objects with keys 
id, title, summary, topics, source_url, extracted_at, updated_at. 
id must be UUIDv4. summary is 2 to 4 sentences. 
topics is a short list of tags. updated_at is current UTC in ISO8601. 
Respond with JSON only.

## JSON Schema
Each record followed this schema:
- id (UUIDv4, primary key)  
- title (short headline)  
- summary (2–4 sentence summary)  
- topics (list of tags)  
- source_url (string)  
- extracted_at (timestamp when collected)  
- updated_at (timestamp when structured)  

## Why LLM Was Helpful
The LLM provided automated summarization and topic tagging.  
This avoided manual parsing and gave a consistent JSON format from raw HTML.  

## Visuals in Streamlit
Two main visuals were deployed:  
1. Count by Topic Bar Chart – shows the frequency of topics across articles.  
2. Timeline Chart – a tick plot of article titles by updated_at, showing when new content was added.  

