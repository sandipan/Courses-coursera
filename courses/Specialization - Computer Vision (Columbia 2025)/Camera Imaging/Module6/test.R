Square <- function(t, w) {
    # if t smaller than a half period -> 1
    # if t greater or equal than half a period -> 0
    T <- 1/w
    ifelse(((t %% T) < (T/2)),1,0)
}

Sinc <- function(t, w) {
  return (sin(w*t) / (w*t))
}

Rect <- function(t, T) {
  ifelse((abs(t) < (T/2)),1,0)
}

Convolve <- function(f, g, w_f, w_g, t, N=100, dN=0.01) {
  x <- 0
  for (k in seq(-N/2,N/2,dN)) {
    x <- x + f(k, w_f)*g(t-k, w_g)*dN   # h(n) = sum_k f(n-k)g(k)
  }
  return(x)
}

x <- seq(-5,5, 0.01)
plot(x, Square(x, 1), type='l')#, ylim=c(-1,2)) # freq = 1kHz, period = 1ms
grid()
w <- 2                          # 2kHz
lines(x, Sinc(x, w), col='red')
lines(x, Convolve(Square, Sinc, 1, 2, x), col='green')

plot(x, Rect(x, 1), type='l', ylim=c(-1,2)) # freq = 1kHz, period = 1ms
grid()
#y <- rep(0, length(x))
#for (i in 1:length(x)) {
#  y[i] <- Convolve(Rect, Rect, 1, 1, x[i])
#}
y <- Convolve(Rect, Rect, 1, 1, x)
lines(x, y, col='green')

