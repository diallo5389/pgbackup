from argparse import Action, ArgumentParser
import time
#commentaire test
class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        namespace.driver = driver.lower()
        namespace.destination = destination



def create_parser():
    parser = ArgumentParser(description="""
    Back up PostgreSQL databases locally or to AWS S3.
    """)
        
    parser.add_argument("url", help="URL of the DB")
    parser.add_argument("--driver","-d",
        help="Ou et comment socker le backup",
        nargs=2,
        metavar=("DRIVER","DESTINATION"),
        action=DriverAction,
        required=True)
    
    return parser


def main():
    import boto3
    from pgbackup import pgdump, stockage
    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    timestamp = time.strftime("%Y-%m-%dT%H%M", time.localtime())
    file_name = pgdump.dump_file_name(args.url, timestamp)
    if args.driver == 's3':
        client = boto3.client('s3')
        # TODO: create a better name based on the database name and the date
        print(f"Backing database up to {args.destination} in S3 as {file_name}")
        stockage.s3(client, dump.stdout, args.destination, file_name)
    else:
         outfile = open(args.destination, 'wb')
         print(f"Backing database up to {outfile.name} in local as {file_name}")
         stockage.local(dump.stdout, outfile)

