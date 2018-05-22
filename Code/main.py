#! /usr/bin/python

import matplotlib.pyplot as plt
import networkx as nx
import random as rd
from array import *


class ABC():
	def __init__(self):
		self.prob_matrix = [[0.1, 0.1], [0.1, 0.1]]
		return

	def infect_model(self, infector, infectee):
		#We will make a matrix which tells what is the prob if i infecting j
		#In this, function we'll just look up from the matrix
		infectee_type = infectee['type']
		infector_type = infector['type']

	   	row = self.prob_matrix[infector_type]
		prob_val = row[infectee_type]

		temp = rd.randint(1,10)
	   	if float(temp) / 10 <= prob_val:
			return 1
	    	else:
			return 0

	#Initial set of infected nodes(50 nodes are chosen randomly)
	def getSeedNodes(self, nodes_list):
		rd.shuffle(nodes_list)
		infected_nodes_list = list()

		for k in range(0, 10):
			infected_nodes_list.append(nodes_list[k])
		return infected_nodes_list

#############################################################################

	def mod_graph_generator(self):
		#numnodes = 10000
		n0 = 500
		m = 20
		k = 10
		#levels = 2
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
				toconnect = rd.random()
				if toconnect < rho1:
				    #connect nodea and nodeb
				    union.add_edge(nodea, nodeb)


		G = union.copy()
		return G

