# Use the official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

RUN RUN apt-get update && rm -rf /var/lib/apt/lists/*


# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the Streamlit default port
EXPOSE 8501

# Set the Streamlit configuration to allow access from any IP
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Add metadata labels
LABEL author="Zhipeng He" \
      email="zhipeng.he@hdr.qut.edu.au" \
      description="Streamlit application container for NEM data analysis"

# Run the Streamlit app
CMD ["sh", "-c", "streamlit run app.py --server.port=$STREAMLIT_SERVER_PORT --server.address=$STREAMLIT_SERVER_ADDRESS"]
