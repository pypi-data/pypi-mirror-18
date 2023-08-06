___NpmSearch - Python 3 Edition___

__Usage__

The NPMListener class was designed to continously monitor a search term on npm
and react to any changes after querying at a set interval. 
that idea was shelved and put into the main app. so please extend this class as you see fit.



from npmsearch2.main import NPMListener

npm_search = NPMListener

#add this to the header anywhere

search_results = npm_search.search_file("yourqueryhere") 

#returns a list of search results of package names that match the string

package_details = npm_search.lookup_project("actual-package-name")

#returns a large dict of all the package details of one package or http 404 error if not found. 
#use try and except to handle this.



