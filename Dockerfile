FROM python:3

WORKDIR .

COPY requirements.txt ./
RUN pip3 install --upgrade --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./theorical_case/drone.py" ]
