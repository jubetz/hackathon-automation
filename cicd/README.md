# Hey there this is where I'll talk about CI

In this folder, you will find the .gitlab-ci.yml include files for each "demo". In our case a demo would be similar to how to manage multiple "sites" or "pods" in real operations.  

Each of these files contains all of the jobs for that site/demo. Pay attention to the `tags:` key for the jobs, they determin which gitlab-runner the job will be picked up by and thereby determining where that job actually runs.  



