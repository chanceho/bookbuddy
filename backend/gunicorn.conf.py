import os

workers = 2 
threads = 2  
timeout = 120
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"