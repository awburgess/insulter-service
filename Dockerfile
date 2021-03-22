FROM python:3

WORKDIR /usr/src/service

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "insulter/insult.py"]
