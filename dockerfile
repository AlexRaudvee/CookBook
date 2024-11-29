# Use a base image (e.g., Python, Node.js, etc.)
FROM python:3.10.14

# Set the working directory inside the container
WORKDIR /CookBook-1

# Copy project files into the container
COPY . .

# Install dependencies (adjust based on your project's requirements)
RUN pip install -r requirements.txt

# Define the default command to run your application
CMD ["python", "bot.py"]
