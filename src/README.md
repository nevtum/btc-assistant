To deploy price collector worker, run the following:

```bash
BUILD_NR=<your newest build number> make deploy
```

This deploys the price collector to the staging environment. Once ready to deploy to PROD, do:

```bash
ENV=prod BUILD_NR=<build number to promote to prod> make deploy.worker
```