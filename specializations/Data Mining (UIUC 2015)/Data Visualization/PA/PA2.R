setwd('C:/courses/Coursera/Current/Data Visualization/PA')

library(networkD3)

### Load Data
library(igraph)
g <- read.graph("dolphins.gml",format=c("gml"))
#g <- read.graph("celegansneural.gml",format=c("gml"))
#g <- read.graph("lesmis.gml",format=c("gml"))
#g <- read.graph("karate.gml",format=c("gml"))
graph.edges <- get.data.frame(g, what="edges")
names(graph.edges) <- c("source", "target") #, "weight")
graph.nodes <- get.data.frame(g, what="vertices")
graph.nodes$group <- 1
graph.nodes$size <- degree(g) * 5 #betweenness(g) / 5 #20

#graph.edges <- read.csv(file = 'Wiki-Vote.txt', sep="\t", skip=4, header=F, col.names=c("source", "target"))

graph.edges <- graph.edges - min(graph.edges) + 1
graph.nodes <- data.frame(id=seq(max(graph.edges) - min(graph.edges) + 1))
graph.nodes$group <- 1

### Cluster with MCL

library(MCL)
graph.cluster <- function(nodes, edges){
  n <- nrow(graph.nodes)
  adjacency <- matrix(0, n, n)
  index <- cbind(graph.edges$source, graph.edges$target)
  adjacency[index] <- 1 #graph.edges$weight #1
  cluster <- mcl(x = adjacency, addLoops=TRUE, ESM = TRUE)
  print(cluster$Cluster)
  cluster$Cluster
}


### Create graph of clustered ego network
graph.nodes$group <- graph.cluster(graph.nodes, graph.edges)

## draw clustered network
## notice that with NetworkD3, index of edges start from 0
MyClickScript <- 'alert("You clicked " + d.NodeID + " which is in row " +
       (d.index + 1) +  " of your original R data frame");'
network.cluster <- forceNetwork(
  Links = graph.edges - 1, Nodes = graph.nodes, Nodesize='size',
  Source = "source", Target = "target",
  NodeID = "label", #"id", #"label",
  Group = "group", charge=-300, fontSize=12, opacity = 0.8, legend = TRUE, bounded = T, zoom = TRUE,
  clickAction = MyClickScript)
print(network.cluster)

wc <- walktrap.community(g)
modularity(wc)
membership(wc)
plot(wc, g)
plot(g, vertex.color=membership(wc))

if (FALSE) {

  library(RnavGraph)
  library(RnavGraphImageData)
  #source("http://bioconductor.org/biocLite.R")
  #biocLite('Rgraphviz')
  #biocLite('RDRToolbox')
  library(Rgraphviz)
  data(package='RnavGraphImageData')
  data(digits)
  dim(digits)
  help("digits")
  matrix(digits[,7*1100+1],ncol = 16, byrow=FALSE)
  sel <- sample(x=1:11000,size = 600)
  p.digits <- digits[,sel]
  ng.i.digits <- ng_image_array_gray('USPS Handwritten Digits',
                                     p.digits,16,16,invert = TRUE,
                                     img_in_row = FALSE)
  
  library(vegan)
  p.digitsT <- t(p.digits)
  dise <- vegdist(p.digitsT, method="euclidean")
  ord <- isomap(dise,k = 8, ndim=6, fragmentedOK = TRUE)
  digits_group <- rep(c(1:9,0), each = 1100)
  ng.iso.digits <- ng_data(name = "ISO_digits",
                           data = data.frame(ord$points),
                           shortnames = paste('i',1:6, sep = ''),
                           group = digits_group[sel],
                           labels = as.character(digits_group[sel]))
  V <- shortnames(ng.iso.digits)
  G <- completegraph(V)
  LG <- linegraph(G)
  LGnot <- complement(LG)
  ng.LG <- ng_graph(name = "3D Transition", graph = LG)
  ng.LGnot <- ng_graph(name = "4D Transition", graph = LGnot)
  vizDigits1 <- ng_2d(data = ng.iso.digits, graph = ng.LG, images = ng.i.digits)
  vizDigits2 <- ng_2d(data = ng.iso.digits, graph = ng.LGnot, images = ng.i.digits)
  nav <- navGraph(data = ng.iso.digits, graph = list(ng.LG, ng.LGnot), viz = list(vizDigits1, vizDigits2))
  
  
  
  # Drawing a scatter plot of raster images
  doInstall <- TRUE  # Change to FALSE if you don't want packages installed.
  toInstall <- c("png", "devtools", "MASS", "RCurl")
  if(doInstall){install.packages(toInstall, repos = "http://cran.r-project.org")}
  lapply(toInstall, library, character.only = TRUE)
  
  # Some helper functions, lineFinder and makeTable
  source_gist("818983")
  source_gist("818986")
  
  # In as few lines as possible, get URLs for .PNGs of each flag
  importHTML <- readLines("http://en.wikipedia.org/wiki/World_flags")
  importHTML[lineFinder("thumbborder", importHTML)]
  pngURLs <- makeTable(makeTable(importHTML[lineFinder("thumbborder",
                                                       importHTML)], "src=\"//")[, 2], "\" width=\"")[, 1]
  pngURLs <- paste0("http://", pngURLs)
  
  # CAUTION: The following loop will download 204 .PNG images
  # of flags from Wikipedia. Please be considerate, and don't run
  # this part of the script any more than you need to.
  pngList <- list()
  for(ii in 1:length(pngURLs)){
    tempName <- paste("Flag", ii)
    tempPNG <- readPNG(getURLContent(pngURLs[ii]))  # Downloads & loads PNGs
    pngList[[tempName]] <- tempPNG  # And assigns them to a list.
  }
  
  # Very simple dimension reduction -- just the mean R, G, and B values
  meanRGB <- t(sapply(pngList, function(ll){
    apply(ll[, , -4], 3, mean)
  }))
  
  # The dimensions of each item are equal to the pixel dimensions of the .PNG
  flagDimensions <- t(sapply(pngList, function(ll){
    dim(ll)[1:2]
  }))
  
  # Similarity, through Kruskal non-metric MDS
  flagDistance <- dist(meanRGB)
  flagDistance[flagDistance <= 0] <- 1e-10
  
  MDS <- isoMDS(flagDistance)$points
  plot(MDS, col = rgb(meanRGB), pch = 20, cex = 2)
  
  # Plot:
  boxParameter <- 5000  #6000  # To alter dimensions of raster image bounding box
  par(bg = gray(8/9))
  plot(MDS, type = "n", asp = 1)
  for(ii in 1:length(pngList)){  # Go through each flag
    tempName <- rownames(MDS)[ii]
    Coords <- MDS[tempName, 1:2]  # Get coordinates from MDS
    Dims <- flagDimensions[tempName, ]  # Get pixel dimensions
    rasterImage(pngList[[tempName]],  # Plot each flag with these boundaries:
                Coords[1]-Dims[2]/boxParameter, Coords[2]-Dims[1]/boxParameter,
                Coords[1]+Dims[2]/boxParameter, Coords[2]+Dims[1]/boxParameter)
  }
  
}
