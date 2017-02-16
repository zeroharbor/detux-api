[![Say Thanks](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg?style=flat)](https://saythanks.io/to/deadbits) [![Donate](https://img.shields.io/badge/donate-BTC-blue.svg?style=flat)](https://www.coinbase.com/deadbits)

# detux-api
Library to interact with the Detux.org Linux sandbox API written in Python. The author and this project is not affiliated with Detux.org in any way.

## Features
- Search Detux.org by
    - Individual hash
    - Text file list of hashes
    - Hashes of all files in a given directory
- Submit files for analysis
    - Submit a single file or an entire directory of files
        - Multithreading optional for submissions that act on more than one file or hash
    - Provide filenames for submissions
    - Submissions can optionally be marked as private (not yet implemented)
    - Submissions can optionally include user comments (not yet implemented)
- Retrieve analysis reports
    - Return raw JSON reports
    - Save JSON reports to a nicely formatted local file
    - Upload JSON reports to an AWS S3 bucket
- Optional multithreading on tasks that act against more than a single file or hash

### Example Uses
Real documentation will be coming in the 'docs' folder after I finish out the library.

***
- **Check if a sample has already been uploaded and if not analyze it then save the report to a local JSON file**

```
detux = Detux('your api key')
sample_hash = detux.Utils.get_sha256('/path/to/evilmalware')

if not detux.search(sample_hash):
    submission = detux.submit_file('/path/to/evilmalware')
    # might want to wait a bit for the file to be analyzed before this next step ...
    report_name = '%s.json' % sample_hash
    new_report = detux.report(submission.sha256, save='json', output=report_name)
```

***
- **Save a report to an S3 location**

```
detux.verbose = True
detux.report('7d9291fbd5ba96ede386e688584a6f873615a141a5363d4431499de5415c02c4',
    save='s3', s3_bucket='samples', aws_key='your access ID key', aws_secret='your secret key',
    output_file='myfolder/zeroaccess1.json')
```

***
- **Submit a directory of malware samples and store the results**

Submit directory will keep a list of the JSON results returned from the submissions so you can iterate through them afterwards
to ensure everything was correctly uploaded.

```
# submit directory of samples using 5 threads
results = detux.submit_directory('/path/to/malware/dir', threads=5)

# submit directory of samples and send their base filename to Detux
# the "threads" argument defaults to None so this example is not threaded
results2 = detux.submit_directory('/path/to/malware/dir', use_filenames=True)


```


***
- **Next Example**


### License
This project uses the GNU GPLv3 license and is made available in it's full form in the `LICENSE` file.