#####################################################################################

	def generateGraph(self, graph_model):
		if graph_model == 'kronecker':
			fh=open("kronecker_graph", 'rb')
			G=nx.read_edgelist(fh, delimiter='\t')
			fh.close()
			print len(G.nodes())
			return G

		if graph_model == 'watts_strogatz':
			G = nx.watts_strogatz_graph(10000,5,0.2)
			return G

		if graph_model == 'modular':
			G = self.mod_graph_generator()
			return G


	
	#SIR Model (Complete)
	def SIR_model(self, figure_label, graph_model):
		G = self.generateGraph(graph_model)
		for i in G.nodes():
			G.node[i]['rnd'] = rd.randint(1,6)
			G.node[i]['type'] = rd.randint(0,1)


		infected_nodes_list = self.getSeedNodes(G.nodes())
		print infected_nodes_list

		total_nodes_infected = len(infected_nodes_list)
	
		#Initial set of infected nodes(20 nodes are chosen randomly)
		infected_nodes = set(infected_nodes_list)
		susceptible_nodes = set(G.nodes())
		susceptible_nodes = susceptible_nodes - infected_nodes
		recovered_nodes = set()

		temp_infected_list = list()				#Temp variable
		#May be we should keep these as object variables
		rounds_list = list()
		contagion_spread = list()
		new_nodes_infected = list()
		

		# For now just focus on first 20 rounds
		for i in range(0, 40):
			rounds_list.append(i)
			#Note: This loop should be on non-infected nodes.

			del temp_infected_list[:]
			for node_iter in list(infected_nodes):
				#Check if node_iter is in infected
				#neigh_iter is an iterator over the neighbours of node_iter
				neigh_iter = G.neighbors_iter(node_iter)
				num_of_neigh = len(G.neighbors(node_iter))

				for n in neigh_iter:
					isInfected = 0
					if n in susceptible_nodes:
						isInfected = self.infect_model(G.node[node_iter], G.node[n])
		    				if isInfected == 1:
							temp_infected_list.append(n)

			#Decrement the rnd attribute of each node here
			#If it becomes 0, transfer these nodes to 'recovered' list
			for L in G.nodes(True):
				if L[0] in infected_nodes:
					#print "%(node)d => %(rnd)d" % {"node": L[0], "rnd": L[1]['rnd'] } 
					L[1]['rnd'] = L[1]['rnd'] - 1
					if L[1]['rnd'] == 0:
						recovered_nodes.add(L[0])
						infected_nodes.remove(L[0])
					
			#Add nodes in temp_infected_list to infected_nodes set and remove them from susceptible_nodes set.
			infected_nodes  = infected_nodes | (set(temp_infected_list))			
			susceptible_nodes = susceptible_nodes - (set(temp_infected_list))

			total_nodes_infected += len(set(temp_infected_list))
			new_nodes_infected.append(len(set(temp_infected_list)))

			contagion_spread.append(len(infected_nodes))
			print "%(round)d --> %(infected)d" % {"round": i, "infected": len(infected_nodes) }
			


		plt.plot(rounds_list, contagion_spread, '-')
		#plt.savefig("Watts_strogatz_ContagionSpread")
		plt.plot(rounds_list, new_nodes_infected, '-')
		plt.savefig(figure_label)

		print total_nodes_infected
		print len(recovered_nodes)

	def SIS_model(self, figure_label, graph_model):
		G = generateGraph(graph_model)
		for i in G.nodes():
			G.node[i]['rnd'] = rd.randint(1,6)
			G.node[i]['type'] = rd.randint(0,1)


		infected_nodes_list = self.getSeedNodes(G.nodes())
		print infected_nodes_list

		total_nodes_infected = len(infected_nodes_list)
	
		#Initial set of infected nodes(20 nodes are chosen randomly)
		infected_nodes = set(infected_nodes_list)
		susceptible_nodes = set(G.nodes())
		susceptible_nodes = susceptible_nodes - infected_nodes
		#recovered_nodes = set()

		temp_infected_list = list()				#Temp variable
		#May be we should keep these as object variables
		rounds_list = list()
		contagion_spread = list()
		new_nodes_infected = list()
		

		# For now just focus on first k rounds
		for i in range(0, 60):
			rounds_list.append(i)
			#Note: This loop should be on non-infected nodes.

			del temp_infected_list[:]
			for node_iter in list(infected_nodes):
				#Check if node_iter is in infected
				#neigh_iter is an iterator over the neighbours of node_iter
				neigh_iter = G.neighbors_iter(node_iter)
				num_of_neigh = len(G.neighbors(node_iter))

				for n in neigh_iter:
					isInfected = 0
					if n in susceptible_nodes:
						isInfected = self.infect_model(G.node[node_iter], G.node[n])
		    				if isInfected == 1:
							temp_infected_list.append(n)

			#Decrement the rnd attribute of each node here
			#If it becomes 0, transfer these nodes to 'recovered' list
			for L in G.nodes(True):
				if L[0] in infected_nodes:
					L[1]['rnd'] = L[1]['rnd'] - 1
					if L[1]['rnd'] == 0:
						L[1]['rnd'] = rd.randint(1,6)			#Reset the 'rnd' attribute
						susceptible_nodes.add(L[0])
						infected_nodes.remove(L[0])
					
			#Add nodes in temp_infected_list to infected_nodes set and remove them from susceptible_nodes set.
			infected_nodes  = infected_nodes | (set(temp_infected_list))			
			susceptible_nodes = susceptible_nodes - (set(temp_infected_list))

			total_nodes_infected += len(set(temp_infected_list))
			new_nodes_infected.append(len(set(temp_infected_list)))

			contagion_spread.append(len(infected_nodes))
			print "%(round)d --> %(infected)d" % {"round": i, "infected": len(infected_nodes) }
			

		plt.plot(rounds_list, contagion_spread, '-')
		plt.plot(rounds_list, new_nodes_infected, '-')
		plt.savefig(figure_label + "Watts_strogatz(SIS)")

		print total_nodes_infected
		#print len(recovered_nodes)


	def SIRS_model(self, figure_label, graph_model):
		G = self.generateGraph(graph_model)
		for i in G.nodes():
			G.node[i]['i_rnd'] =  3#rd.randint(1,3)
			G.node[i]['r_rnd'] =  4 #rd.randint(1,8)
			G.node[i]['type'] = rd.randint(0,1)


		infected_nodes_list = self.getSeedNodes(G.nodes())
		print infected_nodes_list

		total_nodes_infected = len(infected_nodes_list)

		#Initial set of infected nodes(20 nodes are chosen randomly)
		infected_nodes = set(infected_nodes_list)
		susceptible_nodes = set(G.nodes())
		susceptible_nodes = susceptible_nodes - infected_nodes
		recovered_nodes = set()

		temp_infected_list = list()				#Temp variable
		#May be we should keep these as object variables
		rounds_list = list()
		contagion_spread = list()
		new_nodes_infected = list()
	

		# For now just focus on first k rounds
		for i in range(0, 60):
			rounds_list.append(i)
			#Note: This loop should be on non-infected nodes.

			del temp_infected_list[:]
			for node_iter in list(infected_nodes):
				#Check if node_iter is in infected
				#neigh_iter is an iterator over the neighbours of node_iter
				neigh_iter = G.neighbors_iter(node_iter)
				num_of_neigh = len(G.neighbors(node_iter))

				for n in neigh_iter:
					isInfected = 0
					if n in susceptible_nodes:
						isInfected = self.infect_model(G.node[node_iter], G.node[n])
		    				if isInfected == 1:
							temp_infected_list.append(n)

			#Decrement the rnd attribute of each node here
			#If it becomes 0, transfer these nodes to 'recovered' list
			for L in G.nodes(True):
				if L[0] in infected_nodes:
					L[1]['i_rnd'] = L[1]['i_rnd'] - 1
					if L[1]['i_rnd'] == 0:
						L[1]['i_rnd'] = 3 #rd.randint(1,3)		#Reset the 'rnd' attribute to 3
						recovered_nodes.add(L[0])
						infected_nodes.remove(L[0])

				if L[0] in recovered_nodes:
					L[1]['r_rnd'] = L[1]['r_rnd'] - 1
					if L[1]['r_rnd'] == 0:
						L[1]['r_rnd'] = 4 #rd.randint(1,8)		#Reset the 'rnd' attribute to 3
						susceptible_nodes.add(L[0])
						recovered_nodes.remove(L[0])
				
			#Add nodes in temp_infected_list to infected_nodes set and remove them from susceptible_nodes set.
			infected_nodes  = infected_nodes | (set(temp_infected_list))			
			susceptible_nodes = susceptible_nodes - (set(temp_infected_list))

			total_nodes_infected += len(set(temp_infected_list))
			new_nodes_infected.append(len(set(temp_infected_list)))

			contagion_spread.append(len(infected_nodes))
			print "%(round)d --> %(infected)d" % {"round": i, "infected": len(infected_nodes) }
		

		plt.plot(rounds_list, contagion_spread, '-')
		plt.plot(rounds_list, new_nodes_infected, '-')
		plt.savefig(figure_label + "_NewNodesInfected(SIRS)")

		print total_nodes_infected
		print len(recovered_nodes)


	def getSeedNodesFrom_A(self, M):
		A_list = list()

		#for i in M.nodes():
		#	if M.node[i]['cluster'] == 0:
		#		A_list.append(i)

		for L in M.nodes(True):
			if L[1]['cluster'] == 0:
				A_list.append(L[0])

		rd.shuffle(A_list)
		infected_nodes_list = list()

		for k in range(0, 20):
			infected_nodes_list.append(A_list[k])
		return infected_nodes_list


	def generateGraphforSynchronocity(self):
		#Configuration given below gives perfect out of phase synchronocity
		#(provided i_rnd=5 and r_rnd=6)
		#G = nx.watts_strogatz_graph(5000,22,0.1)
		#H = nx.watts_strogatz_graph(5000,20,0.2)
		G = self.generateGraph('kronecker')
		H = self.generateGraph('kronecker')

		for i in G.nodes():
			G.node[i]['cluster'] = 0

		for j in H.nodes():
			H.node[j]['cluster'] = 1

		M = nx.disjoint_union(G, H)

		#print len(M.nodes())
		for L in M.nodes(True):		
			print L[1]['cluster']

		#Make (say) 20 connections from node of type 0 to node of type1
		for i in range(0,20):
			e1 = rd.randint(0,4999)
			e2 = rd.randint(5000,9999)
			M.add_edge(e1, e2)
		
		return M

		#pos=nx.random_layout(M)
		#nx.draw_networkx(M, pos, with_labels=0, node_size=1, width=0.1)
		#plt.savefig(figure_label)

	#SIRS model is used for synchronocity
	def synchronocity(self, figure_label, graph_model):
		
		M = self.generateGraphforSynchronocity()
		for i in M.nodes():
			M.node[i]['i_rnd'] = 5 #rd.randint(1,3)
			M.node[i]['r_rnd'] = 6 #rd.randint(1,8)
			M.node[i]['type'] = rd.randint(0,1)


		#Note the difference in getSeed function
		infected_nodes_list = self.getSeedNodesFrom_A(M)
		print infected_nodes_list

		total_nodes_infected = len(infected_nodes_list)

		#Initial set of infected nodes(20 nodes are chosen randomly)
		infected_nodes = set(infected_nodes_list)
		susceptible_nodes = set(M.nodes())
		susceptible_nodes = susceptible_nodes - infected_nodes
		recovered_nodes = set()

		infected_nodes_in_A = list()
		infected_nodes_in_B = list()
		temp_infected_list = list()				#Temp variable
		#May be we should keep these as object variables
		rounds_list = list()
		contagion_spread = list()
		new_nodes_infected = list()
		contagion_spread_in_A = list()
		contagion_spread_in_B = list()
	

		# For now just focus on first k rounds
		for i in range(0, 60):
			rounds_list.append(i)
			#Note: This loop should be on non-infected nodes.

			del temp_infected_list[:]
			for node_iter in list(infected_nodes):
				#Check if node_iter is in infected
				#neigh_iter is an iterator over the neighbours of node_iter
				neigh_iter = M.neighbors_iter(node_iter)
				num_of_neigh = len(M.neighbors(node_iter))

				for n in neigh_iter:
					isInfected = 0
					if n in susceptible_nodes:
						isInfected = self.infect_model(M.node[node_iter], M.node[n])
		    				if isInfected == 1:
							temp_infected_list.append(n)

			#Decrement the rnd attribute of each node here
			#If it becomes 0, transfer these nodes to 'recovered' list
			for L in M.nodes(True):
				if L[0] in infected_nodes:
					L[1]['i_rnd'] = L[1]['i_rnd'] - 1
					if L[1]['i_rnd'] == 0:
						L[1]['i_rnd'] = 5#rd.randint(1,3)		#Reset the 'rnd' attribute to 3
						recovered_nodes.add(L[0])
						infected_nodes.remove(L[0])

				if L[0] in recovered_nodes:
					L[1]['r_rnd'] = L[1]['r_rnd'] - 1
					if L[1]['r_rnd'] == 0:
						L[1]['r_rnd'] = 6#rd.randint(1,8)		#Reset the 'rnd' attribute to 3
						susceptible_nodes.add(L[0])
						recovered_nodes.remove(L[0])
				
			#Add nodes in temp_infected_list to infected_nodes set and remove them from susceptible_nodes set.
			infected_nodes  = infected_nodes | (set(temp_infected_list))			
			susceptible_nodes = susceptible_nodes - (set(temp_infected_list))

			total_nodes_infected += len(set(temp_infected_list))
			new_nodes_infected.append(len(set(temp_infected_list)))


			#Can you make this efficient??
			for p in infected_nodes:
				if M.node[p]['cluster'] == 0:
					infected_nodes_in_A.append(p)
				else:
					infected_nodes_in_B.append(p)

			contagion_spread.append(len(infected_nodes))
			contagion_spread_in_A.append(len(infected_nodes_in_A))
			contagion_spread_in_B.append(len(infected_nodes_in_B))
			print "%(round)d --> %(infected)d" % {"round": i, "infected": len(infected_nodes) }

			del infected_nodes_in_A[:]
			del infected_nodes_in_B[:]
		

		#plt.plot(rounds_list, contagion_spread, '-')
		#plt.plot(rounds_list, new_nodes_infected, '-')

		plt.plot(rounds_list, contagion_spread_in_A, '-')
		plt.plot(rounds_list, contagion_spread_in_B, '-')
		plt.savefig(figure_label + "_NewNodesInfected(SIRS)")

		print total_nodes_infected
		print len(recovered_nodes)


	def containment(self, figure_label, graph_model):
		G = self.generateGraph(graph_model)


		for i in G.nodes():
			G.node[i]['i_rnd'] =  2#rd.randint(1,3)
			G.node[i]['r_rnd'] =  4 #rd.randint(1,8)
			G.node[i]['type'] = rd.randint(0,1)

		print len(G.nodes())
		infected_nodes_list = self.getSeedNodes(G.nodes())
		print infected_nodes_list

		total_nodes_infected = len(infected_nodes_list)

		#Initial set of infected nodes(20 nodes are chosen randomly)
		infected_nodes = set(infected_nodes_list)
		susceptible_nodes = set(G.nodes())
		susceptible_nodes = susceptible_nodes - infected_nodes
		recovered_nodes = set()

		temp_infected_list = list()				#Temp variable
		#May be we should keep these as object variables
		rounds_list = list()
		contagion_spread = list()
		new_nodes_infected = list()
	
		#Creating dictionary of node_label vs degree
		deg_dict = G.degree(G.nodes())
		it = iter(sorted(deg_dict.iteritems()))
		
		cnt = 0
		flag = 0
		# For now just focus on first k rounds
		for i in range(0, 120):
			rounds_list.append(i)
			#Procedure for containment (threshold = 50%)
			control_factor = 0.3
			 
			if len(infected_nodes) >= control_factor * len(G.nodes()):
				flag = 1

			if flag == 1:
				cnt = cnt + 1
				#control_factor -= 0.1
				quarantine_factor = 400
				for z in range(1,100):
					node = it.next()
					G.remove_node(node[0])
					if node[0] in infected_nodes:
						infected_nodes.remove(node[0])

				if quarantine_factor > 100:
					quarantine_factor -= 100
				if cnt == 5:
					cnt = 0
					flag = 0
					control_factor -= 0.1

			del temp_infected_list[:]
			for node_iter in list(infected_nodes):
				#Check if node_iter is in infected
				#neigh_iter is an iterator over the neighbours of node_iter
				neigh_iter = G.neighbors_iter(node_iter)
				num_of_neigh = len(G.neighbors(node_iter))

				for n in neigh_iter:
					isInfected = 0
					if n in susceptible_nodes:
						isInfected = self.infect_model(G.node[node_iter], G.node[n])
		    				if isInfected == 1:
							temp_infected_list.append(n)

			#Decrement the rnd attribute of each node here
			#If it becomes 0, transfer these nodes to 'recovered' list
			for L in G.nodes(True):
				if L[0] in infected_nodes:
					L[1]['i_rnd'] = L[1]['i_rnd'] - 1
					if L[1]['i_rnd'] == 0:
						L[1]['i_rnd'] = 2 #rd.randint(1,3)		#Reset the 'rnd' attribute to 3
						recovered_nodes.add(L[0])
						infected_nodes.remove(L[0])

				if L[0] in recovered_nodes:
					L[1]['r_rnd'] = L[1]['r_rnd'] - 1
					if L[1]['r_rnd'] == 0:
						L[1]['r_rnd'] = 4 #rd.randint(1,8)		#Reset the 'rnd' attribute to 3
						susceptible_nodes.add(L[0])
						recovered_nodes.remove(L[0])
				
			#Add nodes in temp_infected_list to infected_nodes set and remove them from susceptible_nodes set.
			infected_nodes  = infected_nodes | (set(temp_infected_list))			
			susceptible_nodes = susceptible_nodes - (set(temp_infected_list))

			total_nodes_infected += len(set(temp_infected_list))
			new_nodes_infected.append(len(set(temp_infected_list)))

			contagion_spread.append(len(infected_nodes))
			print "%(round)d --> %(infected)d" % {"round": i, "infected": len(infected_nodes) }
		

		plt.plot(rounds_list, contagion_spread, '-')
		plt.plot(rounds_list, new_nodes_infected, '-')
		plt.savefig(figure_label + "_BigBLAH(SIRS)")
		print cnt

	def competing_contagion(self, figure_label, graph_model):
		G = self.generateGraph(graph_model)

		for i in G.nodes():
			G.node[i]['choice'] =  'B'

		choice_A = list()
		choice_B = list()
		rounds_list = list()
		adoption_A = list()
		adoption_B = list()

		cnt = 0
		seedNodes = self.getSeedNodes(G.nodes())
		print len(seedNodes)
		for i in seedNodes:
			neigh_iter = G.neighbors_iter(i)
			G.node[i]['choice'] = 'A' 
			cnt = cnt + 1
			#choice_A.append(i)
			for n in neigh_iter:
				G.node[n]['choice'] = 'A'
				cnt = cnt + 1
				#choice_A.append(n)float(cnt) / num_of_neigh

		print cnt
		#choice_B = list(set(G.nodes()) - set(choice_A))
		
		
		for i in range(0, 40):
			rounds_list.append(i)

			for node_iter in G.nodes():
				cnt = 0
				neigh_iter = G.neighbors_iter(node_iter)
				num_of_neigh = len(G.neighbors(node_iter))

				for n in neigh_iter:
					if G.node[n]['choice'] == 'A':
						cnt = cnt + 1

				#print float(cnt) /num_of_neigh
				#Think of this threshold!!!
				if float(cnt) / num_of_neigh >= 0.15:
					G.node[node_iter]['choice'] = 'A'
					#print "here"
					choice_A.append(node_iter)
				else:
					G.node[node_iter]['choice'] = 'B'
					choice_B.append(node_iter)
					
				
			#Add nodes in temp_infected_list to infected_nodes set and remove them from susceptible_nodes set.
			
			adoption_A.append(len(choice_A))
			adoption_B.append(len(choice_B))
			print "%(round)d --> %(A)d" % {"round": i, "A": len(choice_A) }
			print "%(round)d --> %(B)d" % {"round": i, "B": len(choice_B) }
			del choice_A[:]
			del choice_B[:]
		

		plt.plot(rounds_list, adoption_A, '-')
		plt.plot(rounds_list, adoption_B, '-')
		plt.savefig(figure_label + "Competing contagion")



