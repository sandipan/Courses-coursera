prod(10:3)

add.func <- function(x) {
  n <- length(x)
  return (sum(10^((n-1):0)*x))
}

#add.func(1:4)

find.sol <- function() {
  for (S in 1:9) {
    for (M in setdiff(1:9, S)) {
      for (E in setdiff(0:9, c(S,M))) {
        for (N in setdiff(0:9, c(S, M, E))) {
          for (D in setdiff(0:9, c(S, M, E, N))) {
            for (O in setdiff(0:9, c(S, M, E, N, D))) {
              for (R in setdiff(0:9, c(S, M, E, N, D, O))) {
                for (Y in setdiff(0:9, c(S, M, E, N, D, O, R))) {
                  if (add.func(c(S, E, N, D)) + add.func(c(M, O, R, E)) == add.func(c(M, O, N, E, Y)))
                      return (c(S, E, N, D, M, O, R, Y))
                  
                }
              }    
            }
          }
        }
      }    
    }
  }
}

#find.sol()
S <- 9
E <- 5 
N <- 6
D <- 7 
M <- 1
O <- 0 
R <- 8 
Y <- 2
# S=9, E=5, N=6, D=7, M=1, O=0, R=8, Y=2
add.func(c(S, E, N, D)) + add.func(c(M, O, R, E)) 
add.func(c(M, O, N, E, Y))