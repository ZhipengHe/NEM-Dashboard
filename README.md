# NEM Dashboard

[![GitHub Actions Build](https://img.shields.io/github/actions/workflow/status/ZhipengHe/NEM-Dashboard/docker-build-push.yml)](https://github.com/ZhipengHe/NEM-Dashboard/actions/workflows/docker-build-push.yml) 
[![Docker Image Version](https://img.shields.io/docker/v/zhipenghe/nem-dashboard)](https://hub.docker.com/r/zhipenghe/nem-dashboard) 
[![Docker Image Size](https://img.shields.io/docker/image-size/zhipenghe/nem-dashboard)](https://hub.docker.com/r/zhipenghe/nem-dashboard) 
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fnem.zhipenghe.me)](https://nem.zhipenghe.me)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/ZhipengHe/NEM-Dashboard)](https://github.com/ZhipengHe/NEM-Dashboard/issues)
[![License](https://img.shields.io/github/license/ZhipengHe/NEM-Dashboard)](LICENSE)


This is a simple dashboard for Australian National Electricity Market (NEM) data. The data is extracted from the AEMO website by using Python package [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS). The extracted data is stored in folder `data` and the dashboard is created using [Streamlit](https://streamlit.io/).

## Installation

You can choose to run the dashboard locally or deploy it with Docker.

### Run Locally

```bash
# clone the repository
git clone https://github.com/ZhipengHe/NEM-Dashboard.git
cd NEM-Dashboard
# create a virtual environment
conda create -n nem-dashboard python=3.11
conda activate nem-dashboard
# install the required packages
pip install -r requirements.txt
# run the dashboard
streamlit run app.py
```

### Run with Docker

You can use the Docker image from Dockerhub to run the dashboard. Then you don't need to install the required packages.

Deploy with Docker Compose.

```bash
# clone the repository
git clone https://github.com/ZhipengHe/NEM-Dashboard.git
cd NEM-Dashboard
docker compose up -d
```

Or you can run the Docker image directly.

```bash
# clone the repository
git clone https://github.com/ZhipengHe/NEM-Dashboard.git
cd NEM-Dashboard
# pull the Docker image
docker pull zhipenghe/nem-dashboard:latest
docker run -p 8501:8501 zhipenghe/nem-dashboard:latest
```

Or you can build the Docker image by yourself.

```bash
# ... after cloning the repository
docker build -t zhipenghe/nem-dashboard:latest .
docker run -p 8501:8501 zhipenghe/nem-dashboard:latest
```

After running the dashboard, you can access it by visiting `http://localhost:8501` in your browser.

## License

Following the [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS) project, this project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The copyright of the data belongs to the Australian Energy Market Operator (AEMO). Use of the data is subject to the [AEMO Copyright Permissions](https://www.aemo.com.au/privacy-and-legal-notices/copyright-permissions).

 
