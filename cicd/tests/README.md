# Tests are split by demo/site

This allows us to better use `changes:` key in gitlab-ci.yml files to control which jobs (for which sites/demos) need to run

You should have folders in here that match your ansible inventory directory structure (maybe we should stuff a CI/CD tests folder under each site in the ansible inventory?)
