# Changelog

<!--next-version-placeholder-->
## v0.2.2 (2025-09-23)
 - Added `aiod.bookmarks` module
 - Added `aiod.get` function for fetching any asset type
 - Added a way to authenticate using a `client_secret`
 - Make Python 3.10 compatible by removing the use of `tomllib`

## v0.2.1 (2025-09-16)

- `create_token(write_to_file=True)` now works even if the parent directories don't exist
- Add a `replace` function for all asset types which completely replaces the asset

## v0.2.0 (2025-09-15)

- Added [authentication](api/authentication.md) to allow authenticated requests.
- Default to version 2 of the REST API.
- Added new methods for uploading, updating, and deleting assets.
- Added new methods obtaining information on taxonomies.
- Updated the documentation significantly.


## v0.1.0 (2023-12-06)

- First release of `aiondemand`!
