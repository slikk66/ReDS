![GitHub Logo](http://i.imgur.com/IAMScGQ.png)
# ReDS - ReActive Database System
RDS automatic resizing and scheduled scale up/down

###Save up to 50% on RDS costs and save yourself headache during traffic spikes

Features:
- Can be dropped into any project
- Handles low credit balance on T2 instances to upgrade to M/R instances automatically if they run out of credits
- Allows schedules to go up to bigger DB during weekdays and back down at nights and weekends (if enabled)
- Automatically increases/decreases capacity if CPU is too high/low
- Creates multiple CloudFormation stacks to encapsulate the pieces
- Built to AWS best practices in terms of security and IAM roles etc.
- Uses CloudWatch alarms (that it creates) to determine when it's time to scale
-  Configurable thresholds and cooldowns
-  Virtually no cost to operate (maybe 10 cents/month?) but can provide big savings over nights and weekends (i.e. m4.large -> t2.small in off times)

Requirements:
- run **make prep** to install dependencies
- only works on multi-AZ RDS (Single AZ instances get taken offline during resize - not good!)
- Manually configure repeating source after install via Lambda console - there is no automated way to do this yet, unfortunately - but only one time (see below for instructions!)

Tests
- run **make test**
- Check ./htmlcov/index.html for coverage report

Instructions:
- Modify vars.yaml to meet your needs.
- set "rds_identifier" to the name of your RDS instance [Click to see picture of where to get it](http://i.imgur.com/G6gRawE.png)
- If you want to enable scheduled scaling:
  - set schedule_enabled: True
  - set "cron" vars in UTC time to represent default start/stop
  - default cron vars are 9a-5p M-F Pacific (or close to it)
  - set "scheduled_index" to be the index of instance size in "instance_sizes" (starting from 0) that you want to scale up to during those hours
- After loading a profile from AWS CLI that has admin access, run from root folder:
    **make prod** to install
- This will create all the stacks, buckets, lambda, cloudwatch, IAM roles etc needed for this project

- After creating, you will need to manually add in the repeating "event source" in the lambda console, there is no cloudformation or aws cli command yet that can enable the repeating of the lambda function.  Recommend 5 minute repeat. [Click for picture overview](http://imgur.com/a/RP2Jt)

This runs approxmiately 300,000 sec/month of lambda, well below the free tier for 128MB functions (3.2M) so it's free

