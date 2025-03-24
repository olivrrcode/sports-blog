# Installation steps

you'll need [Git](https://git-scm.com/downloads) and [Python](https://www.python.org/downloads/) installed

run the following steps in the terminal (cmd or powershell on Windows, Terminal on Mac)

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

or

```bash
py run.py
```

3. Run "flask --app sports_blog run"

4. App should be available at http://127.0.0.1:5000
