import csv
import json
from itertools import dropwhile, takewhile
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os

teams = ['PHI', 'BOS', 'GSW', 'OKC', 'CHA', 'MIL', 'DET', 'BKN', 'MEM', 'IND', 'MIA', 'ORL', 'ATL', 'NYK', 'TOR', 'CLE',
			'HOU', 'NOP', 'SAS', 'MIN', 'SAC', 'UTA', 'LAC', 'DEN', 'PHX', 'DAL', 'CHI', 'WAS', 'POR', 'LAL']

def read_json(filename, team):
	with open(filename) as json_file:
		data = json.load(json_file)
		dict = {}
		for p in data[team]:
			dict[p] = data[team][p]
		# print(dict)
		return dict

def createGraph(dict, thres=20):
	G = nx.DiGraph()
	for key in dict:
		G.add_node(key, name=key)
		iso = False
		for v in dict[key]:
			if dict[key][v] > thres:
				G.add_edge(key, v, weight=dict[key][v])
				iso = True
		if not iso:
			G.remove_node(key)
	# # print(G.in_degree)
	return G

def showGraph(g, team, sub=True, show=False, save=True):
	layout = nx.drawing.layout.circular_layout(g)
	labels = {p: p for p in g.nodes}
	node_sizes = [100*d for n, d in g.degree]
	node_options = {
		"pos": layout,
		# 'node_color': 'black',
		"node_size": node_sizes,
		'labels': labels,
	}
	edges = g.edges
	edge_width = []
	for edge in edges:
		weight = g[edge[0]][edge[1]]['weight']
		weight = weight / 20. if sub else weight / 30.
		weight = 1 if weight < 1 else weight
		edge_width.append(weight)

	edge_options = {
		"pos": layout,
		"edgelist": edges,
		"width": edge_width
	}
	plt.figure()
	g_type = "substitution" if sub else "assist"
	plt.title("{} {}".format(team, g_type))
	nx.draw_networkx_nodes(g, **node_options)
	nx.draw_networkx_edges(g, **edge_options)
	nx.draw_networkx_labels(g, pos=layout, labels=labels)
	# nx.draw(g, **options)
	if save:
		plt.savefig(os.path.join(g_type, "{}.png".format(team)))
	if show:
		plt.show()
	plt.close()


def getTeams(filename):
	with open(filename) as json_file:
		teams = []
		data = json.load(json_file)
		for k in data:
			teams.append(k)
		print(teams)


def clustering_analysis(filename):
	clusterings = []
	for t in teams:
		clusterings.append((t, nx.transitivity(createGraph(read_json(filename, t), 10))))
	sorted_cluster = sorted(clusterings, key=lambda x: x[1])
	plt.barh(np.arange(30) * 2, list(map(lambda x: x[1], sorted_cluster)))
	plt.yticks(np.arange(30) * 2, list(map(lambda x: x[0], sorted_cluster)), fontsize=5)

	plt.show()


def centrality_analysis(filename, team, print_info=True):
	g = createGraph(read_json(filename, team), 10)
	degrees = [d for e, d in g.degree]
	betweenness = [b for b in nx.betweenness_centrality(g, weight="weight").values()]
	clustering = [c for c in nx.clustering(g, weight="weight").values()]
	# print("average degree: ", sum(degrees) / float(len(degrees)))
	# print("average betweenness: ", sum(betweenness) / float(len(betweenness)))
	# print("average clustering: ", sum(clustering) / float(len(clustering)))

	degree_sort = sorted(g.degree, key=lambda t: t[1], reverse=True)
	between_sort = sorted(nx.betweenness_centrality(g, weight="weight").items(), key=lambda t: t[1], reverse=True)
	close_sort = sorted(nx.closeness_centrality(g).items(), key=lambda t: t[1], reverse=True)
	eigen_sort = sorted(nx.eigenvector_centrality(g, weight='weight').items(), key=lambda t: t[1], reverse=True)

	degree_ranking = list(map(lambda x: x[0], degree_sort))
	between_ranking = list(map(lambda x: x[0], between_sort))
	close_ranking = list(map(lambda x: x[0], close_sort))
	eigen_ranking = list(map(lambda x: x[0], eigen_sort))

	if print_info:
		print("Degree: ", degree_ranking)
		print("Betweenness: ", between_ranking)
		print("Closeness: ", close_ranking)
		print("Eigenvector: ", eigen_ranking)
	return degree_ranking, between_ranking, close_ranking, eigen_ranking


def compare_centrality_across_team(filename):
	degree1 = []
	between1 = []
	close1 = []
	eigen1 = []
	for team in teams:
		degree_ranking, between_ranking, close_ranking, eigen_ranking = centrality_analysis(filename, team, print_info=False)
		degree1.append(degree_ranking[0])
		between1.append(between_ranking[0])
		close1.append(close_ranking[0])
		eigen1.append(eigen_ranking[0])

	print("Degree: ", degree1)
	print("Betweenness: ", between1)
	print("Closeness: ", close1)
	print("Eigenvector: ", eigen1)


if __name__ == '__main__':
	sub_file = "sub_18.json"
	assist_file = "assist_18.json"

	# g = createGraph(read_json(assist_file, "GSW"), thres=20)
	# showGraph(g, "GSW", show=True, save=False, sub=False)

	# for team in teams:
	# 	showGraph(createGraph(read_json(sub_file, team), thres=20), team, sub=True)
	# 	showGraph(createGraph(read_json(assist_file, team), thres=20), team, sub=False)

	# ANALYSIS
	centrality_analysis(sub_file, "SAS")
	centrality_analysis(assist_file, "SAS")

	# clustering_analysis(sub_file)
	# clustering_analysis(assist_file)

	# compare_centrality_across_team(sub_file)
	# compare_centrality_across_team(assist_file)

