#!/usr/bin/env sh
setfacl -PRdm u::rwX,g::rwX,o::r $PWD && setfacl -PRm u::rwX,g::rwX,o::r $PWD
