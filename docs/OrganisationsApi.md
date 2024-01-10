# swagger_client.OrganisationsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_of_organisations_counts_organisations_v1_get**](OrganisationsApi.md#count_of_organisations_counts_organisations_v1_get) | **GET** /counts/organisations/v1 | Count Of Organisations
[**list_organisations_organisations_v1_get**](OrganisationsApi.md#list_organisations_organisations_v1_get) | **GET** /organisations/v1 | List Organisations
[**list_organisations_platforms_platform_organisations_v1_get**](OrganisationsApi.md#list_organisations_platforms_platform_organisations_v1_get) | **GET** /platforms/{platform}/organisations/v1 | List Organisations
[**organisation_organisations_v1_identifier_delete**](OrganisationsApi.md#organisation_organisations_v1_identifier_delete) | **DELETE** /organisations/v1/{identifier} | Organisation
[**organisation_organisations_v1_identifier_get**](OrganisationsApi.md#organisation_organisations_v1_identifier_get) | **GET** /organisations/v1/{identifier} | Organisation
[**organisation_organisations_v1_identifier_put**](OrganisationsApi.md#organisation_organisations_v1_identifier_put) | **PUT** /organisations/v1/{identifier} | Organisation
[**organisation_organisations_v1_post**](OrganisationsApi.md#organisation_organisations_v1_post) | **POST** /organisations/v1 | Organisation
[**organisation_platforms_platform_organisations_v1_identifier_get**](OrganisationsApi.md#organisation_platforms_platform_organisations_v1_identifier_get) | **GET** /platforms/{platform}/organisations/v1/{identifier} | Organisation

# **count_of_organisations_counts_organisations_v1_get**
> object count_of_organisations_counts_organisations_v1_get()

Count Of Organisations

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.OrganisationsApi()

try:
    # Count Of Organisations
    api_response = api_instance.count_of_organisations_counts_organisations_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganisationsApi->count_of_organisations_counts_organisations_v1_get: %s\n" % e)
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

# **list_organisations_organisations_v1_get**
> object list_organisations_organisations_v1_get(schema=schema, offset=offset, limit=limit)

List Organisations

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.OrganisationsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Organisations
    api_response = api_instance.list_organisations_organisations_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganisationsApi->list_organisations_organisations_v1_get: %s\n" % e)
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

# **list_organisations_platforms_platform_organisations_v1_get**
> object list_organisations_platforms_platform_organisations_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Organisations

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.OrganisationsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Organisations
    api_response = api_instance.list_organisations_platforms_platform_organisations_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganisationsApi->list_organisations_platforms_platform_organisations_v1_get: %s\n" % e)
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

# **organisation_organisations_v1_identifier_delete**
> object organisation_organisations_v1_identifier_delete(identifier)

Organisation

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.OrganisationsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Organisation
    api_response = api_instance.organisation_organisations_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganisationsApi->organisation_organisations_v1_identifier_delete: %s\n" % e)
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

# **organisation_organisations_v1_identifier_get**
> OrganisationRead organisation_organisations_v1_identifier_get(identifier, schema=schema)

Organisation

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.OrganisationsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Organisation
    api_response = api_instance.organisation_organisations_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganisationsApi->organisation_organisations_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**OrganisationRead**](OrganisationRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organisation_organisations_v1_identifier_put**
> object organisation_organisations_v1_identifier_put(body, identifier)

Organisation

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.OrganisationsApi(swagger_client.ApiClient(configuration))
body = swagger_client.OrganisationCreate() # OrganisationCreate | 
identifier = NULL # object | 

try:
    # Organisation
    api_response = api_instance.organisation_organisations_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganisationsApi->organisation_organisations_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OrganisationCreate**](OrganisationCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organisation_organisations_v1_post**
> object organisation_organisations_v1_post(body)

Organisation

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.OrganisationsApi(swagger_client.ApiClient(configuration))
body = swagger_client.OrganisationCreate() # OrganisationCreate | 

try:
    # Organisation
    api_response = api_instance.organisation_organisations_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganisationsApi->organisation_organisations_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OrganisationCreate**](OrganisationCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **organisation_platforms_platform_organisations_v1_identifier_get**
> OrganisationRead organisation_platforms_platform_organisations_v1_identifier_get(identifier, platform, schema=schema)

Organisation

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.OrganisationsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Organisation
    api_response = api_instance.organisation_platforms_platform_organisations_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrganisationsApi->organisation_platforms_platform_organisations_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**OrganisationRead**](OrganisationRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

