#!/bin/sh
psql ${DATABASE_URL} -f ./app/tables.sql
