# detux-api
Library to interact with the Detux.org Linux sandbox API written in Python. The author and this project is not affiliated with Detux.org in any way. Better documentation is coming. This commit date is the same day I'm finishing up testing so just hold out a bit longer ;-)

## Requirements
- Detux.org account and API key
- Python 2.7 or higher
- Python `requests` library
- Some Linux malware you want to research :)

### Features
- Search Detux.org by
    - Individual hash
    - Text file list of hashes
    - Hashes of all files in a given directory
- Submit files for analysis
    - You can submit a single file or an entire directory of files
    - Provide filenames for submissions
    - Submissions can optionally be marked as private
    - Submissions can optionally include user comments
- Retrieve analysis reports
    - Return raw JSON report for use in your own scripts
    - Save the JSON report to a nicely formatted file
- Optional multithreading on tasks that act against more than a single file or hash


### Example Uses

- **Check if a sample has already been uploaded and if not analyze it then save the report**
```
detux = Detux('your api key')

sample_hash = detux.utils.get_sha256('/path/to/evilmalware')
if not detux.search(sample_hash):
    submission = detux.submit('/path/to/evilmalware')
    # might want to wait a bit for the file to be analyzed before this next step ...
    report_name = '%s.json' % sample_hash
    new_report = detux.report(submission.sha256, save=True, output=report_name)
```

- **Submit a directory of malware samples**
```
detux = Detux('your api key')
detux.submit_directory('/path/to/malware/dir', threads=5)
```
