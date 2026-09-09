---
name: worker-k8s-external
description: Deploy the Data Exchange Worker on an external Kubernetes cluster — image selection, Kubernetes Secret creation, Deployment manifest generation, and verification. Triggers: kubernetes worker, k8s worker, kubectl worker, external cluster worker, helm worker.
parent_skill: data-infrastructure-setup
license: Proprietary. See License-Skills for complete terms
---

# Worker Kubernetes Setup — External Cluster

Deploy the Data Exchange Worker as a Kubernetes `Deployment` on a customer-managed cluster. Unlike SPCS, there is no injected Snowflake token — both source database and Snowflake credentials are supplied explicitly via Kubernetes Secrets.

## Step 1 — Image Version

The worker image version is **pinned to your `scai` CLI release** — do not use `SHOW IMAGES` to pick the latest tag, as it may be incompatible with this version of the CLI.

Get the pinned version by running:

```bash
scai data worker setup --compute-pool <any-pool>
```

The CLI logs: `Using pinned Data Exchange Worker image: /snowflake/images/snowflake_images/data-exchange-worker:<version>`

Record that exact version tag (e.g., `1.11.1`). Use it as `<version>` in all subsequent steps. You can cancel the setup command once you have the version — this step is only needed to read the tag from CLI output. Upgrading the version later requires re-running this skill from the beginning.

**Note:** The image tag is a version number (e.g., `1.12.0`), not a platform identifier. The source type is controlled by the `DATA_SOURCE_TYPE` environment variable. Read it from the project's scai source connection:

| Source system | `DATA_SOURCE_TYPE` |
|---------------|--------------------|
| SQL Server    | `sqlserver`        |
| Redshift      | `redshift`         |
| Oracle        | `oracle`           |
| Teradata      | `teradata`         |
| PostgreSQL    | `postgresql`       |

## Step 2 — Affinity Label

**In all steps below, substitute every `<placeholder>` token with its actual value — never output a literal `<placeholder>` string. Key substitutions:**
- `<label>` — the affinity label confirmed in this step
- `<version>` — the image version from Step 1
- `<source_type>`, `<host>`, `<port>`, `<database>` — from the project's scai source connection
- `<replica_count>` — the count the user provides in Step 3
- `<source_username>`, `<source_password>` — source database credentials from the project's scai source connection; **do not ask the user to type these in the chat** — instruct them to fill them directly into the command
- `<snowflake_account>`, `<snowflake_user>`, `<snowflake_password>`, `<warehouse>` — Snowflake credentials collected from the user in Step 4; **do not ask the user to say passwords in the chat** — instruct them to fill them directly into the command

Affinity binds this worker to the workflow it should process — see the [Affinity Reference](../references/affinity-reference.md) for the model (and why the orchestrator stays null-affinity). This external manifest needs an explicit label because `AGENT_AFFINITY` must exactly match the plugin-generated workflow.

Propose a short, stable label for this source database/server, for example `mdx-salesnorth`.

Tell the user:

> This external worker needs an explicit affinity label. Proposed label: **`<label>`**. I will set it once with `configure(affinity="<label>")` and use the same value as the worker pods' `AGENT_AFFINITY`. Confirm or provide a different label.

Wait for the user to confirm or override, then set it: `configure(affinity="<label>")`.

## Step 3 — Worker Count

Tell the user:

> **How many worker pods should you run?**
>
> - Start with **2–3 replicas** for most migrations.
> - Add more if the source system can sustain higher read throughput and your network has the bandwidth.
> - Monitor source system CPU and I/O before scaling up — too many workers can disrupt production workloads.
>
> You can scale the deployment at any time with:
> ```bash
> kubectl scale deployment data-exchange-worker --replicas=<n>
> ```

Ask for the desired replica count.

**Wait for the user to provide the replica count before continuing to Step 4.**

## Step 4 — Kubernetes Secret

Unlike SPCS, there is no injected Snowflake token. Credentials for both the source database and Snowflake must be provided.

Pre-fill source database values from the project's scai source connection. Collect the following Snowflake values from the user:
- `SNOWFLAKE_ACCOUNT` — account identifier (e.g., `myorg-myaccount`)
- `SNOWFLAKE_USER` — Snowflake username
- `SNOWFLAKE_PASSWORD` — Snowflake password
- `SNOWFLAKE_WAREHOUSE` — warehouse name (already configured in parent skill Question 2)

Show the following command and instruct the user to fill in their actual credentials before running it:

```bash
kubectl create secret generic data-exchange-worker-secrets \
  --from-literal=DATA_SOURCE_USERNAME='<source_username>' \
  --from-literal=DATA_SOURCE_PASSWORD='<source_password>' \
  --from-literal=SNOWFLAKE_ACCOUNT='<snowflake_account>' \
  --from-literal=SNOWFLAKE_USER='<snowflake_user>' \
  --from-literal=SNOWFLAKE_PASSWORD='<snowflake_password>' \
  --from-literal=SNOWFLAKE_WAREHOUSE='<warehouse>'
```

