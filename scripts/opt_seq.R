setwd("/Users/Ken/Documents/Github/optimal_sequence/data")

library(lpSolve)
library(ROI)
library(ROI.plugin.glpk)
library(ompr)
library(ompr.roi)
library(magrittr)
library(dplyr)

cost<-as.matrix(read.csv(file = "cost.csv"))
cost<-cost[1:5,2:6]

n <- 5
h = .25
e = 15

set.seed(1)
result <- MIPModel() %>% 
  add_variable(x[i, j], i = 1:n, j = 1:n, type = "binary") %>%
  set_objective(sum_expr((-1)*((cost[i, j] + h*e)) * x[i, j], i = 1:n, j = 1:n)) %>% 
  add_constraint(sum_expr(x[i, j], j = 1:n) == 1, i = 1:n) %>% 
  add_constraint(sum_expr(h*x[i,j], i= 1:n) <= .5, j = 1:n) %>%
  solve_model(with_ROI("glpk", verbose = TRUE))

get_solution(result, x[i, j]) %>% 
  dplyr::filter(value == 1)

