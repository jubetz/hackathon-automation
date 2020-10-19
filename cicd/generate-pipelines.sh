#!/bin/bash

# only supports this inventory structure right now: https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#alternative-directory-layout
# will need some more logic to support the other (primary?) style

# this discovers the sites based on the ansible inventory 
SITES=`ls ./inventories`

for SITE in $SITES
do
 # the j2 bash command renders jinja2 templates
 # variables for template are easiest as env variables
 export site=$SITE
 export parent_pipeline_id=$CI_PIPELINE_ID

 j2 ./cicd/.gitlab-ci-template.j2 > ${SITE}-pipeline.yml
 
done


