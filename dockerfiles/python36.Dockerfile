# Base image
FROM python:3.6

# Setting the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container
COPY grep_script.py .
COPY test36.py .
COPY file1.txt .
COPY file2.txt .

# Install pytest
RUN pip install pytest==6.0.2

# Run pytest when the container launches
CMD ["pytest", "test36.py"]

