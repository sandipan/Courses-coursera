#
# Tutorial introduction to
# the RnavGraph R package
#  ... Wayne Oldford 
#      (Waterloo, Canada)
#    & Adrian Waddell
#      (Waterloo, Canada)


require(RnavGraph)

# See some stock demos
demo(package="RnavGraph")

# Details and examples are described in the vignette
# vignette("RnavGraph")

#  RnavGraph is all about exploring high-dimensional
#  space via low-dimensional trajectories.
#  The trajectories are defined by paths on a 
#  navigation graph, or "navGraph".
#

ls("package:RnavGraph")

#
#  Begin with any data set that is a data.frame.
#
#
# Create the navgraph data
 
ng.iris <- ng_data(name = "IrisData",  
                   # NB: Name is unique and
                   #     has NO spaces
	                 data = iris[,1:4]					         )
#
# We could start navGraph immediately, simply
# by executing
#
#       navGraph(ng.iris)
#
# But we won't yet.  First, let's look at the
# data structure produced by ng_data(...).
#
# Have a look

ng.iris

attributes(ng.iris)

#
#  Can access variable names

names(ng.iris)

#
# The following is to have short strings
# for display. If empty, the names(.)
# are used.

shortnames(ng.iris)

#
# other access is by ng_get(obj, what) methods
#

ng_get(ng.iris)

ng_get(ng.iris, "group")

ng_get(ng.iris, "labels")

ng_get(ng.iris, "data")

#
# We can set these values using ng_set methods.
#

ng_set(ng.iris)

# E.g. For the Iris data, a reasonable choice
# of groups would be the Species

ng_set(ng.iris, "group") <- iris$Species

ng_get(ng.iris, "group")

ng.iris

# We might also use Species to construct labels
# (or just first to characters)

ng_set(ng.iris, "labels") <- substr(iris$Species,1,2)

ng.iris

# We set shortnames more directly
#
shortnames(ng.iris) <- c('s.L', 's.W', 'p.L', 'p.W')

ng.iris

#
# We could have passed all these as the values
# of arguments at the time of creation

ng.iris <- ng_data(name = "IrisData", 
	                 data = iris[,1:4],
	                 labels=iris$Species,
	                 group=iris$Species,
	                 shortnames=c('s.L','s.W',
	                              'p.L', 'p.W')
				         )

#
# With the ng data defined, we simply
# start navGraph

navGraph(ng.iris)

#  Explore functionality.
#  ... zoom, selection,
#      text, dots, brushing, colouring, choose colour
#  
#  ... graph definition and functionality
#
#  ... 3d transistions
#
#  ... Changing settings
#
#
# We could start a second sesion  navGraph

navGraph(ng.iris)

#  Explore, show brushing, different scatterplots,
#  ... change size, color,
#  
#  ... 4d transitions
#
#  ... save handlers, as nav1 and nav2
#
#  
#
#  An important data analysis requirement is the
#  ability to get and set colours and sizes of points
#  since these can be changed interactively.
#
#  These can be had programmatically from the handler.
#

ng_get_color(nav1)

ng_set_color(nav1,"IrisData") <- sample(colors(),150)
ng_set_color(nav1,"IrisData") <- "red"

#
# Note colours must be acceptable to tcl/tk
# (So no alpha blending; just standard R colours)
ng_get_color(nav1)

ng_set_color(nav1,"IrisData") <- c("thistle",
												  "steelblue",
												  "greenyellow")[as.numeric(iris$Species)]
												  
#
# Similarly for point size
#

ng_get_size(nav1)

ng_set_size(nav1,"IrisData") <- sample(1:10,
												      150, replace=TRUE)
												      
ng_set_size(nav1,"IrisData") <- 3

######
# 
#  A deeper investigation into the navGraph handler.
#  
#  Here's what the navGraph handlers look like
nav1
nav2

ng_get(nav1)

#
# Get the ng graphs
#

nggraphs <- ng_get(nav1, "graphs")

nggraphs

ngg1 <- nggraphs[[1]]
ngg1

#
# Various attributes can be selected from an ng graph
# 
ng_get(ngg1)

ng_get(ngg1,"name")

ng_get(ngg1,"graph")

#
# At the bottom of this, then, is a GraphNEL graph.
# If we access it, we can deal with as with any
# other such graph.
#
g <- ng_get(ngg1,"graph")

#
# Load the Rgraphviz package.

require(Rgraphviz)
plot(g,"circo")

# In particular, we might want to use some of
# the tools from PairViz

require(PairViz)
#
# The graph is even (4-regular) and so an Eulerian
# can be found.

