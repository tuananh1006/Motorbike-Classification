FROM python:3.9

# Create a folder /app if it doesn't exist,
# the /app folder is the current working directory
WORKDIR /app

# Copy necessary files to our app
COPY ./app/main.py /app

COPY ./app/utils/predict_utils.py /app/utils/

COPY ./requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir # Run command install on this line to avoid re-install requirements.txt when model & data has changed

# Take note port expose
EXPOSE 30000

# Disable pip cache to shrink the image size a little bit,
# since it does not need to be re-installed
# RUN pip install -r requirements.txt --no-cache-dir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]