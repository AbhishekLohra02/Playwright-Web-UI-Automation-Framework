# Development and CI run on different operating systems, which is where
# "passes locally, fails in CI" comes from. This image pins the browser stack
# and system libraries so a run is reproducible anywhere Docker is.
#
# The tag must stay in step with the playwright pin in requirements.txt.
FROM mcr.microsoft.com/playwright/python:v1.61.0-noble

WORKDIR /app

# Dependencies first, so editing a test does not invalidate the layer cache.
COPY requirements.txt requirements-dev.txt ./
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements-dev.txt

COPY . .

# Chromium by default; override at run time, for example:
#   docker run --rm saucedemo-tests -m smoke --browser firefox
ENTRYPOINT ["python", "-m", "pytest", "--browser", "chromium"]
CMD ["--numprocesses", "auto"]
