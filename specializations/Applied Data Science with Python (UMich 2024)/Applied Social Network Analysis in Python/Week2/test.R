setwd('C:/courses/Coursera/Past/Specialization-UMich Applied Data Science with Python/Social Network Analysis Python/Week2')
library(igraph)
d <- read.csv("sociogram-employees-un.csv", header=FALSE)
g <- graph.adjacency(as.matrix(d), mode="directed")
V(g)$name <- LETTERS[1:NCOL(d)]
V(g)$color <- "yellow"
V(g)$shape <- "sphere"
E(g)$color <- "gray"
E(g)$arrow.size <- 0.2
plot(g)
diameter(g)
mean(closeness(g))
mean(betweenness(g))
graph.density(g)
mean(degree(g, mode="all"))
reciprocity(g)
mean(transitivity(g))
mean(eccentricity(g))
mean_distance(g)
hs <- hub.score(g)$vector
plot(g, layout=layout.fruchterman.reingold, vertex.size=hs*25)
which.max(hs)
as <- authority.score(g)$vector
plot(g, layout=layout_nicely, vertex.size=as*20)
which.max(as)
diameter.nodes <- get.diameter(g)
diameter.nodes
V(g)$size <- 20
V(g)[diameter.nodes]$color <- "red"
V(g)[diameter.nodes]$size <- V(g)[diameter.nodes]$size+10
E(g)$width <- 1
E(g, path=diameter.nodes)$color <- "red"
E(g, path=diameter.nodes)$width <- 2
plot.igraph(g, layout=layout.fruchterman.reingold)
