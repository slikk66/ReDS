![GitHub Logo](http://i.imgur.com/IAMScGQ.png)
# ReDS - ReActive Database System
RDS automatic resizing and scheduled scale up/down

##Save up to 50% on RDS costs and save yourself headache during traffic spikes

Creates multiple CloudFormation stacks to monitor your RDS instance and scale accordingly.

Requirements:
- run **make prep**
- only works on multi-AZ RDS

Tests
- run **make test**

Instructions:
- Modify lambda/vars.yaml to meet your needs.
- set "rds_identifier" to the name of your RDS
- If you want to enable scheduled scaling:
  - set schedule_enabled: True
  - set "cron" vars in UTC time to represent default start/stop
  - default cron vars are 9a-5p M-F Pacific (or close to it)
  - set "scheduled_index" to be the index of instance size in "instance_sizes" (starting from 0) that you want to scale up to during those hours
- After loading a profile from AWS CLI that has admin access, run from root:
    **make prod**
- This will create all the stacks, buckets, lambda, cloudwatch, IAM roles etc needed for this project

- After creating, you will need to manually add in the repeating "event source" in the lambda console, there is no cloudformation of aws cli command yet that can enable the repeating of the lambda function.  Recommend 5 minute repeat

This runs approxmiately 300,000 sec/month of lambda, well below the free tier for 128MB functions (3.2M) so it's free

