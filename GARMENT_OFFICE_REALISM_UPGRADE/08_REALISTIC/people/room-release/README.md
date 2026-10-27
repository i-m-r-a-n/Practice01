# Reception and Boardroom incremental release

This entrypoint combines exactly ten static fictional people: the four accepted Reception actors in Z02 and six Boardroom actors in Z08. Use `manifestFile: 'room-release/people-manifest.json'`, `frozen: true`, and `activeZones: ['Z02', 'Z08']`. Keep the existing People on/off control and “People shown are illustrative” note.

Reception source files remain byte-for-byte unchanged. The first four actor definitions, the badge and fabric-book definitions, and all four referenced Reception pose definitions are deep-equal to their accepted sources. The cumulative pose file contains only the ten required outfit/pose entries. No other rooms receive people through this manifest.

`source-lock.json` binds the exact runtime files and references the accepted Reception inputs. The approved office blend remains `fa3ed3d58f6d44c3554e3761307841b96115ff7816e4e541c8e6611cb363810d`; its geometry is never opened or altered by `../boardroom/prepare_static.py`.

See `../reception/ACCEPTANCE.md` and the Boardroom independent review for bounded contact evidence. Final viewer integration, the People toggle and source preservation are checked separately from candidate generation.
