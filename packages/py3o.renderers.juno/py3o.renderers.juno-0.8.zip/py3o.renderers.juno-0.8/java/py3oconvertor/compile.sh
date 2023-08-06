#!/bin/bash
#set -ex

# Fedora
#export OOO_HOME=/usr/lib64/libreoffice
#export JUNO_HOME=$OOO_HOME/basis3.3/program/classes

export OOO_HOME=/usr/lib/libreoffice
export JUNO_HOME=$OOO_HOME/program/classes
if [ -d "/usr/lib/ure/share/java" ]
then
    export JOOO_HOME=/usr/lib/ure/share/java
else
    export JOOO_HOME=/usr/share/java
fi

export CLASSPATH="$JOOO_HOME/juh.jar:$JOOO_HOME/jurt.jar:$JOOO_HOME/ridl.jar:$JOOO_HOME/unoloader.jar:$JOOO_HOME/java_uno.jar:$JUNO_HOME/unoil.jar:./bin/py3oconverter/.:.:/usr/bin"

javac py3oconverter/Launch.java -Xlint:deprecation
javac py3oconverter/Convertor.java -Xlint:deprecation

#java py3oconverter/Launch

jar -cf ../../py3o/renderers/juno/py3oconverter.jar py3oconverter/Convertor.class
