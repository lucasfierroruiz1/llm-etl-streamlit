# LLM ETL Project Report

## Data Collected
I collected text from the FC Barcelona team stats page.
https://www.espn.com/soccer/team/stats/_/id/83/barcelona

I chose this source because I follow Barcelona and want a quick way to track how topics change over time in their public stats coverage. The site is updated often which makes it useful for repeated ETL runs.

## Prompt Used
You will receive raw text. Return JSON list of objects with keys
id, title, summary, topics, source_url, extracted_at, updated_at.
id must be UUIDv4. summary is 2 to 4 sentences.
topics is a short list of tags. updated_at is current UTC in ISO8601.
Respond with JSON only.

## JSON Schema
Each record follows this schema.
id UUIDv4
title short headline
summary 2 to 4 sentences
topics list of tags
source_url string
extracted_at timestamp when collected
updated_at timestamp when structured

## Why LLM Helped
The LLM converts unstructured page text into consistent JSON. It produces short summaries and topic tags that work well for search and charts. This removes manual parsing and gives a clean payload for Supabase.

## Visuals in Streamlit
Count by topic bar chart. Shows how often each topic appears.
Timeline ticks by updated_at. Shows when new items were added across runs.

## Runbook
collector.py scrapes the ESPN page and writes data/raw_blob.txt
structurer.py calls the LLM and writes data/structured.json
loader.py upserts into the Supabase table etl_items
app/streamlit_app.py reads from Supabase and renders table and charts
