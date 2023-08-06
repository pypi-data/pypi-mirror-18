"""Upload sites to aws s3 bucket for publish.
"""

import json
import os
from tqdm import tqdm

import boto3


def publish(config_fn):
  """Upload files in site to s3 bucket.

  Args:
    config_fn: configuration file in json format.
      Check the sample file for reference.
  """
  try:
    # load configs.
    configs = json.load(open(config_fn, "r"))
    local_dir = configs["local_folder"]
    s3_dir = configs["bucket_folder"]
    bucket = configs["bucket_name"]
    # create aws session.
    sess = boto3.session.Session(
        aws_access_key_id=configs['access_key'],
        aws_secret_access_key=configs['secret_key'],
        region_name=configs['region'])
    s3_client = sess.client("s3")
    print "s3 client created."
    # enumerate local files recursively
    for root, _, files in os.walk(local_dir):
      for filename in tqdm(files):
        _, file_ext = os.path.splitext(filename)
        # construct the full local path
        local_path = os.path.join(root, filename)
        # construct the relative path
        relative_path = os.path.relpath(local_path, local_dir)
        s3_path = os.path.join(s3_dir, relative_path)
        # upload. html is handled properly.
        print "Uploading {}".format(s3_path)
        content_type = ""
        if file_ext == "html":
          content_type = "text/html"
        s3_client.upload_file(
            Filename=local_path,
            Bucket=bucket,
            Key=s3_path,
            ExtraArgs={"ContentType": content_type})
  except Exception as ex:
    print "error in publish: {}".format(repr(ex))


if __name__ == "__main__":
  publish("config.fn")