obj = ABC()
#for i in graph_model_list:
#obj.containment('Paresh', 'watts_strogatz')
#obj.synchronocity('sync', 'graph_model')
obj.competing_contagion('----', 'kronecker')





#Questions to investigate:
#What geometric properties lead to dying out of epidemic
#Synchronization: Take 2 separate small world graphs, and join them by a few links going across. Start a contagion in one of the graphs and 
#monitor infected nodes in both graphs
#Containment: For SIS and SISR model, after (say)50% of population is infected, you start control procedure by isolating(making them immune) highest degree vertices. Isolate say 10 such nodes per round. After 5-10 rounds of isolation, epidemic will eventually die out.

#pos=nx.random_layout(M)
#nx.draw_networkx(M, pos, with_labels=0, node_size=10, width=0.5)
#plt.savefig("path.png")

#Modeling epidemic spread.
#Each infected neighbour of a node takes an independent shot at infecting a node.
#To model this, we will write a function that generates a random number between 1 and 10.
#Suppose we want to enforce the condition that prob of infecting is 0.2, then
#we will check if the number randomly chosen is 1 or 2. If yes, it will infect the node else not.

#Conclusions
#For watts strogatz model if we keep p high (say 0.4) then the epidemic increases slowly initially but after
# some number of rounds it increases very fast. Whereas, if p is small, epidemic spreads very quickly in the first
#few rounds but then the rate of growth decreases.

#For Kronecker graph: if the period of infection round is slightly lesser (1 or 2 rounds) than the period of recovery 
#rounds then the epidemic stops after 1 or two oscillations. 

#Epidemics on Modular graphs exhibit a similar behaviour to small world. The oscillations in modular graphs decrease in intensity as number of rounds increase.

#Equilibrium condition reached in competing contagion experiment:
#watts_strogatz (10000,5,0.2)
#seed nodes : 30
#Threshold : 0.3

	