**Wait for the user to confirm the secret has been created before continuing.**

Next, create an image pull secret so your cluster can pull from the Snowflake Image Repository. Ask the user for their Snowflake account registry hostname — it follows the pattern `<orgname>-<accountname>.registry.snowflakecomputing.com`. If they are unsure, they can run `SHOW IMAGE REPOSITORIES IN SCHEMA snowflake.images;` to find the `repository_url`.

Show:

```bash
docker login <registry_hostname>
# enter SNOWFLAKE_USER and SNOWFLAKE_PASSWORD when prompted

kubectl create secret generic snowflake-registry-pull \
  --from-file=.dockerconfigjson="${HOME}/.docker/config.json" \
  --type=kubernetes.io/dockerconfigjson
```

**Wait for the user to confirm the pull secret has been created before continuing.**

## Step 5 — Generate Deployment YAML

Write the following manifest to `.scai/worker-deployment.yaml` in the project directory, substituting all non-credential placeholder values:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-exchange-worker
  labels:
    app: data-exchange-worker
spec:
  replicas: <replica_count>
  selector:
    matchLabels:
      app: data-exchange-worker
  template:
    metadata:
      labels:
        app: data-exchange-worker
    spec:
      containers:
        - name: agent
          image: snowflake/images/snowflake_images/data-exchange-worker:<version>
          env:
            - name: DATA_SOURCE_TYPE
              value: "<source_type>"
            - name: DATA_SOURCE_HOST
              value: "<host>"
            - name: DATA_SOURCE_PORT
              value: "<port>"
            - name: DATA_SOURCE_DATABASE
              value: "<database>"
            - name: MAX_PARALLEL_TASKS
              value: "4"
            - name: AGENT_AFFINITY
              value: "<label>"
            - name: SNOWFLAKE_CONNECTION_NAME
              value: "MY_SNOWFLAKE_CONNECTION"
            - name: DATA_SOURCE_USERNAME
              valueFrom:
                secretKeyRef:
                  name: data-exchange-worker-secrets
                  key: DATA_SOURCE_USERNAME
            - name: DATA_SOURCE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: data-exchange-worker-secrets
                  key: DATA_SOURCE_PASSWORD
            - name: SNOWFLAKE_ACCOUNT
              valueFrom:
                secretKeyRef:
                  name: data-exchange-worker-secrets
                  key: SNOWFLAKE_ACCOUNT
            - name: SNOWFLAKE_USER
              valueFrom:
                secretKeyRef:
                  name: data-exchange-worker-secrets
                  key: SNOWFLAKE_USER
            - name: SNOWFLAKE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: data-exchange-worker-secrets
                  key: SNOWFLAKE_PASSWORD
            - name: SNOWFLAKE_WAREHOUSE
              valueFrom:
                secretKeyRef:
                  name: data-exchange-worker-secrets
                  key: SNOWFLAKE_WAREHOUSE
          resources:
            requests:
              memory: "10Gi"
              cpu: "6"
            limits:
              memory: "10Gi"
              cpu: "6"
      imagePullSecrets:
        - name: snowflake-registry-pull
```

Show the generated file to the user.

**Note:** `SNOWFLAKE_CONNECTION_NAME: "MY_SNOWFLAKE_CONNECTION"` is the fixed connection name expected by the Data Exchange Worker in external Kubernetes mode. Do not change this value.

**Oracle/Teradata:** Note that pods must have outbound network access (port 443) to download the database driver on startup. No manifest change is required, but the cluster's network policy must allow this egress.

**Note:** `MAX_PARALLEL_TASKS` defaults to `4`. Reduce this value if the source system cannot handle that many concurrent connections.

**Wait for the user to confirm the manifest before applying.**

## Step 6 — Apply and Verify

Apply the manifest:

```bash
kubectl apply -f .scai/worker-deployment.yaml
```

Check pod status:

```bash
kubectl get pods -l app=data-exchange-worker
```

Expected: all pods reach `Running` state. Check logs to confirm the worker is connected and polling:

```bash
kubectl logs -l app=data-exchange-worker --tail=50
```

**Wait for the user to confirm all pods are running and polling for tasks before continuing.**

## Step 7 — Remind

Tell the user:

> **Important:** When you configure your migration workflow, set the affinity to **`<label>`**. Without this, the orchestrator will not route tasks to your workers.
>
> To check pod status at any time:
> ```bash
> kubectl get pods -l app=data-exchange-worker
> kubectl logs -l app=data-exchange-worker --tail=50
> ```

## Done

The worker deployment is running on the external cluster and all pods are polling for tasks. Return control to the parent skill, which runs Level 1 Data Doctor before proceeding.