eulerian(g)

#
# With the navgraph handler available, we
# can programmatically instruct it to walk this
# Eulerian tour.
#
ng_walk(nav1,eulerian(g))

#  Moreover, the walk is stored in the handler
#  and can be saved, annotated, etc.
#  Go to "Tools" menu on the navigation graph
#  where the walk just occured.
#  Save and annotate it.
#
# Any path, however constructed, can be walked 
# in the same way.

mypath <- eulerian(g)[4:8]
ng_walk(nav1,mypath)

# Moreover, we can interactively select a path
# to walk simply by shift-selecting nodes and
# double clicking on the final destination node.
#
# Try it.
#
#
#  There are also vizualizations associated with
#  a navgraph handler.

ng_get(nav1,"viz")    # Here two, one for 3D, one for 4D.
                      # both are tk2d scatterplots.
                      
# data, graphs, vizualizations are the three essential
# components to a navGraph.
#
######


# 
# Could build the navGraph up from scratch
#
#
# First we get the graph structures we want.
# 
# Get the variable graph vertex names

V <- shortnames(ng.iris)

# We could build what we had before
# by creating a completegraph

G <- completegraph(V)
plot(G, "circo")

# then getting the 3d transition graph from this as its
# linegraph			
LG <- linegraph(G)

# and its complement is the 4d transition graph.
#
LGnot <- complement(LG)

dev.new(width=4,height=6)
par(mfrow=c(3,1))
plot(G,"circo", main="Variable Graph")
plot(LG,"circo", main="Its line Graph")
plot(LGnot,"circo", main="Complement of the line Graph")

# OR, since G is of class 
class(G)

# Start with any variable graph we like
# and repeat the above
#
# E.g. undirected graph with an adjacency matrix
adjM <- matrix(c(0,0,1,1, 
                 0,0,0,1, 
                 1,0,0,1, 
                 1,1,1,0),
              ncol=4, byrow=TRUE)
              
G <- newgraph(V,adjM, isAdjacency=TRUE)

## convert these graphs to NG_graph objects
help(ng_graph)

ng.lg <- ng_graph('3D Transition',LG, layout = 'circle')

ng.lgnot <- ng_graph('4D Transition',LGnot, layout = "circle")

# And gather these up into a list for later use.

graph <- list(LG = ng.lg, LGnot = ng.lgnot)

#
# We can add glyphs to the ng_2d visualizations
#
# help(ng_2d)

viz <- list(ng_2d(data = ng.iris,
                  graph = ng.lg),
            ng_2d(data = ng.iris,
                  graph = ng.lg,
                  glyphs = eulerian(as(G,"graphNEL"))),
            ng_2d(data = ng.iris,
                  graph = ng.lgnot,
                  glyphs = eulerian(as(G,"graphNEL"))))
                  
nav <- navGraph(data = ng.iris,
                graph = graph,
                viz = viz)

#
#  Note that nav is now a navGraph handler where one
#  navigation graph is driving 3 displays.
#  Two of these will appear when ng.lg (3D transition)
#  is the active navigation graph,
#  only one will appear when ng.lgnot is the active
#  navigation graph.
#  Note also that glyphs appear only in two of these displays.
#
#  In this way, one navgraph can drive several displays.
#  
#  Note also that these displays are linked because they
#  all refer to the same NAMED data:  "IrisData".
#
# 
################
#
#
#   The Olive Oil data set.  An illustration of scagnostics.
#
# 
#  Get the data

data(olive, package="RnavGraph")

d.olive <- data.frame(olive[,-c(1,2)])

ng.olive <- ng_data(name = "Olive",
					data = d.olive,
					shortnames = c("p1","p2","s","oleic",
					               "l1","l2","a","e"),
					group = as.numeric(olive[,"Area"]),					labels = as.character(olive[,"Area"])
			)

#
# The following function does a lot of the work
# for you.
help(scagNav)

scagNav(data = ng.olive,
			scags = c("Monotonic", "NotMonotonic",
							"Clumpy", "NotClumpy",
							"Convex", "NotConvex",  
							"Stringy", "NotStringy",
							"Skinny", "NotSkinny",
							"Outlying","NotOutlying",
							"Sparse", "NotSparse",
							"Striated", "NotStriated",
							"Skewed", "NotSkewed"),
			glyphs = hpaths(shortnames(ng.olive)),
			topFrac = 0.15,
			sep = "::")
			
#
# Explore a few of these.
# 
# Get the navGraph handler and assign it to snav
#
# OK, get rid of colours

