# KG Inference API

## Environment Variables

- `BBP_NEXUS_ENDPOINT` The nexus endpoint (eg. `https://staging.nexus.ocp.bbp.epfl.ch/v1`)
- `RULES_BUCKET` The bucket that the rules are located
- `ENVIRONMENT` The environment that the application runs in (`LOCAL`/`DEV`/`PRODUCTION`)
- `WHITELISTED_CORS_URLS` The allowed URLs to accept CORS requests from. The URLs should be passed as a comma-separated list (eg. `http://localhost:3050,http://test.com`)