# Viva Preparation

1. **Why avoid direct pushes to `main`?** Protected `main` should represent reviewed, deployable history. A feature branch and PR provide an audit trail, automated validation, discussion, and a safe point to reject or amend changes.

2. **What is a PR for beyond merging?** A PR is a collaboration and control boundary: it explains intent, shows the diff, runs policy checks, captures review decisions, and permanently links the change to its CI evidence.

3. **Why run CI before merge?** CI finds test, dependency, and container-build failures before they affect the shared release branch. Requiring it as a status check turns validation into an enforceable rule.

4. **Docker image versus container?** An image is an immutable filesystem/configuration template. A container is a runtime instance of that image with a process, writable layer, network, and lifecycle.

5. **Why version images?** Immutable version tags let operators reproduce a deployment, compare releases, audit provenance, and select a known-good rollback target.

6. **Why is `latest` insufficient?** `latest` is a mutable convention, not a version guarantee. It can point to different content over time, so it cannot alone identify exactly what was deployed.

7. **Why promote the same artifact instead of rebuilding?** Rebuilding can select changed base images or dependencies and produce different bytes. Promoting the tested digest ensures staging and production execute the artifact that passed validation.

8. **What is a registry for?** A registry stores, addresses, authenticates, and distributes container artifacts and metadata. It decouples building from deployment and gives environments a shared artifact source.

9. **CI workflow versus release workflow?** CI is PR-triggered and performs tests plus build validation without publishing. Release is semantic-tag-triggered and performs tests, version derivation, metadata attachment, authentication, and publication.

10. **Why store credentials as secrets?** Secrets keep credentials out of source and logs, allow controlled rotation, and restrict their availability. This project uses the short-lived repository-scoped `GITHUB_TOKEN` instead of a hard-coded password.

11. **How do you identify the source commit for an image?** Inspect `org.opencontainers.image.revision`, use the commit-SHA image tag, and follow the semantic tag to its commit. For 1.1.0 all three identify `2990b54f1534fb8850472b25d597eb95f59fa50c`.

12. **Why does layer order affect CI/CD speed?** Docker reuses a layer only while its inputs and previous layers are unchanged. Copying the stable dependency manifest before application source lets frequent code changes reuse the expensive installation layer.

13. **How do you roll back 1.1.0 to 1.0.0?** Deploy `ghcr.io/abdul-mateen-1/student-ml-api:1.0.0` (or its recorded digest) from GHCR and restart the workload. No source edit, dependency installation, or rebuild is needed.

14. **Git tag versus Docker tag?** The Git tag marks the source commit chosen for release. The tag-triggered workflow derives the Docker version by converting `v1.1.0` to `1.1.0`, so source and artifact versions remain traceable.

15. **What happens when application and model versions change independently?** Compatibility can break between preprocessing, feature schemas, runtime libraries, and model inputs/outputs. MLOps systems should record both versions, validate supported combinations, monitor each pairing, and roll back the application or model independently when possible.
