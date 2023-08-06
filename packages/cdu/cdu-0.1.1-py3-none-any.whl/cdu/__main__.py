"""Utility to calculate disk usage on cloud services"""

import sys
import argparse
from urllib.parse import urlparse
import boto3
import json
from .node import Node
from .progress import Progress
import time
from datetime import datetime

FORMAT_VERSION = 1

def main():
    """Entry-point when running the module as an executable"""

    parser = argparse.ArgumentParser(
        description="Utility to calculate disk usage on cloud services"
    )
    parser.add_argument('-p', metavar='aws_profile_name', type=str,
                        help='The name of the aws profile, defined in ~/.aws/credentials',
                        default=None, required=False)
    parser.add_argument('url', type=str, help="S3 URL to process")
    args = parser.parse_args()

    url = urlparse(args.url)

    if url.scheme == 's3':
        session = boto3.Session(profile_name=args.p)
        s3_client = session.client('s3')

        bucket = url.netloc
        # remove the first slash
        prefix = url.path[1:]

        output_filename = '%s_%s.cdu' % (
            bucket,
            datetime.now().replace(microsecond=0).isoformat('_')
        )
        output_file = open(output_filename, 'w')

        output_file.write('%s\n' % json.dumps([
            FORMAT_VERSION,
            bucket,
            prefix,
            int(time.time())
        ]))

        node = Node(bucket, prefix, s3_client, progress_bar=Progress(sys.stderr))
        for x in node.disk_usage():
            output_file.write('%s\n' % json.dumps(x.to_json()))

    else:
        raise Exception('Unsupported url: "%s". At the moment only s3:// is supported' % args.url)


if __name__ == "__main__":
    main()
