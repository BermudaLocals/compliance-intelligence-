from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core Identity
    app_name: str = "Compliance Intelligence API"
    api_prefix: str = "/v1"

    # Deployment & Environment
    environment: str = "development"  # development|staging|production
    deployment_mode: str = "saas"  # saas|customer_managed

    # Compliance & Audit Trail
    audit_log_retention_days: int = 2555  # ~7 years
    require_human_approval: bool = True  # NEVER False in production

    # Rate Limiting (later enforcement)
    api_rate_limit_per_minute: int = 1000

    # Multi-Tenancy (Phase 1: row_level; Phase 2+: schema/database)
    tenant_isolation_mode: str = "row_level"  # row_level|schema|database

    # Data Residency
    default_data_region: str = "us-east-1"
    allow_customer_region_override: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CI_",
        case_sensitive=False,
    )


settings = Settings()
