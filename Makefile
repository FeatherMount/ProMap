JFLAGS = -g -classpath ./httpcomponents-client-4.3.5/org.apache.httpcomponents.httpclient_4.3.5.jar
JC = javac
.SUFFIXES: .java .class
.java.class:
	$(JC) $(JFLAGS) $*.java

CLASSES = \
	  ClientWithResponseHandler.java

default: classes

classes: $(CLASSES:.java=.class)

clean:
	$(RM) *.class *~
