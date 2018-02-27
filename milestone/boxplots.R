library(tidyverse)
library(here)


deep_big <- read_csv('/Users/Walker/Desktop/Winter/CS230/deepiv-gwas/milestone/simulation_results/deep_big.csv',
                     col_names=FALSE)
ffn_big <- read_csv('/Users/Walker/Desktop/Winter/CS230/deepiv-gwas/milestone/simulation_results/ffn_big.csv',
                    col_names=FALSE)

rho <- c(0.1, 0.25, 0.5, 0.75, 0.9)
colnames(deep_big) <- rho
colnames(ffn_big) <- rho

deep_big %>%
  gather(key = "rho", value = "mse") %>%
  mutate(Architecture = as.factor("DeepIV")) -> deep_big

ffn_big %>%
  gather(key = "rho", value = "mse") %>%
  mutate(Architecture = as.factor("FFNet")) %>%
  bind_rows(deep_big) -> performance

performance %>%
  ggplot(aes(x = rho, y = mse, fill = Architecture)) +
  geom_boxplot() + 
  scale_color_manual(labels = c("DeepIV", "FFNet"), values = c("blue", "red")) +
  ylab("Test Error (MSE)") + 
  xlab(expression(rho)) + 
  guides(color=guide_legend("Architecture")) + 
  theme_light()


