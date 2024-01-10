# SchemaDotOrgDataDownload

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **object** |  | [optional] 
**name** | **object** | The name of the item. | [optional] 
**content_url** | **object** | Actual bytes of the media object, for example the image file or video file. | 
**content_size** | **object** | File size in (mega/kilo) bytes. | [optional] 
**encoding_format** | **object** | Media type typically expressed using a MIME format (see [IANA site](http://www.iana.org/assignments/media-types/media-types.xhtml) and [MDN reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types))e.g. application/zip for a SoftwareApplication binary, audio/mpeg for .mp3 etc.).In cases where a [[CreativeWork]] has several media type representations, [[encoding]]can be used to indicate each [[MediaObject]] alongside particular [[encodingFormat]]information. Unregistered or niche encoding and file formats can be indicated insteadvia the most appropriate URL, e.g. defining Web page or a Wikipedia/Wikidata entry. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

