mvn archetype:generate -B \
	-DarchetypeGroupId=com.atlassian.bamboo \
	-DarchetypeArtifactId=bamboo-specs-archetype \
	-DarchetypeVersion=7.0.2 \
	-DgroupId=com.atlassian.bamboo \
	-DartifactId=bamboo-specs \
	-Dversion=1.0.0-SNAPSHOT \
	-Dpackage=tutorial -Dtemplate=minimal
