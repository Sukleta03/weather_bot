FROM python:3.11


WORKDIR /home/sukleta/fox_projects/aiogram_bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


CMD ["python", "run.py"]
