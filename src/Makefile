JFLAGS = -g -classpath ./APIs/org.apache.httpcomponents.httpclient_4.3.5.jar:./APIs/commons-logging-1.2.jar:./:./APIs/opencsv-3.0.jar:./APIs/mysql-connector-java-5.1.32-bin.jar
JC = javac
.SUFFIXES: .java .class
.java.class:
	$(JC) $(JFLAGS) $*.java

CLASSES = \
	  XMLDownloader.java\
	  DataCollectingDriver.java\
	  XMLParser.java\
	  PMCIdRetriever.java\
	  DatabaseManager.java

default: classes

classes: $(CLASSES:.java=.class)

clean:
	$(RM) *.class *~
