import boto3
import logging
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client("ec2")

RETENTION_DAYS = 365

def lambda_handler(event, context):
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)

    deleted = []
    skipped = []
    failed = []

    try:
        paginator = ec2.get_paginator("describe_snapshots")
        page_iterator = paginator.paginate(OwnerIds=["self"])

        for page in page_iterator:
            for snapshot in page.get("Snapshots", []):
                snapshot_id = snapshot["SnapshotId"]
                start_time = snapshot["StartTime"]

                if start_time < cutoff_date:
                    try:
                        logger.info(f"Deleting snapshot: {snapshot_id}")
                        ec2.delete_snapshot(SnapshotId=snapshot_id)
                        deleted.append(snapshot_id)
                    except ClientError as e:
                        logger.error(f"Failed to delete snapshot {snapshot_id}: {str(e)}")
                        failed.append(snapshot_id)
                else:
                    skipped.append(snapshot_id)

        result = {
            "deleted_count": len(deleted),
            "skipped_count": len(skipped),
            "failed_count": len(failed),
            "deleted_snapshots": deleted
        }

        logger.info(result)
        return result

    except ClientError as e:
        logger.error(f"Error retrieving snapshots: {str(e)}")
        raise
