require(igraph)
#setwd("C:/courses/Coursera/Past/BioInformatics Algorithms II/PA")
#lines <- readLines("Neighbor_Joining_O.txt")
#lines <- readLines("out1.txt")
#lines <- readLines("inp16o.txt")
#lines <- readLines("out.txt")
#lines <- readLines("Small_Parsimony_Unrooted_Tree_O.txt")
#lines <- readLines("inp19.txt")
lines <- readLines('out/user.demo.adjacency.sub.txt')
lines <- readLines('out/booth.demo.adjacency.sub.txt')

process.chain <- function(filename, root) {
  lines <- readLines(filename)
  U <- c()
  V <- c()
  gdf <- NULL
  for (line in lines) {
    line <- gsub(">", "", line)
    vertices <- unlist(strsplit(line, "-"))
    #print(u_v_w)
    for (i in 1:(length(vertices)-1)) {
      if (!(vertices[i] %in% U) | !(vertices[i+1] %in% V)) {
        gdf <- rbind(gdf, data.frame(from=vertices[i], to=vertices[i+1]))
        U <- c(vertices[i], U)
        V <- c(vertices[i+1], V)        
      }
    }
  }
  gdf
  g <- graph.data.frame(gdf)
  plot(g, vertex.size=17, vertex.label.cex=0.55, #vertex.label.dist=0.1, vertex.label.degree=0, 
       #edge.label=round(unlist(E(g)$weight), 2), 
       edge.arrow.size=0.15, 
       layout = layout.reingold.tilford(g, root=root)) #, circular=T))
  
}

#filename <- 'outc.txt'
#root <- '(209,217,225,1)'
#process.chain(filename, root)

gdf <- NULL
U <- c()
V <- c()
for (line in lines) {
  line <- gsub(":", "-", line)
  line <- gsub(">", "", line)
  u_v_w <- unlist(strsplit(line, "-"))
  #print(u_v_w)
  if (length(u_v_w) >= 2) {
    u <- u_v_w[1] #as.integer(u_v_w[[1]][1])
    v <- u_v_w[2] #as.integer(u_v_w[[1]][2])
    w <- ifelse(length(u_v_w) >= 3, as.numeric(u_v_w[3]), 0)
    U <- c(u, U)
    V <- c(v, V)
    if (!(u %in% V) | !(v %in% U)) {
      gdf <- rbind(gdf, data.frame(from=u, to=v, weight=w))
      print(paste(u, v, w, sep=","))
    }
  }
}
#gdf

gdf <- gdf[!is.na(gdf$weight),]
gdf$from <- substring(gdf$from, 1, 5)
gdf$to <- substring(gdf$to, 1, 5)

#gdf1 <- gdf[gdf$from == '360 Technologies',]
g <- as.directed(graph.data.frame(gdf))

#karate <- graph.famous("Zachary")
wc <- walktrap.community(g)
modularity(wc)
membership(wc)
plot(wc, g)
plot(g, vertex.color=membership(wc), vertex.size=5, edge.arrow.size=0.1)

#k = length(V(g))
#g <- graph.edgelist(as.matrix(gdf[,c('V1', 'V2')]))
#E(g)$weight <- gdf[,c('V1', 'V2')]
#edge.attributes(g) <- gdf[,c('V1', 'V2')]
#g
plot(g, 
     vertex.size=5, vertex.color=c(2, as.integer(10*unlist(E(g)$weight))), #c(3, as.integer(5*unlist(E(g)$weight))), #"green",
     vertex.label=NA,
     #vertex.label.cex=0.8, vertex.label.dist=0.3, #vertex.label.degree=0, 
     #edge.label=round(unlist(E(g)$weight), 2), 
     #edge.width=round(unlist(E(g)$weight)), 
     edge.arrow.size=0.2, 
     main='graph',
     layout=layout.kamada.kawai) 

colors <- rainbow(as.integer(max(10*E(g)$weight)-min(10*E(g)$weight)+1)) #colfunc(as.integer(max(10*scores$Distance)))
minval <- min(as.integer(10*unlist(E(g)$weight)))
plot(g, 
     vertex.size=8, 
     vertex.color=c('white', colors[as.integer(10*unlist(E(g)$weight)-minval+1)]), #c(3, as.integer(5*unlist(E(g)$weight))), #"green",
     vertex.label = 1:nrow(gdf), 
     vertex.label.font=2,
     vertex.label.family = "sans",
     vertex.label.cex=1.5, 
     vertex.label.dist=0.3, #vertex.label.degree=0, 
     vertex.frame.color= "black",
     edge.label=round(unlist(E(g)$weight), 2), 
     edge.label.cex=1.5, 
     edge.label.family = "sans",
     edge.label.font=4,
     #edge.width=round(unlist(E(g)$weight)), 
     edge.arrow.size=1, 
     edge.width=1, #2,  
     edge.color="black",
     main='Nearest Nbr graph',
     #layout=layout.lgl
     #layout=layout.fruchterman.reingold(g,niter=500,area=vcount(g)^2.3,repulserad=vcount(g)^2.8)
     #layout=layout.fruchterman.reingold(g)*5
     layout=layout.fruchterman.reingold(g, weights=100/exp(E(g)$weight+1))
     #layout=layout.sphere
     #layout=layout.spring
     #layout=layout.reingold.tilford
     #layout=layout.graphopt
     #layout=layout.fruchterman.reingold.grid
     #layout=layout.svd
     #layout=layout.kamada.kawai
)   

gdf$weight <- 500*gdf$weight
g <- as.directed(graph.data.frame(gdf))
coords <- layout.fruchterman.reingold(g, dim=3)
rglplot(g, layout=coords, vertex.color=c(2, as.integer(unlist(E(g)$weight)) %% 23 + 1),
        vertex.label.cex=0.7, vertex.label.dist=0.3, vertex.label.color='white') 
        #edge.label=round(unlist(E(g)$weight), 2)
bg3d('black')

vertices <- V(g)$name
r <- as.character(max(vertices[!is.na(as.integer(vertices))]))
#plot(g, layout = layout.reingold.tilford(g, root=r)) #, circular=T))
plot(g, vertex.size=40, vertex.label.cex=1, #vertex.label.dist=0.1, vertex.label.degree=0, 
     edge.label=round(unlist(E(g)$weight), 2), edge.arrow.size=0.1, 
     layout = layout.reingold.tilford(g, root='ATAGACAA')) #, circular=T))
