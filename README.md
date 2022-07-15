## JSON REDO log service

* This service provide resend/reply functionality of pending operations from JSON log file.
* Program send SMS, make POST request and sent emails using high-level design with
hidden implementations of end service providers.
* All notifications which must be processed  are validated and information of invalid data logged in system.
* There were also attempts for handle interaction errors with end service providers which could be 
used for autoretry send notifications.
* Successfully operations would be stored in result JSON file.


### Getting started
Setup environment configuration (create .env file in the root of directory).
You could provide your own url to JSON file with setup REDO_DATA_SOURCE_URL.

  <details>
    <summary><i><b>.env</b> example</i></summary>

  ```buildoutcfg
  REDO_DATA_SOURCE_URL=<some_url_to_json_file>
  ```
  </details>

If not - default url would be used.
