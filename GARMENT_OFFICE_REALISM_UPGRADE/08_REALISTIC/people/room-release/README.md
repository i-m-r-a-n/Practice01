# Reception, Boardroom and Experience Centre incremental release

This entrypoint combines exactly thirteen static fictional people: four accepted Reception actors in Z02, six accepted Boardroom actors in Z08, and three Experience Centre actors in Z30. Use `manifestFile: 'room-release/people-manifest.json'`, `frozen: true`, and `activeZones: ['Z02', 'Z08', 'Z30']`. Keep the existing People on/off control and “People shown are illustrative” note.

Reception and Boardroom source files remain byte-for-byte unchanged. The first ten actor definitions, their four prop definitions, and all ten referenced pose definitions are deep-equal to published commit `039091d5d35ea97adf95ff439231f6336ed05381`. The cumulative pose file contains only the thirteen required outfit/pose entries. No other rooms receive people through this manifest. `preservation-check.json` records these comparisons and the four unchanged character GLB hashes.

`source-lock.json` binds the exact runtime files and references the accepted Reception inputs. The approved office blend remains `fa3ed3d58f6d44c3554e3761307841b96115ff7816e4e541c8e6611cb363810d`; its geometry is never opened or altered by `../boardroom/prepare_static.py`.

See `../reception/ACCEPTANCE.md` and the Boardroom independent review for bounded contact evidence. Final viewer integration, the People toggle and source preservation are checked separately from candidate generation.
