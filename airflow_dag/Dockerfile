# Use official Airflow image as the base
FROM apache/airflow:2.10.2

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

# Copy the requirements.txt file to the Docker container
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

# Copy DAGs and other necessary files (optional)
COPY dags /opt/airflow/dags
COPY plugins /opt/airflow/plugins

# Set the entrypoint for Airflow
ENTRYPOINT ["/entrypoint"]

# Default command to run Airflow webserver
CMD ["webserver"]