ng_set_color(snav,'Olive') <- 'steelblue'

#
#  And maybe try some automated clustering methods
#

data <- data.frame(scale(d.olive))

#
# Say model based clustering
#

# require(mclust)
# mcdata <- Mclust(data, 1:20)
# groups <- mcdata$classification
# results are
groups <- c(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2,  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2,  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,  3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,  4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,  4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,  5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,  5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,  5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)


ng_set_color(snav,'Olive') <- c("red","orange","green","blue","grey")[groups]

# Then play some more
#
########

#
#
#  IMAGES
#
#  RnavGraph has a couple of ways of handling images.
#
#  1. Images (esp. colour images) may be read in as files
#     e.g. see  demo(ng_2d_image_files_aloi,package="RnavGraph")
#  2. As grey scale arrays (below)
#  3. By using tcl commands directly and inventing a new NG_image 
#     data type. 
#     e.g. see demo(ng_2d_images_iris,package="RnavGraph")
#
#
#   Here we look at the Frey image data and
#   two different manifold learning methods
#   Local Linear Embedding (or LLE) and ISOMAP
#
#   The images are stored in the companion package
#   RnavGraphImageData

require(RnavGraphImageData)
data(frey,package="RnavGraphImageData")

# ISOMAP data dimensionality reduction
# In the interest of time, we won't do the calculations here
# They have been done and the results saved in ordfrey
#
# require(vegan)   # isomap found here

# frey2 <- t(frey)
dims <- 6 
# dise <- vegdist(frey2, method="euclidean")
# ordfrey <- isomap(dise,k = 12, ndim= dims, fragmentedOK = TRUE)

data(ordfrey,package="RnavGraphImageData")
			
iso.frey <- data.frame(ordfrey$points)
			
# Images
# sample a few

sel <- seq(1,dim(frey)[2],3)

ng.frey <- ng_image_array_gray('Brendan_Frey',
											frey[,sel],28,20, 
											img_in_row = FALSE, 
											rotate = 90)

#
# Look at the images
#

ng.frey
V <- mapply(function(x){paste("i",x,sep="")},1:dims)

ng.iso.frey <- ng_data(name = "FreyImages",
						data = iso.frey[sel,],
						shortnames = V)
				
G <- completegraph(V)
LG <- linegraph(G)
LGnot <- complement(LG)
			
ng.LG <- ng_graph("3d frey", LG)
ng.LGnot <- ng_graph("4d frey", LGnot)
			
viz3d <- ng_2d(ng.iso.frey,ng.LG, images = ng.frey)
viz4d <- ng_2d(ng.iso.frey,ng.LGnot, images = ng.frey)
			
navGraph(ng.iso.frey,list(ng.LG,ng.LGnot),list(viz3d,viz4d))

#
# Local Linear Embedding from the RDRToolbox package
#
require(RDRToolbox)
d_low <- LLE(t(frey),dim=5,k=12)
			
# Images as before
# stored in ng.frey
						
V <- mapply(function(x){paste("i",x,sep="")},1:5)

#
# Make a new ng_data object with the SAME name causes
# the linkage.
# 
ng.lle.frey <- ng_data(name = "FreyImages",
					         data = data.frame(d_low[sel,]),
					         shortnames = V)
			
G <- completegraph(V)
LG <- linegraph(G)
LGnot <- complement(LG)
			
ng.LG <- ng_graph("3d frey", LG)
ng.LGnot <- ng_graph("4d frey", LGnot)
			
viz3d <- ng_2d(ng.lle.frey,ng.LG, images = ng.frey)
viz4d <- ng_2d(ng.lle.frey,ng.LGnot, images = ng.frey)
			
navGraph(ng.lle.frey,list(ng.LG,ng.LGnot),list(viz3d,viz4d))

#
#
# 
##########


##########
#
#
#  Other special plotting
#
#
#
#
######


#
#  rggobi
#
#  ng_2d_ggobi  could be used in place, or in addition to,
#  ng_2d 
#  This will allow rggobi to ve used to display the scatterplots
#  and give the user access to everything in rggobi.
#
# 
require(rggobi)

#
# Use the LLE Frey data (no images)
#

ng.LG <- ng_graph("3d frey", LG)
ng.LGnot <- ng_graph("4d frey", LGnot)
			
viz3d <- ng_2d_ggobi(ng.lle.frey,ng.LG)
viz4d <- ng_2d_ggobi(ng.lle.frey,ng.LGnot)
			
navGraph(ng.lle.frey,list(ng.LG,ng.LGnot),list(viz3d,viz4d))



