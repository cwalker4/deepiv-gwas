library(tidyverse)
library(here)


deep <- read_csv('/Users/Walker/Desktop/Winter/CS230/deepiv-gwas/milestone/simulation_results/deep_big.csv',
                     col_names=FALSE)
ffn <- read_csv('/Users/Walker/Desktop/Winter/CS230/deepiv-gwas/milestone/simulation_results/ffn_big.csv',
                    col_names=FALSE)

rho <- c(0.1, 0.25, 0.5, 0.75, 0.9)
colnames(deep) <- rho
colnames(ffn) <- rho

deep %>%
  gather(key = "rho", value = "mse") %>%
  mutate(Architecture = as.factor("DeepIV")) -> deep

ffn %>%
  gather(key = "rho", value = "mse") %>%
  mutate(Architecture = as.factor("FFNet")) %>%
  bind_rows(deep) -> performance

performance %>%
  ggplot(aes(x = rho, y = mse, fill = Architecture)) +
  geom_boxplot() + 
  scale_color_manual(labels = c("DeepIV", "FFNet"), values = c("blue", "red")) +
  ylab("Test Error (MSE)") + 
  xlab(expression(rho)) + 
  ylim(0, 1) + 
  guides(color=guide_legend("Architecture")) + 
  theme_light()


