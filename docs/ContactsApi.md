# swagger_client.ContactsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**contact_contacts_v1_identifier_delete**](ContactsApi.md#contact_contacts_v1_identifier_delete) | **DELETE** /contacts/v1/{identifier} | Contact
[**contact_contacts_v1_identifier_get**](ContactsApi.md#contact_contacts_v1_identifier_get) | **GET** /contacts/v1/{identifier} | Contact
[**contact_contacts_v1_identifier_put**](ContactsApi.md#contact_contacts_v1_identifier_put) | **PUT** /contacts/v1/{identifier} | Contact
[**contact_contacts_v1_post**](ContactsApi.md#contact_contacts_v1_post) | **POST** /contacts/v1 | Contact
[**contact_platforms_platform_contacts_v1_identifier_get**](ContactsApi.md#contact_platforms_platform_contacts_v1_identifier_get) | **GET** /platforms/{platform}/contacts/v1/{identifier} | Contact
[**count_of_contacts_counts_contacts_v1_get**](ContactsApi.md#count_of_contacts_counts_contacts_v1_get) | **GET** /counts/contacts/v1 | Count Of Contacts
[**list_contacts_contacts_v1_get**](ContactsApi.md#list_contacts_contacts_v1_get) | **GET** /contacts/v1 | List Contacts
[**list_contacts_platforms_platform_contacts_v1_get**](ContactsApi.md#list_contacts_platforms_platform_contacts_v1_get) | **GET** /platforms/{platform}/contacts/v1 | List Contacts

# **contact_contacts_v1_identifier_delete**
> object contact_contacts_v1_identifier_delete(identifier)

Contact

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ContactsApi(swagger_client.ApiClient(configuration))
identifier = NULL # object | 

try:
    # Contact
    api_response = api_instance.contact_contacts_v1_identifier_delete(identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->contact_contacts_v1_identifier_delete: %s\n" % e)
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

# **contact_contacts_v1_identifier_get**
> ContactRead contact_contacts_v1_identifier_get(identifier, schema=schema)

Contact

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ContactsApi()
identifier = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Contact
    api_response = api_instance.contact_contacts_v1_identifier_get(identifier, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->contact_contacts_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ContactRead**](ContactRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contact_contacts_v1_identifier_put**
> object contact_contacts_v1_identifier_put(body, identifier)

Contact

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ContactsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ContactCreate() # ContactCreate | 
identifier = NULL # object | 

try:
    # Contact
    api_response = api_instance.contact_contacts_v1_identifier_put(body, identifier)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->contact_contacts_v1_identifier_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ContactCreate**](ContactCreate.md)|  | 
 **identifier** | [**object**](.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contact_contacts_v1_post**
> object contact_contacts_v1_post(body)

Contact

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ContactsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ContactCreate() # ContactCreate | 

try:
    # Contact
    api_response = api_instance.contact_contacts_v1_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->contact_contacts_v1_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ContactCreate**](ContactCreate.md)|  | 

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contact_platforms_platform_contacts_v1_identifier_get**
> ContactRead contact_platforms_platform_contacts_v1_identifier_get(identifier, platform, schema=schema)

Contact

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ContactsApi()
identifier = NULL # object | 
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)

try:
    # Contact
    api_response = api_instance.contact_platforms_platform_contacts_v1_identifier_get(identifier, platform, schema=schema)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->contact_platforms_platform_contacts_v1_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | [**object**](.md)|  | 
 **platform** | [**object**](.md)|  | 
 **schema** | [**object**](.md)|  | [optional] [default to aiod]

### Return type

[**ContactRead**](ContactRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **count_of_contacts_counts_contacts_v1_get**
> object count_of_contacts_counts_contacts_v1_get()

Count Of Contacts

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ContactsApi()

try:
    # Count Of Contacts
    api_response = api_instance.count_of_contacts_counts_contacts_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->count_of_contacts_counts_contacts_v1_get: %s\n" % e)
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

# **list_contacts_contacts_v1_get**
> object list_contacts_contacts_v1_get(schema=schema, offset=offset, limit=limit)

List Contacts

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ContactsApi()
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Contacts
    api_response = api_instance.list_contacts_contacts_v1_get(schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->list_contacts_contacts_v1_get: %s\n" % e)
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

# **list_contacts_platforms_platform_contacts_v1_get**
> object list_contacts_platforms_platform_contacts_v1_get(platform, schema=schema, offset=offset, limit=limit)

List Contacts

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ContactsApi()
platform = NULL # object | 
schema = aiod # object |  (optional) (default to aiod)
offset = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # List Contacts
    api_response = api_instance.list_contacts_platforms_platform_contacts_v1_get(platform, schema=schema, offset=offset, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->list_contacts_platforms_platform_contacts_v1_get: %s\n" % e)
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

