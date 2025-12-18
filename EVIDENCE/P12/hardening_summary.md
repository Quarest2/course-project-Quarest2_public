# Hardening Summary (P12)

## Overview

This document describes the hardening measures applied to the Dockerfile and IaC (compose.yaml) for the features-api project.
## Dockerfile Hardening

### Before (Initial State)

- Used base image python:3.11-slim without a specific version
- No explicit version pinning for packages
- Minimal restrictions on access permissions

### After (Current State)

#### 1. Version Pinning of Images and Packages

**Changes:**

- FROM python:3.11-slim → FROM python:3.11.10-slim
- Added version pinning for gcc in build stage: gcc=4:12.2.0-3ubuntu1- Добавлена фиксация версии gcc в build stage: `gcc=4:12.2.0-3ubuntu1`

**Rationale:**
- Prevents unexpected changes from base image updates
- Ensures reproducible builds
- Simplifies vulnerability tracking- Обеспечивает воспроизводимость сборок

#### 2. Enhanced Non-Root User Configuration

**Changes:**
- Explicit UID/GID specification: groupadd -r appuser -g 1000 and useradd -r -g appuser -u 1000
- Proper permission settings: chmod 755 /app
- Temporary directory configuration: chmod 1777 /tmp /var/tmp- Установка правильных прав доступа: `chmod 755 /app`

**Rationale:**
- Prevents privilege escalation
- Restricts filesystem access
- Aligns with the principle of least privilege

#### 3. Additional Security Environment Variables

**Changes:**
Added variables:
- PYTHONHASHSEED=random - prevents hash-based DoS attacks
- PIP_NO_CACHE_DIR=1 - disables pip cache to reduce attack surface
- PIP_DISABLE_PIP_VERSION_CHECK=1 - disables pip version checks- `PIP_NO_CACHE_DIR=1` - отключает кэш pip для уменьшения поверхности атаки

**Rationale:**
- Reduces risk of exploiting known vulnerabilities
- Decreases image size
- Improves runtime security

## IaC Hardening (compose.yaml)

### Before (Initial State)

- Ports were exposed on all interfaces (0.0.0.0)
- No explicit user specification
- Minimal network access restrictions

### After (Current State)

#### 1. Restricted Network Access

**Changes:**
- ports: - "8000:8000" → ports: - "127.0.0.1:8000:8000"
- ports: - "5432:5432" → ports: - "127.0.0.1:5432:5432"- 

**Rationale:**
- Ports accessible only from localhost
- Prevents unauthorized external access
- Aligns with minimal attack surface principle

#### 2. Explicit User Specification

**Changes:**
Added:
```yaml
user: "1000:1000"
```

**Rationale:**
- Ensures container runs as non-root user
- Additional protection layer even if USER in Dockerfile fails

#### 3. AppArmor Profile

**Changes:**
Added:
```yaml
security_opt:
  - apparmor:docker-default
```

**Rationale:**
- Applies Docker's default AppArmor profile
- Restricts container system calls
- Additional host-level protection layer

## Existing Security Measures

### Dockerfile

- Multi-stage build to reduce image size
- Non-root user (appuser)
- HEALTHCHECK for state monitoring
- Minimal base image (slim)
- APT cache cleanup after package installation

### compose.yaml

- no-new-privileges:true - prevents gaining new privileges
- cap_drop: ALL - drops all capabilities
- read_only: true - mounts root filesystem as read-only
- tmpfs with noexec,nosuid - prevents execution from /tmp
- Health checks for both services

## Scan Results

### Hadolint

After applying hardening measures:
- All critical rules (DL3001, DL3002, DL3006, DL3007) are compliant
- Package version warnings handled through configuration

### Checkov

- All Dockerfile checks passed
- No critical findings in IaC

### Trivy

- Regular image vulnerability scanning
- Critical and high vulnerabilities tracked and resolved through base image updates

## Recommendations for Further Improvement

- Secrets Management: Use Docker secrets or external vault instead of environment variables
- Image Scanning: Integrate scanning into the image build process
- Network Policies: Apply network policies for container isolation
- Audit Logging: Enable container action auditing
- Regular Updates: Regularly update base images and dependencies
