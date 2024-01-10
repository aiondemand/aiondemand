# RunnableDistribution

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**platform** | **object** | The external platform from which this resource originates. Leave empty if this item originates from AIoD. If platform is not None, the platform_resource_identifier should be set as well. | [optional] 
**platform_resource_identifier** | **object** | A unique identifier issued by the external platform that&#x27;s specified in &#x27;platform&#x27;. Leave empty if this item is not part of an external platform. | [optional] 
**checksum** | **object** | The value of a checksum algorithm ran on this content. | [optional] 
**checksum_algorithm** | **object** | The checksum algorithm. | [optional] 
**copyright** | **object** |  | [optional] 
**content_url** | **object** |  | 
**content_size_kb** | **object** |  | [optional] 
**date_published** | **object** | The datetime (utc) on which this Distribution was first published on an external platform.  | [optional] 
**description** | **object** |  | [optional] 
**encoding_format** | **object** | The mimetype of this file. | [optional] 
**name** | **object** |  | [optional] 
**technology_readiness_level** | **object** | The technology readiness level (TRL) of the distribution. TRL 1 is the lowest and stands for &#x27;Basic principles observed&#x27;, TRL 9 is the highest and stands for &#x27;actual system proven in operational environment&#x27;. | [optional] 
**installation_script** | **object** | An url pointing to a script that can be run to setup the environment necessary for running this distribution. This can be a relative url, if this distribution is a file archive. | [optional] 
**installation** | **object** | A human readable explanation of the installation, primarily meant as alternative for when there is no installation script. | [optional] 
**installation_time_milliseconds** | **object** | An illustrative time that the installation might typically take. | [optional] 
**deployment_script** | **object** | An url pointing to a script that can be run to use this resource. This can be a relative url, if this distribution is a file archive. | [optional] 
**deployment** | **object** | A human readable explanation of the deployment, primarily meant as alternative for when there is no installation script. | [optional] 
**deployment_time_milliseconds** | **object** | An illustrative time that the deployment might typically take. | [optional] 
**os_requirement** | **object** | A human readable explanation for the required os. | [optional] 
**dependency** | **object** | A human readable explanation of (software) dependencies. | [optional] 
**hardware_requirement** | **object** | A human readable explanation of hardware requirements. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

