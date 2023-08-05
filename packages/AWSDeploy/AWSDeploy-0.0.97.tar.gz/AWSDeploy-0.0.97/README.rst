AWS Deployment Pre-Processor Project
====================================

The AWS Deployment Pre-Processor Project exists to facilitate the use of the 
Amazon Web Service (AWS) CodeDeploy service.  AWS CodeDeploy has a variety of 
requirements that can become stumbling blocks for inexperience users.  
AWSDeploy removes most of these issues by automating the CodeDeploy setup process.  

AWSDeploy ss a pre-processor for AWS CodeDeploy, it is by no means a replacement. 

It's features include:
1)  Transform the contents of a source directory into an AWS Deployment Package
2)  Convert line delimiters to a value that is appropriate for the destination
3)  (re-)Write an application specification in AWS CodeDeploy format based upon 
    the directory mappings found in profile.ini and the contents of the source 
    directory.
4)  Zip the prepared deployment package into an archive
5)  Upload the archive to S3 storage on AWS
6)  Trigger the initial AWS CodeDeployment
7)  Report the results     

File Requirements: 
1)  Code Deploy 
    1.1 appspec.yml

2)  AWSDeploy 
    2.1 profile.ini 
