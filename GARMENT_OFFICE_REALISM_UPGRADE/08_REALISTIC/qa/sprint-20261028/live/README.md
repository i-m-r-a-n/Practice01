# Live browser QA — blocked, not passed

The Chromium navigation at 1440×900 failed before the application loaded:
`net::ERR_CERT_AUTHORITY_INVALID`.

A bounded Firefox alternative used the existing environment-proxy CA in a task-only NSS database under `/workspace`, with certificate verification enabled. Firefox then failed to launch within30seconds: read-only `uid_map` sandbox failure and `RenderCompositorSWGL` framebuffer failure. No certificate verification bypass or global trust change was used.

Therefore no live model-ready time or live WebGL screenshot is claimed. The separate `../local-baseline/` screenshots are actual local Chromium WebGL frames from the fetched20a3de9 baseline and cannot establish live WAN performance or MacBook behavior.
