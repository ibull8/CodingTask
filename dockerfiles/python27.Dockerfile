# Base image
FROM python:2.7

# Setting the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container
COPY grep_script.py .
COPY test27.py .
COPY file1.txt .
COPY file2.txt .

# Install pytest
RUN pip install pytest==4.6.11

# Run pytest when the container launches
CMD ["pytest", "test27.py"]

