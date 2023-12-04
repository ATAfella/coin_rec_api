# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /coin_rec_api

# Copy the application files into the working directory
COPY . /coin_rec_api

# Install the application dependencies
RUN pip install -r requirements.txt

# Define the entry point for the container
CMD ["python", "coin_photo_rec.py"]