# Use a base Python image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the application dependencies
RUN pip install -r requirements.txt

# Copy all contents from the current directory into the container
COPY . .

# Expose port 5000 (or the port your Flask application runs on)
EXPOSE 5000

# Command to run your Flask application
CMD ["python", "app.py"]
