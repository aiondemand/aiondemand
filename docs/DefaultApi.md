# swagger_client.DefaultApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**home_get**](DefaultApi.md#home_get) | **GET** / | Home
[**test_authorization_authorization_test_get**](DefaultApi.md#test_authorization_authorization_test_get) | **GET** /authorization_test | Test Authorization

# **home_get**
> object home_get()

Home

Provides a redirect page to the docs.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()

try:
    # Home
    api_response = api_instance.home_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->home_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/html

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_authorization_authorization_test_get**
> object test_authorization_authorization_test_get()

Test Authorization

Returns the user, if authenticated correctly.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(configuration))

try:
    # Test Authorization
    api_response = api_instance.test_authorization_authorization_test_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->test_authorization_authorization_test_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[OpenIdConnect](../README.md#OpenIdConnect)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

