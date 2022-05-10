## **Using AWS Web Application Firewall and Amazon Route53 to secure the LAMP stack** 

LAMP stands for Linux, Apache, MySQL, and PHP.  Together, they provide a time-tested stack of software for delivering high-performance web applications. LAMP has a classic layered architecture, with Linux at the lowest level. The next layer is Apache and MySQL, followed by PHP.

Customers can build a LAMP stack application from scratch or by following this [AWS tutorial](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-LAMP.html). However, the documentation does not dive deep into ways to secure the LAMP stack application against web application vulnerabilities and DDoS attacks. As with any open source project, LAMP stack applications are vulnerable to common web exploits and bots that may affect availability, compromise security, or consume excessive resources. Insecure open source code means software stacks are vulnerable and organizations remain exposed.

In [this blog post](https://aws.amazon.com/blogs/infrastructure-and-automation/secure-lamp-stack-aws-waf-web-application-firewall/), we give you prescriptive guidance and automation steps to deploy a secure and highly available LAMP stack application using AWS WAF, Application Load Balancer, AWS Route 53 and secured by a TLS certificate using AWS Certificate Manager. We walk you through how to launch this classic layered architecture LAMP stack application that can host a variety of popular web applications, such as WordPress, Wikipedia and Drupal in minutes.

## Solution Overview

The following screenshot shows a high-level solution overview. 

![img](architecture.png)

For a detailed implementation walkthrough, please visit our blog: Using [AWS Web Application Firewall and Amazon Route53 to secure the LAMP stack](https://amazon.awsapps.com/workdocs/index.html#/document/1080b6287172d47efa47ab721c468fc7f2965ecc0478f9a11b661b276a4f3266). 
