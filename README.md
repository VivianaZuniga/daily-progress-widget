# Daily Progress Monitoring Widget with Dockerized Architecture

A comprehensive productivity system designed for monitoring daily activities and analyzing long-term consistency. The project features an interactive desktop interface that communicates natively with a robust REST API backed by a modern relational database infrastructure.

## Tech Stack

* **Desktop Frontend:** Python 3.11 + PyQt6 (Modern, frameless UI featuring dynamic reactive states based on daily progress percentage).
* **Backend / API:** Django 5.2 + Django REST Framework.
* **Database:** PostgreSQL 15 (Relational modeling for persistence of historical consistency and contribution heatmaps).
* **Infrastructure & Deployment:** Docker & Docker Compose (Independent containers ensuring portability and isolated development environments).

## Architecture & Overview

The project is architected into two fully decoupled layers:
1. **The API & Infrastructure (Docker):** Manages the Django web server and the PostgreSQL engine running seamlessly in the background, isolating data storage and exposing the endpoints required for data consumption.
2. **The Widget (PyQt6):** A native desktop application that interacts with the backend API to reflect real-time progress and render a dynamic consistency heatmap.

---

## Installation & Usage Guide

To run this project on your local machine, follow these steps:

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* Python 3.11 installed locally (required only to run the desktop interface).

### 2. Set Up Infrastructure (Backend)
Clone the repository, navigate to the project root, and spin up the containers in detached mode:
```bash
docker-compose up -d