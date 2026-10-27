# Live site after GPT fix (frontend 6be2c0f, Worker deployment 7066e29a), checked 27 Oct 2026 ~17:30 Dhaka

- Chromium (software GPU) on the live URL: Reception and Boardroom land on their render cameras with correct geometry
  (`live_fixed_reception.jpg`, `live_fixed_boardroom.jpg`); 0 page errors.
- Firefox 159 on a local copy of the exact live files (`index.html` + `app.js?v=6be2c0f4a899`, sha256 c6af8144...; model =
  the same 19,452,524-byte baked GLB): Reception and Boardroom correct, 0 errors (`firefox_live_*.jpg`). The live URL itself
  could not be opened in this sandbox's Firefox (the sandbox proxy certificate is not in Firefox's store).
- Still open on the live site: in the guided tour the room card and the tour bar overlap (`firefox_live_tour_stop3.jpg`);
  fixed in Claude's interface (`08_WORKER_READY_TOUR`, Mac package), not integrated by GPT.
- `/present`, `/pitch.mp4`, `/tour.mp4` (HTTP 206, video/mp4), `/presentation.pdf`, `/render-book.pdf`: HTTP 200.
