# SchemaDotOrgDataset

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**context** | **object** |  | [optional] 
**type** | **object** |  | [optional] 
**name** | **object** | The name of the item. | 
**description** | **object** | A description of the item. | [optional] 
**identifier** | **object** | The AIoD identifier | 
**alternate_name** | **object** | An alias for the item. | [optional] 
**citation** | **object** | A reference to another creative work, such as another publication, web page,scholarly article, etc. | [optional] 
**creator** | **object** | The creator/author of this CreativeWork. This is the same as the Author property for CreativeWork. | [optional] 
**date_modified** | **object** | The date on which the CreativeWork was most recently modified or when the item&#x27;s entry was modified within a DataFeed. | [optional] 
**date_published** | **object** | Date of first broadcast/publication. | [optional] 
**is_accessible_for_free** | **object** | A flag to signal that the item, event, or place is accessible for free. | [optional] 
**keywords** | **object** | Keywords or tags used to describe this content. Multiple entries in a keywords list are typically delimited by commas. | [optional] 
**same_as** | **object** | URL of a reference Web page that unambiguously indicates the item&#x27;s identity. E.g. the URL of the item&#x27;s Wikipedia page, Wikidata entry, or official website. | [optional] 
**version** | **object** | The version of the CreativeWork embodied by a specified resource. | [optional] 
**url** | **object** | URL of the item. | [optional] 
**distribution** | **object** | A downloadable form of this dataset, at a specific location, in a specific format. | [optional] 
**funder** | **object** | A person or organization that supports (sponsors) something through some kind of financialcontribution. | [optional] 
**issn** | **object** | The International Standard Serial Number (ISSN) that identifies this serial publication. You can repeat this property to identify different formats of, or the linking ISSN (ISSN-L) for, this serial publication. | [optional] 
**license** | **object** | A license document that applies to this content, typically indicated by URL. | [optional] 
**measurement_technique** | **object** | A technique or technology used in a [[Dataset]] (or [[DataDownload]], [[DataCatalog]]), corresponding to the method used for measuring the corresponding variable(s) (described using [[variableMeasured]]). This is oriented towards scientific and scholarly dataset publication but may have broader applicability; it is not intended as a full representation of measurement, but rather as a high level summary for dataset discovery. For example, if [[variableMeasured]] is: molecule concentration, [[measurementTechnique]] could be: \&quot;mass spectrometry\&quot; or \&quot;nmr spectroscopy\&quot; or \&quot;colorimetry\&quot; or \&quot;immunofluorescence\&quot;. If the [[variableMeasured]] is \&quot;depression rating\&quot;, the [[measurementTechnique]] could be \&quot;Zung Scale\&quot; or \&quot;HAM-D\&quot; or \&quot;Beck Depression Inventory\&quot;. If there are several [[variableMeasured]] properties recorded for some given data object, use a [[PropertyValue]] for each [[variableMeasured]] and attach the corresponding [[measurementTechnique]]. | [optional] 
**size** | **object** | A standardized size of a product or creative work, specified either through a simple textual string (for example &#x27;XL&#x27;, &#x27;32Wx34L&#x27;), a QuantitativeValue with a unitCode, | [optional] 
**temporal_coverage** | **object** | The temporalCoverage of a CreativeWork indicates the period that the content applies to, i.e. that it describes, either as a DateTime or as a textual string indicating a time period in [ISO 8601 time interval format](https://en.wikipedia.org/wiki/ISO_8601#Time_intervals).In the case of a Dataset it will typically indicate the relevant time period in a precise notation (e.g. for a 2011 census dataset, the year 2011 would be written \&quot;2011/2012\&quot;). Other forms of content e.g. ScholarlyArticle, Book, TVSeries or TVEpisode may indicate their temporalCoverage in broader terms - textually or via well-known URL. Written works such as books may sometimes have precise temporal coverage too, e.g. a work set in 1939 - 1945 can be indicated in ISO 8601 interval format format via \&quot;1939/1945\&quot;. Open-ended date ranges can be written with \&quot;..\&quot; in place of the end date. For example, \&quot;2015-11/..\&quot; indicates a range beginning in November 2015 and with no specified final date. This is tentative and might be updated in future when ISO 8601 is officially updated. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

