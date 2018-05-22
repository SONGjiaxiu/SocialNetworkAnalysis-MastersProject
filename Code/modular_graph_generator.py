def mod_graph_generator:
	numnodes = 300
	n0 = 30
	m = 10
	k = 6
	levels = 2
	r = 0.002
	#print 'turn = ', turn, 'r = ', r
	p = k/((n0 - 1) + (n0*m - n0)*r) 
	ergraphs = []
	for i in range(m):
	    ergraphs.append(nx.generators.erdos_renyi_graph(n0, p))

	#Now to union all m graphs
	union = nx.Graph()
	for i in range(m):
	    union = nx.disjoint_union(union, ergraphs[i])

	#nx.draw(union)
	#plt.show() 
	#Connectivity
	rho1 = p*r
	for i in range(m):
	    for j in range(i - 1):
		#Now do node to node p attachment
		for k in range(n0):
		    nodea = n0*i + k
		    for l in range(n0):
		        #Check whether to join nodea and nodeb
		        nodeb = n0*j + l
		        toconnect = random.random()
		        if toconnect < rho1:
		            #connect nodea and nodeb
		            union.add_edge(nodea, nodeb)


	G = union.copy()
	return G


