# detux-api
Library to interact with the Detux.org Linux sandbox API written in Python. The author and this project is not affiliated with Detux.org in any way. _Better documentation is coming._ These first few commit dates are literally as I am writing the code and testing it so just hold out a bit longer ;-)

## Requirements
- Detux.org account + API key
- Python 2.7 or higher
- Python `requests` library
- Python `boto3` library
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
    - Return raw JSON reports
    - Save JSON reports to a nicely formatted local file
    - Upload JSON reports to an AWS S3 bucket
- Optional multithreading on tasks that act against more than a single file or hash

### Example Uses
Real documentation will be coming after I finish out the library. This is just the initial code and README I've written over the past day-ish.

- **Check if a sample has already been uploaded and if not analyze it then save the report**
```
detux = Detux('your api key')
sample_hash = detux.Utils.get_sha256('/path/to/evilmalware')

if not detux.search(sample_hash):    
    submission = detux.submit_file('/path/to/evilmalware')    
    # might want to wait a bit for the file to be analyzed before this next step ...    
    report_name = '%s.json' % sample_hash    
    new_report = detux.report(submission.sha256, save=True, output=report_name)
```

***
- **Submit a directory of malware samples**
```
detux = Detux('your api key')
detux.submit_directory('/path/to/malware/dir', threads=5)
```

### License
This project uses the GNU GPLv3 license and is made available in it's full form in the `LICENSE` file.
