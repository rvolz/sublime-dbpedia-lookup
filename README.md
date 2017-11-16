# sublime-dbpedia-lookup
A  Sublime Text 3 plugin for the DBpedia Lookup service

This plugin uses the [DBpedia Lookup](https://github.com/dbpedia/lookup) service for keyword searches.   

## Use case

This plugin was made to enable quick word lookups while going through a text, for example while perusing a Markdown or Asciidoctor document. _Lookup_ here means _looking for context_, not spell checking. 

The DBpedia lookup service answers with descriptions of resources connected to the expression searched, their classes, categories. That makes it easy to dig further, if you are interested.

The output is formatted as a YAML document, so it is nicely structured when read by us humans, but could also be processed by a program when saved.

## Usage

The plugin provides a command in the context menu:

* right-click on a text selection for the context menu, then select _DBpedia Lookup_ to look up the selection
* right-click on the cursor position for the context menu, then select _DBpedia Lookup_ to look up the surrounding word

![Selecting for lookup](docs/ipsum1.png)

After that ...

* the plugin will search the DBpedia Lookup service for possible hits
* if there were hits the results will be presented in a scratch window named _DBpedia Lookup_
* all links in the result window can be right-clicked to open them in a browser, for further study

![Result view](docs/ipsum2.png)

For convenience all answers are displayed in a single scratch buffer, meaning the plugin won't clutter your editor with lots of result windows. Results of multiple lookups will overwrite each other. 

Since we are using a scratch buffer, Sublime Text will also not complain about unsaved changes when exiting. You can save the results, but you are not required to do so.

## Limitations

The DBpedia lookup service is currently only available in English. Support for other languages is mentioned, but not yet here. So the initial results will be always in English. However, by following the links you'll often get to the equivalent resources in other languages.

If you want to know more about the service or have questions please use information in the [DBpedia Lookup](https://github.com/dbpedia/lookup) project on Github to get in contact.

## Server configuration

By default the plugin will use the public endpoint for the DBpedia Lookup service at http://lookup.dbpedia.org. However, it is possible to also configure a _local_ endpoint. The DBpedia project provides a [Docker image](https://hub.docker.com/r/dbpedia/lookup/) that makes it possible to run the service on your own machine or elsewhere.

To use the local endpoint configure the user preferences accordingly:

* change the setting _default_server_ to _local_. The default is _remote_.
* change the setting _dbpedia_lookup_server_local_ to the address/port of your machine. The default is _http://localhost:1111_, which is the address the Docker image uses.

## License

This plugin is freely available under the [MIT license](LICENSE).


