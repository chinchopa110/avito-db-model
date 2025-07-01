# PostgreSQL Deployment with Docker

## Project Overview

This project provides a complete production-ready PostgreSQL environment with:
- Database migrations
- Test data seeding
- Monitoring and visualization
- High availability
- Automated backups
- Performance optimization

## Detailed Features

### 1. Database Migrations (Flyway)
- Version-controlled SQL migrations
- Automatic migration on container startup
- Supports partial upgrades (MIGRATION_VERSION)
- Idempotent migration scripts
- Schema version tracking

Migration files are stored in:
/migrations/
  V1__Initial_schema.sql
  V2__Add_indexes.sql
  V3__Create_roles.sql
  V4__Partition_tables.sql

### 2. Data Seeding System
- Uses Python + Faker for realistic test data
- Controlled by environment variables:
  - APP_ENV=dev (enables seeding)
  - SEED_COUNT=1000 (records per table)
- Maintains data consistency across relationships
- Supports all migration versions

Seeding process:
1. Waits for database readiness
2. Checks current schema version
3. Generates appropriate test data
4. Validates data integrity

### 3. High Availability (Patroni)
- 3-node PostgreSQL cluster:
  - 1 primary (read-write)
  - 2 synchronous replicas (read-only)
- Automatic failover
- Configuration:
  /patroni/config.yml
  - etcd for leader election
  - health checks every 10s
  - failover timeout: 30s

### 4. Performance Optimization
#### Indexes
- B-tree for standard queries
- GIN for JSONB columns
- Partial indexes for common filters
- Covering indexes for critical queries

#### Partitioning
- Range partitioning for time-series data
- List partitioning for categorical data
- Subpartitioning for complex datasets

Example partitioning scheme:
CREATE TABLE measurements (
  id SERIAL,
  logdate DATE NOT NULL,
  device_id INT,
  data JSONB
) PARTITION BY RANGE (logdate);

#### Materialized Views
- Pre-computed aggregates
- Refresh on schedule
- Automatic refresh triggers

### 5. Monitoring Stack
Components:
- Prometheus: metrics collection
- Grafana: visualization
- pg_exporter: PostgreSQL metrics

Key metrics tracked:
- Query performance
- Replication lag
- Cache hit ratio
- Locks and conflicts
- Connection pool stats

### 6. Backup System
- WAL archiving for point-in-time recovery
- Base backups every 24 hours
- Retention policy (default 7 backups)
- Backup verification

Backup commands:
# Manual base backup
docker-compose exec postgres pg_basebackup -D /backups/full_$(date +%Y-%m-%d)

# Restore from backup
docker-compose exec postgres pg_restore -C -d postgres /backups/latest.dump

## Detailed Setup Guide

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM recommended

### Installation Steps
1. Clone repository:
git clone https://github.com/chinchopa110/postgres-docker-setup.git

2. Configure environment:
cp .env.example .env
nano .env

3. Start services:
docker-compose up -d

4. Verify:
docker-compose ps

### Configuration Options

#### Database
POSTGRES_USER=admin
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=app_db
MAX_CONNECTIONS=100
SHARED_BUFFERS=1GB

#### Replication
PATRONI_REPLICATION_USERNAME=replicator
PATRONI_REPLICATION_PASSWORD=replica_pass
PATRONI_POSTGRESQL_LISTEN=0.0.0.0:5432
PATRONI_POSTGRESQL_CONNECT_ADDRESS=postgres:5432

#### Monitoring
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin123
PROMETHEUS_RETENTION=15d

## Maintenance

### Common Operations
# Check cluster status
docker-compose exec patroni patronictl list

# Promote replica
docker-compose exec patroni patronictl failover

# Rebuild indexes
docker-compose exec postgres psql -U $POSTGRES_USER -c "REINDEX DATABASE $POSTGRES_DB;"

### Troubleshooting
1. Replication issues:
- Check patroni logs: docker-compose logs patroni
- Verify etcd health: docker-compose exec etcd etcdctl cluster-health

2. Performance problems:
- Examine slow queries: docker-compose exec postgres psql -U $POSTGRES_USER -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"
- Check locks: docker-compose exec postgres psql -U $POSTGRES_USER -c "SELECT * FROM pg_locks;"

## Security

### Role Management
- Application roles with least privilege
- Read-only analytic role
- Password encryption
- Connection limits

### Network Security
- Internal Docker network
- Exposed ports limited to:
  - 5432 (PostgreSQL)
  - 3000 (Grafana)
  - 9090 (Prometheus)
- TLS encryption for replication
