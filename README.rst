# Pipeline Telemetry

**Pipeline Telemetry** makes it easy for project to generate store telemetry data from within your data pipelines.

```python

    from counters import INVALID_DATA, PROCESSED_DATA_POINTS


    def my_data_pipeline():
        telemetry = Telemetry(**TELEMETRY_PARAMS)

        from url in data_urls:
            data = get_data_from_url(url)
            telemetry.add_telemetry_counter(telemetry_counter=URL_RETRIEVALS)    # increase counter for retrieved URLS
            if data.invalid:
                telemetry.add_telemetry_counter(telemetry_counter=INVALID_DATA)  # increase counter for failed retrievals
                continue
            
            processed_data_points = process_and_store_data(data)
            telemetry.add_telemetry_counter(                                     # increase counter number of datapoints retrieved
                telemetry_counter=PROCESSED_DATA_POINTS,
                increment=len(processed_data_points))  
        
        telemetry.save_and_close()
```

In this example data is retrieved for a list of urls. Total retrievals, insuccesfull retrievals as well as number of processed datapoints are stored in the telemetry object.
This allows you to closely monitor the quality and behavior of your datapipeline. For example all retrievals might be OK but if the number of processed datapoints suddenly drops there might be an issue with some the endpoints.



[![Supported Versions](https://img.shields.io/pypi/pyversions/pipeline-telemetry.svg)](https://pypi.org/project/pipeline-telemetry)
