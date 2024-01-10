# swagger_client.EnumsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**application_area_application_areas_v1_get**](EnumsApi.md#application_area_application_areas_v1_get) | **GET** /application_areas/v1 | Application Area
[**badge_badges_v1_get**](EnumsApi.md#badge_badges_v1_get) | **GET** /badges/v1 | Badge
[**computational_asset_type_computational_asset_types_v1_get**](EnumsApi.md#computational_asset_type_computational_asset_types_v1_get) | **GET** /computational_asset_types/v1 | Computational Asset Type
[**edu_access_mode_edu_access_modes_v1_get**](EnumsApi.md#edu_access_mode_edu_access_modes_v1_get) | **GET** /edu_access_modes/v1 | Edu Access Mode
[**edu_educational_level_edu_educational_levels_v1_get**](EnumsApi.md#edu_educational_level_edu_educational_levels_v1_get) | **GET** /edu_educational_levels/v1 | Edu Educational Level
[**edu_pace_edu_paces_v1_get**](EnumsApi.md#edu_pace_edu_paces_v1_get) | **GET** /edu_paces/v1 | Edu Pace
[**edu_prerequisite_edu_prerequisites_v1_get**](EnumsApi.md#edu_prerequisite_edu_prerequisites_v1_get) | **GET** /edu_prerequisites/v1 | Edu Prerequisite
[**edu_target_audience_edu_target_audiences_v1_get**](EnumsApi.md#edu_target_audience_edu_target_audiences_v1_get) | **GET** /edu_target_audiences/v1 | Edu Target Audience
[**educational_resource_type_educational_resource_types_v1_get**](EnumsApi.md#educational_resource_type_educational_resource_types_v1_get) | **GET** /educational_resource_types/v1 | Educational Resource Type
[**event_mode_event_modes_v1_get**](EnumsApi.md#event_mode_event_modes_v1_get) | **GET** /event_modes/v1 | Event Mode
[**event_status_event_status_v1_get**](EnumsApi.md#event_status_event_status_v1_get) | **GET** /event_status/v1 | Event Status
[**expertise_expertises_v1_get**](EnumsApi.md#expertise_expertises_v1_get) | **GET** /expertises/v1 | Expertise
[**industrial_sector_industrial_sectors_v1_get**](EnumsApi.md#industrial_sector_industrial_sectors_v1_get) | **GET** /industrial_sectors/v1 | Industrial Sector
[**keyword_keywords_v1_get**](EnumsApi.md#keyword_keywords_v1_get) | **GET** /keywords/v1 | Keyword
[**language_languages_v1_get**](EnumsApi.md#language_languages_v1_get) | **GET** /languages/v1 | Language
[**license_licenses_v1_get**](EnumsApi.md#license_licenses_v1_get) | **GET** /licenses/v1 | License
[**ml_model_type_ml_model_types_v1_get**](EnumsApi.md#ml_model_type_ml_model_types_v1_get) | **GET** /ml_model_types/v1 | Ml Model Type
[**news_category_news_categorys_v1_get**](EnumsApi.md#news_category_news_categorys_v1_get) | **GET** /news_categorys/v1 | News Category
[**organisation_type_organisation_types_v1_get**](EnumsApi.md#organisation_type_organisation_types_v1_get) | **GET** /organisation_types/v1 | Organisation Type
[**publication_type_publication_types_v1_get**](EnumsApi.md#publication_type_publication_types_v1_get) | **GET** /publication_types/v1 | Publication Type
[**relevant_link_relevant_links_v1_get**](EnumsApi.md#relevant_link_relevant_links_v1_get) | **GET** /relevant_links/v1 | Relevant Link
[**research_area_research_areas_v1_get**](EnumsApi.md#research_area_research_areas_v1_get) | **GET** /research_areas/v1 | Research Area
[**scientific_domain_scientific_domains_v1_get**](EnumsApi.md#scientific_domain_scientific_domains_v1_get) | **GET** /scientific_domains/v1 | Scientific Domain
[**status_status_v1_get**](EnumsApi.md#status_status_v1_get) | **GET** /status/v1 | Status

# **application_area_application_areas_v1_get**
> object application_area_application_areas_v1_get()

Application Area

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Application Area
    api_response = api_instance.application_area_application_areas_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->application_area_application_areas_v1_get: %s\n" % e)
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

# **badge_badges_v1_get**
> object badge_badges_v1_get()

Badge

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Badge
    api_response = api_instance.badge_badges_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->badge_badges_v1_get: %s\n" % e)
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

# **computational_asset_type_computational_asset_types_v1_get**
> object computational_asset_type_computational_asset_types_v1_get()

Computational Asset Type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Computational Asset Type
    api_response = api_instance.computational_asset_type_computational_asset_types_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->computational_asset_type_computational_asset_types_v1_get: %s\n" % e)
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

# **edu_access_mode_edu_access_modes_v1_get**
> object edu_access_mode_edu_access_modes_v1_get()

Edu Access Mode

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Edu Access Mode
    api_response = api_instance.edu_access_mode_edu_access_modes_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->edu_access_mode_edu_access_modes_v1_get: %s\n" % e)
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

# **edu_educational_level_edu_educational_levels_v1_get**
> object edu_educational_level_edu_educational_levels_v1_get()

Edu Educational Level

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Edu Educational Level
    api_response = api_instance.edu_educational_level_edu_educational_levels_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->edu_educational_level_edu_educational_levels_v1_get: %s\n" % e)
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

# **edu_pace_edu_paces_v1_get**
> object edu_pace_edu_paces_v1_get()

Edu Pace

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Edu Pace
    api_response = api_instance.edu_pace_edu_paces_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->edu_pace_edu_paces_v1_get: %s\n" % e)
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

# **edu_prerequisite_edu_prerequisites_v1_get**
> object edu_prerequisite_edu_prerequisites_v1_get()

Edu Prerequisite

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Edu Prerequisite
    api_response = api_instance.edu_prerequisite_edu_prerequisites_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->edu_prerequisite_edu_prerequisites_v1_get: %s\n" % e)
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

# **edu_target_audience_edu_target_audiences_v1_get**
> object edu_target_audience_edu_target_audiences_v1_get()

Edu Target Audience

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Edu Target Audience
    api_response = api_instance.edu_target_audience_edu_target_audiences_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->edu_target_audience_edu_target_audiences_v1_get: %s\n" % e)
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

# **educational_resource_type_educational_resource_types_v1_get**
> object educational_resource_type_educational_resource_types_v1_get()

Educational Resource Type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Educational Resource Type
    api_response = api_instance.educational_resource_type_educational_resource_types_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->educational_resource_type_educational_resource_types_v1_get: %s\n" % e)
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

# **event_mode_event_modes_v1_get**
> object event_mode_event_modes_v1_get()

Event Mode

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Event Mode
    api_response = api_instance.event_mode_event_modes_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->event_mode_event_modes_v1_get: %s\n" % e)
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

# **event_status_event_status_v1_get**
> object event_status_event_status_v1_get()

Event Status

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Event Status
    api_response = api_instance.event_status_event_status_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->event_status_event_status_v1_get: %s\n" % e)
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

# **expertise_expertises_v1_get**
> object expertise_expertises_v1_get()

Expertise

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Expertise
    api_response = api_instance.expertise_expertises_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->expertise_expertises_v1_get: %s\n" % e)
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

# **industrial_sector_industrial_sectors_v1_get**
> object industrial_sector_industrial_sectors_v1_get()

Industrial Sector

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Industrial Sector
    api_response = api_instance.industrial_sector_industrial_sectors_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->industrial_sector_industrial_sectors_v1_get: %s\n" % e)
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

# **keyword_keywords_v1_get**
> object keyword_keywords_v1_get()

Keyword

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Keyword
    api_response = api_instance.keyword_keywords_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->keyword_keywords_v1_get: %s\n" % e)
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

# **language_languages_v1_get**
> object language_languages_v1_get()

Language

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Language
    api_response = api_instance.language_languages_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->language_languages_v1_get: %s\n" % e)
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

# **license_licenses_v1_get**
> object license_licenses_v1_get()

License

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # License
    api_response = api_instance.license_licenses_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->license_licenses_v1_get: %s\n" % e)
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

# **ml_model_type_ml_model_types_v1_get**
> object ml_model_type_ml_model_types_v1_get()

Ml Model Type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Ml Model Type
    api_response = api_instance.ml_model_type_ml_model_types_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->ml_model_type_ml_model_types_v1_get: %s\n" % e)
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

# **news_category_news_categorys_v1_get**
> object news_category_news_categorys_v1_get()

News Category

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # News Category
    api_response = api_instance.news_category_news_categorys_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->news_category_news_categorys_v1_get: %s\n" % e)
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

# **organisation_type_organisation_types_v1_get**
> object organisation_type_organisation_types_v1_get()

Organisation Type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Organisation Type
    api_response = api_instance.organisation_type_organisation_types_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->organisation_type_organisation_types_v1_get: %s\n" % e)
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

# **publication_type_publication_types_v1_get**
> object publication_type_publication_types_v1_get()

Publication Type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Publication Type
    api_response = api_instance.publication_type_publication_types_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->publication_type_publication_types_v1_get: %s\n" % e)
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

# **relevant_link_relevant_links_v1_get**
> object relevant_link_relevant_links_v1_get()

Relevant Link

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Relevant Link
    api_response = api_instance.relevant_link_relevant_links_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->relevant_link_relevant_links_v1_get: %s\n" % e)
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

# **research_area_research_areas_v1_get**
> object research_area_research_areas_v1_get()

Research Area

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Research Area
    api_response = api_instance.research_area_research_areas_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->research_area_research_areas_v1_get: %s\n" % e)
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

# **scientific_domain_scientific_domains_v1_get**
> object scientific_domain_scientific_domains_v1_get()

Scientific Domain

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Scientific Domain
    api_response = api_instance.scientific_domain_scientific_domains_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->scientific_domain_scientific_domains_v1_get: %s\n" % e)
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

# **status_status_v1_get**
> object status_status_v1_get()

Status

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.EnumsApi()

try:
    # Status
    api_response = api_instance.status_status_v1_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnumsApi->status_status_v1_get: %s\n" % e)
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

