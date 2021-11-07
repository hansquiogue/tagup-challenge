# Tagup Data Engineering Challenge

Here is my submission for the Tagup data engineering challenge. 

I initially started this exercise by writing code and working with the data inside a Jupyter notebook. That work can be found [here](walkthrough.ipynb). The designs, visualizations, and summary statistics are explained there. 

Overall, I ended with a design that consisted of the following:

```
- xarray DataArrays
    - Each element represents each company machine

- Each DataArray element contains the machine's
    - Timestamps
    - Signal values by time
    - Labels
```

Afterwards, I wrote Python scripts based on my Jupyter notebook work to automate the ML pipeline process. 

I focused a lot on organization, reusability and scalability—I tried to ensure that the code was generalized and changable for different data inputs, as well written professionally. For example, if the ExampleCo, Inc company had new data, the scripts can handle that by changing some configuration parameters in [the configuration file](settings.json) and [the main script](main.py).

Note: the configuration file should normally be hidden and not on a public repository as it will contain sensitive company information. But for demonstration purposes (and to make the scripts work), I uploaded the file. The same reasoning applies to the uploaded database file.

The final data results can be downloaded from [an AWS S3 bucket](https://tagup-challenge-bucket.s3.amazonaws.com/ExampleCo%2C+Inc_data.nc) or on this GitHub repository labled 'ExampleCo, Inc_data.nc'.

## Python Script Setup

Prequisites: install necessary Python libraries with pip
- pandas
- xarray
- boto3
- sqlalchemy

After installing the required libraries, the main script can be ran:

```
python main.py
```

This will extract data from the ExampleCo, Inc database, transform and clean the data, and load everything to an Amazon S3 bucket. In order to automatically upload data to AWS, my personal configuration keys are needed. I did not upload these keys to this repository for security purposes so the script will initially skip over the AWS upload process unless `UPLOAD` is set to `True` in the [the main script](main.py). Note that the upload process will fail unless proper AWS credentials are given. For the purposes of this exercise, the default parameters in the main script are set to skip over the uploading process to avoid relating errors.

## Summarized Process

```
1) main.py - start script
2) setup.py - load company info from settings.json
3) db.py/dbManager.py - join requested data and extract
4) transform.py - clean data and convert to xarray DataArrays
5) upload.py/uploadManager.py - upload DataArrays to Amazon S3
```