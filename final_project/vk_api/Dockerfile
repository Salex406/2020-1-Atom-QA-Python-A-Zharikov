FROM python:latest
EXPOSE 5000
# Импортируем 'client.py' в папку '/client/'.

ADD mock.py /home/alex/dc/vk_api/

# Устанавливаем в качестве рабочей директории '/client/'.
WORKDIR /home/alex/dc/vk_api/
RUN pip install --no-cache-dir flask
