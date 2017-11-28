import sublime
import sublime_plugin
from urllib.request import urlopen, Request, HTTPError, URLError
from urllib.parse import urlencode
import json
import io
import logging, pprint

logger = logging.getLogger('DBpedia Lookup')

class DbpediaLookupCommand(sublime_plugin.TextCommand):

	VIEW_NAME = 'DBpedia Lookup'

	def run(self, edit):
		sels = self.view.sel()
		if sels[0].empty(): # no selection, try to find the surronding word
			lookup_region = self.view.word(sels[0])
			lookup_item = self.view.substr(lookup_region)
		else: # selection found
			lookup_item = self.view.substr(sels[0])	
		logger.info('DBpedia: looking up '+lookup_item)
		results = self.lookup(lookup_item)
		if results == None or not results['results']:
			logger.warning('DBpedia Lookup: no results')
			return
		contents = self.output(results, lookup_item)
		f = self.get_view()
		f.set_read_only(False)
		f.run_command('select_all')
		f.run_command('right_delete')
		f.insert(edit, 0, contents)
		f.set_read_only(True)
		f.run_command('fold_all')
		sublime.active_window().focus_view(f)

	def output(self, results, lookup_item):
		output = io.StringIO()
		output.write('Looked up: '+lookup_item+'\n\n')
		for r in results['results']:
			output.write(r['label']+': '+r['uri']+'\n')
			output.write('  description: '+(r['description'] or '')+'\n')
			output.write('  reference counter: '+str(r['refCount'])+'\n')
			for a in ['categories', 'classes', 'templates', 'redirects']:
				output.write('  '+a+':\n')
				for b in r[a]:
					output.write('    '+b['label']+': '+b['uri']+'\n')
		contents = output.getvalue()
		output.close()
		return contents

	def get_view(self, name = VIEW_NAME):
		dlv = None
		for w in sublime.windows():
			for v in w.views():
				if v.name() == name:
					dlv = v
					break
		if dlv == None:
			f = sublime.active_window().new_file()
			f.set_encoding('utf-8')
			f.set_name(name)
			f.set_scratch(True)
			f.set_syntax_file('Packages/YAML/YAML.tmLanguage')
			return f
		else:
			return dlv

	def lookup(self, name):
		settings = sublime.load_settings('dbpedia_lookup.sublime-settings')
		if settings.get('default_server', 'remote') == 'remote':
			host = settings.get('dbpedia_lookup_server_remote', 'http://lookup.dbpedia.org')
		else:
			host = settings.get('dbpedia_lookup_server_local', '')
		try:
			headers = {'Accept': 'application/json'}
			params = f = { 'QueryClass' : '', 'MaxHits' : 5, 'QueryString' : name }
			req = Request(host+'/api/search/KeywordSearch?'+urlencode(params), None, headers)
			resp = urlopen(req)
			s = resp.read().decode('utf-8')
			return json.loads(s)
		except HTTPError as e:
			err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
			sublime.error_message(err)
			return None
		except URLError as e:
			err = '%s: URL error %s contacting API' % (__name__, str(e.reason))
			sublime.error_message(err)
			return None
