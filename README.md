# python-instrumentation-enabler
Simple python app(s) to demonstrate observability with OTel and Instana

## Branch `s2i-dockerfile`
> [!TIP]
> Use this branch to demonstrate Openshift's S2I (Source-to-Image) feature.

Contains the space explorer app with the following routes/ endpoints:

1. Home endpoint: `/`

<img src="assets/Screenshot 2025-12-31 at 5.37.24 PM.png" alt="Home route" width="400">

2. Runtime version endpoint: `/runtime_version`

```
{
  "runtime_version": "3.12.11"
}
```

3. Request endpoint: `/space`

<img src="assets/Screenshot 2025-12-31 at 5.37.48 PM.png" alt="Home route" width="400">

