# Installation steps

You'll need [Git](https://git-scm.com/downloads) and [Python](https://www.python.org/downloads/) installed

Run the following steps in the terminal (cmd or powershell on Windows, Terminal on Mac)

1. Get the code

  ```bash
  git clone https://github.com/olivrrcode/sports-blog.git
  cd sports-blog
  ```

2. Install deps

  ```bash
  pip install -r requirements.txt
  ```
  
  3. Run it
  
  ```bash
  python run.py
  ```
  
  if this doesn't work on Windows, try
  
  ```bash
  python3 run.py
  ```

3. Run the following command
  ```bash
  flask --app sports_blog run
  ```
  
  if this doesn't work, try
  
  ```bash
  py run.py
  ```

5. Load up a browser and navigate to
  ```bash
  http://127.0.0.1:5000
  ```