#
#  myplot
#
#   ng_2d_myplot can be used to allow action to be taken on
#   a user defined display.
#
#   Examples:
#
#  Base plotting functionality
#
#
# Already have ng.iris
#
V <- shortnames(ng.iris)
G <- completegraph(V)
LG <- linegraph(G)
LGnot <- complement(LG)
ng.lg <- ng_graph(name = '3D Transition', graph = LG, layout = 'circle')
ng.lgnot <- ng_graph(name = '4D Transition', graph = LGnot, layout = 'circle')
			
#
#  Here's the new part
#
		
myPlot <- function(x,y,group,labels,order) {
				plot(x,y,col = group, pch = 19)
			}
			
viz1 <- ng_2d_myplot(ng.iris,ng.lg,
                     fnName = "myPlot" , 
                     device = "base", 
                     scaled=TRUE)
                     
viz2 <- ng_2d_myplot(ng.iris,ng.lgnot,
                     fnName = "myPlot" , 
                     device = "base", 
                     scaled=TRUE)
			
nav <- navGraph(ng.iris,list(ng.lg,ng.lgnot), 
								  list(viz1, viz2))			
		
#
#
# Now just change myplot definition 
#
require(hexbin)

myPlot <- function(x,y,group,labels,order) {
				plot(hexbin(x,y,xbins=15))	
			}

myPlot <- function(x,y,group,labels,order) {
				bins <- hexbin(x,y,xbins=15)
				plot(bins,colramp=terrain.colors)	
			}
			
require(MASS)

myPlot <- function(x,y,group,labels,order) {
					den <- kde2d(x,y,
					             h = c(width.SJ(x), 
					                   width.SJ(y)))
	           plot(x, y, col = group,
	                pch = 19, axes=FALSE,
	                main="Iris Data",
	                xlab = "", ylab = "")
	           box()	
	           contour(den, add = TRUE, 
	                   col = 'orange', lwd = 2)

			}
			


#
#  Visualizations having device rgl
#

require(rgl)
require(MASS)

myPlot <- function(x,y,group,labels,order) {
				den <- kde2d(x,y)
				persp3d(den$x,den$y,den$z, col = "steelblue")  
			}

viz1 <- ng_2d_myplot(ng.iris,ng.lg,
                     fnName = "myPlot" , 
                     device = "rgl", 
                     scaled=TRUE)
                     
viz2 <- ng_2d_myplot(ng.iris,ng.lgnot,
                     fnName = "myPlot" , 
                     device = "rgl", 
                     scaled=TRUE)
			
nav <- navGraph(ng.iris,list(ng.lg,ng.lgnot), 
								  list(viz1, viz2))

#
# mixing two devices
#

myPlot <- function(x,y) {
	den <- kde2d(x,y,h = c(width.SJ(x), width.SJ(y)))
	plot(x, y, col = "steelblue", 
	     pch = 19, axes=FALSE, xlab = "", ylab = "")
	box()	
	contour(den, add = TRUE, col = 'orange', lwd = 2)

	persp3d(den$x,den$y,den$z, col = "steelblue")  
}

#
#
# Change device to "grid"
#
require(grid) 

myPlot.init <- function(x,y,group,labels,order) {
				pushViewport(plotViewport(c(5,4,2,2)))
				pushViewport(dataViewport(c(-1,1),
				             c(-1,1),name="plotRegion"))
				
				grid.points(x,y, name = "dataSymbols")
				grid.rect()
				grid.xaxis()
				grid.yaxis()
				grid.edit("dataSymbols", pch = 19)
				grid.edit("dataSymbols", gp = gpar(col = group))
			}
			
			myPlot <<- function(x,y,group,labels,order) {
				grid.edit("dataSymbols", x = unit(x,"native"), y = unit(y,"native"))
			}
			

viz1 <- ng_2d_myplot(ng.iris,ng.lg,
                     fnName = "myPlot" , 
                     device = "grid", 
                     scaled=TRUE)
                     
viz2 <- ng_2d_myplot(ng.iris,ng.lgnot,
                     fnName = "myPlot" , 
                     device = "grid", 
                     scaled=TRUE)
			
nav <- navGraph(ng.iris,list(ng.lg,ng.lgnot), 
								  list(viz1, viz2))			
								  
#
#
#  Even change the semantics of the transition
#  from rotation to slicing
#
#  demo(ng_2d_slice,package="RnavGraph")			
#
#  Could also demonstrate some java devices
#  But this requires a different R.
#  (e.g. Java Gui R and JavaExample.R)