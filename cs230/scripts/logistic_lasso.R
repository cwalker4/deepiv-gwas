library(here)
library(glmnet)
library(tidyverse)

# loading data (takes a hot sec)
expression <- read_csv(here::here("analysis/data/simulate/covariance/expression.csv"))
outcomes <- read_csv(here::here("analysis/data/simulate/covariance/outcomes.csv"))

# cv fitting 2000-observation model (to cv-select lambda)
expression_mini <- expression[1:2000,]
outcomes_mini <- outcomes[1:2000,]
cvfit.mini <- cv.glmnet(as.matrix(expression_mini),
                        as.matrix(outcomes_mini))
lambda.1se <- cvfit.mini$lambda.1se

# fitting lasso with regularization parameter from cvfit.mini
expression_sub <- expression[1:20000,]
outcomes_sub <- outcomes[1:20000,]
fit <- glmnet(as.matrix(expression_sub), as.matrix(outcomes_sub), alpha=1, family="binomial")

plot(fit, xvar = "lambda", label = TRUE)

# looking at coefficients on full model at s = lambda.1se
coefs <- as.vector(coef(fit, s = lambda.1se))
coefs <- coefs[2:length(coefs)] # dropping intercept term
as.data.frame(coefs) %>%
  mutate(ind = 0:(length(coefs)-1)) %>%
  filter(coefs != 0) %>%
  arrange(-abs(coefs)) -> coef_rankings

readr::write_csv(coef_rankings, here::here('derived_data/lasso_coeffs.csv'))

# creating df that makes it easy to prettify our LaTeX table
read_csv(here::here('crosswalks/mrna_index_crosswalk.csv')) %>%
  right_join(coef_rankings[1:10,], by = c("py_index"="ind")) %>%
  select(mrna = mrna_crosswalk, coefs) %>%
  write_csv(here::here('analysis/figures/lasso_coefs.csv'))

