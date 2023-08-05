To use CGEA:
Install: pip install CGEA

CGEA offers two primary classes:
drugListCGEA(druglist, saveAs = "json", sort = 'up', outputDir = None, prefix = 'CGEAResults', 
			 data = {}, numWorkers = cpu_count(), verbose = False, numPermutations = 1000):
geneListCGEA(upgenes, downgenes, saveAs = "json", sort = 'up', outputDir = None, prefix = 'CGEAResults', 
			 data = {}, numWorkers = cpu_count(), verbose = False, numPermutations = 1000):

arguments:
	upgenes = list of up regulated genes in your gene set.
	downgenes = list of down regulated genes in your gene set. Input None if you don't discriminate between up and down regulation.
	druglist = list of drugs in quuery set.
	outputDir: if you want to have the function save the outputs for you, supply an output directory here.
	prefix: all the file outputs will have this as a prefix if outputDir is defined
	async: set this to True if you want the program to run asynchronously
	numPermutations: increasing this number will increase accuracy at the cost of speed
	verbose: set this to True to have the program give status updates about its progress
	numWorkers: how many cores to use
	data: you can change what data is used by the program. Advanced users only.

methods:
	run - run the process
	
objects:
	results - holds the result data
	
Example operation:
	myUpgenes = [1,2,3]
	myDowngenes = [4,5,6]
	myCGEA = geneListCGEA(myUpgenes, myDowngenes)
	myCGEA.run()
	results = myCGEA.results