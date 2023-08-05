txlogstash
==========

A twisted LogObserver sending json lines to a logstash, splunk, or any modern json capable event/log server.

The log events are tweaked in order to be properly indexed by elasticsearch.
Special attention has been given to properly dump the failures.

Usage::

    from txlogstash import TCPJsonLineLogObserver
    from twisted.logger import globalLogPublisher
    globalLogPublisher.addObserver(TCPJsonLineLogObserver("tcp:logger.example.com:5000")


Logstash.json::

    input {
    	tcp {
    		port => 5000
    		codec => json_lines
    	}
    }
    output {
    	elasticsearch {
    		hosts => "elasticsearch:9200"
    	}
    }



