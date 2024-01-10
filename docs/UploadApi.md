# swagger_client.UploadApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**hugging_face_upload_upload_datasets_identifier_huggingface_post**](UploadApi.md#hugging_face_upload_upload_datasets_identifier_huggingface_post) | **POST** /upload/datasets/{identifier}/huggingface | Huggingfaceupload

# **hugging_face_upload_upload_datasets_identifier_huggingface_post**
> object hugging_face_upload_upload_datasets_identifier_huggingface_post(file, token, username, identifier)

Huggingfaceupload

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UploadApi()
file = NULL # object | 
token = NULL # object | The access token of HuggingFace
username = NULL # object | The username of HuggingFace
identifier = NULL # object | 

try:
    # Huggingfaceupload
    api_response = api_instance.hugging_face_upload_upload_datasets_identifier_huggingface_post(file, token, username, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UploadApi->hugging_face_upload_upload_datasets_identifier_huggingface_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | [**object**](.md)|  | 
 **token** | [**object**](.md)| The access token of HuggingFace | 
 **username** | [**object**](.md)| The username of HuggingFace | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

