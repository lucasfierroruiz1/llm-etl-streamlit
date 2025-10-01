from modal import App, Image, web_server
import os
import subprocess
import sys
import time

image = (
    Image.debian_slim()
    .pip_install("streamlit", "supabase", "pandas", "altair", "python-dotenv")
    .add_local_dir("app", "/root/app")
    .env({
        "SUPABASE_URL": os.getenv("SUPABASE_URL", ""),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY", ""),
        "SUPABASE_TABLE": os.getenv("SUPABASE_TABLE", "etl_items"),
    })
)

app = App("llm-etl-streamlit")

@app.function(image=image)
def serve():
    # Expose port 8000 to the internet
    with web_server(port=8000):
        # Start Streamlit
        p = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "/root/app/streamlit_app.py",
                "--server.port",
                "8000",
                "--server.address",
                "0.0.0.0",
            ]
        )
        try:
            # Keep the function alive while Streamlit runs
            while True:
                code = p.poll()
                if code is not None:
                    # Streamlit exited, stop the function with same code
                    raise SystemExit(code)
                time.sleep(2)
        finally:
            p.terminate()

