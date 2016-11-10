FROM alpine:3.3
MAINTAINER liz@lizrice.com

ARG mybuildarg

LABEL com.lizrice.test="$mybuildarg" \
      org.label-schema.vcs-url="https://github.com/lizrice/imagetest" \
      org.label-schema.vcs-ref="1234567" 

