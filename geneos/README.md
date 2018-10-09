# PagerDuty Integration
ITRS &copy; Integration for PagerDuty service. This script allows you to view, create, acknowledge, resolve, and close PagerDuty incidents via the Geneos environment. This script can be configured by a set of environment variables or command line options (possibly both).  Below are requirements, installation process, and command examples for particular filtered and non-filtered outputs.

#### Overview
> "PagerDuty is a SaaS-based platform used for agile incident management, not a monitoring system. PagerDuty is used as an add-on to trigger the right actions to all the data from your existing monitoring tools. PagerDuty provides sophisticated event management as well as infrastructure health visualizations to identify patterns and trends, but leaves finding problems with your systems to your existing monitoring tools." [reference](https://www.pagerduty.com/faq/)

With that being said, Geneos comes into play as eloquent monitoring tool with PagerDuty. This include file lets you automate or manually manage your incidents through the Gateway and Active Console.

#### Requirements
There are two current methods for integrating Geneos with PagerDuty.

##### Method 1

##### Method 2

You must have python 2.7 or higher to install:

`$ python -V`

This script does depend on the requests module:

`$ pip install requests`
