library(tidyverse)
library(reticulate)
library(scales)
use_condaenv('nhack', required=TRUE)

py_run_file('logistic-regression.py')

# Plot
accuracy_brainonly <- py$accuracy_brainonly
accuracy_all <- py$accuracy_all
roc_score_brainonly <- py$roc_score_brainonly
roc_score_all <- py$roc_score_all

accuracy_dist <- py$accuracy_dist
roc_score_dist <- unlist(py$roc_score_dist)

acc <- data.frame(metric = 'accuracy', values = accuracy_dist)
roc <- data.frame(metric = 'roc_score', values = roc_score_dist)
null <- rbind(acc, roc)

quantiles <- expand.grid(metric = c('ROC Score', 'Accuracy'),
                        method = c('All data', 'Brain only'))
quantiles$values <- c(roc_score_all, accuracy_all, roc_score_brainonly, accuracy_brainonly)

thresholds <- data.frame(metric = c('Accuracy', 'ROC Score'),
                         cutoff = c(quantile(accuracy_dist, probs=.95),
                                    quantile(roc_score_dist, probs=.95)))

show_col(brewer_pal(palette = 'Set2')(8))
green <- brewer_pal(palette = 'Set2')(8)[1]
orange <- brewer_pal(palette = 'Set2')(8)[2]

null %>% 
    mutate(metric = recode(metric, `accuracy` = 'Accuracy', `roc_score` = 'ROC Score')) %>% 
    ggplot(aes(x = values)) + 
    geom_vline(data = thresholds, aes(xintercept = cutoff), linetype = 'dotted') + 
    geom_histogram(color = 'black', fill = 'steelblue', alpha = .5) + 
    geom_point(data = quantiles, aes(color = method, y = 1), size = 7, shape = 17) + 
    facet_wrap(~metric) + 
    xlim(0, 1) + 
    labs(
        title = 'Logistic Regression Classifier',
        x = '',
        y = 'Frequency',
        color = '',
        caption = 'Null distribution reflects 1000 simulations of randomly permuting prediction target.'
    ) +
    scale_color_manual(values = c(`All data` = green, `Brain only` = orange)) + 
    theme_bw() + 
    theme(panel.grid = element_blank(),
          strip.background = element_rect(fill = NA, color = 'black'),
          axis.ticks = element_blank(),
          legend.position = c(.4, .6),
          text = element_text(size = 16),
          plot.caption = element_text(size = 12))
    

ggsave('scripts/ml/logistic-regression/lr_performance.png', width = 1280, height = 720, units = 'px', dpi = 120)
