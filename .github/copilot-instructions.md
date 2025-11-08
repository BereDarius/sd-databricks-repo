# Databricks Asset Bundle - Airbnb SF Project

## Project Structure

This is a **Databricks Asset Bundle** (DAB) project for a Delta Live Tables (DLT) pipeline processing Airbnb San Francisco data. The bundle follows Databricks' standard structure:

- `airbnb_sf/databricks.yml` - Main bundle configuration defining deployment targets (`dev`, `prod`)
- `airbnb_sf/resources/` - Resource definitions (pipelines, jobs) as YAML files
- `airbnb_sf/resources/airbnb_sf_etl/transformations/` - Python files with DLT table definitions

## Key Architecture Patterns

### Bundle Configuration & Deployment Targets

The project uses **two deployment modes**:

- **dev**: `mode: development` - resources prefixed with `[dev username]`, job schedules paused, deployed to user workspace
- **prod**: `mode: production` - explicit root path `/Workspace/Users/darius@standout-development.ro/.bundle/...`, schedules active

Variables are target-specific:

- `catalog`: Always `airbnb_sf`
- `schema`: `${workspace.current_user.short_name}` for dev, `prod` for production

### DLT Table Definitions

Each dataset lives in a separate Python file under `transformations/`. Example from `listings_raw.py`:

```python
from pyspark import pipelines as dp

@dp.table
def listings_raw():
    return spark.read.csv("/Volumes/airbnb/v01/sf-listings/sf-airbnb.csv", ...)
```

**Convention**: One `@dp.table` decorated function per file, function name = table name.

### Resource Includes Pattern

`databricks.yml` uses glob includes to discover resources:

```yaml
include:
  - resources/*.yml
  - resources/*/*.yml
```

Pipeline discovers transformations via:

```yaml
libraries:
  - glob:
      include: transformations/**
```

## Development Workflow

### Deploy and Run Commands

```bash
# Authenticate first (one-time)
databricks configure

# Deploy to dev (default target)
databricks bundle deploy

# Deploy to production
databricks bundle deploy --target prod

# Run pipeline
databricks bundle run
```

### File Organization Rules

- **Add new datasets**: Create new `.py` files in `transformations/` with `@dp.table` decorator
- **Explorations ignored**: Ad-hoc notebooks go in `explorations/` (gitignored per `.gitignore`)
- **No lib/ folder**: This project doesn't use the `lib/` structure mentioned in main README

## Critical Details

- **Workspace host**: `https://dbc-158cf735-0308.cloud.databricks.com`
- **Data source**: `/Volumes/airbnb/v01/sf-listings/sf-airbnb.csv` (Unity Catalog volume)
- **Serverless pipeline**: `serverless: true` in pipeline config
- **Scheduled job**: Runs daily via `airbnb_sf_job` (periodic trigger, 1 day interval)

## Testing & Validation

_(Future): Add testing workflows here as the project matures_

## Common Mistakes to Avoid

- Don't add schema/catalog values directly in transformation code - use variables from `databricks.yml`
- The pipeline auto-discovers transformations via glob - no need to manually register new files
- When adding CSV reads, include `quote='"', escape='"', multiLine=True` for Airbnb data format
