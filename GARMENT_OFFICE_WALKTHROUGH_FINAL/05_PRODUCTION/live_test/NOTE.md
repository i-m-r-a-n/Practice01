# Live-site functional test (stopped)

Started 27 Oct 2026 07:58 UTC against the live Worker (bundle f9048ef) and stopped by Claude at 08:05 UTC after six
screenshots (overview, boardroom, photoreal render, ceilings on, isometric, plan), to free the CPU for the video encode and
for testing the new interface. The test was killed before it wrote its results (`../live_test.log` ends with the browser
being closed), so no pass / fail is claimed from this run. The new build is tested in `../layout_test/`,
`../viewer_test_v3/` and `../firefox_check/`.
