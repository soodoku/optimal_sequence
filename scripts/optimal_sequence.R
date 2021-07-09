# Optimal Sequence
setwd(githubdir)
setwd("optimal_sequence/")


library(lpSolve)

# x_ij dichotomous; whether or not ticket i is resolved on day j
# c_ij continuous; cost to resolve ticket i on day j
# h = .25; hrs needed to resolve one ticket
# e = 15; $/hr --- cost of an employee
# maxh_j = rep(2, j)
# j = 10

# minimize total cost to ship + cost of your labor
sum(xij*cij + xij*h*e)

# constraints
#colSums(xij) < maxhj
rowSums(xij) == 1

# Read cost matrix
cost <- read.csv("data/cost.csv")
j <- length(cost)
maxhj <- c(.5, j)

obj <-  as.matrix(cost)
f.constr =  matrix(rep(1, 25), nrow= 5)
f.dir <- rep(">=", 5)
f.rhs <- rep(1, 5)

lp(direction = "min", obj, f.constr, f.dir, f.rhs)$solution
