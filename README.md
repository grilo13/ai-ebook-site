# ai-ebook-site
Website to generate ebooks using AI


### Cors aws s3 policy

`[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]`

### To show the pdf file in the frame using the public aws url we need to give the correct content-type when uploading the file

- check this stack overflow issue: https://stackoverflow.com/questions/14150854/aws-s3-display-file-inline-instead-of-force-download?noredirect=1&lq=1
- and the extra args parameters - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
