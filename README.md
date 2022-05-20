[![Publish multi-arch Docker images](https://github.com/Der-Henning/earnapp-metrics/actions/workflows/docker-multi-arch.yml/badge.svg?branch=main)](https://github.com/Der-Henning/earnapp-metrics/actions/workflows/docker-multi-arch.yml)
[![CodeQL](https://github.com/Der-Henning/earnapp-metrics/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Der-Henning/earnapp-metrics/actions/workflows/codeql-analysis.yml)

# earnApp Metrics

Prometheus Metrics Server for [earnApp.com](https://earnapp.com/i/73zzlxi)

Based on [fazalfarhan01/EarnApp-API](https://github.com/fazalfarhan01/EarnApp-API)

## Prometheus scrape config

````xml
  - job_name: 'earnapp-metrics'
    scrape_interval: 1m
    scheme: http
    metrics_path: /
    static_configs:
    - targets:
      - 'localhost:8000'
````
