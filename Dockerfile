FROM python
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales
RUN pip install --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
ENV LANG ru_RU.UTF-8  
ENV LANGUAGE ru_RU:en  
ENV LC_ALL ru_RU.UTF-8  
COPY . .
