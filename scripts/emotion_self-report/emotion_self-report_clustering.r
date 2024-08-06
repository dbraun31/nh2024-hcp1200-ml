library(tidyverse) 
library(here)

setwd(here())

d <- read.csv('data/unrestricted_dbraun31_8_5_2024_16_37_47.csv')

cols <- data.frame(
    assessment = c(
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Psychological Well-being (Positive Affect, Life Satisfaction, Meaning and Purpose)",
        "Psychological Well-being (Positive Affect, Life Satisfaction, Meaning and Purpose)",
        "Psychological Well-being (Positive Affect, Life Satisfaction, Meaning and Purpose)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Stress and Self Efficacy (Perceived Stress, Self-Efficacy)",
        "Stress and Self Efficacy (Perceived Stress, Self-Efficacy)"
    ),
    column_header = c(
        "AngAffect_Unadj",
        "AngHostil_Unadj",
        "AngAggr_Unadj",
        "FearAffect_Unadj",
        "FearSomat_Unadj",
        "Sadness_Unadj",
        "LifeSatisf_Unadj",
        "MeanPurp_Unadj",
        "PosAffect_Unadj",
        "Friendship_Unadj",
        "Loneliness_Unadj",
        "PercHostil_Unadj",
        "PercReject_Unadj",
        "EmotSupp_Unadj",
        "InstruSupp_Unadj",
        "PercStress_Unadj",
        "SelfEff_Unadj"
    )
)

# Format cols
colnames(cols)[2] <- 'item'
d <- d[, c('Subject', cols$item)]
cols$item <- tolower(cols$item)
cols$item <- sapply(cols$item, gsub, pattern = '_unadj', replacement = '')
abbrev <- c('negative_affect', 'well_being', 'relationships', 'stress_efficacy')
cols <- inner_join(cols, data.frame(assessment=unique(cols$assessment), abbrev=abbrev))

colnames(d) <- tolower(colnames(d))
d <- d[complete.cases(d),]
colnames(cols)[colnames(cols) == 'column_header'] <- 'item'
colnames(d) <- sapply(colnames(d), gsub, pattern = '_unadj', replacement = '')


clustering <- function(d, centers) {
    km <- kmeans(d[,2:(ncol(d))], centers = centers, nstart=20)
    return(km$tot.withinss)
}


nclusters <- 10
out <- data.frame()

for (clusters in 1:nclusters) {
    wss <- clustering(d[,2:(ncol(d))], centers=clusters)
    trial <- data.frame(clusters=clusters, wss=wss)
    out <- rbind(out, trial)
}


plot(out)


# Roughly 3-4 clusters works

km <- kmeans(d[, 2:(ncol(d))], centers=3, nstart=20)
d$cluster <- km$cluster

d %>% 
    gather(item, response, angaffect:selfeff) %>% 
    inner_join(cols) %>% 
    group_by(cluster, abbrev) %>% 
    summarize(response_mean = mean(response), se = sd(response) / sqrt(n())) %>% 
    mutate(cluster = recode(cluster, `1` = 'Cluster 1', `2` = 'Cluster 2', `3` = 'Cluster 3')) %>% 
    ggplot(aes(x = abbrev, y = response_mean)) + 
    geom_hline(yintercept=50, linetype='dashed') + 
    geom_hline(yintercept=60, linetype='dotted') + 
    geom_hline(yintercept=40, linetype='dotted') + 
    geom_bar(stat='identity') + 
    geom_errorbar(aes(ymin = response_mean - se, ymax = response_mean + se), width = .5) + 
    facet_wrap(~cluster) + 
    labs(
        x = 'NIH Toolkit Survey Factors',
        y = 'Mean Response',
        caption = 'Dashed line represents item means. Dotted line represents 1 SD.'
    )  +
    theme_bw() + 
    theme(
        panel.grid = element_blank(),
        strip.background = element_rect(fill = NA, color = 'black'),
        axis.ticks = element_blank(),
        axis.text.x = element_text(angle = 45, hjust=1)
    )


ggsave('scripts/emotion_self-report/prelim_clustering_result.png', height = 720, width = 1280, units = 'px', dpi = 120)

write.csv(d[,c('subject', 'cluster')], 'scripts/emotion_self-report/cluster_subject_mapping.csv', 
          row.names=FALSE)


























