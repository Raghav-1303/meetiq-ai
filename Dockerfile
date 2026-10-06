# Use the official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /code

# Copy requirements first
COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application
COPY . .

# Start the FastAPI application on port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]