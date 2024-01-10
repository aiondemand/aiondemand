# swagger_client.PublicationsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_publications_counts_publications_v1_get**](PublicationsApi.md#count_of_publications_counts_publications_v1_get) | **GET** /counts/publications/v1 | Count Of Publications
[**list_publications_platforms_platform_publications_v1_get**](PublicationsApi.md#list_publications_platforms_platform_publications_v1_get) | **GET** /platforms/{platform}/publications/v1 | List Publications
[**list_publications_publications_v1_get**](PublicationsApi.md#list_publications_publications_v1_get) | **GET** /publications/v1 | List Publications
[**publication_platforms_platform_publications_v1_identifier_get**](PublicationsApi.md#publication_platforms_platform_publications_v1_identifier_get) | **GET** /platforms/{platform}/publications/v1/{identifier} | Publication
[**publication_publications_v1_identifier_content_distribution_idx_get**](PublicationsApi.md#publication_publications_v1_identifier_content_distribution_idx_get) | **GET** /publications/v1/{identifier}/content/{distribution_idx} | Publication
[**publication_publications_v1_identifier_content_get**](PublicationsApi.md#publication_publications_v1_identifier_content_get) | **GET** /publications/v1/{identifier}/content | Publication
[**publication_publications_v1_identifier_delete**](PublicationsApi.md#publication_publications_v1_identifier_delete) | **DELETE** /publications/v1/{identifier} | Publication
[**publication_publications_v1_identifier_get**](PublicationsApi.md#publication_publications_v1_identifier_get) | **GET** /publications/v1/{identifier} | Publication
[**publication_publications_v1_identifier_put**](PublicationsApi.md#publication_publications_v1_identifier_put) | **PUT** /publications/v1/{identifier} | Publication
[**publication_publications_v1_post**](PublicationsApi.md#publication_publications_v1_post) | **POST** /publications/v1 | Publication

# **count_of_publications_counts_publications_v1_get**
> object count_of_publications_counts_publications_v1_get()

Count Of Publications

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()

try:
    # Count Of Publications
    api_response = api_instance.count_of_publications_counts_publications_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->count_of_publications_counts_publications_v1_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_publications_platforms_platform_publications_v1_get**
> object list_publications_platforms_platform_publications_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Publications

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Publications
    api_response = api_instance.list_publications_platforms_platform_publications_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->list_publications_platforms_platform_publications_v1_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]
 **offset** | [**object**](.md)|  | [optional] [default to 0]
 **limit** | [**object**](.md)|  | [optional] [default to 100]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_publications_publications_v1_get**
> object list_publications_publications_v1_get(schema=schema, offset=offset, limit=limit)

List Publications

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Publications
    api_response = api_instance.list_publications_publications_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->list_publications_publications_v1_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **schema** | [**object**](.md)|  | [optional] [default to aiod]
 **offset** | [**object**](.md)|  | [optional] [default to 0]
 **limit** | [**object**](.md)|  | [optional] [default to 100]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **publication_platforms_platform_publications_v1_identifier_get**
> PublicationRead publication_platforms_platform_publications_v1_identifier_get(identifier, platform, schema=schema)

Publication

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Publication
    api_response = api_instance.publication_platforms_platform_publications_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->publication_platforms_platform_publications_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**PublicationRead**](PublicationRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **publication_publications_v1_identifier_content_distribution_idx_get**
> object publication_publications_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)

Publication

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()
identifier = NULL # object | 
distribution_idx = NULL # object | 
default = false # object |  (optional) (default to false)

try:
    # Publication
    api_response = api_instance.publication_publications_v1_identifier_content_distribution_idx_get(identifier, distribution_idx, default=default)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->publication_publications_v1_identifier_content_distribution_idx_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **distribution_idx** | [**object**](.md)|  | 
 **default** | [**object**](.md)|  | [optional] [default to false]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **publication_publications_v1_identifier_content_get**
> object publication_publications_v1_identifier_content_get(identifier)

Publication

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()
identifier = NULL # object | 

try:
    # Publication
    api_response = api_instance.publication_publications_v1_identifier_content_get(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->publication_publications_v1_identifier_content_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **publication_publications_v1_identifier_delete**
> object publication_publications_v1_identifier_delete(identifier)

Publication

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PublicationsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Publication
    api_response = api_instance.publication_publications_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->publication_publications_v1_identifier_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **publication_publications_v1_identifier_get**
> PublicationRead publication_publications_v1_identifier_get(identifier, schema=schema)

Publication

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PublicationsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Publication
    api_response = api_instance.publication_publications_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->publication_publications_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**PublicationRead**](PublicationRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **publication_publications_v1_identifier_put**
> object publication_publications_v1_identifier_put(body, identifier)

Publication

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PublicationsApi(swagger_client.ApiClient(configuration))
body = swagger_client.PublicationCreate() # PublicationCreate | 
identifier = NULL # object | 

try:
    # Publication
    api_response = api_instance.publication_publications_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->publication_publications_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PublicationCreate**](PublicationCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **publication_publications_v1_post**
> object publication_publications_v1_post(body)

Publication

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PublicationsApi(swagger_client.ApiClient(configuration))
body = swagger_client.PublicationCreate() # PublicationCreate | 

try:
    # Publication
    api_response = api_instance.publication_publications_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PublicationsApi->publication_publications_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PublicationCreate**](PublicationCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

